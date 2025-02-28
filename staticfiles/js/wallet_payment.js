document.addEventListener("DOMContentLoaded", function () {
    var razorpayKeyId = document.getElementById("razorpay-key").dataset.key;
    var loggedInUserId = document.getElementById("user-id").dataset.user;
    
    document.getElementById('pay-btn').onclick = async function () {
        console.log("🛎️ Pay button clicked");
        let amount = document.getElementById("amount").value.trim(); 

        if (!amount || isNaN(amount) || Number(amount) <= 0) {
            alert("Please enter a valid amount.");
            return;
        }

        let csrfToken = getCSRFToken();
        if (!csrfToken) {
            console.error("🚨 CSRF Token missing");
            alert("CSRF Token is missing. Please refresh the page.");
            return;
        }

        let requestData = { amount: parseInt(amount), logged_in_user_id : loggedInUserId };

        console.log("📤 Sending Order Request:", requestData);

        try {
            let response = await fetch('/wallet/add_money/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(requestData)
            });

            let order = await response.json();
            console.log("📜 Order Data:", order);

            if (order.error) {
                console.error("❌ Order Creation Failed:", order.error);
                window.location.href = "/wallet/error/?error=" + encodeURIComponent(order.error);
                return;
            }

            if (typeof Razorpay === "undefined") {
                console.error("🚨 Razorpay is not loaded. Please check the script inclusion.");
                alert("Payment service unavailable. Please refresh the page.");
                return;
            }

            if (!razorpayKeyId) {
                console.error("🚨 Razorpay key is missing. Check the configuration.");
                alert("Payment cannot proceed due to missing configuration.");
                return;
            }

            var options = {
                "key": razorpayKeyId,
                "amount": order.amount,
                "currency": order.currency,
                "name": "Skylink",
                "description": "Test Transaction",
                "order_id": order.id,
                "handler": async function (response) {
                    console.log("💰 Payment Successful, Response:", response);

                    try {
                        let verifyResponse = await fetch('/wallet/verify_payment/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken
                            },
                            body: JSON.stringify({
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_signature: response.razorpay_signature
                            })
                        });

                        let verifyData = await verifyResponse.json();
                        console.log("✅ Payment verification success:", verifyData);

                        let redirectUrl = `/wallet/success?payment_id=${encodeURIComponent(response.razorpay_payment_id)}&order_id=${encodeURIComponent(response.razorpay_order_id)}&signature=${encodeURIComponent(response.razorpay_signature)}&amount=${encodeURIComponent(order.amount)}&currency=${encodeURIComponent(order.currency)}`;
                        window.location.href = redirectUrl;

                    } catch (error) {
                        console.error("🚨 Error verifying payment:", error);
                        alert("Payment verification failed. Please try again.");
                        window.location.href = "/wallet/error/?error=" + encodeURIComponent("Payment verification failed.");
                    }
                },
                "theme": { "color": "#3399cc" }
            };

            console.log("⚙️ Initializing Razorpay with options:", options);
            var rzp1 = new Razorpay(options);
            rzp1.open();

        } catch (error) {
            console.error("🚨 Error in payment process:", error);
            alert("An error occurred while processing your payment. Please try again.");
            window.location.href = "/wallet/error/?error=" + encodeURIComponent("Payment process failed.");
        }
    };

    // ✅ Get CSRF Token
    function getCSRFToken() {
        let tokenElement = document.querySelector('meta[name="csrf-token"]');
        return tokenElement ? tokenElement.getAttribute('content') : null;
    }
});

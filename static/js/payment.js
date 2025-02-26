document.getElementById('pay-btn').onclick = function () {
    console.log("🛎️ Pay button clicked");

    let csrfToken = getCSRFToken();

    // Ensure variables are defined in the template before including payment.js
    console.log("🔑 CSRF Token:", csrfToken);
    console.log("🔹 Client ID:", clientId, "🔹 Amount:", amount);

    let requestData = {
        amount: amount, 
        client_id: clientId,
        client_name: clientName,
        end_date: endDate,
        device_id: deviceId,
        channel_id: channelId,
        channel_name: channelName
    };

    fetch('/subscribe/create_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(requestData)  
    })
    .then(response => response.json())
    .then(order => {
        console.log("📜 Order Data:", order);

        if (order.error) {
            console.error("❌ Order Creation Failed:", order.error);
            window.location.href = "/subscribe/error/?error=" + encodeURIComponent(order.error);
            return;
        }

        if (typeof Razorpay === "undefined") {
            console.error("🚨 Razorpay is not loaded. Please check the script inclusion.");
            return;
        }

        var options = {
            "key": razorpayKeyId,  
            "amount": order.amount,
            "currency": order.currency,
            "name": "Skylink",
            "description": "Test Transaction",
            "order_id": order.order_id,
            "handler": function (response) {
                console.log("💰 Payment Successful, Response:", response);

                fetch('/subscribe/verify_payment/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        razorpay_order_id: response.razorpay_order_id,
                        razorpay_payment_id: response.razorpay_payment_id,
                        razorpay_signature: response.razorpay_signature,
                        client_id: clientId,
                        client_name: clientName,
                        end_date: endDate,
                        device_id: deviceId,
                        channel_id: channelId,
                        channel_name: channelName
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("✅ Payment verification success:", data);

                    const redirectUrl = `/subscribe/success?payment_id=${encodeURIComponent(response.razorpay_payment_id)}&order_id=${encodeURIComponent(response.razorpay_order_id)}&signature=${encodeURIComponent(response.razorpay_signature)}&amount=${encodeURIComponent(order.amount)}&currency=${encodeURIComponent(order.currency)}&clientId=${encodeURIComponent(clientId)}&clientName=${encodeURIComponent(clientName)}&endDate=${encodeURIComponent(endDate)}&deviceId=${encodeURIComponent(deviceId)}&channelId=${encodeURIComponent(channelId)}`;

                    window.location.href = redirectUrl;
                })
                .catch(error => {
                    console.error("🚨 Error verifying payment:", error);
                    window.location.href = "/subscribe/error/?error=" + encodeURIComponent("Payment verification failed. Please try again.");
                });
            },
            "theme": { "color": "#3399cc" }
        };

        console.log("⚙️ Initializing Razorpay with options:", options);
        var rzp1 = new Razorpay(options);
        rzp1.open();
    })
    .catch(error => {
        console.error("🚨 Error creating order:", error);
        window.location.href = "/subscribe/error/?error=" + encodeURIComponent("Failed to create payment order. Please try again.");
    });
};

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

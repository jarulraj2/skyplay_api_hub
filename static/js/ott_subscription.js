var randomNum = Math.floor(Math.random() * 1000) + 1;
document.getElementById('randomNumber').innerText = randomNum;

function toggleSidebar() {
    let sidebar = document.getElementById('profileSidebar');
    sidebar.classList.toggle('active');
}

function showOtts(value) {
    // Get the target ID from the data-bs-target attribute
    var targetId = value.dataset.bsTarget;  // This will be something like "#watcho", "#play_box", etc.
    var platformId = value.dataset.id;  // Get platform ID
    var skylinkPlansList = document.querySelector(targetId + ' .card-container'); // Find the .card-container inside this tab
    skylinkPlansList.innerHTML = '';  // Clear the previous content

    var sky_plan_id = 1;  // You can adjust this based on your context
    var randomNumberElement = document.getElementById("randomNumber") // Example client ID, replace it with dynamic value based on your context
    var clientId = randomNumberElement.textContent || randomNumberElement.innerText;
   // var clientId =  1;
    // Fetch the plans for the selected platform
    if (platformId) {
        fetch(`/ott_subscription/get-skylink-plans/?platform_id=${platformId}&sky_plan_id=${sky_plan_id}&clinet_id=${clientId}`)
            .then(response => response.json())
            .then(data => {
                // If we have Skylink plans, display them
                if (data.plans && data.plans.length > 0) {
                    data.plans.forEach(plan => {
                        // Create a new div for each plan (card)
                        var cardDiv = document.createElement('div');
                        cardDiv.classList.add('card', "col-md-4");

                        var cardContentDiv = document.createElement('div');
                        cardContentDiv.classList.add('card-content');

                        var cardTitleDiv = document.createElement('div');
                        cardTitleDiv.classList.add('card-title');
                        cardTitleDiv.textContent = plan.name;
                        cardContentDiv.appendChild(cardTitleDiv);

                        // Add the image wrap (OTTs)
                        var imageWrapDiv = document.createElement('div');
                        imageWrapDiv.classList.add('image-wrap');

                        plan.otts.forEach(ott => {
                            var ottImage = document.createElement('img');
                            ottImage.src = ott.image;  // Set the image source
                            ottImage.alt = ott.name;   // Set the alt text to the OTT name
                            imageWrapDiv.appendChild(ottImage);
                        });

                        cardContentDiv.appendChild(imageWrapDiv);

                        // Add the card text (description) based on plan type
                        var cardTextDiv = document.createElement('div');
                        cardTextDiv.classList.add('card-text');
                        if (plan.subscription_tiers === 'free') {
                            cardTextDiv.textContent = "Activate your free plan instantly."; // Free plan text
                        } else {
                            cardTextDiv.textContent = "Subscribe to access premium content instantly."; // Paid plan text
                        }
                        cardContentDiv.appendChild(cardTextDiv);

                        // Add expiration date below the plan
                        if (plan.status_flag === 1) {
                            var expirationDateDiv = document.createElement('div');
                            expirationDateDiv.classList.add('expiration-date');
                            expirationDateDiv.textContent = 'Expiration Date: ' + (plan.expiration_date || 'N/A'); // Display expiration date
                            cardContentDiv.appendChild(expirationDateDiv);
                        }

                        // Add the subscription button and price based on the plan's tier
                        var subscribeButton = document.createElement('a');
                        subscribeButton.classList.add('card-btn');

                        // Check the subscription tier and adjust the button and price accordingly
                        if (plan.subscription_tiers === 'free') {
                            subscribeButton.textContent = 'Activate Now';  // Free subscription
                            subscribeButton.href = '#';  // Link can be handled for activation

                            // Disable button if the plan is expired
                            if (plan.status_flag === 1) {
                                subscribeButton.classList.add('disabled');
                                subscribeButton.setAttribute('disabled', 'disabled');
                            }

                            // Add event listener for activation
                            subscribeButton.addEventListener('click', function () {
                                // Call the function to activate the OTT subscription for free plan
                                if (plan.status_flag === 0) {
                                    activateOttSubscription(clientId, platformId, plan.id);
                                }
                            });
                        } else {
                            subscribeButton.textContent = 'Pay Now';  // Paid subscription
                            subscribeButton.href = '#';  // Link to payment page or similar

                            // Disable button if the plan is expired
                            if (plan.status_flag === 1) {
                                subscribeButton.classList.add('disabled');
                                subscribeButton.setAttribute('disabled', 'disabled');
                            }

                            // Add price for paid plans
                            var priceDiv = document.createElement('div');
                            priceDiv.classList.add('plan-price');
                            priceDiv.textContent = 'Price: ' + plan.price;  // Show price for paid plans
                            cardContentDiv.appendChild(priceDiv);

                            // Add event listener for Razorpay payment
                            subscribeButton.addEventListener('click', function () {
                                if (plan.status_flag === 0) {
                                    initiateRazorpayPayment(clientId, platformId, plan.id, plan.price);
                                }
                            });
                        }

                        cardContentDiv.appendChild(subscribeButton);

                        cardDiv.appendChild(cardContentDiv);
                        skylinkPlansList.appendChild(cardDiv);  // Append the card to the container
                    });
                } else {
                    skylinkPlansList.textContent = 'No Skylink plans available for this platform.';
                }
            })
            .catch(error => {
                console.error('Error fetching Skylink plans:', error);
            });
    } else {
        skylinkPlansList.innerHTML = '';  // Clear the content if no platform ID
    }
}


// Function to call the ott_activation API with the client ID, platform ID, and plan ID
function activateOttSubscription(clientId, platformId, planId, paymentDetails = {}) {
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature, payment_amount, payment_currency, subscription_tiers = 'free' } = paymentDetails;
    // Define the data to send in the API request
    var data = {
        client_id: clientId,
        platform_id: platformId,
        plan_id: planId,
        subscription_tiers: subscription_tiers
    };

     // Only add payment details for paid subscriptions
     if (subscription_tiers === 'paid') {
        data.razorpay_order_id = razorpay_order_id;
        data.razorpay_payment_id = razorpay_payment_id;
        data.razorpay_signature = razorpay_signature;
        data.payment_amount = payment_amount;
        data.payment_currency = payment_currency;
    }

    // Send the data to the ott_activation API via a POST request
    fetch('/ott_subscription/api/ott_activation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'  // Include CSRF token for Django security
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(result => {
            // Handle success response
            if (result.success) {
                var defaultTab = document.getElementById('watcho-tab');
                showOtts(defaultTab);  // Call the function to load content for Watcho
                alert('Subscription activated successfully!');
              
            } else {
                alert('Failed to activate subscription: ' + result.message);
            }
        })
        .catch(error => {
            console.error('Error activating subscription:', error);
            alert('An error occurred while activating the subscription.');
        });
}

// Function to handle Razorpay payment
async function initiateRazorpayPayment(clientId, platformId, planId, price) {
    var razorpayKeyId = document.getElementById("razorpay-key").dataset.key;
    console.log(razorpayKeyId)
    if (isNaN(price) || price <= 0) {
        alert("Invalid price amount. Please check and try again.");
        return;
    }
    let csrfToken = getCSRFToken();
    if (!csrfToken) {
        console.error("🚨 CSRF Token missing");
        alert("CSRF Token is missing. Please refresh the page.");
        return;
    }


    if (!razorpayKeyId) {
        console.error("Razorpay key is missing. Please check your configuration.");
        alert("Payment service unavailable. Please refresh the page.");
        return;
    }

    let requestData = {
        client_id: clientId,
        platform_id: platformId,
        plan_id: planId,
        amount: parseInt(price), logged_in_user_id: clientId
    };
    try {
        console.log("📤 Sending Order Request:", requestData);

        // Call the server to create a Razorpay order
        let response = await fetch('/ott_subscription/create-ott-order/', {
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
            "description": "OTT Transaction",
            "order_id": order.id,
            "handler": async function (response) {
                console.log("💰 Payment Successful, Response:", response);

                try {
                    let verifyResponse = await fetch('/ott_subscription/verify_payment/', {
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

                    let paymentDetails = {
                        razorpay_order_id: response.razorpay_order_id,
                        razorpay_payment_id: response.razorpay_payment_id,
                        razorpay_signature: response.razorpay_signature,
                        payment_amount: order.amount,
                        payment_currency: order.currency,
                        subscription_tiers: 'paid'  // Mark as paid
                    };
                    activateOttSubscription(clientId, platformId, planId, paymentDetails)
                    let redirectUrl = `/wallet/success?payment_id=${encodeURIComponent(response.razorpay_payment_id)}&order_id=${encodeURIComponent(response.razorpay_order_id)}&signature=${encodeURIComponent(response.razorpay_signature)}&amount=${encodeURIComponent(order.amount)}&currency=${encodeURIComponent(order.currency)}`;
                    // window.location.href = redirectUrl;
                } catch (error) {
                    console.error("🚨 Error verifying payment:", error);
                    alert("Payment verification failed. Please try again.");
                    // window.location.href = "/wallet/error/?error=" + encodeURIComponent("Payment verification failed.");
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
        //window.location.href = "/wallet/error/?error=" + encodeURIComponent("Payment process failed.");
    }
}


function getCSRFToken() {
    let tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : null;
}

// Automatically trigger "Watcho" tab on page load
window.onload = function () {
    // Simulate a click on the active tab (Watcho by default)
    var defaultTab = document.getElementById('watcho-tab');
    showOtts(defaultTab);  // Call the function to load content for Watcho
};

document.addEventListener("DOMContentLoaded", function () {
    // Ensure all elements are available before proceeding
    var razorpayKeyId = document.getElementById("razorpay-key")?.dataset.key;
    var loggedInUserId = document.getElementById("user-id")?.dataset.user;

    // Subscription Form
    var subscriptionForm = document.getElementById('subscription-form');
    var payBtn = document.getElementById('pay-btn-subscription');

    // Check if payBtn exists in the DOM
    if (!payBtn) {
        console.error("❌ 'pay-btn-subscription' button not found in the DOM");
        return;
    }

    // Show subscription confirmation popup
    function showSubscriptionConfirmation(clientName, channelName, amount, clientId, channelId, deviceId, endDate) {
        var confirmationContent = `
            <h3>Subscription Details</h3>
            <p><strong>Client Name:</strong> ${clientName}</p>
            <p><strong>Channel Name:</strong> ${channelName}</p>
            <p><strong>Amount:</strong> ₹${amount}</p>
            <p><strong>Client ID:</strong> ${clientId}</p>
            <p><strong>Channel ID:</strong> ${channelId}</p>
            <p><strong>Device ID:</strong> ${deviceId}</p>
            <p><strong>End Date:</strong> ${endDate}</p>
        `;
        
        var confirmationPopup = document.getElementById('confirmation-popup');
        if (confirmationPopup) {
            confirmationPopup.querySelector('.popup-content').innerHTML = confirmationContent;
            confirmationPopup.style.display = 'block';

            document.getElementById('confirm-subscription-btn').onclick = function () {
                confirmSubscription(clientId, channelId, deviceId, endDate);
            };

            document.getElementById('cancel-subscription-btn').onclick = function () {
                confirmationPopup.style.display = 'none';
            };
        } else {
            console.error("❌ Confirmation popup element not found");
        }
    }

    // Get Client and Channel Details
    async function getClientAndChannelDetails(clientId, channelId) {
        try {
            let csrfToken = getCSRFToken();

            let clientResponse = await fetch(`/subscription/get_client_name/${clientId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            let clientData = await clientResponse.json();
            let clientName = clientData.name;

            let channelResponse = await fetch(`/subscription/get_channel_name/${channelId}/`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            let channelData = await channelResponse.json();
            let channelName = channelData.name;

            return { clientName, channelName };
        } catch (error) {
            console.error("🚨 Error fetching client/channel details:", error);
            alert("Failed to fetch client/channel details. Please try again.");
        }
    }

    // Submit Subscription and Show Confirmation
    payBtn.onclick = async function () {
        console.log("🛎️ Subscription Pay button clicked");

        let clientId = document.getElementById('client-id')?.value.trim();
        let channelId = document.getElementById('channel-id')?.value.trim();
        let deviceId = document.getElementById('device-id')?.value.trim();
        let endDate = document.getElementById('end-date')?.value.trim();

        if (!clientId || !channelId || !deviceId || !endDate) {
            alert("Please fill out all fields.");
            return;
        }

        // Get client and channel names
        let { clientName, channelName } = await getClientAndChannelDetails(clientId, channelId);

        // Fetch subscription amount (this can vary, assume it's dynamic or fetched from backend)
        let amount = 500; // You can replace this with a dynamic amount calculation if needed

        // Show subscription confirmation
        showSubscriptionConfirmation(clientName, channelName, amount, clientId, channelId, deviceId, endDate);
    };

    // Confirm Subscription
    async function confirmSubscription(clientId, channelId, deviceId, endDate) {
        try {
            let csrfToken = getCSRFToken();
            let requestData = { 
                client_id: clientId, 
                channel_id: channelId, 
                device_id: deviceId, 
                end_date: endDate,
                logged_in_user_id: loggedInUserId
            };

            let response = await fetch('/subscription/set_subscribe_to_channel/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(requestData)
            });

            let data = await response.json();
            console.log("✅ Subscription Response:", data);

            if (data.success) {
                alert("Subscription successful!");
                window.location.href = "/subscription/success/";
            } else {
                alert("Failed to subscribe. Please try again.");
            }

        } catch (error) {
            console.error("🚨 Error confirming subscription:", error);
            alert("Subscription failed. Please try again.");
        }
    }

    // ✅ Get CSRF Token
    function getCSRFToken() {
        let tokenElement = document.querySelector('meta[name="csrf-token"]');
        return tokenElement ? tokenElement.getAttribute('content') : null;
    }
});

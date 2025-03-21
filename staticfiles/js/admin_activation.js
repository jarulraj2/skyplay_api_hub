document.addEventListener("DOMContentLoaded", function () {
    var saveButton = document.querySelector('input[name="_save"]');

    if (saveButton) {
        saveButton.addEventListener("click", async function (event) {  
            // Remove the event.preventDefault() to allow form submission
            // event.preventDefault(); 
            
            alert("Button Clicked!");

            // Get required elements
            var clientInput = document.getElementById('id_channel_id');
            var endDateInput = document.getElementById('id_end_date');
            var deviceInput = document.getElementById('id_device_id');
            var channelInput = document.getElementById('id_channel_id');

            if (!clientInput || !endDateInput || !deviceInput || !channelInput) {
                console.error("One or more required fields are missing in the DOM.");
                return;
            }

            // Get values
            var clientId = clientInput.value;
            var endDate = endDateInput.value;
            var deviceId = deviceInput.value;
            var channelId = channelInput.value;          

            if (!clientId || !endDate || !deviceId || !channelId) {
                console.error("Missing required fields for subscription.");
                return; // Prevent API call if fields are missing
            }

            // Construct API URL
            var apiUrl = `/skyplay_api/set_subscribe_to_channel/${clientId}/${endDate}/${deviceId}/${channelId}/`;

            try {
                let response = await fetch(apiUrl, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' }
                });

                let data = await response.json();
                console.log("Subscription API Response:", data);
                
                // After API call completes, submit the form after a short delay
                setTimeout(function() {
                    // Now submit the form (trigger a click event on the save button)
                    saveButton.click(); 
                }, 1000);  // Delay in milliseconds (1 second)
              
            } catch (error) {
                console.error("Error in subscription API:", error);
            }
        });
    } else {
        console.error("Save button not found.");
    }
});

jQuery(document).ready(function($) {
    // Initially hide the chatbox
    $('.chatbot-chatbox').css('display', 'none');

    // Toggle chatbox visibility when the checkbox input is clicked
    $('input[type="checkbox"]').change(function() {
        // Check if the checkbox is checked
        if ($(this).is(':checked')) {
            // If checked, show the chatbox
            $('.chatbot-chatbox').slideDown();
        } else {
            // If unchecked, hide the chatbox
            $('.chatbot-chatbox').slideUp();
        }
    });
});

jQuery(document).ready(function($) {
    // Handle click event on Send button
    $(".chatbot-send").click(function () {
        // Get the current time
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + minute;

        // Get the user input message
        var rawText = $(".chatbot-chat-input").val();

        // Construct HTML for user message
        var userHtml = '<div class="chatbot-chat-message user">' + rawText + '<span class="msg_time" style="font-family: Georgia, serif;font-size: 1.2em; color: blue;">' + str_time + '</span></div>';

        // Append the user message to the chat area
        $(".chatbot-chat-messages").append(userHtml);

        // Clear the input field
        $(".chatbot-chat-input").val("");

        // Send the user message to the Flask API
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/get",
            data: { msg: rawText },
            success: function(data) {
                // Upon successful response from Flask API
                if (data.trim() !== "") { // Check if response is not empty
                    // Construct HTML for bot message
                    var botHtml = '<div class="chatbot-chat-message assistant">' + data + '<span class="msg_time" style="font-family: Georgia, serif;; font-size: 1.2em; color: blue;">' + str_time + '</span></div>';
                    // Append the bot message to the chat area
                    $(".chatbot-chat-messages").append($.parseHTML(botHtml));
                } else {
                    // Response is empty, handle accordingly (e.g., display an error message)
                    console.error("Empty response received from Flask API");
                }
            },
            error: function(xhr, status, error) {
                // Handle error if any
                console.error("Error sending message to Flask API:", error);
            }
        });
    });
});

// Select all elements with the class .chatbot-chat-message
const chatMessages = document.querySelectorAll('.chatbot-chat-message');

// Loop through each chat message element
chatMessages.forEach(message => {
    // Check if the message is empty
    if (!message.textContent.trim()) {
        // If empty, hide the message
        message.style.display = 'none';
    }
});

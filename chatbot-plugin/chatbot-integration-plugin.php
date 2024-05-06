<?php
/*
Plugin Name: Custom Chatbot plugin
Description: A custom chatbot plugin for WordPress.
Version: 1.0
Author: Abhishek kumar
*/



// Enqueue scripts and styles
function custom_chatbot_enqueue_scripts() {
    // Enqueue CSS
    wp_enqueue_style('chatbot-style', plugins_url('assets/css/style.css', __FILE__ ));
    wp_enqueue_style('chatbot-style2', plugins_url('assets/css/toggle.css', __FILE__ ));
    // Enqueue Font Awesome CSS
    wp_enqueue_style('bootstrap-css', '//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css');
    wp_enqueue_style('font-awesome-css', 'https://use.fontawesome.com/releases/v5.5.0/css/all.css');
    // Enqueue JavaScript with jQuery dependency
    wp_enqueue_script('chatbot-script', plugins_url('assets/js/script.js', __FILE__ ), array('jquery'), '1.0', true);
}
add_action('wp_enqueue_scripts', 'custom_chatbot_enqueue_scripts');

// Enqueue CSS
##wp_enqueue_style('chatbot-style', plugins_url('assets/css/style.css', __FILE__ ));

// Hook the chatbox HTML to wp_footer action
add_action('wp_footer', function() {
    ?>
    <input type="checkbox">
    <div class="chatbot-chatbox">
        <div class="chatbot-chat-messages">
            <div class="chatbot-chat-message assistant">
                Hello! I am your assistant.
            </div>
            <div class="chatbot-chat-message user">
                What's up?
            </div>
        </div>
        <div class="chatbot-chat-input-wrapper">
            <textarea class="chatbot-chat-input"></textarea>
            <button class="chatbot-send">Send</button>
        </div>
    </div>
    <?php
});







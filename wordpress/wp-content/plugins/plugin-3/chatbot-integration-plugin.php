<?php
/*
Plugin Name: Custom Chatbot 
Description: A custom chatbot plugin for WordPress.
Version: 1.0
Author: Abhishek Kumar
*/

function enqueue_custom_styles_scripts() {
    // Enqueue Bootstrap CSS
    wp_enqueue_style('bootstrap-css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css');

    // Enqueue Bootstrap JavaScript
    wp_enqueue_script('bootstrap-js', 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js', array('jquery'), '', true);

    // Enqueue jQuery
    wp_enqueue_script('jquery', 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js');

    // Enqueue Font Awesome CSS
    wp_enqueue_style('font-awesome-css', 'https://use.fontawesome.com/releases/v5.5.0/css/all.css');

    // Enqueue Custom CSS
    wp_enqueue_style('custom-css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css');

    // Enqueue Custom JavaScript
    wp_enqueue_script('custom-js', 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js');

    // Enqueue Chatbot CSS
    wp_enqueue_style('chatbot-style', plugins_url('assets/css/style.css', __FILE__ ));

    wp_enqueue_script('chatbot-script', plugins_url('asset/js/script.js', __FILE__ ), array('jquery'), '1.0', true);

}
add_action('wp_enqueue_scripts', 'enqueue_custom_styles_scripts');

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
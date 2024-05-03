<?php
/*
Plugin Name: Webhook Trigger
Description: This plugin triggers a webhook when a post is published or updated.
Version: 1.0
Author: Abhishek kumar
*/

// Register webhook trigger
function register_webhook_trigger() {
    // Trigger webhook for new or updated posts
    add_action('save_post', 'webhook_on_post_save', 10, 3);

    // Send all existing posts to webhook when plugin is activated for the first time or reactivated
    if (get_option('webhook_plugin_activated') !== 'true') {
        send_all_posts_to_webhook();
        update_option('webhook_plugin_activated', 'true');
    }
}
add_action('init', 'register_webhook_trigger');

// Function to send all posts to webhook
function send_all_posts_to_webhook() {
    $args = array(
        'post_type' => 'post', // Change to your post type if necessary
        'post_status' => 'publish',
        'posts_per_page' => -1,
    );
    $posts = get_posts($args);
    foreach ($posts as $post) {
        send_post_to_webhook($post->ID);
    }
}

// Function to send webhook request for a specific post
function send_post_to_webhook($post_id) {
    // Fetch post data
    $post = get_post($post_id);

    // Prepare webhook payload
    $payload = array(
        'post_id' => $post_id,
        'post_title' => $post->post_title,
        'post_content' => $post->post_content,
        'post_url' => get_permalink($post_id),
        // Add any other data you want to include in the payload
    );

    // Webhook URL (replace with your actual webhook URL)
    $webhook_url = 'http://127.0.0.1:5000/webhook';

    // Send POST request to webhook URL
    $response = wp_remote_post($webhook_url, array(
        'body' => json_encode($payload),
        'headers' => array('Content-Type' => 'application/json'),
    ));

    // Check if request was successful
    if (is_wp_error($response)) {
        $error_message = $response->get_error_message();
        error_log("Webhook request failed: $error_message");
    } else {
        $response_code = wp_remote_retrieve_response_code($response);
        if ($response_code !== 200) {
            error_log("Webhook request failed with status code: $response_code");
        }
    }
}

// Function to trigger webhook when a post is published or updated
function webhook_on_post_save($post_id, $post, $update) {
    // Check if this is not an autosave and the post is published or updated
    if (!$update || ($update && $post->post_status === 'publish')) {
        // Ignore revisions
        if (wp_is_post_revision($post_id)) {
            return;
        }

        // Send the post to the webhook URL
        send_post_to_webhook($post_id);
    }
}

// Reset activation option on plugin deactivation
function reset_webhook_activation() {
    delete_option('webhook_plugin_activated');
}
register_deactivation_hook(__FILE__, 'reset_webhook_activation');
?>

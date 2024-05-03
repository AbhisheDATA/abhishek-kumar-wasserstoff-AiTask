import requests
import json
import os

# URL of the WordPress REST API endpoint
wordpress_url = 'http://localhost/wordpress/wp-json/webhook/v1/posts'

# Define the post_list variable outside the function
post_list = []

# Function to add fetched posts to the post_list
def add_to_json(posts, post_list):
    for post in posts:
        # Check if 'post_title' key is present in the post
        if 'post_title' in post:
            # Append post details to the list
            post_list.append({
                'ID': post['ID'],
                'Title': post['post_title'],
                'Content': post['post_content'],
                'Author': post['post_author'],
                'Date': post['post_date']
            })
        else:
            print("Error: 'post_title' key not found in post")

# Function to fetch post details from the WordPress REST API
def fetch_posts_and_save():
    try:
        # Send GET request to the WordPress API endpoint
        response = requests.get(wordpress_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            posts = response.json()
            
            # Check if the JSON file exists
            if os.path.exists('wordpress_posts.json'):
                with open('wordpress_posts.json', 'r') as json_file:
                    existing_posts = json.load(json_file)
                    for post in existing_posts:
                        # Check if 'ID' key is present in the post
                        if 'ID' in post:
                            # Check if the post ID already exists in the existing_posts list
                            if any(existing_post['ID'] == post['ID'] for existing_post in existing_posts):
                                print(f"Post with ID {post['ID']} already exists in JSON file. Skipping...")
                            else:
                                add_to_json(posts, post_list)
                        else:
                            print("Error: 'ID' key not found in post")
            else:
                add_to_json(posts, post_list)

            # Save the post details to a JSON file
            with open('wordpress_posts.json', 'w') as json_file:  # Change 'a' to 'w' to overwrite existing file
                json.dump(post_list, json_file, indent=4)
                print("Posts saved to 'wordpress_posts.json' file successfully!")
        else:
            print("Failed to fetch posts:", response.text)
    except Exception as e:
        print("Error:", e)

# Call the function to fetch posts and save them to a JSON file
fetch_posts_and_save()

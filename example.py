from html2text import HTML2Text

def html_to_text(html):
    # Create an instance of HTML2Text
    h = HTML2Text()

    # Set options to retain links
    h.ignore_links = False
    h.ignore_images = True  # Optionally ignore images if desired

    # Convert HTML to plain text
    return h.handle(html)

# Example usage:
html = "<p>This is a <a href='https://example.com'>link</a> and some <strong>bold</strong> text.</p>"
plain_text = html_to_text(html)
print(plain_text)

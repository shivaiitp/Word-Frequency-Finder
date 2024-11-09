from flask import Flask, request, jsonify  # Import Flask and request handling utilities
from flask_cors import CORS  # Import CORS to allow cross-origin requests
from selenium import webdriver  # Import Selenium for browser automation
from selenium.webdriver.chrome.service import Service  # Service to manage WebDriver execution
from selenium.webdriver.chrome.options import Options  # Options to configure Chrome (e.g., headless)
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manages ChromeDriver version
from bs4 import BeautifulSoup  # BeautifulSoup for parsing HTML content
import re  # Regular expressions for text processing
from collections import Counter  # Counter for counting word frequencies
import time  # Time for adding delays

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Function to fetch dynamic content from a URL
def fetch_dynamic_content(url):
    # Configure Chrome options for headless mode to run without a GUI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
    chrome_options.add_argument("--no-sandbox")  # Needed for running in some restricted environments

    # Set up the Chrome driver using the ChromeDriverManager for compatibility
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Wait for JavaScript content to load

    # Retrieve the page source (HTML) after JavaScript rendering
    html = driver.page_source
    driver.quit()  # Close the browser session

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Extract and clean visible text from HTML
    visible_text = soup.get_text(separator=' ')
    visible_text = re.sub(r'\s+', ' ', visible_text).strip()  # Remove extra whitespaces
    return visible_text

# Function to calculate the most frequent words in a text
def calculate_top_words(text, n=10):
    # Tokenize text into words and count frequency (case-insensitive)
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    # Return the 'n' most common words as a dictionary
    return dict(word_counts.most_common(n))

# API route to process the URL and return top frequent words
@app.route('/api/words', methods=['POST'])
def get_top_words():
    # Parse JSON data from request
    data = request.json
    url = data.get('url')
    n = data.get('n', 10)  # Default number of top words is 10
    
    # Validate if URL is provided
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Fetch the dynamic content and calculate top words
        text = fetch_dynamic_content(url)
        top_words = calculate_top_words(text, int(n))
        return jsonify(top_words)
    except Exception as e:
        # Handle any errors and return error message
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

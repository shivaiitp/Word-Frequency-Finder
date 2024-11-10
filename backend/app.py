from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
from collections import Counter
import time

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Initialize an in-memory cache to store content for each URL
cache = {}

# Function to fetch dynamic content from a URL
def fetch_dynamic_content(url):
    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up the Chrome driver using ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Wait for JavaScript content to load

    # Retrieve the page source (HTML) after JavaScript rendering
    html = driver.page_source
    driver.quit()

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Extract and clean visible text from HTML
    visible_text = soup.get_text(separator=' ')
    visible_text = re.sub(r'\s+', ' ', visible_text).strip()
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

    # Check if the URL content is in cache
    if url in cache:
        text = cache[url]  # Retrieve content from cache
    else:
        # Fetch new content if not in cache and save it
        try:
            text = fetch_dynamic_content(url)
            cache[url] = text
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Calculate top words with the cached content or newly fetched content
    top_words = calculate_top_words(text, int(n))
    return jsonify(top_words)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

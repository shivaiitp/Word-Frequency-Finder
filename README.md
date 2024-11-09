
# Word Frequency Finder

A simple application that extracts and identifies the most frequent words from a dynamically rendered web page using a specified URL. The application consists of a backend API developed with Flask and Selenium and a frontend interface built with HTML and Tailwind CSS. This tool is particularly useful for analyzing frequently used words on websites that require JavaScript to render their content.

## Features

- **Backend with Flask**: Extracts visible text content from a dynamically rendered webpage.
- **Selenium for Web Scraping**: Uses a headless browser to render JavaScript-heavy pages and retrieve page content.
- **Word Frequency Analysis**: Parses text to identify and count word occurrences.
- **Frontend with Tailwind CSS**: Provides a clean UI for users to input URLs and view word frequency results.
- **Loader Animation**: Indicates data fetching in progress.

## Prerequisites

- **Python** (recommended version 3.8 or higher)
- **Flask** and **Flask-CORS**
- **Selenium** and **webdriver-manager**
- **Google Chrome** and **ChromeDriver** installed on your system

To install the required Python packages:
```bash
pip install flask flask-cors selenium webdriver-manager beautifulsoup4
```

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Set Up ChromeDriver**:
   Ensure Google Chrome is installed on your system as Selenium uses ChromeDriver for browser automation. Webdriver-manager automatically manages the version.

3. **Run the Backend Server**:
   Start the Flask server to handle requests from the frontend.
   ```bash
   python app.py
   ```
   By default, this runs the server on `http://127.0.0.1:5000`.

4. **Open the Frontend**:
   Open `index.html` in a browser to access the frontend interface.

## Usage

1. **Enter the URL** of the webpage from which to extract the most frequent words.
2. **Specify the Number of Words (N)** to display (optional; defaults to 10).
3. **Click "Get Words"** to retrieve and display the top N words and their frequencies in a table.

## Project Structure

- **app.py**: Backend Flask application containing the API endpoint and scraping logic.
- **index.html**: Frontend interface for user input and result display.
- **static**: Contains Tailwind CSS for styling.

## API Endpoint

- **Endpoint**: `POST /api/words`
- **Request JSON**:
   ```json
   {
       "url": "https://example.com",
       "n": 10
   }
   ```
- **Response JSON**:
   ```json
   {
       "word": frequency,
       ...
   }
   ```

## Technologies Used

- **Backend**: Python, Flask, Selenium, BeautifulSoup
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Other**: Webdriver-Manager for managing ChromeDriver

## License

This project is licensed under the MIT License.

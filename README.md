AI-Powered Instagram Reel Classifier
This project is an automated tool for analyzing Instagram Reels. It uses the Playwright library to navigate Instagram, scrape reel content (captions and comments), and then leverages a large language model (LLM) to classify the content.

The tool is designed to provide a customizable and efficient way to categorize vast amounts of video content based on user engagement and text.

Features
Automated Scraping: Automatically watches and scrapes data from Instagram Reels.

AI Integration: Utilizes various LLMs (Groq, OpenAI, Google Gemini, Ollama) for intelligent content classification.

Persistent Sessions: Uses cookies to save login sessions, avoiding the need to log in repeatedly.

Command-Line Interface (CLI): Easy-to-use command-line arguments for controlling the scraping process.

Data Export: Saves classified data to both JSON and CSV files for easy analysis.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x: The script is written in Python.

Pip: Python's package installer.

Google Chrome: The script uses a Chromium browser channel.

Installation
Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

Install dependencies:

pip install -r requirements.txt

Note: You may need to create a requirements.txt file by running pip freeze > requirements.txt after installing all your project's dependencies.

Set up configuration and API keys:

Create a config.json file in the root directory. This file should contain configuration settings, such as data saving preferences.

{
  "processing": {
    "save_to_json": true,
    "save_to_csv": true
  }
}

Create an api_key.py file to store your API keys securely.

API_KEY = "your_groq_api_key_here"
openrouter_api = "your_openrouter_api_key_here"
google_gemini_api_key = "your_google_gemini_api_key_here"
# Add any other API keys you need here

Usage
The script is controlled via the start.py file with command-line arguments.

1. Initial Login:
To log in for the first time and save cookies, use the --relogin flag. The script will pause and wait for you to log in manually.

python start.py --relogin true

2. Running the Analyzer:
Once your cookies are saved, you can run the script normally.

Run indefinitely:

python start.py

Run for a specific number of iterations (e.g., 40 batches of reels):

python start.py --it 40

Project Structure
start.py: The command-line interface entry point. Handles parsing arguments.

main.py: Contains the core logic for the Playwright automation, including navigating to the Instagram Reels page, watching videos, and calling other functions.

handle_comments.py: A utility script for extracting, cleaning, and handling comments from the page's HTML.

additional_tools.py: A collection of functions for interacting with various AI APIs and for saving the processed data to different file formats (JSON, CSV).

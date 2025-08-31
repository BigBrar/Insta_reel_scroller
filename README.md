# AI-Powered Instagram Reel Trainer

Ever feel like your Instagram feed is just endless "brain rot"? You know, those pointless videos that just make you scroll forever without actually learning or doing anything useful? This project is here to help you fight back.

This tool is a simple but smart way to teach the Instagram algorithm what you actually want to see. Instead of a feed full of junk food content, you can train it to serve you a healthy diet of informational and useful reels.

It's perfect if you want to take back control of your own digital life or if you're trying to help a loved one (like your little brother or sister) spend less time on those dopamine-heavy platforms.

---

### Features

* **Smart Reels Trainer:** Automatically watches and analyzes reels to figure out what kind of content they are.
* **AI-Powered:** Uses awesome large language models (Groq, OpenAI, Google Gemini, Ollama) to classify reels based on their content, captions, and comments.
* **Set and Forget:** Uses cookies to save your Instagram login, so you don't have to deal with logging in every time you run the script.
* **Easy to Use:** Just a few simple command-line arguments to get the ball rolling.
* **Data Export:** Saves all the classified data into handy JSON and CSV files for you to look at later.

---

### Installation

To get this project up and running, all you need is a working installation of the `chrome playwright channel`.

1.  **Clone the repository:**

    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```
    *Note: You may need to create a `requirements.txt` file by running `pip freeze > requirements.txt` after installing all your project's dependencies.*

3.  **Set up configuration and API keys:**

    * Create a `config.json` file in the main directory to set up your preferences.

    ```json
    {
      "processing": {
        "save_to_json": true,
        "save_to_csv": true
      }
    }
    ```

    * Create an `api_key.py` file to keep all your API keys safe and sound.

    ```python
    API_KEY = "your_groq_api_key_here"
    openrouter_api = "your_openrouter_api_key_here"
    google_gemini_api_key = "your_google_gemini_api_key_here"
    # Add any other API keys you need here
    ```

---

### Usage

Ready to start training the algorithm? Just use the `start.py` file with these commands.

**1. Initial Login:**
The first time you run this, you'll need to log in manually. Just use the `--relogin` flag, and the script will pause and wait for you.

```sh
python start.py --relogin true

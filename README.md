# LinkedIn Auto-Decline Bot 🤖✋

A Python bot that automates declining sales pitches and recruitment offers on LinkedIn. It uses **Playwright** for browser automation and **Google Gemini** (LLM) to generate polite, context-aware, and multi-lingual responses.

## Features

- **Smart Detection**: Filters messages based on keywords (e.g., "recruitment", "sales", "outsourcing", "php", "java").
- **AI-Powered Responses**: Uses Google Gemini to write tailored responses in the same language as the sender (English/Czech/etc.).
- **Safety First**:
  - **Draft Mode**: By default, the bot only *types* the message and waits for your manual confirmation before sending.
  - **Duplicate Check**: Prevents replying to the same person twice.
  - **Human-like Delays**: Random pauses to avoid triggering anti-bot protections.

## Prerequisites

- Python 3.8+
- A LinkedIn account
- A Google Gemini API Key (free via [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/padak/linkedin_no-thanks.git
   cd linkedin_no-thanks
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=AIzaSy...YourKeyHere...
   ```

## Usage

### 1. Authentication
First, you need to log in to LinkedIn to save your session cookies.
Run the auth script:
```bash
python auth.py
```
- A browser window will open.
- Log in to LinkedIn manually.
- Once you reach the feed, the script will save your session to `state.json` and close.

### 2. Running the Bot
Start the bot:
```bash
python bot.py
```

- The bot will open the browser and navigate to your messages.
- It will scan the last 50 conversations.
- If it finds a sales/recruitment message, it will generate a response and type it into the message box.
- **Review the message**: Since `DRAFT_MODE` is on by default, you must press **Enter** in the terminal to move to the next conversation. You can manually click "Send" in the browser if you like the draft.

### 3. Auto-Sending (Optional)
To enable automatic sending without manual review:
1. Open `bot.py`.
2. Change `DRAFT_MODE = True` to `DRAFT_MODE = False`.

## Disclaimer
**Use at your own risk.** Automating LinkedIn interactions violates their Terms of Service and can lead to account restriction or banning. This tool is intended for educational purposes only.

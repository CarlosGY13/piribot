## Piribot – Companion chatbot for pregnant women

Piribot is a conversational Telegram chatbot that provides **general information**, **basic guidance**, and **emotional support** for pregnant women.  
It is designed to work in **Spanish**, **Quechua**, and **Shipibo-Konibo**, with a respectful, simple, and intercultural tone.

**Piribot does NOT replace a health professional.  
It does not make medical diagnoses or prescribe specific treatments.**

---

### Main features

- **Telegram bot** for pregnancy support.
- Uses **Google Gemini** (official API) to generate responses.
- Speaks **Spanish (es)**, **Quechua (qu)** and **Shipibo-Konibo (shp)**.
- Provides:
  - General information about pregnancy.
  - Emotional support and accompaniment.
  - Recommendations to visit a health center when there are doubts or warning signs.
- Includes:
  - `/start` command with welcome and language selection.
  - Text-only interaction (no voice).
  - Visible medical disclaimer.
  - Basic detection of possible **warning signs** (bleeding, strong pain, fever, etc.) to suggest going to a health facility.

Piribot **does not store personal data** and does not define any database.  
Messages are processed in memory only to build the AI model response.

---

### Using Piribot on Telegram

- Open the Telegram app.
- Search for the bot by username: **`Piriht_bot`**.
- Type `/start`.
- Choose the language you prefer (Spanish, Quechua or Shipibo-Konibo).
- Then you can write how you feel, your questions about pregnancy or comments about your exams (via text or image with caption), and Piribot will answer with general information and emotional support.

---

### Prerequisites (only if you want to run your own instance)

- **Python 3.10+**
- Telegram account (to get a bot token if you run your own backend).
- Google Gemini account and API key.

---

### 1. Get and configure the Google Gemini API (development)

1. Go to the Google Gemini developer page (`https://ai.google.dev/`).
2. Create an account or sign in with your Google account.
3. Create a project and enable the Gemini API.
4. Generate an **API key**.
5. Copy the key: you will use it to configure the project.

> Be aware of usage, privacy and cost policies of the API.

---

### 2. Prepare the local environment (development)

Go to your project folder:

```bash
cd piribot
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables (development)

At the project root there is a `.env.example` file.  
Copy it to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# Default language before the user chooses one.
# es = Spanish, qu = Quechua, shp = Shipibo-Konibo
PIRIBOT_DEFAULT_LANGUAGE=es
```

---

### 4. Run Piribot (development)

From the project root:

```bash
python main.py
```

If the configuration is correct, you will see a log message indicating the bot is running.

Then:

1. Open Telegram.
2. Search for the public bot **`Piriht_bot`** (or the bot you configured in your development environment).
3. Type `/start`.

You should see:

- A welcome message.
- A message to choose the language (Spanish, Quechua, Shipibo-Konibo).
- A medical disclaimer.

From there you can send your questions or share how you feel, and Piribot will answer.

---

### 6. Basic usage flow

- **/start**  
  - Starts the conversation.
  - Shows the language selection keyboard.
  - Sends the disclaimer.

- **/help**  
  - Shows example questions and reminders on how to use the bot.

- **/language**  
  - Shows the language selection keyboard again.

- **Text messages**  
  - The bot uses the user’s chosen language.
  - Performs a very simple detection of possible **warning signs** using keywords (`data/alerts.json`).
  - Sends a local warning message (if appropriate).
  - Calls Google Gemini with a prompt designed to:
    - Avoid diagnoses.
    - Avoid prescribing specific treatments or doses.
    - Use simple, empathetic language.
    - Recommend going to a health center when there are important doubts or warning signs.
  - Always adds a disclaimer at the end.

- **Exam images**  
  - You can send photos of lab tests or medical exams with a short caption explaining what they are.
  - Piribot can comment in general terms on what type of exam it is and what it usually measures. If the result itself includes **reference ranges**, Piribot can say whether your value is inside or outside those ranges (for example, “this value is within the lab’s reference range”).  
  - Still, it **does not diagnose or say whether you are healthy or sick**; it will always remind you that results must be reviewed by a health professional.

> The bot does **not** process voice messages.  
> It mainly works with text and, in a limited way, with images accompanied by text.

---

### 7. Project structure

```text
piribot/
  bot/
    __init__.py          # Telegram bot package
    telegram_bot.py      # Handlers, conversation flow and Application configuration
    gemini_client.py     # Simple client for the Google Gemini API
    prompts.py           # Base system prompt builder
    language.py          # Language handling and static messages
  data/
    alerts.json          # Keywords and messages for basic alert detection
    faq.json             # Example FAQs used as context
  config:
    settings.py          # Environment settings loader and validation
  main.py                # Bot entry point
  requirements.txt       # Minimal dependencies
  .env.example           # Example environment configuration
  README.md              # This file
```

---

### 8. Ethical and safety considerations

Piribot is designed with basic **safety** and **do-no-harm** principles:

- It does not replace care from a health professional.
- It does not make medical diagnoses.
- It does not prescribe treatments or medication doses.
- It recommends going to a health center or hospital when there are:
  - Very strong pain.
  - Bleeding.
  - Fever.
  - Loss of fluid.
  - No perceived fetal movements.
  - Difficulty breathing, seizures, fainting or other warning signs.
- It does not ask for personally identifiable information.
- Messages are used only in memory to build the AI response and are not stored in a database.

For real-world deployment, we recommend:

- Reviewing and improving Quechua and Shipibo-Konibo translations with native speakers.
- Adapting prompts and messages to the specific cultural context.
- Reviewing privacy and consent policies according to local regulations (e.g., personal data protection laws in Peru).

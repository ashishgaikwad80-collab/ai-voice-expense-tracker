# 📌 AI Voice Expense Tracker with Speech-to-Text

An intelligent **Python-based Voice Expense Tracker** that allows users to manage their daily expenses using voice commands. It converts spoken words into text and automatically extracts and logs financial data (Amount, Category, Description). Developed as an interview portfolio project.

## 🛠️ Tech Stack & Tools
- **Language:** Python 3.x
- **Speech Recognition:** `SpeechRecognition` library (Google Speech-to-Text API)
- **Audio Processing:** `PyAudio` (for microphone input)
- **Database/Storage:** `CSV` / `SQLite` (to store expense records)

## 🔄 How It Works (Project Workflow)
1. **Voice Input:** The system listens to the user's voice command through the microphone (e.g., *"Spent 50 rupees on coffee"*).
2. **Speech-to-Text Conversion:** The `SpeechRecognition` library converts the recorded audio into text.
3. **Data Extraction:** The Python script parses the text to find the **Amount** (50), **Category** (Food/Coffee), and **Date**.
4. **Data Logging:** The extracted information is automatically saved into an Excel/CSV file or database for tracking.

## 💡 Key Features
- **Hands-Free Logging:** Add expenses instantly just by speaking.
- **Real-Time Processing:** Quick conversion from speech to organized text.
- **Automated Categorization:** Smartly identifies numbers as amounts and words as expense categories.

## 🚀 How to Run the Project

Follow these steps to run the project on your local machine:

### 1. Clone the Repository
```bash
git clone [[https://github.com/ashishgaikwad80-collab/ai-voice-expense-tracker]
cd [ashishgaikwad80_collab]
```

### 2. Install Dependencies
Make sure you install the required Python packages before running the application:
```bash
pip install SpeechRecognition pyaudio
```
*(Note: If you face issues installing pyaudio on Windows, use `pip install pipwin` followed by `pipwin install pyaudio`)*

### 3. Run the Application
Execute your main Python file:
```bash
python [newgitaivoice].py
```

## 📄 License
This project is licensed under the **MIT License** - see the `LICENSE` file for details.

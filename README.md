# SerenityAI 🤖💬



**SerenityAI** is a mental health chatbot designed to provide a safe, supportive space for users to express their feelings, track their mood, and access mental health resources. Built with **Python** and **PyQt5**, it combines an intuitive UI with emotion detection (mocked in this version) to offer personalized support. 🌟

---

## ✨ Features

- **💬 Chat Interface** – Engage in natural conversations and receive empathetic responses.
- **🧠 Emotion Detection** – Uses a DistilBERT model to detect emotions (mocked; training steps included).
- **📋 Mental Health Quiz** – Take a PHQ-9-based assessment for mental health evaluation.
- **📊 Mood Tracker** – Visualize mood trends over time with graphical insights.
- **🎙️ Voice Input** – Speak to the bot using hands-free voice recognition.
- **🚨 Emergency Support** – Detects crisis situations and provides immediate helpline resources.

---

## 🌟 How It Helps

- **Safe Space** 🛡️ – Share emotions without judgment in a private environment.
- **Self-Awareness** 📈 – Mood tracking and quizzes aid emotional insight.
- **Accessibility** 🎤 – Voice input simplifies user interaction.
- **Crisis Support** 📞 – Helpline access in urgent situations.
- **Encouragement** 💖 – Receive motivational quotes and empathetic responses.

---

## 🛠️ Setup and Installation

### Prerequisites
- **Python 3.8+** 🐍
- **Git** (`brew install git` on macOS)
- **Virtual Environment** (recommended)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/AbhiShek-vardhanapu/SerenityAI.git
   cd SerenityAI
   ```
2. **Set Up a Virtual Environment** (optional but recommended)
   ```bash
   python3 -m venv serenity
   source serenity/bin/activate  # On Windows: serenity\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add Icon Files** (Ensure the following icons are in the project directory):
   - `logo.png` (App logo)
   - `mic_icon.png` (Microphone icon)
   - `quiz_icon.png` (Quiz icon)
   - `mood_icon.png` (Mood chart icon)

5. **Run the Chatbot**
   ```bash
   python chatbot.py
   ```

---

## 🏋️ Training the Model

SerenityAI currently uses mocked emotion detection. To train a real model:

1. **Prepare a Dataset**
   - Use an emotion classification dataset (e.g., [Emotion Dataset](https://huggingface.co/datasets)).
2. **Install Additional Dependencies**
   ```bash
   pip install transformers torch datasets
   ```
3. **Train DistilBERT Model**
   - Expect ~85-90% accuracy after 3 epochs.

---

## 🎨 UI Design

- **Dark Theme** 🎨 – Calming navy blue and black tones.
- **Chat Bubbles** 💬 – User messages on the right, bot messages on the left.
- **Toolbar Icons** 🛠️ – Quick access to quizzes and mood tracking.

---

## 🔍 Functionality

- **Chat** – SerenityAI provides empathetic responses based on your emotions.
- **Quiz** – PHQ-9 scale evaluation (scores range from 0-27).
- **Mood Tracker** – Saves trends in `mood_history.csv` and visualizes data.
- **Voice Input** – Speak instead of typing for seamless interaction.
- **Emergency Support** – Crisis keywords trigger helpline recommendations.

---

## 🚀 How to Use SerenityAI

1. **Start the Chatbot**
   ```bash
   python chatbot.py
   ```
2. **Chat with SerenityAI**
   - Respond to: *"How are you feeling today?"*
   - Example: *"I’m feeling sad."* → *"You are stronger than you think."*
3. **Take the Quiz**
   - Click **Quiz** 📋 to start the PHQ-9 assessment.
4. **Track Your Mood**
   - Click **Mood** 📊 to see emotional trends.
5. **Use Voice Input**
   - Click **Microphone** 🎙️ to speak instead of typing.
6. **Access Emergency Support**
   - Crisis phrases trigger **helpline recommendations**. 📞

---

## 👨‍💻 About

SerenityAI is an open-source project aimed at supporting mental health awareness. It is not a substitute for professional help but serves as a first step towards emotional well-being.

- **Developer**: [AbhiShek Vardhanapu](https://github.com/AbhiShek-vardhanapu)
- **Created**: April 2025
- **License**: MIT License (see `LICENSE` file)

---

## 🤝 Contributing

We welcome contributions! 🛠️

1. **Fork the repository**
2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make changes and commit**
   ```bash
   git commit -m "Add your feature"
   ```
4. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```
5. **Open a Pull Request** on GitHub.

---

## 📜 License

This project is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for details.

---

## ❓ Need Help?

If you have questions or issues, open an **issue on GitHub** or reach out to the developer. Let’s make mental health support accessible for everyone! 🚀

---

### 📌 How to Add This `README.md` to Your Repository

1. **Create the `README.md` File**
   ```bash
   nano README.md
   ```
   - Paste the content and save (Ctrl+O, then Ctrl+X in nano).

2. **Add and Commit the README.md**
   ```bash
   git add README.md
   git commit -m "Add professional README"
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   ```

4. **Verify on GitHub**
   - Visit [SerenityAI Repo](https://github.com/AbhiShek-vardhanapu/SerenityAI) to see the updated `README.md`.

This README gives **SerenityAI** a professional look on GitHub! 🚀 Let me know if you need any modifications! 🎯

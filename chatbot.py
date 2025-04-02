import sys
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QStatusBar,
                            QDialog, QRadioButton, QButtonGroup, QMessageBox)
from PyQt5.QtGui import QTextCursor, QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize
import speech_recognition as sr
from datetime import datetime
import numpy as np

class QuizDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mental Health Assessment")
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumSize(550, 450)
        
        # Set dark background
        self.setStyleSheet("""
            QDialog {
                background-color: #1E3A4D;
            }
            QLabel {
                color: #E0ECE4;
                font-size: 14px;
            }
        """)
        
        self.questions = [
            "Little interest or pleasure in doing things?",
            "Feeling down, depressed, or hopeless?",
            "Trouble falling or staying asleep, or sleeping too much?",
            "Feeling tired or having little energy?",
            "Poor appetite or overeating?",
            "Feeling bad about yourself or that you're a failure?",
            "Trouble concentrating on things?",
            "Moving or speaking slowly, or being fidgety?",
            "Thoughts that you would be better off dead?"
        ]
        
        self.responses = {
            "Not at all": 0,
            "Several days": 1,
            "More than half the days": 2,
            "Nearly every day": 3
        }
        
        self.current_question = 0
        self.scores = []
        
        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Question label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("""
            font-size: 15px; 
            font-weight: bold;
            color: #E0ECE4;
            padding-bottom: 10px;
        """)
        self.layout.addWidget(self.question_label)
        
        # Response options
        self.options_group = QButtonGroup(self)
        for text, value in self.responses.items():
            radio = QRadioButton(text)
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 14px; 
                    padding: 8px;
                    color: #E0ECE4;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            self.options_group.addButton(radio, value)
            self.layout.addWidget(radio)
        
        # Navigation buttons
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setSpacing(15)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet("""
            QPushButton {
                background-color: #4A7685;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5A8799;
            }
            QPushButton:disabled {
                background-color: #2A527A;
                color: #7F9FB5;
            }
        """)
        self.prev_button.clicked.connect(self.prev_question)
        self.prev_button.setEnabled(False)
        self.nav_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5AA0F2;
            }
        """)
        self.next_button.clicked.connect(self.next_question)
        self.nav_layout.addWidget(self.next_button)
        
        self.layout.addLayout(self.nav_layout)
        
        # Progress indicator
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-size: 13px; color: #7F9FB5;")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress_label)

    def show_question(self):
        self.question_label.setText(self.questions[self.current_question])
        self.progress_label.setText(f"Question {self.current_question + 1} of {len(self.questions)}")
        
        # Clear selection
        self.options_group.setExclusive(False)
        for btn in self.options_group.buttons():
            btn.setChecked(False)
        self.options_group.setExclusive(True)
        
        # Update navigation
        self.prev_button.setEnabled(self.current_question > 0)
        self.next_button.setText("Finish" if self.current_question == len(self.questions) - 1 else "Next")

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()

    def next_question(self):
        selected = self.options_group.checkedButton()
        if not selected and self.next_button.text() != "Finish":
            QMessageBox.warning(self, "Selection Needed", "Please select an option before continuing.")
            return
        
        if selected:
            self.scores.append(self.options_group.id(selected))
        
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.accept()

    def get_score(self):
        return sum(self.scores)

class MoodChartDialog(QDialog):
    def __init__(self, mood_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Your Mood History")
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumSize(650, 450)
        
        self.setStyleSheet("background-color: #1E3A4D;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create figure with dark theme
        plt.style.use('dark_background')
        self.figure = plt.figure(facecolor='#1E3A4D')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        # Plot data
        self.plot_mood_data(mood_data)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #4A7685;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 100px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #5A8799;
            }
        """)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button, 0, Qt.AlignCenter)

    def plot_mood_data(self, mood_data):
        ax = self.figure.add_subplot(111)
        
        # Sample data (replace with actual mood data)
        dates = [datetime.now().replace(hour=0, minute=0, second=0) for _ in range(15)]
        scores = [random.randint(1, 10) for _ in range(15)]
        
        ax.plot(dates, scores, marker='o', color='#4A90E2', linewidth=2, markersize=8)
        ax.set_title("Your Mood Over Time", color='#E0ECE4', pad=20)
        ax.set_xlabel("Date", color='#7F9FB5')
        ax.set_ylabel("Mood Score (1-10)", color='#7F9FB5')
        
        # Customize appearance
        ax.set_facecolor('#1E3A4D')
        self.figure.patch.set_facecolor('#1E3A4D')
        ax.tick_params(colors='#7F9FB5')
        ax.grid(color='#2A527A', linestyle='--', alpha=0.5)
        
        for spine in ax.spines.values():
            spine.set_color('#7F9FB5')
        
        self.canvas.draw()

class SerenityChatbot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.name = None
        self.dark_mode = True
        self.mood_history = []
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        self.responses = {
            "sad": [
                "I'm sorry you're feeling sad. It takes courage to acknowledge these feelings.\n"
                "Would you like to talk about what's bothering you?",
                
                "It's completely normal to feel sad sometimes. These emotions are part of being human.\n"
                "Remember that feelings are temporary visitors.",
                
                "I'm here to listen without judgment if you'd like to share what's making you feel this way."
            ],
            "happy": [
                "That's wonderful to hear! What's bringing you happiness today?\n"
                "Savoring these moments can help build emotional resilience.",
                
                "It's heartening to know you're experiencing happiness.\n"
                "Would you like to share what's creating these good feelings?",
                
                "Happiness is precious and deserves attention.\n"
                "I'm glad you're experiencing this."
            ],
            "default": [
                "Thank you for sharing your feelings with me.\n"
                "Would you like to elaborate on how you're feeling?",
                
                "Your feelings matter, whatever they may be.\n"
                "Would you like to talk more about what you're experiencing?",
                
                "I appreciate you opening up about how you're feeling.\n"
                "Would you like to explore these feelings further?"
            ]
        }
        
        self.setup_ui()
        self.show_welcome_message()
        self.apply_theme()

    def setup_ui(self):
        self.setWindowTitle("SerenityAI - Mental Health Companion")
        self.setGeometry(100, 100, 850, 650)
        self.setMinimumSize(700, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFrameShape(QFrame.NoFrame)
        self.chat_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #0F1C26;
                color: #E0ECE4;
                font-family: 'Helvetica Neue', Arial;
                font-size: 14px;
                padding: 20px;
                border: none;
                line-height: 1.5;
            }
            QScrollBar:vertical {
                border: none;
                background: #1E3A4D;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #4A7685;
                min-height: 20px;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.chat_area)
        
        # Input area
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #1E3A4D;
                border-top: 1px solid #2A527A;
                padding: 12px;
            }
        """)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 5, 10, 5)
        input_layout.setSpacing(10)
        
        # Voice button - now with proper icon
        self.voice_button = QPushButton()
        self.voice_button.setIcon(QIcon.fromTheme("audio-input-microphone"))
        if self.voice_button.icon().isNull():
            # Fallback icon if system icon not available
            self.voice_button.setText("🎤")
        self.voice_button.setIconSize(QSize(24, 24))
        self.voice_button.setFixedSize(40, 40)
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #4A7685;
                border-radius: 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5A8799;
            }
            QPushButton:pressed {
                background-color: #3A6575;
            }
        """)
        self.voice_button.setToolTip("Voice input")
        self.voice_button.clicked.connect(self.toggle_voice_input)
        input_layout.addWidget(self.voice_button)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type how you're feeling...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2A527A;
                color: white;
                border: 1px solid #3D5A66;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, 1)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(90, 40)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5AA0F2;
            }
            QPushButton:pressed {
                background-color: #3A80D2;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        # Tools layout
        tools_layout = QHBoxLayout()
        tools_layout.setContentsMargins(10, 5, 10, 5)
        tools_layout.setSpacing(10)
        
        # Quiz button
        self.quiz_button = QPushButton("Mental Health Quiz")
        self.quiz_button.setStyleSheet("""
            QPushButton {
                background-color: #5A7685;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6A8799;
            }
        """)
        self.quiz_button.clicked.connect(self.start_quiz)
        tools_layout.addWidget(self.quiz_button)
        
        # Mood chart button
        self.mood_button = QPushButton("View Mood Chart")
        self.mood_button.setStyleSheet("""
            QPushButton {
                background-color: #5A7685;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6A8799;
            }
        """)
        self.mood_button.clicked.connect(self.show_mood_chart)
        tools_layout.addWidget(self.mood_button)
        
        main_layout.addWidget(input_frame)
        main_layout.addLayout(tools_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #1E3A4D;
                color: #E0ECE4;
                border-top: 1px solid #2A527A;
                font-size: 12px;
                padding: 5px;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def apply_theme(self):
        palette = self.palette()
        if self.dark_mode:
            palette.setColor(palette.Window, QColor(15, 28, 38))
            palette.setColor(palette.WindowText, QColor(224, 236, 228))
            palette.setColor(palette.Base, QColor(30, 58, 77))
            palette.setColor(palette.Text, QColor(224, 236, 228))
            palette.setColor(palette.Button, QColor(42, 82, 122))
            palette.setColor(palette.ButtonText, QColor(224, 236, 228))
        else:
            palette.setColor(palette.Window, QColor(240, 240, 240))
            palette.setColor(palette.WindowText, Qt.black)
            palette.setColor(palette.Base, QColor(255, 255, 255))
            palette.setColor(palette.Text, Qt.black)
            palette.setColor(palette.Button, QColor(240, 240, 240))
            palette.setColor(palette.ButtonText, Qt.black)
        self.setPalette(palette)

    def show_welcome_message(self):
        welcome_msg = """
        <div style='margin-bottom: 20px;'>
            <div style='background-color: #1E3A4D; color: #E0ECE4; border-radius: 10px; 
                        padding: 15px; display: inline-block; max-width: 80%; 
                        line-height: 1.5;'>
                <b>🤖 SerenityAI:</b> Welcome to your mental health companion.<br><br>
                I'm here to provide a safe space where you can express your feelings.<br><br>
                To begin, may I know your name?
            </div>
        </div>
        """
        self.append_to_chat(welcome_msg)

    def append_to_chat(self, html, is_user=False):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if is_user:
            html = f"""
            <div style='margin-bottom: 15px; text-align: right;'>
                <div style='background-color: #2A527A; color: white; border-radius: 10px; 
                            padding: 12px 15px; display: inline-block; max-width: 80%; 
                            line-height: 1.5;'>
                    {html}
                </div>
            </div>
            """
        else:
            html = f"""
            <div style='margin-bottom: 15px;'>
                <div style='background-color: #1E3A4D; color: #E0ECE4; border-radius: 10px; 
                            padding: 12px 15px; display: inline-block; max-width: 80%; 
                            line-height: 1.5;'>
                    {html}
                </div>
            </div>
            """
        
        cursor.insertHtml(html)
        self.chat_area.ensureCursorVisible()

    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return
        
        self.append_to_chat(message, is_user=True)
        self.input_field.clear()
        self.process_user_message(message)

    def process_user_message(self, message):
        # First message is name
        if not self.name:
            self.name = message
            response = f"""
            <b>🤖 SerenityAI:</b> Thank you, {self.name}.<br><br>
            How are you feeling today? I'm here to listen.
            """
            self.append_to_chat(response)
            return
        
        # Record mood
        self.record_mood(message)
        
        # Generate response
        if "sad" in message.lower() or "depressed" in message.lower():
            response = random.choice(self.responses["sad"])
        elif "happy" in message.lower() or "good" in message.lower():
            response = random.choice(self.responses["happy"])
        else:
            response = random.choice(self.responses["default"])
        
        # Simulate typing delay
        self.status_bar.showMessage("SerenityAI is typing...")
        QApplication.processEvents()
        time.sleep(1.5)
        
        self.append_to_chat(f"<b>🤖 SerenityAI:</b> {response}")
        self.status_bar.showMessage("Ready")

    def record_mood(self, message):
        # Simple mood scoring for demo
        score = 5  # Neutral
        if "sad" in message.lower() or "depressed" in message.lower():
            score = random.randint(1, 3)
        elif "happy" in message.lower() or "good" in message.lower():
            score = random.randint(7, 10)
        
        self.mood_history.append({
            "timestamp": datetime.now(),
            "message": message,
            "score": score
        })

    def start_quiz(self):
        quiz = QuizDialog(self)
        if quiz.exec_():
            total_score = quiz.get_score()
            if total_score <= 4:
                result = "minimal depression"
                advice = "Your mood seems generally positive."
            elif total_score <= 9:
                result = "mild depression"
                advice = "You might be experiencing some low mood."
            elif total_score <= 14:
                result = "moderate depression"
                advice = "Consider speaking with a professional."
            elif total_score <= 19:
                result = "moderately severe depression"
                advice = "Professional support could be helpful."
            else:
                result = "severe depression"
                advice = "Please consider reaching out to a professional."
            
            response = f"""
            <b>🤖 SerenityAI:</b> Assessment results suggest {result} (score: {total_score}/27).<br><br>
            {advice}<br><br>
            Remember, this is not a diagnosis.
            """
            self.append_to_chat(response)

    def show_mood_chart(self):
        if not self.mood_history:
            self.append_to_chat("<b>🤖 SerenityAI:</b> No mood data yet. Chat more to track your mood.")
            return
        
        dialog = MoodChartDialog(self.mood_history, self)
        dialog.exec_()

    def toggle_voice_input(self):
        if self.is_listening:
            self.stop_voice_input()
        else:
            self.start_voice_input()

    def start_voice_input(self):
        self.is_listening = True
        self.voice_button.setStyleSheet("background-color: #E74C3C;")
        self.status_bar.showMessage("Listening... Speak now")
        QApplication.processEvents()
        
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                
                self.status_bar.showMessage("Processing...")
                QApplication.processEvents()
                
                text = self.recognizer.recognize_google(audio)
                self.input_field.setText(text)
                self.status_bar.showMessage("Ready - press Send")
                
        except sr.WaitTimeoutError:
            self.status_bar.showMessage("No speech detected")
        except sr.UnknownValueError:
            self.status_bar.showMessage("Could not understand audio")
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
        finally:
            self.stop_voice_input()

    def stop_voice_input(self):
        self.is_listening = False
        self.voice_button.setStyleSheet("background-color: #4A7685;")
        self.voice_button.setIcon(QIcon.fromTheme("audio-input-microphone"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont()
    font.setFamily("Helvetica Neue" if sys.platform == "darwin" else "Arial")
    font.setPointSize(12)
    app.setFont(font)
    
    window = SerenityChatbot()
    window.show()
    sys.exit(app.exec_())
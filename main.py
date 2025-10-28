import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


# ----------------- Pages -----------------
class StartPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        lbl = QLabel("به بازی آموزش حروف الفبا خوش آمدید!")
        lbl.setStyleSheet("font-size:70px; font-weight:600;")
        lbl.setAlignment(Qt.AlignCenter)

        start_btn = QPushButton("شروع")
        start_btn.clicked.connect(lambda: self.controller.start_game())
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setStyleSheet("""
            font-size:70px;
            padding:30px 80px;
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: black;
        """)

        about_btn = QPushButton("درباره بازی")
        about_btn.clicked.connect(lambda: self.controller.show_page('About'))
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setStyleSheet("""
            font-size:50px;
            padding:15px 40px;
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: black;
        """)

        layout.addStretch()
        layout.addWidget(lbl, alignment=Qt.AlignCenter)
        layout.addSpacing(200)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(about_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)


class AboutPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        back_btn = QPushButton("برگشت")
        back_btn.clicked.connect(lambda: self.controller.show_page('Start'))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            font-size:40px;
            padding:10px 30px;
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: black;
        """)

        about_lbl = QLabel("این بازی برای آموزش حروف الفبای فارسی طراحی شده است.")
        about_lbl.setStyleSheet("font-size:50px; font-weight:600;")
        about_lbl.setAlignment(Qt.AlignCenter)

        layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        layout.addStretch()
        layout.addWidget(about_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)


class LetterPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.player = QMediaPlayer()
        self.init_ui()

    def init_ui(self):
        # Clear layout if re-initialized
        for i in reversed(range(self.layout().count() if self.layout() else 0)):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        layout = QVBoxLayout()

        exit_btn = QPushButton("خروج")
        exit_btn.clicked.connect(lambda: self.controller.end_game())
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.setStyleSheet("""
            font-size:40px;
            padding:10px 30px;
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: black;
        """)
        layout.addWidget(exit_btn, alignment=Qt.AlignLeft)
        layout.addStretch()

        # ----- Generate letters -----
        if not self.controller.game:
            round_number = 1
        else:
            round_number = max(self.controller.game.keys()) + 1

        choice_letters = random.sample(self.controller.persian_letters, 6)
        correct_letter = random.choice(choice_letters)

        self.controller.game[round_number] = [choice_letters, correct_letter]

        # Play sound for correct letter (future-ready)
        try:
            sound_path = f"sounds/{correct_letter}.mp3"
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_path)))
            self.player.play()
        except Exception as e:
            print(f"Sound not found for {correct_letter}: {e}")

        # ----- Create buttons -----
        buttons = []
        for letter in choice_letters:
            btn = QPushButton(letter)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                font-size:70px;
                padding:30px 80px;
                border-style: outset;
                border-width: 2px;
                border-radius: 15px;
                border-color: black;
            """)
            btn.clicked.connect(lambda _, l=letter: self.controller.check_answer(l))
            buttons.append(btn)

        # Layout for letters
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        for i in range(3):
            h1.addWidget(buttons[i])
        for i in range(3, 6):
            h2.addWidget(buttons[i])

        layout.addLayout(h1)
        layout.addSpacing(50)
        layout.addLayout(h2)
        layout.addStretch()

        self.setLayout(layout)


class ResultPage(QWidget):
    def __init__(self, controller, correct, selected, is_correct):
        super().__init__()
        self.controller = controller
        self.correct = correct
        self.selected = selected
        self.is_correct = is_correct
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        if self.is_correct:
            result_lbl = QLabel("آفرین! جواب درست بود 🎉")
        else:
            result_lbl = QLabel(f"اشتباه! جواب درست: {self.correct}")
        result_lbl.setStyleSheet("font-size:50px; font-weight:600;")
        result_lbl.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(result_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)


class EndPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        lbl = QLabel("پایان بازی! 🌟")
        lbl.setStyleSheet("font-size:60px; font-weight:600;")
        lbl.setAlignment(Qt.AlignCenter)

        back_btn = QPushButton("بازگشت به منوی اصلی")
        back_btn.clicked.connect(lambda: self.controller.show_page('Start'))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            font-size:40px;
            padding:15px 40px;
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: black;
        """)

        layout.addStretch()
        layout.addWidget(lbl, alignment=Qt.AlignCenter)
        layout.addSpacing(100)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)


# ----------------- Main Window -----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alphabet Learning Game (بازی آموزش حروف الفبا)")
        self.setGeometry(100, 100, 1700, 1000)

        self.persian_letters = [
            'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز',
            'ژ', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ',
            'ل', 'م', 'ن', 'و', 'ه', 'ی'
        ]
        self.game = {}

        # Stack for pages
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create pages
        self.start_page = StartPage(self)
        self.about_page = AboutPage(self)
        self.letter_page = LetterPage(self)
        self.end_page = EndPage(self)

        # Add to stack
        for p in (self.start_page, self.about_page, self.letter_page, self.end_page):
            self.stack.addWidget(p)

        # Show start
        self.show_page('Start')

    # Navigation
    def show_page(self, name):
        if name == 'Start':
            self.stack.setCurrentWidget(self.start_page)
        elif name == 'About':
            self.stack.setCurrentWidget(self.about_page)
        elif name == 'Letter':
            self.stack.setCurrentWidget(self.letter_page)
        elif name == 'End':
            self.stack.setCurrentWidget(self.end_page)
        elif name == 'Result':
            self.stack.setCurrentWidget(self.result_page)

    # Game logic
    def start_game(self):
        self.letter_page = LetterPage(self)
        self.stack.addWidget(self.letter_page)
        self.show_page('Letter')

    def end_game(self):
        self.show_page('End')

    def check_answer(self, selected_letter):
        current_round = max(self.game.keys())
        correct_letter = self.game[current_round][1]
        is_correct = selected_letter == correct_letter

        # Save results
        self.game[current_round].extend([selected_letter, is_correct])
        print("✅ Correct!" if is_correct else f"❌ Wrong! Correct was {correct_letter}")

        # Show result page
        self.result_page = ResultPage(self, correct_letter, selected_letter, is_correct)
        self.stack.addWidget(self.result_page)
        self.show_page('Result')

        # Load next after delay
        QTimer.singleShot(2000, self.load_next_letter)

    def load_next_letter(self):
        self.stack.removeWidget(self.letter_page)
        self.letter_page.deleteLater()
        self.letter_page = LetterPage(self)
        self.stack.addWidget(self.letter_page)
        self.show_page('Letter')

# ----------------- Run App -----------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
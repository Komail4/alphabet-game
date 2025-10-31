import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os


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
        self.correct_letter = None  # Keep track of current letter sound
        self.init_ui()

    def init_ui(self):
        # Clear old layout if it exists
        for i in reversed(range(self.layout().count() if self.layout() else 0)):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        layout = QVBoxLayout()

        # ---- Exit button ----
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

        # ---- Generate letters ----
        if not self.controller.game:
            round_number = 1
        else:
            round_number = max(self.controller.game.keys()) + 1

        letters_pool = self.controller.persian_letters.copy()

        # Prevent confusing pairs from appearing together
        confusing_pairs = [
            ('ح', 'ه')
        ]

        # Remove a pair partner if one is chosen
        choice_letters = random.sample(letters_pool, 6)
        for a, b in confusing_pairs:
            if a in choice_letters and b in choice_letters:
                # Remove the second one and replace with a different letter
                replace = random.choice([x for x in letters_pool if x not in choice_letters])
                choice_letters.remove(b)
                choice_letters.append(replace)

        correct_letter = random.choice(choice_letters)
        self.correct_letter = correct_letter  # Save for Listen button

        self.controller.game[round_number] = [choice_letters, correct_letter]


        # ---- “Listen Again” button ----
        listen_btn = QPushButton("🔊 گوش دادن دوباره")
        listen_btn.setCursor(Qt.PointingHandCursor)
        listen_btn.setStyleSheet("""
            font-size:35px;
            padding:10px 40px;
            border-radius:15px;
            border:2px solid black;
        """)
        listen_btn.clicked.connect(lambda: self.play_sound(self.correct_letter))
        layout.addWidget(listen_btn, alignment=Qt.AlignCenter)
        layout.addSpacing(30)

        # ---- Letter buttons ----
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

        if not self.controller.first_play:
            QTimer.singleShot(1000, lambda: self.play_sound(correct_letter))

        self.controller.first_play = False

        self.setLayout(layout)

    def play_sound(self, letter):
        """Plays the sound of the given letter."""
        try:
            sound_path = os.path.abspath(f"sounds/{letter}.wav")
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(sound_path)))
            self.player.play()
        except Exception as e:
            print(f"❌ Could not play sound for {letter}: {e}")

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

        # ---- Title ----
        title_lbl = QLabel("پایان بازی 🎉")
        title_lbl.setStyleSheet("font-size:70px; font-weight:600;")
        title_lbl.setAlignment(Qt.AlignCenter)

        # ---- Calculate Score ----
        if len(self.controller.game) > 2:
            if self.controller.check_1:
                number = 2
                self.controller.check_1 = False
            else:
                number = 1
            total = len(self.controller.game) - number
            correct = sum(1 for data in self.controller.game.values() if len(data) >= 4 and data[3] is True)

            # Prevent division by zero
            if total > 0:
                percentage = (correct / total) * 100
                score_text = f"امتیاز شما: {total} / {correct}"
                if percentage == 100:
                    msg = "عالی بود! 👏"
                elif percentage >= 70:
                    msg = "خیلی خوب بود! ادامه بده 🌟"
                elif percentage >= 40:
                    msg = "خوب بود! تمرین بیشتر کن 💪"
                else:
                    msg = "مشکلی نیست، دوباره امتحان کن 🙂"
            else:
                score_text = "شما هنوز هیچ سوالی پاسخ نداده‌اید."
                msg = ""
        else:
            score_text = "شما هنوز هیچ سوالی پاسخ نداده‌اید."
            msg = ""
            
        


        score_lbl = QLabel(score_text)
        score_lbl.setStyleSheet("font-size:60px; color:blue; font-weight:600;")
        score_lbl.setAlignment(Qt.AlignCenter)

        # ---- Encouragement Message ----
        

        msg_lbl = QLabel(msg)
        msg_lbl.setStyleSheet("font-size:50px; color:green; font-weight:500;")
        msg_lbl.setAlignment(Qt.AlignCenter)

        # ---- Back Button ----
        back_btn = QPushButton("بازگشت به صفحه اصلی")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            font-size:40px;
            padding:15px 50px;
            border:2px solid black;
            border-radius:15px;
        """)
        back_btn.clicked.connect(lambda: self.controller.back_start_page())

        # ---- Layout ----
        layout.addStretch()
        layout.addWidget(title_lbl, alignment=Qt.AlignCenter)
        layout.addSpacing(50)
        layout.addWidget(score_lbl, alignment=Qt.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(msg_lbl, alignment=Qt.AlignCenter)
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

        self.first_play = True

        self.check_1 = True

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
        # Ensure the current question is saved properly
        if self.game:
            current_round = max(self.game.keys())
            # If user exited before answering, mark it as incorrect
            if len(self.game[current_round]) < 4:
                self.game[current_round].extend([None, False])

        # Now show the End page with correct data
        self.end_page = EndPage(self)
        self.stack.addWidget(self.end_page)
        self.show_page('End')
        self.check_1 = False


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
    
    def back_start_page(self):
        self.show_page('Start')
        self.game = {}
        

# ----------------- Run App -----------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
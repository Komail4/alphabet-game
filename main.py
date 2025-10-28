import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import random

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

        start_btn = QPushButton("برگشت")
        start_btn.clicked.connect(lambda: self.controller.show_page('Start'))
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setStyleSheet("""
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

        layout.addWidget(start_btn, alignment=Qt.AlignLeft)
        layout.addStretch()
        
        layout.addWidget(about_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

class LetterPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
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

        max_number = self.controller.game.keys()
        if max_number == None or len(max_number) == 0:
            max_number = 1
        else:
            max_number = max(max_number) + 1
        
        choice_letters = []

        for i in range(6):
            while True:
                letter = random.choice(self.controller.persian_letters)
                if letter not in choice_letters:
                    choice_letters.append(letter)
                    break

        self.correct_letter = random.choice(choice_letters)

        self.controller.game[max_number] = [choice_letters, self.correct_letter]

        btn_1 = QPushButton(f"{choice_letters[0]}")
        btn_2 = QPushButton(f"{choice_letters[1]}")
        btn_3 = QPushButton(f"{choice_letters[2]}")
        btn_4 = QPushButton(f"{choice_letters[3]}")
        btn_5 = QPushButton(f"{choice_letters[4]}")
        btn_6 = QPushButton(f"{choice_letters[5]}")

        for j in (btn_1, btn_2, btn_3, btn_4, btn_5, btn_6):
            j.setCursor(Qt.PointingHandCursor)
            j.setStyleSheet("""
                                    font-size:70px;
                                    padding:30px 80px;
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 15px;
                                    border-color: black;
                                    
                                    """)
        btn_1.clicked.connect(lambda: self.controller.check_answer(choice_letters[0]))
        btn_2.clicked.connect(lambda: self.controller.check_answer(choice_letters[1]))
        btn_3.clicked.connect(lambda: self.controller.check_answer(choice_letters[2]))
        btn_4.clicked.connect(lambda: self.controller.check_answer(choice_letters[3]))
        btn_5.clicked.connect(lambda: self.controller.check_answer(choice_letters[4]))
        btn_6.clicked.connect(lambda: self.controller.check_answer(choice_letters[5]))
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(btn_1)
        h_layout.addWidget(btn_2)
        h_layout.addWidget(btn_3)
        h2_layout = QHBoxLayout()
        h2_layout.addWidget(btn_4)
        h2_layout.addWidget(btn_5)
        h2_layout.addWidget(btn_6)
        layout.addLayout(h_layout)
        layout.addSpacing(50)
        layout.addLayout(h2_layout)
        layout.addStretch()

        self.setLayout(layout)

class EndPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)

class ResultPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        result = self.controller.game[max(self.controller.game.keys())][3]
        if result:
            result_lbl = QLabel("آفرین! جواب درست بود.")
        else:
            correct_letter = self.controller.game[max(self.controller.game.keys())][1]
            result_lbl = QLabel(f"متاسفانه جواب اشتباه بود. جواب درست: {correct_letter}")
        result_lbl.setStyleSheet("font-size:50px; font-weight:600;")
        result_lbl.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(result_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

# ----------------- Main Window -----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alphabet Learning Game (بازی آموزش حروف الفبا)")
        self.setGeometry(100, 100, 1700, 1000)

        # Alphabet letters
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
        self.letter_page = LetterPage(self)
        self.end_page = EndPage(self)
        self.about_page = AboutPage(self)
        # self.result_page = ResultPage(self)

        # Add to stack
        for p in (self.start_page, self.letter_page, self.end_page, self.about_page):
            self.stack.addWidget(p)

        # Show start
        self.show_page('Start')

    # Navigation API used by pages
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

    def start_game(self):
        self.show_page('Letter')

    def end_game(self):
        self.show_page('End')

    def check_answer(self, selected_letter):
        current_number = max(self.game.keys())
        correct_letter = self.game[current_number][1]
        if selected_letter == correct_letter:
            print(f"Correct! The letter was: selected {selected_letter} correct {correct_letter}")
        else:
            print(f"Wrong! The correct letter was: {correct_letter} selected {selected_letter}")
        self.game[current_number].append(selected_letter)  
        self.game[current_number].append(True if selected_letter == correct_letter else False)
        self.result_page = ResultPage(self)
        self.stack.addWidget(self.result_page)
        self.show_page('Result')
        QTimer.singleShot(2000, self.load_next_letter)
    def load_next_letter(self):
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
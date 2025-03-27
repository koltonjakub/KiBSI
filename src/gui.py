import sys

from PyQt6.QtWidgets import QApplication, QBoxLayout, QMainWindow, QPushButton, QLineEdit, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPalette, QColor


import PyQt6.QtWidgets as Widgets
from PyQt6.QtCore import Qt

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Multi Output App")
        self.setGeometry(100, 100, 800, 600)
        
        # Set dark background
        self.setStyleSheet("background-color: #2E2E2E;")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        
        self.input_texts = ["Alice", "Bazy(Alice): ", "Bob: ", "Bazy(Bob): ", "Eve: "]
        
        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedHeight(40)
        self.start_button.setStyleSheet("color: white; background-color: #555;")
        self.start_button.clicked.connect(self.process_input)
 
        
        # right_layout.addStretch()
        left_layout = self.get_input_output_layout()
        right_layout = QHBoxLayout()
        right_layout.addWidget(self.start_button)

        # Add layouts and spacer in between
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        main_layout.setStretchFactor(left_layout, 7)
        main_layout.setStretchFactor(right_layout, 3)
        
        central_widget.setLayout(main_layout)

    def get_input_output_layout(self):
        text_layout = QVBoxLayout()
        in_out_layout = QVBoxLayout()
        left_layout = QHBoxLayout()
        height = 100
        font_size = 40

        for txt in self.input_texts:
            text_widget = Widgets.QLabel(txt)
            text_widget.setStyleSheet("color: white;"
                                      "background-color:"
                                      "#3E3E3E;"
                                      f"font-size: {font_size}px;")
            text_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            text_widget.setFixedHeight(height)
            text_layout.addWidget(text_widget)
            text_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet(f"color: white; background-color: #3E3E3E; font-size: {font_size}px;")
        self.input_field.setFixedHeight(height)
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignTop)
        in_out_layout.addWidget(self.input_field)
        in_out_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.text_edit_fields = []
        for i in range(4):
            text_edit = QTextEdit(self)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet(f"color: white; background-color: #3E3E3E; font-size: {font_size}px;")
            text_edit.setFixedHeight(height)
            # text_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.text_edit_fields.append(text_edit)
            in_out_layout.addWidget(text_edit)
            in_out_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        left_layout.addLayout(text_layout)
        left_layout.addLayout(in_out_layout)
        left_layout.setStretchFactor(text_layout, 1)
        left_layout.setStretchFactor(in_out_layout, 4)

        return left_layout
        
    def process_input(self):
        text = self.input_field.text()
        for output_window in self.text_edit_fields:
            output_window.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())

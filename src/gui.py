import sys
import random

from PyQt5.QtWidgets import QApplication, QBoxLayout, QMainWindow, QPushButton, QLineEdit, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QColor


import PyQt5.QtWidgets as Widgets
from PyQt5.QtCore import Qt

import src.bb84 as bb84
import numpy as np

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BB84 Quantum Key Distribution Example")
        self.setGeometry(100, 100, 1200, 600)
        
        # Set dark background
        self.setStyleSheet("background-color: #2E2E2E;")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        self.input_texts = ["Alice", "Bazy(Alice): ", "Bazy(Bob): ", "Bob: ", "Eve: "]
        
        # Start button
        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedHeight(40)
        self.start_button.setStyleSheet("color: white; background-color: #992299;")
        self.start_button.clicked.connect(self.process_input)

        # Right side labels
        right_side_labels_layout = QVBoxLayout()
        right_side_labels_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_side_labels_layout.setContentsMargins(0, 0, 0, 0)
        right_side_labels_layout.setSpacing(0)
 
        for txt in ['RND Key length', 'Eavesdropping %']:
            text_widget = Widgets.QLabel(txt)
            text_widget.setStyleSheet("color: white;"
                                      "background-color:"
                                      "#3E3E3E;"
                                      f"font-size: {40}px;")
            text_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            text_widget.setFixedHeight(100)
            right_side_labels_layout.addWidget(text_widget)
            right_side_labels_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Right side input fields
        right_side_input_fields_layout = QVBoxLayout()
        right_side_input_fields_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_side_input_fields_layout.setContentsMargins(0, 0, 0, 0)
        right_side_input_fields_layout.setSpacing(0)

        self.input_rnd_key_length = QLineEdit()
        self.input_rnd_key_length.setStyleSheet(f"color: white; background-color: #3E3E3E; font-size: {40}px;")
        self.input_rnd_key_length.setFixedHeight(100)
        self.input_rnd_key_length.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_side_input_fields_layout.addWidget(self.input_rnd_key_length)
        right_side_input_fields_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.input_eavesdropping_prc = QLineEdit()
        self.input_eavesdropping_prc.setStyleSheet(f"color: white; background-color: #3E3E3E; font-size: {40}px;")
        self.input_eavesdropping_prc.setFixedHeight(100)
        self.input_eavesdropping_prc.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_side_input_fields_layout.addWidget(self.input_eavesdropping_prc)
        right_side_input_fields_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


        # Connect layouts
        right_side_layout = QHBoxLayout()
        right_side_layout.addLayout(right_side_labels_layout)
        right_side_layout.addLayout(right_side_input_fields_layout)

        left_layout = self.get_output_layout()
        right_layout = QVBoxLayout()
        right_layout.addLayout(right_side_layout)
        right_layout.addWidget(self.start_button)
        right_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add layouts and spacer in between
        main_layout.addLayout(right_layout)
        main_layout.addLayout(left_layout)
        main_layout.setStretchFactor(left_layout, 7)
        main_layout.setStretchFactor(right_layout, 3)
        
        central_widget.setLayout(main_layout)

    def get_output_layout(self):
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

        # self.input_field = QLineEdit()
        # self.input_field.setStyleSheet(f"color: white; background-color: #3E3E3E; font-size: {font_size}px;")
        # self.input_field.setFixedHeight(height)
        # self.input_field.setAlignment(Qt.AlignmentFlag.AlignTop)
        # in_out_layout.addWidget(self.input_field)
        # in_out_layout.addSpacerItem(QSpacerItem(40, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.text_edit_fields = []
        for i in range(5):
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
        def is_convertible_to_int(text):
            try:
                int(text)
                return True
            except ValueError:
                return False

        def is_convertible_to_float(text):
            try:
                float(text)
                return True
            except ValueError:
                return False
        
        # Read input from the QLineEdit fields
        rnd_key_length = self.input_rnd_key_length.text()
        eavesdropping_prc = self.input_eavesdropping_prc.text()

        if(not is_convertible_to_int(rnd_key_length)):
            print("Invalid input. Please enter valid integers for RND Key Length(int)")
            return
        
        if(not is_convertible_to_float(eavesdropping_prc) and eavesdropping_prc != ''):
            print("Invalid input. Please enter valid float for Eavesdropping %(float)")
            return

        random_bit_string = ''.join(random.choice('01') for _ in range(int(rnd_key_length)))
        # Print the inputs to the console (for debugging purposes)
        print(f"RND Key Length: {rnd_key_length}")
        print(f"Eavesdropping %: {eavesdropping_prc}")

        # You can now use these inputs for further processing
 
        b, b_prime, _, bob_bits, alice_bits = bb84.bb84(random_bit_string, float(eavesdropping_prc) if eavesdropping_prc != '' else 0.0)

        b = "".join(b.astype('str'))
        b_prime = "".join(b_prime.astype('str'))
        bob_bits = bob_bits[::-1]

        formatted_alice_bits = ""
        formatted_b = ""
        formatted_b_prime = ""
        formatted_bob_bits = ""

        # Apply formatting based on matching characters
        for bit1, bit2, alice_bit, bob_bit in zip(b, b_prime, alice_bits, bob_bits):
            if bit1 == bit2:
                formatted_b += f'<span style="color:green;">{bit1}</span>'
                formatted_b_prime += f'<span style="color:green;">{bit2}</span>'
                formatted_alice_bits += f'<span style="color:blue;">{alice_bit}</span>'
                formatted_bob_bits += f'<span style="color:blue;">{bob_bit}</span>'
            else:
                formatted_b += f'<span style="color:red;">{bit1}</span>'
                formatted_b_prime += f'<span style="color:red;">{bit2}</span>'
                formatted_alice_bits += f'<span style="color:gray;">{alice_bit}</span>'
                formatted_bob_bits += f'<span style="color:gray;">{bob_bit}</span>'

        # Prepare outputs
        output_texts = [
            formatted_alice_bits,
            formatted_b,
            formatted_b_prime,
            formatted_bob_bits,
            "Eavesdropping"
        ]

        # Set formatted text in the text edit fields
        for out_txt, output_window in zip(output_texts, self.text_edit_fields):
            output_window.setHtml(out_txt)  # Use setHtml for rich text formatting


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())

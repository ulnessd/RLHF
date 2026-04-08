import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QMessageBox)
from PyQt6.QtGui import QAction


class TextEncryptor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Encryptor")
        self.resize(600, 400)

        # Setup UI and Menu
        self.init_ui()
        self.init_menu()

    def init_ui(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Main Console (Text Area)
        self.console = QTextEdit()
        self.console.setPlaceholderText("Type or paste your text here...")
        main_layout.addWidget(self.console)

        # Bottom Controls Layout
        controls_layout = QHBoxLayout()

        # Passkey Input
        self.passkey_input = QLineEdit()
        self.passkey_input.setPlaceholderText("Enter passkey...")
        self.passkey_input.setEchoMode(QLineEdit.EchoMode.Password)  # Masks the passkey
        controls_layout.addWidget(self.passkey_input)

        # Encrypt Button
        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        controls_layout.addWidget(self.encrypt_btn)

        # Decrypt Button
        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        controls_layout.addWidget(self.decrypt_btn)

        main_layout.addLayout(controls_layout)

    def init_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Open Action
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Save Action
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

    def calculate_p(self, passkey):
        """Calculates P = ASCII sum % 256"""
        if not passkey:
            return 0
        return sum(ord(char) for char in passkey) % 256

    def encrypt_text(self):
        text = self.console.toPlainText()
        passkey = self.passkey_input.text()

        if not text:
            return

        p = self.calculate_p(passkey)
        encrypted_hex_list = []

        # Encrypt and convert to Hex
        for char in text:
            # Char = (Char + P) % 256
            encrypted_val = (ord(char) + p) % 256
            # Format as 2-character uppercase Hex
            encrypted_hex_list.append(f"{encrypted_val:02X}")

        # Replace text, clear passkey
        self.console.setPlainText(" ".join(encrypted_hex_list))
        self.passkey_input.clear()

    def decrypt_text(self):
        hex_text = self.console.toPlainText().strip()
        passkey = self.passkey_input.text()

        if not hex_text:
            return

        p = self.calculate_p(passkey)
        decrypted_text = ""

        try:
            # Split the hex string by spaces
            hex_parts = hex_text.split()
            for hex_val in hex_parts:
                # Convert Hex back to integer
                val = int(hex_val, 16)
                # Reverse encryption: (Val - P) % 256
                decrypted_val = (val - p) % 256
                decrypted_text += chr(decrypted_val)

            # Replace text, clear passkey
            self.console.setPlainText(decrypted_text)
            self.passkey_input.clear()

        except ValueError:
            QMessageBox.warning(self, "Decryption Error",
                                "The text in the console is not valid encrypted hexadecimal data.")

    def open_file(self):
        # Open file dialog defaulting to .dju files
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "DJU Files (*.dju);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.console.setPlainText(file.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not read file:\n{e}")

    def save_file(self):
        # Save file dialog defaulting to .dju files
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "DJU Files (*.dju);;All Files (*)"
        )
        if file_name:
            # Ensure the extension is .dju if the user didn't type it
            if not file_name.endswith('.dju'):
                file_name += '.dju'
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.console.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEncryptor()
    window.show()
    sys.exit(app.exec())

from PyQt5.QtWidgets import QApplication
import src.gui as gui
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = gui.MainApp()
    main_window.show()
    sys.exit(app.exec())
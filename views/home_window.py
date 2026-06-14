from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Tools Hub - Main Menu")
        self.setFixedSize(650, 400) 

        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        lbl_title = QLabel("NETWORK TOOLS ANALYZER")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("color: #1a1a1a;")
        main_layout.addWidget(lbl_title)

        lbl_sub = QLabel("Silakan pilih modul perangkat kerja yang ingin digunakan:")
        lbl_sub.setFont(QFont("Segoe UI", 10))
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_sub.setStyleSheet("color: #555555;")
        main_layout.addWidget(lbl_sub)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)

        self.btn_rssi = QPushButton("📊 RSSI & SNR\nCalculation")
        self.btn_rssi.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.btn_rssi.setStyleSheet("""
            QPushButton {
                background-color: #0078d7; color: white; border-radius: 10px;
                padding: 20px; min-height: 120px;
            }
            QPushButton:hover { background-color: #005a9e; }
        """)

        self.btn_radio = QPushButton("📻 Radio Editor\nModule")
        self.btn_radio.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.btn_radio.setStyleSheet("""
            QPushButton {
                background-color: #c00000; color: white; border-radius: 10px;
                padding: 20px; min-height: 120px;
            }
            QPushButton:hover { background-color: #a00000; }
        """)

        btn_layout.addWidget(self.btn_rssi)
        btn_layout.addWidget(self.btn_radio)
        main_layout.addLayout(btn_layout)

        lbl_footer = QLabel("Version 2.0 • Powered by PyQt6 & SQLite")
        lbl_footer.setFont(QFont("Segoe UI", 8))
        lbl_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_footer.setStyleSheet("color: #888888; margin-top: 15px;")
        main_layout.addWidget(lbl_footer)

        self.btn_rssi.clicked.connect(self.open_rssi_module)
        self.btn_radio.clicked.connect(self.open_radio_module)

    def open_rssi_module(self):
        from views.main_window import DriveTestAppPyQt
        self.rssi_window = DriveTestAppPyQt()
        self.rssi_window.show()
        self.hide()

    def open_radio_module(self):
        from views.radio_window import RadioEditorWindow
        self.radio_window = RadioEditorWindow()
        self.radio_window.show()
        self.hide()
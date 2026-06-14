import sys
from PyQt6.QtWidgets import QApplication
from database.db_manager import init_db
from views.home_window import HomeWindow

if __name__ == "__main__":
    # Inisialisasi database lokal SQLite di folder aktif sebelum memuat UI
    init_db()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Membuka aplikasi langsung ke halaman Menu Utama (Home)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())
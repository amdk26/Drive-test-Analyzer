import os
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox

class PreviewDialog(QDialog):
    def __init__(self, fig, default_filename, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview Dashboard Laporan")
        self.resize(1100, 600)
        
        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)
        
        self.btn_save = QPushButton(f"💾 Simpan Gambar ({default_filename})")
        self.btn_save.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 11pt; padding: 10px;")
        self.btn_save.clicked.connect(self.save_image)
        layout.addWidget(self.btn_save)
        
        self.fig = fig
        self.default_filename = default_filename

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Simpan Gambar", 
            os.path.join(os.getcwd(), self.default_filename), 
            "PNG Images (*.png)"
        )
        if filepath:
            try:
                self.fig.savefig(filepath, dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Sukses", f"Gambar berhasil disimpan di:\n{filepath}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal menyimpan gambar:\n{str(e)}")
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt
from database.db_manager import get_all_history, delete_history_item

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📜 Riwayat Perhitungan Data")
        self.resize(950, 450)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        
        self.selected_raw_data = None
        self.selected_mode = None
        self.history_records = []
        
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        headers = ["ID", "Waktu Perhitungan", "Kategori Mode", "Total Baris", "Excellent", "Good", "Fair", "Poor"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("📂 Load Data Riwayat")
        self.btn_load.setStyleSheet("background-color: #0078d7; color: white; font-weight: bold; padding: 8px 15px;")
        
        self.btn_delete = QPushButton("🗑 Hapus Log")
        self.btn_delete.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold; padding: 8px 15px;")
        
        self.btn_close = QPushButton("❌ Tutup")
        self.btn_close.setStyleSheet("padding: 8px 15px;")
        
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)
        
        self.btn_load.clicked.connect(self.load_selected)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_close.clicked.connect(self.reject)
        
        self.refresh_data()

    def refresh_data(self):
        self.table.setRowCount(0)
        self.history_records = get_all_history()
        
        for row_idx, record in enumerate(self.history_records):
            self.table.insertRow(row_idx)
            for col_idx in range(8):
                item = QTableWidgetItem(str(record[col_idx]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

    def load_selected(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih salah satu baris riwayat!")
            return
        
        row = selected_ranges[0].topRow()
        record = self.history_records[row]
        self.selected_mode = record[2]
        self.selected_raw_data = record[8] 
        self.accept()

    def delete_selected(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih baris riwayat yang ingin dihapus!")
            return
        
        row = selected_ranges[0].topRow()
        record = self.history_records[row]
        item_id = record[0]
        
        reply = QMessageBox.question(self, "Konfirmasi", f"Hapus log riwayat ID {item_id}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_history_item(item_id)
            self.refresh_data()
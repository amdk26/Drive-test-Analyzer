from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QMessageBox, QHeaderView, QAbstractItemView, QCheckBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont
from database.db_manager import get_all_history, delete_history_item

class HistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📜 Riwayat Perhitungan Data")
        self.resize(1000, 500)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        
        self.selected_raw_data = None
        self.selected_mode = None
        self.history_records = []
        
        # --- TEMA & CSS ---
        self.setStyleSheet("""
            QDialog { background-color: #f8f9fa; }
            QTableWidget { 
                font-family: 'Segoe UI'; font-size: 10pt; 
                background-color: #ffffff; gridline-color: #e0e0e0; 
                border: 1px solid #cccccc; border-radius: 4px;
            }
            QHeaderView::section { 
                font-family: 'Segoe UI'; font-size: 10pt; font-weight: bold; 
                background-color: #e9ecef; padding: 6px; border: 1px solid #d0d0d0; 
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_title = QLabel("Riwayat Data Tersimpan")
        lbl_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(lbl_title)
        
        # --- TABEL HISTORY ---
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Tambahan Kolom "Pilih" di awal
        headers = ["Pilih", "ID", "Waktu Perhitungan", "Kategori Mode", "Total Baris", "Excellent", "Good", "Fair", "Poor"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Mengatur kelebaran kolom agar lebih rapi dan tidak terpotong
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Kolom Waktu dibuat paling lebar
        layout.addWidget(self.table)
        
        # --- TOMBOL & KONTROL BAWAH ---
        btn_layout = QHBoxLayout()
        
        # Checkbox Pilih Semua
        self.chk_select_all = QCheckBox("☑ Pilih Semua")
        self.chk_select_all.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.chk_select_all.setStyleSheet("color: #333333;")
        self.chk_select_all.stateChanged.connect(self.toggle_select_all)
        
        self.btn_load = QPushButton("📂 Load Data Terpilih")
        self.btn_load.setStyleSheet("""
            QPushButton { background-color: #0078d7; color: white; font-weight: bold; padding: 8px 15px; border-radius: 4px; }
            QPushButton:hover { background-color: #005a9e; }
        """)
        
        self.btn_delete = QPushButton("🗑 Hapus Terpilih")
        self.btn_delete.setStyleSheet("""
            QPushButton { background-color: #dc3545; color: white; font-weight: bold; padding: 8px 15px; border-radius: 4px; }
            QPushButton:hover { background-color: #c82333; }
        """)
        
        self.btn_close = QPushButton("❌ Tutup")
        self.btn_close.setStyleSheet("""
            QPushButton { padding: 8px 15px; font-weight: bold; border-radius: 4px; background-color: #e2e6ea; border: 1px solid #dae0e5; }
            QPushButton:hover { background-color: #dae0e5; }
        """)
        
        btn_layout.addWidget(self.chk_select_all)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)
        
        # --- SAMBUNGAN EVENT ---
        self.btn_load.clicked.connect(self.load_selected)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_close.clicked.connect(self.reject)
        
        self.refresh_data()

    def refresh_data(self):
        self.table.setRowCount(0)
        self.history_records = get_all_history()
        
        # Matikan sementara event toggle saat mereset checkbox utama
        self.chk_select_all.blockSignals(True)
        self.chk_select_all.setChecked(False)
        self.chk_select_all.blockSignals(False)
        
        # Kunci ukuran kolom checkbox dan ID agar pas
        self.table.setColumnWidth(0, 50)  # Pilih
        self.table.setColumnWidth(1, 50)  # ID
        self.table.setColumnWidth(3, 150) # Kategori Mode

        bg_odd = QColor("#f9f9f9")
        bg_even = QColor("#ffffff")
        
        for row_idx, record in enumerate(self.history_records):
            self.table.insertRow(row_idx)
            row_color = bg_even if row_idx % 2 == 0 else bg_odd
            
            # --- Membuat Checkbox di Kolom Pertama (0) ---
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            chk_item.setCheckState(Qt.CheckState.Unchecked)
            chk_item.setBackground(QBrush(row_color))
            self.table.setItem(row_idx, 0, chk_item)
            
            # --- Memasukkan Sisa Data dari Database ---
            for col_idx in range(8):
                item = QTableWidgetItem(str(record[col_idx]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QBrush(row_color))
                self.table.setItem(row_idx, col_idx + 1, item)

    def toggle_select_all(self, state):
        """Mencentang atau membatalkan centang semua baris secara otomatis"""
        is_checked = (state == Qt.CheckState.Checked.value)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked)

    def get_checked_rows(self):
        """Mendapatkan daftar indeks baris yang sedang dicentang"""
        checked_rows = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                checked_rows.append(row)
        return checked_rows

    def load_selected(self):
        checked_rows = self.get_checked_rows()
        
        if len(checked_rows) == 0:
            QMessageBox.warning(self, "Peringatan", "Silakan centang satu data riwayat yang ingin di-load!")
            return
        if len(checked_rows) > 1:
            QMessageBox.warning(self, "Peringatan", "Hanya bisa meload 1 data dalam satu waktu.\nSilakan centang satu saja!")
            return
            
        row = checked_rows[0]
        record = self.history_records[row]
        self.selected_mode = record[2]
        self.selected_raw_data = record[8] 
        self.accept() # Menutup dialog dan mengirim sinyal sukses ke main_window

    def delete_selected(self):
        checked_rows = self.get_checked_rows()
        
        if len(checked_rows) == 0:
            QMessageBox.warning(self, "Peringatan", "Silakan centang minimal satu data yang ingin dihapus!")
            return
            
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus {len(checked_rows)} data riwayat yang dipilih?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
                                     
        if reply == QMessageBox.StandardButton.Yes:
            # Hapus dari DB berdasarkan ID
            for row in checked_rows:
                record = self.history_records[row]
                item_id = record[0] # Mengambil ID dari record
                delete_history_item(item_id)
            
            self.refresh_data()
            QMessageBox.information(self, "Sukses", f"{len(checked_rows)} data riwayat berhasil dihapus secara permanen.")
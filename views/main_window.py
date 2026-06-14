import os
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QMessageBox, QLabel, QDialog, QLineEdit, QAbstractItemView, 
    QComboBox, QApplication, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QFont

from components.preview_dialog import PreviewDialog
from components.history_dialog import HistoryDialog

class DriveTestAppPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drive Test Data Processor (High Performance) - PyQt6")
        self.setGeometry(50, 50, 1350, 650)

        self.bg_color_btn_frame = "#f5f5f5"
        self.bg_color_odd = QColor("#f9f9f9")
        self.bg_color_even = QColor("#ffffff")
        self.bg_color_avg = QColor("#fff3cd")

        self.columns = [
            "No.", "Test Point", "Test Count", "Recommended Value", 
            "Avg Field Strength", "Max Field Strength", "Min Field Strength", 
            "Channel", "Test Result", "SNR", "SNR Result"
        ]
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        btn_frame = QWidget()
        btn_frame.setStyleSheet(f"background-color: {self.bg_color_btn_frame};")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.setSpacing(10)

        self.btn_back = QPushButton("🔙 Kembali")
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #ffffff; color: #333333; font-weight: bold; 
                font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;
                border: 1px solid #cccccc; border-radius: 4px;
            }
            QPushButton:hover { background-color: #e6e6e6; }
        """)

        self.btn_paste = QPushButton("📋 Paste Data")
        self.btn_paste.setStyleSheet("background-color: #0078d7; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")
        
        self.btn_custom_col = QPushButton("➕ Add Custom Column")
        self.btn_custom_col.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")
        
        self.btn_avg = QPushButton("📊 Hitung Rata-Rata")
        self.btn_avg.setStyleSheet("background-color: #ffc107; color: black; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")
        
        self.btn_clear = QPushButton("🗑 Clear Data")
        self.btn_clear.setStyleSheet("color: red; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")
        
        self.btn_history = QPushButton("📜 Lihat History")
        self.btn_history.setStyleSheet("background-color: #17a2b8; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")

        self.lbl_select = QLabel("Pilih Data Laporan:")
        self.lbl_select.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; font-weight: bold; background: transparent;")
        
        self.combo_type = QComboBox()
        self.combo_type.addItems(["RSSI (Test Result)", "SNR (SNR Result)"])
        self.combo_type.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; padding: 4px; background-color: white; border: 1px solid #cccccc;")
        
        self.btn_export_png = QPushButton("🖼️ Preview Laporan (PNG)")
        self.btn_export_png.setStyleSheet("background-color: #6f42c1; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")
        
        self.btn_copy = QPushButton("📑 Copy All Result")
        self.btn_copy.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px;")

        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_paste)
        btn_layout.addWidget(self.btn_custom_col)
        btn_layout.addWidget(self.btn_avg)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_history)
        btn_layout.addStretch() 
        btn_layout.addWidget(self.lbl_select)
        btn_layout.addWidget(self.combo_type)
        btn_layout.addWidget(self.btn_export_png)
        btn_layout.addWidget(self.btn_copy)
        main_layout.addWidget(btn_frame)

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget { font-family: 'Segoe UI'; font-size: 10pt; background-color: #ffffff; }
            QHeaderView::section { font-family: 'Segoe UI'; font-size: 10pt; font-weight: bold; background-color: #e1e1e1; padding: 4px; border: 1px solid #d0d0d0; }
        """)
        main_layout.addWidget(self.table)
        self.update_table_columns()

        self.status_label = QLabel("Siap. Silakan copy data dari Excel lalu tekan tombol 'Paste Data'.")
        self.status_label.setStyleSheet("background-color: #eaeaea; font-family: 'Segoe UI'; font-size: 9pt; padding: 5px; border: 1px solid #cccccc;")
        main_layout.addWidget(self.status_label)

        self.btn_back.clicked.connect(self.back_to_home)
        self.btn_paste.clicked.connect(self.paste_data)
        self.btn_avg.clicked.connect(self.calculate_average)
        self.btn_custom_col.clicked.connect(self.add_custom_column)
        self.btn_clear.clicked.connect(self.clear_data)
        self.btn_copy.clicked.connect(self.copy_all)
        self.btn_export_png.clicked.connect(self.generate_png_report)
        self.btn_history.clicked.connect(self.show_history_dialog)

    def back_to_home(self):
        from views.home_window import HomeWindow
        self.home = HomeWindow()
        self.home.show()
        self.close()

    def update_table_columns(self):
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        for i, col in enumerate(self.columns):
            if col == "No.": self.table.setColumnWidth(i, 50)
            elif "Result" in col or "Point" in col or "Recommended" in col: self.table.setColumnWidth(i, 130)
            else: self.table.setColumnWidth(i, 110)

    def paste_data(self):
        clipboard_data = QApplication.clipboard().text()
        if not clipboard_data.strip():
            QMessageBox.critical(self, "Error", "Clipboard kosong! Silakan COPY data terlebih dahulu dari Excel.")
            return
        self.process_raw_text(clipboard_data, save_to_db=True)

    def process_raw_text(self, raw_text, save_to_db=True):
        lines = raw_text.strip().split('\n')
        if not lines or lines == ['']: return

        for row in range(self.table.rowCount() - 1, -1, -1):
            item = self.table.item(row, 0)
            if item and item.text() == "AVG": self.table.removeRow(row)

        first_line = lines[0]
        delimiter = '\t' if '\t' in first_line else ','
        current_rows = self.table.rowCount()
        inserted_count = 0
        
        self.table.setUpdatesEnabled(False)
        stats = {"Excellent": 0, "Good": 0, "Fair": 0, "Poor": 0}

        for line in lines:
            line = line.strip()
            if not line: continue
            cols = line.split(delimiter)
            if len(cols) < 8: continue
            if "average" in cols[3].lower() or "field" in cols[3].lower() or "test point" in cols[0].lower(): continue

            row_data = [c.strip() for c in cols[:8]]
            try:
                avg_fs = float(row_data[3])
                snr = avg_fs - (-90)
                if snr >= 25: snr_result = "Excellent"
                elif snr >= 15: snr_result = "Good"
                elif snr >= 10: snr_result = "Fair"
                else: snr_result = "Poor"
                row_data.extend([round(snr, 2), snr_result])
                stats[snr_result] += 1
            except ValueError:
                row_data.extend(["N/A", "N/A"])

            row_number = current_rows + inserted_count + 1
            row_data.insert(0, str(row_number))

            while len(row_data) < len(self.columns): row_data.append("")

            row_idx = current_rows + inserted_count
            self.table.insertRow(row_idx)
            row_color = self.bg_color_even if row_number % 2 == 0 else self.bg_color_odd
            
            for col_idx, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QBrush(row_color))
                self.table.setItem(row_idx, col_idx, item)
            inserted_count += 1

        self.table.setUpdatesEnabled(True)
        self.status_label.setText(f"Berhasil memuat {inserted_count} data baru.")

        if save_to_db and inserted_count > 0:
            selected_mode = self.combo_type.currentText()
            mode_label = "RSSI" if "RSSI" in selected_mode else "SNR"
            from database.db_manager import insert_history
            insert_history(mode_label, inserted_count, stats["Excellent"], stats["Good"], stats["Fair"], stats["Poor"], raw_text)

    def show_history_dialog(self):
        dialog = HistoryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.selected_raw_data:
                self.table.setRowCount(0)
                self.combo_type.setCurrentText("RSSI (Test Result)" if dialog.selected_mode == "RSSI" else "SNR (SNR Result)")
                self.process_raw_text(dialog.selected_raw_data, save_to_db=False)

    def calculate_average(self):
        row_count = self.table.rowCount()
        if row_count == 0:
            QMessageBox.warning(self, "Peringatan", "Tabel masih kosong!")
            return

        for row in range(row_count - 1, -1, -1):
            item = self.table.item(row, 0)
            if item and item.text() == "AVG": self.table.removeRow(row)
                
        row_count = self.table.rowCount()
        if row_count == 0: return

        num_cols = len(self.columns)
        avg_row = ["-"] * num_cols
        avg_row[0] = "AVG"

        for col_index in range(1, num_cols):
            total = 0.0
            count = 0
            for row in range(row_count):
                item = self.table.item(row, col_index)
                if item:
                    try:
                        num = float(item.text())
                        total += num
                        count += 1
                    except ValueError: pass
            if count > 0:
                avg_row[col_index] = str(round(total / count, 2))

        self.table.insertRow(row_count)
        for col_index, val in enumerate(avg_row):
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QBrush(self.bg_color_avg))
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            self.table.setItem(row_count, col_index, item)
        self.table.scrollToBottom()

    def add_custom_column(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tambah Kolom Baru")
        dialog.setFixedSize(400, 230)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        layout = QVBoxLayout(dialog)

        lbl_name = QLabel("Nama Kolom Baru:")
        lbl_name.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(lbl_name)
        col_name_entry = QLineEdit()
        layout.addWidget(col_name_entry)

        lbl_formula = QLabel("Formula Matematika (Contoh: c5 - c7):")
        lbl_formula.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(lbl_formula)
        lbl_hint = QLabel("Keterangan: c5 = Avg Field, c6 = Max Field, c7 = Min Field")
        lbl_hint.setStyleSheet("color: dimgray; font-size: 8pt;")
        layout.addWidget(lbl_hint)
        formula_entry = QLineEdit()
        layout.addWidget(formula_entry)

        def apply_formula_action():
            col_name = col_name_entry.text().strip()
            formula_str = formula_entry.text().strip()
            if not col_name or not formula_str: return

            self.columns.append(col_name)
            self.update_table_columns()
            self.table.setUpdatesEnabled(False)
            
            for row in range(self.table.rowCount()):
                item_no = self.table.item(row, 0)
                if item_no and item_no.text() == "AVG": continue

                local_vars = {}
                for col in range(self.table.columnCount() - 1):
                    item = self.table.item(row, col)
                    val_str = item.text() if item else ""
                    try: local_vars[f"c{col+1}"] = float(val_str)
                    except ValueError: local_vars[f"c{col+1}"] = 0.0
                
                new_val = "-"
                try:
                    result = eval(formula_str, {}, local_vars)
                    new_val = str(round(result, 2))
                except Exception: pass
                    
                new_item = QTableWidgetItem(new_val)
                new_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                bg_brush = self.table.item(row, 0).background() if self.table.item(row, 0) else QBrush(self.bg_color_even)
                new_item.setBackground(bg_brush)
                self.table.setItem(row, self.table.columnCount() - 1, new_item)

            self.table.setUpdatesEnabled(True)
            dialog.accept()

        btn_apply = QPushButton("Hitung & Tambahkan")
        btn_apply.setStyleSheet("background-color: #0078d7; color: white; font-weight: bold;")
        btn_apply.clicked.connect(apply_formula_action)
        layout.addSpacing(15)
        layout.addWidget(btn_apply)
        dialog.exec()

    def generate_png_report(self):
        if self.table.rowCount() == 0: return

        selected_mode = self.combo_type.currentText()
        if "RSSI" in selected_mode:
            target_col_name = "Test Result"
            header_text = "Count of Average Field Strength (dBm)"
            main_title = "Laporan Distribusi - RSSI"
            default_filename = "Dashboard_RSSI_Result.png"
        else:
            target_col_name = "SNR Result"
            header_text = "Count of SNR Result"
            main_title = "Laporan Distribusi - SNR"
            default_filename = "Dashboard_SNR_Result.png"

        col_idx = self.columns.index(target_col_name)
        counts = {"Excellent": 0, "Good": 0, "Fair": 0, "Poor": 0}
        total_rows = 0
        
        for row in range(self.table.rowCount()):
            item_no = self.table.item(row, 0)
            if item_no and item_no.text() == "AVG": continue
            item = self.table.item(row, col_idx)
            if item:
                res = item.text().strip()
                if res in counts:
                    counts[res] += 1
                    total_rows += 1

        labels, sizes, colors = [], [], []
        colors_map = {"Excellent": "#4472c4", "Good": "#ed7d31", "Fair": "#a5a5a5", "Poor": "#ffc000"}
        for cat, val in counts.items():
            if val > 0:
                labels.append(cat)
                sizes.append(val)
                colors.append(colors_map[cat])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1, 1.3]})
        fig.patch.set_facecolor('white')
        fig.suptitle(main_title, fontsize=20, fontweight='bold', color="#2f2f2f", y=0.98)

        wedges, texts, autotexts = ax1.pie(sizes, labels=None, autopct='%1.0f%%', startangle=90, colors=colors)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
            autotext.set_bbox(dict(facecolor='#333333', alpha=0.7, edgecolor='none', boxstyle='square,pad=0.2'))

        ax1.set_title("Total", fontweight="bold", fontsize=16)
        ax1.legend(labels, loc="center left", bbox_to_anchor=(0.9, 0.5), frameon=True)
        ax1.axis('equal') 
        
        ax2.axis('off')
        table_data = [[cat, counts[cat]] for cat in ["Excellent", "Good", "Fair", "Poor"] if counts[cat] > 0]
        table_data.append(["Grand Total", total_rows])
        
        table = ax2.table(cellText=table_data, colLabels=["Row Labels", header_text], loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 2) 
        table.auto_set_column_width(col=list(range(2)))
        
        for (row, col), cell in table.get_celld().items():
            if row == 0 or row == len(table_data):
                cell.set_facecolor('#d9e1f2')
                cell.set_text_props(weight='bold')

        plt.tight_layout()
        plt.subplots_adjust(top=0.85) 

        preview = PreviewDialog(fig, default_filename, self)
        preview.exec()
        plt.close(fig)

    def clear_data(self):
        reply = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus seluruh data?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.table.setRowCount(0)
            self.columns = self.columns[:11]  
            self.update_table_columns()

    def copy_all(self):
        if self.table.rowCount() == 0: return
        all_data = ['\t'.join(self.columns)]
        for row in range(self.table.rowCount()):
            row_data = [self.table.item(row, col).text() if self.table.item(row, col) else "" for col in range(self.table.columnCount())]
            all_data.append('\t'.join(row_data))
        QApplication.clipboard().setText('\n'.join(all_data))
        QMessageBox.information(self, "Sukses", "Data berhasil disalin!")
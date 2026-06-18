import csv
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox,
    QLineEdit, QComboBox, QAbstractItemView, QApplication, QListView
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QColor, QFont, QBrush, QStandardItemModel, QStandardItem

# ==========================================
# KELAS KUSTOM: COMBOBOX CHECKBOX ANTI-BUG
# ==========================================
class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        # Menggunakan QListView agar item bisa diklik tanpa langsung menutup dropdown
        self.setView(QListView(self))
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))
        
        self.lineEdit_custom = QLineEdit()
        self.lineEdit_custom.setReadOnly(True)
        self.setLineEdit(self.lineEdit_custom)
        self.lineEdit_custom.setText("✨ Pilih SSID...")
        
        self.model().dataChanged.connect(self.update_text)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    def add_item(self, text, checked=False):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self.model().appendRow(item)
        
    def get_checked_items(self):
        checked = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked.append(item.text())
        return checked

    def update_text(self):
        checked = self.get_checked_items()
        if not checked:
            self.lineEdit_custom.setText("✨ Pilih SSID...")
        else:
            self.lineEdit_custom.setText(", ".join(checked))

    def clear_items(self):
        self.model().clear()


# ==========================================
# APLIKASI UTAMA
# ==========================================
class RadioEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radio Editor Module - Network Tools")
        self.setGeometry(50, 50, 1200, 650)
        
        self.bg_color_odd = QColor("#f2f2f2") 
        self.bg_color_even = QColor("#ffffff")

        self.columns = [
            "AP Name", "Channel 2.4GHz", "Power 2.4GHz", 
            "Channel 5GHz", "Power 5GHz", "SSID"
        ]
        
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # ==========================================
        # 1. FRAME KONTROL ATAS
        # ==========================================
        top_frame = QWidget()
        top_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 5px; border: 1px solid #ddd;")
        top_layout = QVBoxLayout(top_frame)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # --- BARIS 1: TOMBOL DENGAN PEMANIS ---
        btn_layout = QHBoxLayout()
        self.btn_back = QPushButton("🔙 Kembali 🏠")
        self.btn_back.setStyleSheet("background-color: #ffffff; color: #333333; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 12px; border: 1px solid #cccccc; border-radius: 4px;")
        
        self.btn_upload = QPushButton("📥 Upload CSV Radio 🚀")
        self.btn_upload.setStyleSheet("background-color: #c00000; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 15px; border-radius: 4px; border: 1px solid #800000;")

        self.btn_copy = QPushButton("📋 Copy Tabel (Word/Excel) ✨")
        self.btn_copy.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 10pt; padding: 6px 15px; border-radius: 4px; border: 1px solid #1e7e34;")

        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_upload)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addStretch()
        
        # --- BARIS 2: FILTER & BULK ASSIGN ---
        filter_layout = QHBoxLayout()
        lbl_filter = QLabel("🔍 Cari Data:")
        lbl_filter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["AP Name", "SSID"])
        self.combo_filter.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; padding: 4px; background: white; border: 1px solid #aaa;")
        
        self.txt_filter = QLineEdit()
        self.txt_filter.setPlaceholderText("Ketik nama AP/SSID...")
        self.txt_filter.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; padding: 5px; min-width: 200px; border: 1px solid #aaa;")

        lbl_ssid = QLabel("🎯 Set Target SSID ✨:")
        lbl_ssid.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_ssid.setStyleSheet("color: #c00000;") # Warna teks merah agar menarik
        
        self.combo_ssid_check = CheckableComboBox()
        self.combo_ssid_check.setStyleSheet("font-family: 'Segoe UI'; font-size: 10pt; padding: 4px; background: white; border: 1px solid #c00000; min-width: 250px; color: #333;")
        
        # MEMASUKKAN 4 DUMMY SSID (Default)
        self.default_ssids = ["BRI-Digital", "Brivolution", "Direksi-BRI"]
        for s in self.default_ssids:
            self.combo_ssid_check.add_item(s, False)

        filter_layout.addWidget(lbl_filter)
        filter_layout.addWidget(self.combo_filter)
        filter_layout.addWidget(self.txt_filter)
        filter_layout.addSpacing(30)
        filter_layout.addWidget(lbl_ssid)
        filter_layout.addWidget(self.combo_ssid_check)
        filter_layout.addStretch()

        top_layout.addLayout(btn_layout)
        top_layout.addLayout(filter_layout)
        main_layout.addWidget(top_frame)

        # ==========================================
        # 2. TABEL DATA RADIO 
        # ==========================================
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        self.table.setStyleSheet("""
            QTableWidget { font-family: 'Segoe UI'; font-size: 10pt; background-color: #ffffff; gridline-color: #000000; }
            QHeaderView::section { font-family: 'Segoe UI'; font-size: 10pt; font-weight: bold; background-color: #c00000; color: #ffffff; padding: 6px; border: 1px solid #000000; }
            QTableWidget::item { border-right: 1px solid #000000; border-bottom: 1px solid #000000; padding: 5px; }
        """)
        
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSortingEnabled(True) 
        
        main_layout.addWidget(self.table)

        self.status_label = QLabel("Siap. Silakan upload file CSV Radio Info. 🚀")
        self.status_label.setStyleSheet("color: #666; font-family: 'Segoe UI'; font-size: 9pt;")
        main_layout.addWidget(self.status_label)

        # ==========================================
        # 3. EVENT CONNECTIONS
        # ==========================================
        self.btn_back.clicked.connect(self.back_to_home)
        self.btn_upload.clicked.connect(self.upload_csv)
        self.btn_copy.clicked.connect(self.copy_to_clipboard_html)
        self.txt_filter.textChanged.connect(self.apply_search_filter)
        
        # Memicu fungsi Apply SSID ke Tabel saat Checkbox dicentang
        self.combo_ssid_check.model().dataChanged.connect(self.apply_ssid_to_table)

    def back_to_home(self):
        from views.home_window import HomeWindow
        self.home = HomeWindow()
        self.home.show()
        self.close()

    def get_val(self, row_dict, keywords):
        for key, val in row_dict.items():
            clean_key = key.replace('\t', '').replace('"', '').strip().lower() if key else ""
            if any(k in clean_key for k in keywords):
                return val.replace('\t', '').replace('"', '').strip()
        return ""

    def extract_left_power(self, power_string):
        if not power_string or power_string == "--" or power_string == "-": return "-"
        if "/" in power_string: return power_string.split("/")[0].strip()
        return power_string.strip()

    def upload_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Pilih File CSV Radio Info", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not filepath: return

        self.status_label.setText("Sedang memproses dan mengelompokkan data... ⏳")
        processed_ap = {}
        unique_ssids = set() 

        try:
            with open(filepath, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ap_name = self.get_val(row, ["ap name", "apname"])
                    radio_id = self.get_val(row, ["radio id", "radioid"])
                    channel = self.get_val(row, ["channel", "ch"])
                    raw_power = self.get_val(row, ["eirp", "power", "tx power"]) 
                    power = self.extract_left_power(raw_power)
                    ssid = self.get_val(row, ["ssid"])

                    if not ap_name: continue
                    
                    if ssid and ssid != "-" and ssid != "--":
                        unique_ssids.add(ssid)

                    if ap_name not in processed_ap:
                        processed_ap[ap_name] = {
                            "ssid": ssid if ssid else "-",
                            "ch_24": "-", "pwr_24": "-", "radio_5g": [] 
                        }

                    if radio_id == '0':
                        processed_ap[ap_name]["ch_24"] = channel if channel and channel != "--" else "-"
                        processed_ap[ap_name]["pwr_24"] = power
                    elif radio_id in ['1', '2']:
                        ch_val = channel if channel and channel != "--" else "-"
                        pwr_val = power if power and power != "-" else "-"
                        if ch_val != "-" or pwr_val != "-":
                            processed_ap[ap_name]["radio_5g"].append({"ch": ch_val, "pwr": pwr_val})

            # PERBAIKAN: Menggabungkan SSID Dummy dengan SSID dari CSV agar tidak hilang
            self.combo_ssid_check.model().dataChanged.disconnect(self.apply_ssid_to_table) 
            self.combo_ssid_check.clear_items()
            
            # Gabungkan dan urutkan
            all_combined_ssids = sorted(list(set(self.default_ssids) | unique_ssids))
            
            for s in all_combined_ssids:
                self.combo_ssid_check.add_item(s, False)
                
            self.combo_ssid_check.model().dataChanged.connect(self.apply_ssid_to_table)

            self.populate_table(processed_ap)
            self.status_label.setText(f"✅ Berhasil memproses data dari: {filepath.split('/')[-1]}")

        except Exception as e:
            QMessageBox.critical(self, "Error ❌", f"Gagal membaca CSV:\n{str(e)}")
            self.status_label.setText("❌ Gagal upload data.")

    def populate_table(self, grouped_data):
        self.table.setSortingEnabled(False)
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(0)

        for row_idx, (ap_name, data) in enumerate(grouped_data.items()):
            self.table.insertRow(row_idx)

            r5_list = data["radio_5g"]
            ch_5_str = "-"
            pwr_5_str = "-"
            
            if len(r5_list) == 1:
                ch_5_str = str(r5_list[0]["ch"])
                pwr_5_str = str(r5_list[0]["pwr"])
            elif len(r5_list) >= 2:
                def safe_int(val):
                    try: return int(val)
                    except ValueError: return 0
                r5_sorted = sorted(r5_list, key=lambda x: safe_int(x["ch"]), reverse=True)
                ch_5_str = f"High : {r5_sorted[0]['ch']}\nLow  : {r5_sorted[1]['ch']}"
                pwr_5_str = f"{r5_sorted[0]['pwr']}\n{r5_sorted[1]['pwr']}"

            # SUSUNAN FIX: SSID ada di Index ke-5 (Paling Kanan)
            row_values = [ap_name, data["ch_24"], data["pwr_24"], ch_5_str, pwr_5_str, data["ssid"]]
            row_color = self.bg_color_even if row_idx % 2 == 0 else self.bg_color_odd

            for col_idx, val in enumerate(row_values):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QBrush(row_color))
                
                try:
                    if val != "-" and "\n" not in str(val) and "High" not in str(val) and str(val).replace('.','',1).isdigit():
                        if "." in str(val): item.setData(Qt.ItemDataRole.EditRole, float(val))
                        else: item.setData(Qt.ItemDataRole.EditRole, int(val))
                    else:
                        item.setData(Qt.ItemDataRole.EditRole, val)
                except ValueError:
                    item.setData(Qt.ItemDataRole.EditRole, val)
                
                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeRowsToContents()
        self.table.setUpdatesEnabled(True)
        self.table.setSortingEnabled(True)
        
        # Mengecek apakah ada Checkbox yang sedang tercentang untuk diaplikasikan
        self.apply_ssid_to_table()

    # --- FUNGSI MENGISI KOLOM SSID BERDASARKAN CHECKBOX ---
    def apply_ssid_to_table(self):
        if self.table.rowCount() == 0:
            return
            
        checked_ssids = self.combo_ssid_check.get_checked_items()
        
        # Menggunakan format baris baru (\n) agar SSID menyusun atas-bawah persis seperti High/Low
        new_ssid_value = "\n".join(checked_ssids) if checked_ssids else "-"
        
        self.table.setUpdatesEnabled(False)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 5) # Indeks 5 adalah kolom SSID di paling kanan
            if item:
                item.setText(new_ssid_value)
                
        self.table.resizeRowsToContents()
        self.table.setUpdatesEnabled(True)
        
        # Panggil ulang filter search bar barangkali ada SSID yang baru diaplikasikan
        self.apply_search_filter()

    # --- FUNGSI MENCARI TEKS ---
    def apply_search_filter(self):
        search_text = self.txt_filter.text().lower()
        filter_target = self.combo_filter.currentText()
        col_index = 0 if filter_target == "AP Name" else 5 # AP Name=0, SSID=5

        for row in range(self.table.rowCount()):
            item = self.table.item(row, col_index)
            if item:
                if search_text in item.text().lower(): 
                    self.table.setRowHidden(row, False)
                else: 
                    self.table.setRowHidden(row, True)

    # --- FUNGSI COPY TO HTML EXCEL/WORD ---
    def copy_to_clipboard_html(self):
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Peringatan ⚠️", "Tidak ada data untuk disalin.")
            return

        html = '<html><head><meta charset="utf-8"></head><body>\n'
        html += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; font-family: Calibri, sans-serif; font-size: 11pt; width: 100%; border: 1pt solid black;">\n'
        
        html += '  <thead>\n'
        html += '    <tr bgcolor="#c00000" style="background-color: #c00000;">\n'
        for col_name in self.columns:
            html += (f'      <td bgcolor="#c00000" style="background-color: #c00000; border: 1pt solid black; '
                     f'padding: 6px; text-align: center; vertical-align: middle;">'
                     f'<font color="#ffffff"><b>{col_name}</b></font></td>\n')
        html += '    </tr>\n'
        html += '  </thead>\n'
        
        html += '  <tbody>\n'
        for row in range(self.table.rowCount()):
            if self.table.isRowHidden(row): continue
            
            bg_hex = "#ffffff" if row % 2 == 0 else "#f2f2f2" 
            html += f'    <tr bgcolor="{bg_hex}" style="background-color: {bg_hex};">\n'
            
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                text = item.text() if item else ""
                text_html = text.replace('\n', '<br style="mso-data-placement:same-cell;" />')
                html += (f'      <td bgcolor="{bg_hex}" style="background-color: {bg_hex}; border: 1pt solid black; padding: 6px; '
                         f'text-align: center; vertical-align: middle;">{text_html}</td>\n')
            html += '    </tr>\n'
            
        html += '  </tbody>\n</table>\n</body></html>'

        mime_data = QMimeData()
        mime_data.setHtml(html)
        
        fallback_text = ""
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                row_data = [self.table.item(row, col).text().replace('\n', ' / ') for col in range(self.table.columnCount())]
                fallback_text += '\t'.join(row_data) + '\n'
        mime_data.setText(fallback_text)

        QApplication.clipboard().setMimeData(mime_data)
        QMessageBox.information(self, "Sukses ✨", "Tabel berhasil disalin!\n\nSilakan 'Paste' (Ctrl+V) langsung ke Word/Excel dengan format Calibri 11pt.")
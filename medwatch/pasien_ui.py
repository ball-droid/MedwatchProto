"""
Modul UI Pasien
Dashboard untuk pasien dengan fitur search obat dan rekomendasi cerdas

@author: MedWatch Team
@maintained: Mahasiswa
@description:
    Modul ini menangani tampilan dashboard pasien yang mencakup:
    1. Profil pasien
    2. Riwayat rekam medis
    3. Rekomendasi obat dengan algoritma kecocokan
    4. Pencarian obat dengan filter kategori
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from utils.json_helper import JSONHelper
from modules.medical_record import MedicalRecordManager
from modules.drug_recommend import DrugRecommender
from modules.drug_data import DrugDataManager
import os


class PasienDashboard(ctk.CTk):
    """
    Kelas Dashboard Pasien
    Menampilkan semua fitur yang bisa diakses oleh pasien
    """

    def __init__(self, username):
        """Constructor: inisialisasi dashboard pasien"""
        super().__init__()
        self.username = username
        self.json_helper = JSONHelper()
        self.record_manager = MedicalRecordManager()
        self.recommender = DrugRecommender()
        self.drug_manager = DrugDataManager()

        # Load data pasien
        self.patient_data = self.get_patient_data()
        self.search_results = []

        # Setup UI
        self.init_ui()

    def get_patient_data(self):
        """
        Ambil data pasien berdasarkan username
        Returns: dict data pasien atau None
        """
        patients = self.json_helper.load_patients()
        for patient in patients:
            if patient['username'] == self.username:
                return patient
        return None

    def init_ui(self):
        """Inisialisasi UI dashboard pasien"""
        # Set judul window dengan nama pasien
        self.patient_data = self.patient_data or {}
        self.title(f"MedWatch - Pasien: {self.patient_data.get('name', 'Pasien')}")
        self.geometry("1100x700")

        # Configure grid layout untuk responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Bind ESC untuk keluar fullscreen (akan di-set saat dibuka)
        self.bind("<Escape>", self.toggle_fullscreen)

        # Buat header
        header_frame = self.create_header()
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # Buat tabview (tab navigation)
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Tambahkan tabs
        self.profile_tab = self.tab_view.add("👤 Profil Saya")
        self.records_tab = self.tab_view.add("📋 Rekam Medis")
        self.prescription_tab = self.tab_view.add("💊 Resep Obat")
        self.drug_search_tab = self.tab_view.add("🔍 Cari Obat")

        # Setup setiap tab
        self.setup_profile_tab()
        self.setup_records_tab()
        self.setup_prescription_tab()
        self.setup_drug_search_tab()

        # Tombol logout
        logout_frame = ctk.CTkFrame(self, fg_color="transparent")
        logout_frame.grid(row=2, column=0, sticky="e", padx=10, pady=(5, 10))

        logout_btn = ctk.CTkButton(
            logout_frame,
            text="Keluar",
            command=self.logout,
            width=100,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        logout_btn.pack()

    def create_header(self):
        """Buat header dashboard dengan info pasien"""
        header_frame = ctk.CTkFrame(self, height=80)
        header_frame.grid_columnconfigure(1, weight=1)

        # Avatar/icon pasien
        avatar_label = ctk.CTkLabel(
            header_frame,
            text="👤",
            font=ctk.CTkFont(size=40)
        )
        avatar_label.grid(row=0, column=0, padx=20, pady=15)

        # Info pasien (nama)
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10)

        title_label = ctk.CTkLabel(
            info_frame,
            text="Dashboard Pasien",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(anchor="w")

        name_label = ctk.CTkLabel(
            info_frame,
            text=f"Nama: {self.patient_data.get('name', 'Unknown')}",
            font=ctk.CTkFont(size=14)
        )
        name_label.pack(anchor="w")

        return header_frame

    def setup_profile_tab(self):
        """Setup tab profil pasien"""
        scroll_frame = ctk.CTkScrollableFrame(self.profile_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Card info pribadi
        info_frame = ctk.CTkFrame(scroll_frame)
        info_frame.pack(fill="x", padx=10, pady=10)

        title = ctk.CTkLabel(
            info_frame,
            text="Informasi Pribadi",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(15, 10))

        # Tampilkan data pasien
        info_data = [
            ("Nama Lengkap", self.patient_data.get('name', '-')),
            ("Usia", str(self.patient_data.get('age', '-'))),
            ("Jenis Kelamin", self.patient_data.get('gender', '-')),
            ("No. Telepon", self.patient_data.get('phone', '-')),
            ("Golongan Darah", self.patient_data.get('blood_type', '-')),
            ("Alamat", self.patient_data.get('address', '-')),
        ]

        # Tambahkan kondisi medis jika ada
        patient_conditions = self.patient_data.get('conditions', [])
        if patient_conditions:
            info_data.append(("Kondisi Medis", ", ".join(patient_conditions)))

        # Render info
        for label, value in info_data:
            row_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=5)

            label_widget = ctk.CTkLabel(
                row_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                width=150
            )
            label_widget.pack(side="left")

            value_widget = ctk.CTkLabel(
                row_frame,
                text=value,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            value_widget.pack(side="left", padx=10)

    def setup_records_tab(self):
        """Setup tab riwayat rekam medis"""
        main_frame = ctk.CTkFrame(self.records_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Riwayat Rekam Medis",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 15))

        # Frame tabel
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Setup treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=('Segoe UI', 11))
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))

        # Buat treeview
        self.records_tree = ttk.Treeview(
            table_frame,
            columns=("Tanggal", "Diagnosis", "Dokter", "Obat", "Catatan"),
            show="headings",
            height=12
        )

        self.records_tree.heading("Tanggal", text="Tanggal")
        self.records_tree.heading("Diagnosis", text="Diagnosis")
        self.records_tree.heading("Dokter", text="Dokter")
        self.records_tree.heading("Obat", text="Obat")
        self.records_tree.heading("Catatan", text="Catatan")

        self.records_tree.column("Tanggal", width=120, anchor="center")
        self.records_tree.column("Diagnosis", width=200)
        self.records_tree.column("Dokter", width=180)
        self.records_tree.column("Obat", width=200)
        self.records_tree.column("Catatan", width=250)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        self.records_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load data rekam medis
        self.load_records()

    def setup_prescription_tab(self):
        """Setup tab rekomendasi obat berdasarkan gejala"""
        main_frame = ctk.CTkScrollableFrame(self.prescription_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="💊 Rekomendasi Obat Berdasarkan Gejala",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 15))

        # Info card
        info_card = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray25"))
        info_card.pack(fill="x", padx=10, pady=(0, 15))

        info_label = ctk.CTkLabel(
            info_card,
            text="💡 Masukkan gejala yang Anda alami untuk mendapatkan rekomendasi obat.\n"
                 "   Sistem akan menganalisis kecocokan obat berdasarkan gejala dan kondisi kesehatan Anda.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=15, pady=10)

        # Input frame
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Input gejala
        symptom_label = ctk.CTkLabel(input_frame, text="Gejala:", font=ctk.CTkFont(size=14, weight="bold"))
        symptom_label.pack(anchor="w", padx=15, pady=(10, 5))

        input_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_row.pack(fill="x", padx=15, pady=(0, 10))

        self.symptom_input = ctk.CTkEntry(
            input_row,
            placeholder_text="Contoh: demam, sakit kepala, batuk"
        )
        self.symptom_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind Enter key untuk langsung cari
        self.symptom_input.bind("<Return>", lambda e: self.get_recommendation())

        # Tombol cari rekomendasi
        recommend_btn = ctk.CTkButton(
            input_row,
            text="🔍 Cari Rekomendasi",
            command=self.get_recommendation,
            width=160,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        recommend_btn.pack(side="right")

        # Checkbox untuk kondisi medis
        conditions_frame = ctk.CTkFrame(main_frame)
        conditions_frame.pack(fill="x", padx=10, pady=(0, 15))

        conditions_label = ctk.CTkLabel(
            conditions_frame,
            text="Kondisi Medis yang Anda Miliki (opsional):",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        conditions_label.pack(anchor="w", padx=15, pady=(10, 5))

        # Checkbox untuk kondisi medis umum
        self.condition_vars = {}
        common_conditions = ['Asma', 'Maag/Ulkus', 'Gangguan Ginjal', 'Gangguan Hati', 'Hamil']

        checkboxes_frame = ctk.CTkFrame(conditions_frame, fg_color="transparent")
        checkboxes_frame.pack(fill="x", padx=15, pady=(0, 10))

        for i, condition in enumerate(common_conditions):
            var = ctk.BooleanVar()
            self.condition_vars[condition] = var
            checkbox = ctk.CTkCheckBox(
                checkboxes_frame,
                text=condition,
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            checkbox.pack(side="left", padx=(0, 15))

        # Auto-check kondisi existing dari data pasien
        if self.patient_data and 'conditions' in self.patient_data:
            for cond in self.patient_data['conditions']:
                for common_cond in common_conditions:
                    if cond.lower() in common_cond.lower() or common_cond.lower() in cond.lower():
                        self.condition_vars[common_cond].set(True)

        # Hasil rekomendasi
        results_label = ctk.CTkLabel(
            main_frame,
            text="Hasil Rekomendasi:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(anchor="w", padx=15, pady=(10, 5))

        # Textbox untuk hasil
        self.prescription_text = ctk.CTkTextbox(main_frame, height=400)
        self.prescription_text.insert("1.0", "Hasil rekomendasi obat akan muncul di sini...")
        self.prescription_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    def setup_drug_search_tab(self):
        """Setup tab pencarian obat"""
        main_frame = ctk.CTkFrame(self.drug_search_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🔍 Cari Obat & Informasi Obat",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 15))

        # Search frame
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Input search
        search_label = ctk.CTkLabel(search_frame, text="Kata Kunci:", font=ctk.CTkFont(size=14, weight="bold"))
        search_label.pack(anchor="w", padx=15, pady=(10, 5))

        search_input_row = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_row.pack(fill="x", padx=15, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_input_row,
            placeholder_text="Cari nama obat, kategori, indikasi, atau tag..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_drugs())

        search_btn = ctk.CTkButton(
            search_input_row,
            text="Cari",
            command=self.search_drugs,
            width=120,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        search_btn.pack(side="right")

        # Filter kategori
        filter_row = ctk.CTkFrame(search_frame, fg_color="transparent")
        filter_row.pack(fill="x", padx=15, pady=(0, 10))

        filter_label = ctk.CTkLabel(filter_row, text="Filter Kategori:", font=ctk.CTkFont(size=13))
        filter_label.pack(side="left", padx=(0, 10))

        categories = ["Semua Kategori"] + self.drug_manager.get_all_categories()
        self.category_combo = ctk.CTkOptionMenu(
            filter_row,
            values=categories,
            command=lambda x: self.filter_by_category(),
            width=250
        )
        self.category_combo.set("Semua Kategori")
        self.category_combo.pack(side="left")

        # Hasil pencarian
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Label jumlah hasil
        self.results_count_label = ctk.CTkLabel(
            results_frame,
            text="Menampilkan semua obat",
            font=ctk.CTkFont(size=13)
        )
        self.results_count_label.pack(pady=(10, 5))

        # Treeview untuk hasil
        tree_frame = ctk.CTkFrame(results_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=('Segoe UI', 11))
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))

        self.drugs_tree = ttk.Treeview(
            tree_frame,
            columns=("Nama", "Kategori", "Dosis", "Indikasi", "Harga"),
            show="headings",
            height=15
        )

        self.drugs_tree.heading("Nama", text="Nama Obat")
        self.drugs_tree.heading("Kategori", text="Kategori")
        self.drugs_tree.heading("Dosis", text="Dosis")
        self.drugs_tree.heading("Indikasi", text="Indikasi")
        self.drugs_tree.heading("Harga", text="Harga")

        self.drugs_tree.column("Nama", width=200)
        self.drugs_tree.column("Kategori", width=180)
        self.drugs_tree.column("Dosis", width=150)
        self.drugs_tree.column("Indikasi", width=300)
        self.drugs_tree.column("Harga", width=100, anchor="e")

        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.drugs_tree.yview)
        self.drugs_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.drugs_tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

        # Double-click untuk lihat detail
        self.drugs_tree.bind("<Double-1>", lambda e: self.show_drug_detail())

        # Tombol detail
        detail_btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        detail_btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        detail_btn = ctk.CTkButton(
            detail_btn_frame,
            text="📋 Lihat Detail Obat",
            command=self.show_drug_detail,
            width=180,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        detail_btn.pack(side="left", padx=(15, 0))

        # Load semua obat saat awal
        self.load_all_drugs()

    def load_all_drugs(self):
        """Load semua obat ke tabel pencarian"""
        # Clear existing items
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)

        drugs = self.drug_manager.get_all_drugs()

        self.results_count_label.configure(text=f"Menampilkan {len(drugs)} obat")

        for drug in drugs:
            # Truncate indikasi jika terlalu panjang
            indication = drug['indication']
            if len(indication) > 50:
                indication = indication[:50] + "..."

            self.drugs_tree.insert(
                "",
                "end",
                values=(
                    drug['name'],
                    drug['category'],
                    drug['dosage'],
                    indication,
                    f"Rp {drug.get('price', 0):,}"
                )
            )

    def search_drugs(self):
        """
        Cari obat berdasarkan keyword (case-insensitive)
        Mencari di: nama, kategori, indikasi, tags
        """
        keyword = self.search_entry.get().strip()
        keyword_lower = keyword.lower()  # Ubah ke lowercase untuk case-insensitive

        if not keyword:
            self.load_all_drugs()
            return

        # Clear existing
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)

        # Search menggunakan drug manager dengan keyword lowercase
        results = self.drug_manager.search_drugs(keyword)

        self.search_results = results
        self.results_count_label.configure(text=f"Ditemukan {len(results)} obat untuk '{keyword}'")

        for drug in results:
            indication = drug['indication']
            if len(indication) > 50:
                indication = indication[:50] + "..."

            self.drugs_tree.insert(
                "",
                "end",
                values=(
                    drug['name'],
                    drug['category'],
                    drug['dosage'],
                    indication,
                    f"Rp {drug.get('price', 0):,}"
                )
            )

    def filter_by_category(self):
        """Filter obat berdasarkan kategori"""
        category = self.category_combo.get()

        # Clear existing
        for item in self.drugs_tree.get_children():
            self.drugs_tree.delete(item)

        if category == "Semua Kategori":
            self.load_all_drugs()
            return

        # Filter by category
        drugs = self.drug_manager.get_drugs_by_category(category)

        self.results_count_label.configure(text=f"Menampilkan {len(drugs)} obat kategori '{category}'")

        for drug in drugs:
            indication = drug['indication']
            if len(indication) > 50:
                indication = indication[:50] + "..."

            self.drugs_tree.insert(
                "",
                "end",
                values=(
                    drug['name'],
                    drug['category'],
                    drug['dosage'],
                    indication,
                    f"Rp {drug.get('price', 0):,}"
                )
            )

    def show_drug_detail(self):
        """Tampilkan dialog detail obat"""
        selected = self.drugs_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih obat terlebih dahulu!")
            return

        item = selected[0]
        values = self.drugs_tree.item(item)['values']
        drug_name = values[0]

        # Get drug detail
        drug = self.drug_manager.get_drug_by_name(drug_name)

        if drug:
            DrugDetailDialog(self, drug)

    def load_records(self):
        """Load rekam medis pasien ke tabel"""
        # Clear existing items
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        records = self.record_manager.get_patient_records(self.patient_data['id'])

        for record in records:
            self.records_tree.insert(
                "",
                "end",
                values=(
                    record.get('date', '-'),
                    record.get('diagnosis', '-'),
                    record.get('doctor', '-'),
                    record.get('medications', '-'),
                    record.get('notes', '-')
                )
            )

    def get_recommendation(self):
        """
        Dapatkan rekomendasi obat dengan algoritma kecocokan
        Mengambil gejala dari input dan kondisi medis dari checkbox
        """
        symptoms = self.symptom_input.get().strip()
        if not symptoms:
            messagebox.showwarning("Error", "Mohon masukkan gejala!")
            return

        # Ambil kondisi medis yang dicentang
        patient_conditions = []
        for condition, var in self.condition_vars.items():
            if var.get():
                # Split kondisi yang memiliki slash
                if '/' in condition:
                    patient_conditions.extend([c.strip().lower() for c in condition.split('/')])
                else:
                    patient_conditions.append(condition.lower())

        # Dapatkan rekomendasi dari drug recommender
        recommendations = self.recommender.recommend(symptoms, patient_conditions)

        # Format hasil menggunakan format_recommendation_text
        result_text = self.recommender.format_recommendation_text(symptoms, recommendations)

        # Tampilkan hasil
        self.prescription_text.delete("1.0", "end")
        self.prescription_text.insert("1.0", result_text)

    def logout(self):
        """Keluar dari aplikasi dan kembali ke login (fullscreen)"""
        from auth import AuthWindow
        self.destroy()

        # Buat window login baru dengan fullscreen
        auth_window = AuthWindow()
        auth_window.attributes('-fullscreen', True)
        # Bind ESC sudah ada di AuthWindow.__init__
        auth_window.mainloop()

    def toggle_fullscreen(self, event=None):
        """
        Toggle fullscreen mode
        Dipanggil saat tombol ESC ditekan
        """
        try:
            current = self.attributes('-fullscreen')
            self.attributes('-fullscreen', not current)
        except:
            pass  # Window sudah di-destroy, abaikan

    def toggle_fullscreen_auth(self, event=None):
        """Method untuk dipanggil dari auth window (alias)"""
        self.toggle_fullscreen(event)


class DrugDetailDialog(ctk.CTkToplevel):
    """
    Dialog untuk menampilkan detail obat
    Menampilkan informasi lengkap tentang obat
    """

    def __init__(self, parent, drug):
        """Constructor dialog detail obat"""
        super().__init__(parent)
        self.drug = drug
        self.init_ui()

    def init_ui(self):
        """Setup UI dialog detail"""
        self.title(f"Detail Obat - {self.drug['name']}")
        self.geometry("650x600")

        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (325)
        y = (self.winfo_screenheight() // 2) - (300)
        self.geometry(f'650x600+{x}+{y}')

        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title dengan nama obat
        title = ctk.CTkLabel(
            main_frame,
            text=f"💊 {self.drug['name']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))

        # Info utama obat
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=(0, 15))

        # Severity badge
        severity = self.drug.get('severity', 'low')
        severity_color = {
            'low': '#27ae60',
            'medium': '#f39c12',
            'high': '#e74c3c'
        }.get(severity, '#95a5a6')

        severity_text = {
            'low': '💚 Rendah',
            'medium': '💛 Sedang',
            'high': '❤️ Tinggi'
        }.get(severity, '⚪ Unknown')

        severity_label = ctk.CTkLabel(
            info_frame,
            text=f"Tingkat Keparahan: {severity_text}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=severity_color
        )
        severity_label.pack(pady=(10, 5))

        if self.drug.get('requires_prescription', False):
            rx_label = ctk.CTkLabel(
                info_frame,
                text="📝 Memerlukan Resep Dokter",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#e74c3c"
            )
            rx_label.pack(pady=(0, 10))

        # Info items
        info_items = [
            ("Kategori", self.drug['category']),
            ("Dosis", self.drug['dosage']),
            ("Indikasi", self.drug['indication']),
            ("Efek Samping", self.drug['side_effects']),
            ("Peringatan", self.drug['warnings']),
            ("Kontraindikasi", self.drug.get('contraindications', '-')),
            ("Harga", f"Rp {self.drug.get('price', 0):,}"),
        ]

        for label, value in info_items:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)

            label_widget = ctk.CTkLabel(
                row,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w",
                width=130
            )
            label_widget.pack(side="left")

            value_widget = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=12),
                anchor="w",
                wraplength=450
            )
            value_widget.pack(side="left", fill="x", expand=True)

        # Tags
        if 'tags' in self.drug and self.drug['tags']:
            tags_frame = ctk.CTkFrame(main_frame)
            tags_frame.pack(fill="x", pady=(0, 15))

            tags_label = ctk.CTkLabel(
                tags_frame,
                text="Tags:",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            tags_label.pack(anchor="w", padx=15, pady=(10, 5))

            tags_container = ctk.CTkFrame(tags_frame, fg_color="transparent")
            tags_container.pack(fill="x", padx=15, pady=(0, 10))

            for tag in self.drug['tags']:
                tag_label = ctk.CTkLabel(
                    tags_container,
                    text=f" #{tag}",
                    font=ctk.CTkFont(size=11),
                    text_color="#3498db"
                )
                tag_label.pack(side="left", padx=2)

        # Aliases
        if 'aliases' in self.drug and self.drug['aliases']:
            alias_frame = ctk.CTkFrame(main_frame)
            alias_frame.pack(fill="x", pady=(0, 15))

            alias_label = ctk.CTkLabel(
                alias_frame,
                text="Nama Lain/Aliases:",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            alias_label.pack(anchor="w", padx=15, pady=(10, 5))

            alias_value = ctk.CTkLabel(
                alias_frame,
                text=", ".join(self.drug['aliases']),
                font=ctk.CTkFont(size=12),
                wraplength=550
            )
            alias_value.pack(anchor="w", padx=15, pady=(0, 10))

        # Disclaimer wajib
        disclaimer_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray20"))
        disclaimer_frame.pack(fill="x", pady=(0, 15))

        disclaimer_text = (
            "⚠️ PERHATIAN: Informasi ini hanya untuk edukasi. "
            "Konsultasikan dengan dokter atau tenaga medis sebelum menggunakan obat."
        )
        disclaimer_label = ctk.CTkLabel(
            disclaimer_frame,
            text=disclaimer_text,
            font=ctk.CTkFont(size=11),
            wraplength=550
        )
        disclaimer_label.pack(padx=15, pady=10)

        # Tombol tutup
        close_btn = ctk.CTkButton(
            main_frame,
            text="Tutup",
            command=self.destroy,
            width=120,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        close_btn.pack(pady=(10, 0))

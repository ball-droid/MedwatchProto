"""
Modul UI Dokter
Dashboard untuk dokter
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from utils.json_helper import JSONHelper
from modules.patient_crud import PatientCRUD
from modules.doctor_crud import DoctorCRUD
from modules.medical_record import MedicalRecordManager
from modules.visualization import DiseaseTrendVisualizer
import os


class DokterDashboard(ctk.CTk):
    """Dashboard untuk dokter"""

    def __init__(self, doctor_name):
        super().__init__()
        self.doctor_name = doctor_name
        self.json_helper = JSONHelper()
        self.patient_crud = PatientCRUD()
        self.doctor_crud = DoctorCRUD()
        self.record_manager = MedicalRecordManager()
        self.visualizer = DiseaseTrendVisualizer()
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        self.title(f"MedWatch - Dokter: {self.doctor_name}")
        self.geometry("1300x800")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Bind ESC untuk keluar fullscreen
        self.bind("<Escape>", self.toggle_fullscreen)

        # Header
        header_frame = self.create_header()
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # Tabview
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Create tabs
        self.patients_tab = self.tab_view.add("Data Pasien")
        self.records_tab = self.tab_view.add("Rekam Medis")
        self.new_record_tab = self.tab_view.add("Tambah Rekam Medis")
        self.doctors_tab = self.tab_view.add("Kelola Dokter/Bidan")
        self.trends_tab = self.tab_view.add("Tren Penyakit")

        self.setup_patients_tab()
        self.setup_records_tab()
        self.setup_new_record_tab()
        self.setup_doctors_tab()
        self.setup_trends_tab()

        # Logout button
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
        """Buat header dashboard"""
        header_frame = ctk.CTkFrame(self, height=80)
        header_frame.grid_columnconfigure(1, weight=1)

        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text="👨‍⚕️",
            font=ctk.CTkFont(size=40)
        )
        icon_label.grid(row=0, column=0, padx=20, pady=15)

        # Info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=10)

        title_label = ctk.CTkLabel(
            info_frame,
            text="Dashboard Dokter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(anchor="w")

        name_label = ctk.CTkLabel(
            info_frame,
            text=f"Dokter: {self.doctor_name}",
            font=ctk.CTkFont(size=14)
        )
        name_label.pack(anchor="w")

        return header_frame

    def setup_patients_tab(self):
        """Setup tab data pasien dengan fitur pencarian nama pasien"""
        main_frame = ctk.CTkFrame(self.patients_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ========================
        # FITUR PENCARIAN PASIEN
        # ========================
        # Frame pencarian pasien - memungkinkan dokter mencari pasien
        # berdasarkan nama, ID, atau informasi lainnya dengan cepat
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=(10, 15))

        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Cari Pasien:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(anchor="w", padx=15, pady=(10, 5))

        search_input_row = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_row.pack(fill="x", padx=15, pady=(0, 10))

        # Input field untuk kata kunci pencarian
        self.patient_search_entry = ctk.CTkEntry(
            search_input_row,
            placeholder_text="Masukkan nama pasien, telepon, atau golongan darah..."
        )
        self.patient_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind Enter key untuk langsung mencari
        self.patient_search_entry.bind("<Return>", lambda e: self.search_patients())

        # Tombol untuk melakukan pencarian pasien
        search_btn = ctk.CTkButton(
            search_input_row,
            text="Cari",
            command=self.search_patients,
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=(0, 10))

        # Tombol untuk reset pencarian dan menampilkan semua pasien
        reset_btn = ctk.CTkButton(
            search_input_row,
            text="Reset",
            command=self.load_patients,
            width=100,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        reset_btn.pack(side="left")

        # Label untuk menampilkan jumlah hasil pencarian
        self.patient_search_count_label = ctk.CTkLabel(
            search_frame,
            text="Menampilkan semua pasien",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.patient_search_count_label.pack(anchor="w", padx=15, pady=(0, 10))
        # ========================

        # Button frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(10, 15))

        add_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Tambah Pasien",
            command=self.add_patient,
            width=140,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        add_btn.pack(side="left", padx=(0, 10))

        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Edit Pasien",
            command=self.edit_patient,
            width=140,
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        edit_btn.pack(side="left", padx=(0, 10))

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus Pasien",
            command=self.delete_patient,
            width=140,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        delete_btn.pack(side="left", padx=(0, 10))

        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self.load_patients,
            width=120
        )
        refresh_btn.pack(side="right")

        # Table frame
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=('Segoe UI', 11))
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))

        self.patients_tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Nama", "Tgl Lahir", "Umur", "JK", "Telepon", "Gol. Darah"),
            show="headings",
            height=15
        )

        self.patients_tree.heading("ID", text="ID")
        self.patients_tree.heading("Nama", text="Nama Lengkap")
        self.patients_tree.heading("Tgl Lahir", text="Tanggal Lahir")
        self.patients_tree.heading("Umur", text="Umur")
        self.patients_tree.heading("JK", text="Jenis Kelamin")
        self.patients_tree.heading("Telepon", text="No. Telepon")
        self.patients_tree.heading("Gol. Darah", text="Gol. Darah")

        self.patients_tree.column("ID", width=60, anchor="center")
        self.patients_tree.column("Nama", width=220)
        self.patients_tree.column("Tgl Lahir", width=120, anchor="center")
        self.patients_tree.column("Umur", width=60, anchor="center")
        self.patients_tree.column("JK", width=120, anchor="center")
        self.patients_tree.column("Telepon", width=150)
        self.patients_tree.column("Gol. Darah", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)

        self.patients_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_patients()

    def setup_records_tab(self):
        """
        Setup tab rekam medis dengan fitur pencarian

        PENTING - SISTEM ID UNIK:
        ========================
        Setiap pasien memiliki ID unik yang tidak mungkin sama.
        ID unik ini mencegah tertukarnya informasi dan rekam medis
        antar pasien yang memiliki nama sama.

        Contoh:
        - Pasien "Budi Santoso" dengan ID 1
        - Pasien "Budi Santoso" dengan ID 2
        -> Meskipun nama sama, rekam medis mereka TIDAK akan tertukar
           karena sistem menggunakan ID unik, bukan nama.
        """
        main_frame = ctk.CTkFrame(self.records_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ========================
        # FITUR PENCARIAN REKAM MEDIS
        # ========================
        # Frame pencarian rekam medis - memungkinkan dokter mencari
        # rekam medis pasien berdasarkan berbagai kriteria dengan cepat
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=(10, 15))

        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Cari Rekam Medis:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(anchor="w", padx=15, pady=(10, 5))

        search_input_row = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_row.pack(fill="x", padx=15, pady=(0, 10))

        # Input field untuk kata kunci pencarian rekam medis
        self.record_search_entry = ctk.CTkEntry(
            search_input_row,
            placeholder_text="Cari nama pasien, diagnosis, dokter, atau obat..."
        )
        self.record_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Bind Enter key untuk langsung mencari
        self.record_search_entry.bind("<Return>", lambda e: self.search_records())

        # Tombol untuk melakukan pencarian rekam medis
        search_btn = ctk.CTkButton(
            search_input_row,
            text="Cari",
            command=self.search_records,
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        search_btn.pack(side="left", padx=(0, 10))

        # Tombol untuk reset pencarian dan menampilkan semua rekam medis
        reset_btn = ctk.CTkButton(
            search_input_row,
            text="Reset",
            command=lambda: self.load_records(None),
            width=100,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        reset_btn.pack(side="left")

        # Label untuk menampilkan jumlah hasil pencarian
        self.record_search_count_label = ctk.CTkLabel(
            search_frame,
            text="Menampilkan semua rekam medis",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.record_search_count_label.pack(anchor="w", padx=15, pady=(0, 10))
        # ========================

        # Filter frame
        filter_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=10, pady=(10, 15))

        filter_label = ctk.CTkLabel(filter_frame, text="Filter berdasarkan Pasien:")
        filter_label.pack(side="left", padx=(0, 10))

        self.patient_filter_values = ["Semua Pasien"]
        patients = self.json_helper.load_patients()
        self.patient_filter_ids = [None]
        for patient in patients:
            self.patient_filter_values.append(f"{patient['name']} (ID: {patient['id']})")
            self.patient_filter_ids.append(patient['id'])

        self.patient_filter_combo = ctk.CTkOptionMenu(
            filter_frame,
            values=self.patient_filter_values,
            command=self.load_records
        )
        self.patient_filter_combo.set("Semua Pasien")
        self.patient_filter_combo.pack(side="left", padx=(0, 10))

        refresh_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            command=lambda: self.load_records(None),
            width=120
        )
        refresh_btn.pack(side="right")

        # Table frame
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=('Segoe UI', 11))
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))

        self.records_tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Tanggal", "Pasien", "Diagnosis", "Obat", "Dokter"),
            show="headings",
            height=15
        )

        self.records_tree.heading("ID", text="ID")
        self.records_tree.heading("Tanggal", text="Tanggal")
        self.records_tree.heading("Pasien", text="Nama Pasien")
        self.records_tree.heading("Diagnosis", text="Diagnosis")
        self.records_tree.heading("Obat", text="Obat")
        self.records_tree.heading("Dokter", text="Dokter")

        self.records_tree.column("ID", width=60, anchor="center")
        self.records_tree.column("Tanggal", width=120, anchor="center")
        self.records_tree.column("Pasien", width=200)
        self.records_tree.column("Diagnosis", width=200)
        self.records_tree.column("Obat", width=200)
        self.records_tree.column("Dokter", width=180)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        self.records_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_records(None)

    def setup_new_record_tab(self):
        """Setup tab tambah rekam medis"""
        scroll_frame = ctk.CTkScrollableFrame(self.new_record_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text="Form Rekam Medis Baru",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))

        # Form container
        form_frame = ctk.CTkFrame(scroll_frame)
        form_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Patient selection
        patient_label = ctk.CTkLabel(form_frame, text="Pasien:", font=ctk.CTkFont(size=14, weight="bold"))
        patient_label.pack(anchor="w", padx=20, pady=(15, 5))

        self.record_patient_names = []
        patients = self.json_helper.load_patients()
        for patient in patients:
            self.record_patient_names.append(f"{patient['name']} (ID: {patient['id']})")

        self.record_patient_combo = ctk.CTkOptionMenu(form_frame, values=self.record_patient_names)
        if self.record_patient_names:
            self.record_patient_combo.set(self.record_patient_names[0])
        self.record_patient_combo.pack(fill="x", padx=20, pady=(0, 15))

        # Date
        date_label = ctk.CTkLabel(form_frame, text="Tanggal:", font=ctk.CTkFont(size=14, weight="bold"))
        date_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.record_date_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD")
        today = datetime.now().strftime("%Y-%m-%d")
        self.record_date_entry.insert(0, today)
        self.record_date_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Diagnosis
        diagnosis_label = ctk.CTkLabel(form_frame, text="Diagnosis:", font=ctk.CTkFont(size=14, weight="bold"))
        diagnosis_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.record_diagnosis = ctk.CTkEntry(form_frame, placeholder_text="Masukkan diagnosis")
        self.record_diagnosis.pack(fill="x", padx=20, pady=(0, 15))

        # Medications
        med_label = ctk.CTkLabel(form_frame, text="Obat-obatan:", font=ctk.CTkFont(size=14, weight="bold"))
        med_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.record_medications = ctk.CTkEntry(
            form_frame,
            placeholder_text="Contoh: Paracetamol 500mg, Amoxicillin 500mg"
        )
        self.record_medications.pack(fill="x", padx=20, pady=(0, 15))

        # Notes
        notes_label = ctk.CTkLabel(form_frame, text="Catatan:", font=ctk.CTkFont(size=14, weight="bold"))
        notes_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.record_notes = ctk.CTkTextbox(form_frame, height=100)
        self.record_notes.pack(fill="x", padx=20, pady=(0, 20))

        # Save button
        save_btn = ctk.CTkButton(
            form_frame,
            text="💾 Simpan Rekam Medis",
            command=self.save_medical_record,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27ae60",
            hover_color="#229954"
        )
        save_btn.pack(fill="x", padx=20, pady=(10, 20))

    def setup_trends_tab(self):
        """Setup tab tren penyakit dengan fitur download"""
        scroll_frame = ctk.CTkScrollableFrame(self.trends_tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            scroll_frame,
            text="📊 Tren Penyakit Pasien",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))

        # Info card
        info_card = ctk.CTkFrame(scroll_frame, fg_color=("gray85", "gray25"))
        info_card.pack(fill="x", padx=20, pady=(0, 15))

        info_label = ctk.CTkLabel(
            info_card,
            text="💡 Tampilkan grafik dan download laporan untuk keperluan cetak/dokumentasi.",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=15, pady=10)

        # Button frame - Chart buttons
        chart_btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        chart_btn_frame.pack(fill="x", padx=20, pady=(0, 10))

        chart_btn = ctk.CTkButton(
            chart_btn_frame,
            text="📊 Tampilkan Grafik (Preview)",
            command=self.show_trend_chart,
            height=40,
            width=200,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        chart_btn.pack(side="left", padx=(0, 10))

        # Download buttons frame
        download_frame = ctk.CTkFrame(scroll_frame)
        download_frame.pack(fill="x", padx=20, pady=(0, 20))

        download_label = ctk.CTkLabel(
            download_frame,
            text="📥 Download Laporan:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        download_label.pack(anchor="w", padx=15, pady=(10, 10))

        buttons_row = ctk.CTkFrame(download_frame, fg_color="transparent")
        buttons_row.pack(fill="x", padx=15, pady=(0, 15))

        # Download PNG (Grafik)
        png_btn = ctk.CTkButton(
            buttons_row,
            text="🖼️ PNG (Grafik)",
            command=self.download_png_chart,
            width=150,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        png_btn.pack(side="left", padx=(0, 10))

        # Download PDF
        pdf_btn = ctk.CTkButton(
            buttons_row,
            text="📄 PDF (Laporan)",
            command=self.download_pdf_report,
            width=150,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        pdf_btn.pack(side="left", padx=(0, 10))

        # Download TXT
        txt_btn = ctk.CTkButton(
            buttons_row,
            text="📝 TXT (Teks)",
            command=self.download_text_report,
            width=150,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        txt_btn.pack(side="left")

        # Status label
        self.download_status = ctk.CTkLabel(
            download_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.download_status.pack(anchor="w", padx=15, pady=(0, 10))

        # Statistics frame
        stats_frame = ctk.CTkFrame(scroll_frame)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📈 Statistik Penyakit",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_title.pack(pady=(15, 10))

        self.trends_text = ctk.CTkTextbox(stats_frame, height=300)
        self.trends_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.update_trends_stats()

    def setup_doctors_tab(self):
        """
        Setup tab kelola dokter/bidan

        FITUR:
        =======
        - Tambah dokter/bidan baru
        - Edit data dokter/bidan
        - Hapus dokter/bidan
        - Auto-generate username & password (sama format seperti pasien)
        """
        main_frame = ctk.CTkFrame(self.doctors_tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Info card
        info_card = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray25"))
        info_card.pack(fill="x", padx=10, pady=(10, 15))

        info_text = (
            "💡 Kelola Dokter & Bidan: Username & Password akan di-generate otomatis "
            "dengan format Nama lengkap (boleh ada spasi) + 4 digit terakhir no. HP"
        )
        info_label = ctk.CTkLabel(
            info_card,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=15, pady=10)

        # Button frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(10, 15))

        add_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Tambah Dokter/Bidan",
            command=self.add_doctor,
            width=180,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        add_btn.pack(side="left", padx=(0, 10))

        edit_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Edit Data",
            command=self.edit_doctor,
            width=140,
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        edit_btn.pack(side="left", padx=(0, 10))

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Hapus",
            command=self.delete_doctor,
            width=140,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        delete_btn.pack(side="left", padx=(0, 10))

        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self.load_doctors,
            width=120
        )
        refresh_btn.pack(side="right")

        # Table frame
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Create treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=('Segoe UI', 11))
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))

        self.doctors_tree = ttk.Treeview(
            table_frame,
            columns=("Username", "Nama", "Role", "Spesialis", "Telepon"),
            show="headings",
            height=15
        )

        self.doctors_tree.heading("Username", text="Username")
        self.doctors_tree.heading("Nama", text="Nama Lengkap")
        self.doctors_tree.heading("Role", text="Role")
        self.doctors_tree.heading("Spesialis", text="Spesialisasi")
        self.doctors_tree.heading("Telepon", text="No. Telepon")

        self.doctors_tree.column("Username", width=200)
        self.doctors_tree.column("Nama", width=250)
        self.doctors_tree.column("Role", width=120, anchor="center")
        self.doctors_tree.column("Spesialis", width=200)
        self.doctors_tree.column("Telepon", width=180)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.doctors_tree.yview)
        self.doctors_tree.configure(yscrollcommand=scrollbar.set)

        self.doctors_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_doctors()

    def load_doctors(self):
        """Load data dokter/bidan ke tabel"""
        # Clear existing
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)

        doctors = self.doctor_crud.get_all_doctors()

        for doctor in doctors:
            self.doctors_tree.insert(
                "",
                "end",
                values=(
                    doctor['username'],
                    doctor['name'],
                    doctor['role'].capitalize(),
                    doctor.get('specialization', 'Umum'),
                    doctor.get('phone', '-')
                )
            )

    def add_doctor(self):
        """Buka dialog tambah dokter/bidan"""
        DoctorDialog(self)
        self.load_doctors()

    def edit_doctor(self):
        """Buka dialog edit dokter/bidan"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih dokter/bidan terlebih dahulu!")
            return

        item = selected[0]
        values = self.doctors_tree.item(item)['values']
        username = values[0]

        DoctorDialog(self, username)
        self.load_doctors()

    def delete_doctor(self):
        """Hapus dokter/bidan yang dipilih"""
        selected = self.doctors_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih dokter/bidan terlebih dahulu!")
            return

        item = selected[0]
        values = self.doctors_tree.item(item)['values']
        username = values[0]
        doctor_name = values[1]

        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus {doctor_name}?\n\n"
            f"⚠️ Rekam medis yang dibuat oleh dokter ini TIDAK akan dihapus."
        )

        if confirm:
            self.doctor_crud.delete_doctor(username)
            self.load_doctors()
            messagebox.showinfo("Sukses", f"{doctor_name} berhasil dihapus!")

    def load_patients(self):
        """Load data pasien ke tabel"""
        # Clear existing
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        patients = self.patient_crud.get_all_patients()

        # Update label jumlah pasien
        self.patient_search_count_label.configure(text=f"Menampilkan {len(patients)} pasien")

        for patient in patients:
            # Tampilkan tanggal lahir atau '-' jika tidak ada
            birth_date = patient.get('birth_date', '-')

            self.patients_tree.insert(
                "",
                "end",
                values=(
                    patient['id'],
                    patient['name'],
                    birth_date,
                    patient['age'],
                    patient['gender'],
                    patient['phone'],
                    patient['blood_type']
                )
            )

    def search_patients(self):
        """
        Cari pasien berdasarkan kata kunci dengan konsep TOLOWER (case-insensitive)

        ========================================
        KONSEP TOLOWER (CASE-INSENSITIVE):
        ========================================
        Semua huruf akan diubah menjadi lowercase sebelum dibandingkan,
        sehingga pencarian tidak terpengaruh oleh besar/kecilnya huruf.

        Contoh:
        - "Budi" = "budi" = "BUDI" = "BuDi" (semuanya akan ditemukan)
        - "AHMAD" akan menemukan "Ahmad", "ahmad", "AHMAD"

        Mencari pasien berdasarkan:
        - Nama pasien (prioritas utama)
        - Nomor telepon
        - Golongan darah

        Args:
            None (mengambil input dari self.patient_search_entry)

        Returns:
            None (hasil langsung ditampilkan ke tabel pasien)
        """
        # Ambil kata kunci pencarian dari input field
        keyword = self.patient_search_entry.get().strip()

        # Jika kata kunci kosong, tampilkan semua pasien
        if not keyword:
            self.load_patients()
            return

        # Clear existing items di tabel
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)

        # Load semua pasien untuk pencarian
        all_patients = self.patient_crud.get_all_patients()

        # ========================================
        # IMPLEMENTASI KONSEP TOLOWER:
        # ========================================
        # 1. Konversi keyword ke lowercase
        # 2. Setiap field pasien juga dikonversi ke lowercase saat dibandingkan
        # 3. Ini memastikan pencarian case-insensitive
        keyword_lower = keyword.lower()  # Konversi keyword ke lowercase
        filtered_patients = []

        for patient in all_patients:
            # Cek kecocokan di berbagai field dengan konsep TOLOWER
            # ========================================
            # FIELD 1: Nama Pasien (Prioritas Utama)
            # ========================================
            # patient['name'].lower() - konversi nama pasien ke lowercase
            # keyword_lower in ... - cek apakah keyword ada dalam nama
            if keyword_lower in patient['name'].lower():
                filtered_patients.append(patient)

            # ========================================
            # FIELD 2: Nomor Telepon
            # ========================================
            # patient['phone'].lower() - konversi nomor telepon ke lowercase
            elif keyword_lower in patient['phone'].lower():
                filtered_patients.append(patient)

            # ========================================
            # FIELD 3: Golongan Darah
            # ========================================
            # patient['blood_type'].lower() - konversi golongan darah ke lowercase
            elif keyword_lower in patient['blood_type'].lower():
                filtered_patients.append(patient)

        # Update label jumlah hasil pencarian
        self.patient_search_count_label.configure(
            text=f"Ditemukan {len(filtered_patients)} pasien untuk '{keyword}'"
        )

        # Tampilkan hasil pencarian ke tabel
        for patient in filtered_patients:
            # Tampilkan tanggal lahir atau '-' jika tidak ada
            birth_date = patient.get('birth_date', '-')

            self.patients_tree.insert(
                "",
                "end",
                values=(
                    patient['id'],
                    patient['name'],
                    birth_date,
                    patient['age'],
                    patient['gender'],
                    patient['phone'],
                    patient['blood_type']
                )
            )

    def load_records(self, value):
        """Load rekam medis ke tabel"""
        # Clear existing
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        # Get selected patient
        selected = self.patient_filter_combo.get()
        idx = self.patient_filter_values.index(selected) if selected in self.patient_filter_values else 0
        patient_id = self.patient_filter_ids[idx]

        if patient_id:
            records = self.record_manager.get_patient_records(patient_id)
        else:
            records = self.record_manager.get_all_records()

        for record in records:
            self.records_tree.insert(
                "",
                "end",
                values=(
                    record['id'],
                    record['date'],
                    record['patient_name'],
                    record['diagnosis'],
                    record['medications'],
                    record['doctor']
                )
            )

        # Update label jumlah rekam medis
        self.record_search_count_label.configure(text=f"Menampilkan {len(records)} rekam medis")

    def search_records(self):
        """
        Cari rekam medis berdasarkan kata kunci dengan konsep TOLOWER (case-insensitive)

        ========================================
        KONSEP TOLOWER (CASE-INSENSITIVE):
        ========================================
        Semua huruf akan diubah menjadi lowercase sebelum dibandingkan,
        sehingga pencarian tidak terpengaruh oleh besar/kecilnya huruf.

        Contoh:
        - "demam" = "Demam" = "DEMAM" = "DeMaM" (semuanya akan ditemukan)
        - "dr. ahmad" akan menemukan "Dr. Ahmad", "dr. AHMAD"

        Mencari rekam medis berdasarkan:
        - Nama pasien (prioritas utama)
        - Diagnosis/penyakit
        - Nama dokter
        - Obat-obatan

        Catatan:
        Sistem menggunakan ID unik pasien untuk mencegah tertukarnya
        rekam medis antar pasien yang memiliki nama sama.

        Args:
            None (mengambil input dari self.record_search_entry)

        Returns:
            None (hasil langsung ditampilkan ke tabel rekam medis)
        """
        # Ambil kata kunci pencarian dari input field
        keyword = self.record_search_entry.get().strip()

        # Jika kata kunci kosong, tampilkan semua rekam medis
        if not keyword:
            self.load_records(None)
            return

        # Clear existing items di tabel
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        # Load semua rekam medis untuk pencarian
        all_records = self.record_manager.get_all_records()

        # ========================================
        # IMPLEMENTASI KONSEP TOLOWER:
        # ========================================
        # 1. Konversi keyword ke lowercase
        # 2. Setiap field rekam medis juga dikonversi ke lowercase saat dibandingkan
        # 3. Ini memastikan pencarian case-insensitive
        keyword_lower = keyword.lower()  # Konversi keyword ke lowercase
        filtered_records = []

        for record in all_records:
            # Cek kecocokan di berbagai field dengan konsep TOLOWER
            # ========================================
            # FIELD 1: Nama Pasien (Prioritas Utama)
            # ========================================
            # record['patient_name'].lower() - konversi nama pasien ke lowercase
            # keyword_lower in ... - cek apakah keyword ada dalam nama
            if keyword_lower in record['patient_name'].lower():
                filtered_records.append(record)

            # ========================================
            # FIELD 2: Diagnosis/Penyakit
            # ========================================
            # record['diagnosis'].lower() - konversi diagnosis ke lowercase
            elif keyword_lower in record['diagnosis'].lower():
                filtered_records.append(record)

            # ========================================
            # FIELD 3: Nama Dokter
            # ========================================
            # record['doctor'].lower() - konversi nama dokter ke lowercase
            elif keyword_lower in record['doctor'].lower():
                filtered_records.append(record)

            # ========================================
            # FIELD 4: Obat-obatan
            # ========================================
            # record['medications'].lower() - konversi obat ke lowercase
            elif keyword_lower in record['medications'].lower():
                filtered_records.append(record)

        # Update label jumlah hasil pencarian
        self.record_search_count_label.configure(
            text=f"Ditemukan {len(filtered_records)} rekam medis untuk '{keyword}'"
        )

        # Tampilkan hasil pencarian ke tabel
        for record in filtered_records:
            self.records_tree.insert(
                "",
                "end",
                values=(
                    record['id'],
                    record['date'],
                    record['patient_name'],
                    record['diagnosis'],
                    record['medications'],
                    record['doctor']
                )
            )

    def add_patient(self):
        """Buka dialog tambah pasien"""
        PatientDialog(self)
        self.load_patients()

    def edit_patient(self):
        """Buka dialog edit pasien"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih pasien terlebih dahulu!")
            return

        item = selected[0]
        values = self.patients_tree.item(item)['values']
        patient_id = int(values[0])

        PatientDialog(self, patient_id)
        self.load_patients()

    def delete_patient(self):
        """Hapus pasien yang dipilih"""
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih pasien terlebih dahulu!")
            return

        item = selected[0]
        values = self.patients_tree.item(item)['values']
        patient_id = int(values[0])
        patient_name = values[1]

        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Apakah Anda yakin ingin menghapus pasien {patient_name}?"
        )

        if confirm:
            self.patient_crud.delete_patient(patient_id)
            self.load_patients()
            messagebox.showinfo("Sukses", "Pasien berhasil dihapus!")

    def save_medical_record(self):
        """Simpan rekam medis baru"""
        # Get patient ID from selected name
        selected_patient = self.record_patient_combo.get()
        patient_id = None
        for p in self.json_helper.load_patients():
            if f"{p['name']} (ID: {p['id']})" == selected_patient:
                patient_id = p['id']
                break

        if not patient_id:
            messagebox.showerror("Error", "Pasien tidak valid!")
            return

        date = self.record_date_entry.get().strip()
        diagnosis = self.record_diagnosis.get().strip()
        medications = self.record_medications.get().strip()
        notes = self.record_notes.get("1.0", "end").strip()

        if not diagnosis:
            messagebox.showwarning("Error", "Diagnosis harus diisi!")
            return

        self.record_manager.create_record({
            'patient_id': patient_id,
            'date': date,
            'diagnosis': diagnosis,
            'medications': medications,
            'notes': notes,
            'doctor': self.doctor_name
        })

        messagebox.showinfo("Sukses", "Rekam medis berhasil disimpan!")

        # Clear form
        self.record_diagnosis.delete(0, "end")
        self.record_medications.delete(0, "end")
        self.record_notes.delete("1.0", "end")

    def show_trend_chart(self):
        """Tampilkan grafik tren penyakit"""
        self.visualizer.show_trend_chart()

    def update_trends_stats(self):
        """Update statistik tren"""
        stats = self.visualizer.get_statistics()

        text = "Statistik Penyakit:\n\n"
        for disease, count in stats.items():
            text += f"• {disease}: {count} kasus\n"

        self.trends_text.delete("1.0", "end")
        self.trends_text.insert("1.0", text)

    def download_png_chart(self):
        """
        Download grafik sebagai file PNG
        File disimpan di folder exports/
        """
        try:
            # Buat grafik dan simpan
            file_path = self.visualizer.create_disease_chart()

            if file_path:
                self.download_status.configure(
                    text=f"✅ Grafik tersimpan: {os.path.basename(file_path)}",
                    text_color="#27ae60"
                )
                messagebox.showinfo(
                    "Sukses",
                    f"Grafik berhasil disimpan!\n\n"
                    f"Lokasi: {file_path}\n\n"
                    f"File dapat dibuka dan dicetak menggunakan aplikasi image viewer."
                )
            else:
                self.download_status.configure(
                    text="❌ Gagal: Matplotlib tidak tersedia",
                    text_color="#e74c3c"
                )
                messagebox.showerror(
                    "Error",
                    "Gagal membuat grafik. Pastikan matplotlib sudah terinstall."
                )
        except Exception as e:
            self.download_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color="#e74c3c"
            )
            messagebox.showerror("Error", f"Gagal membuat grafik: {str(e)}")

    def download_pdf_report(self):
        """
        Download laporan sebagai file PDF
        File disimpan di folder exports/
        """
        try:
            # Buat PDF
            file_path = self.visualizer.export_to_pdf()

            if file_path:
                self.download_status.configure(
                    text=f"✅ PDF tersimpan: {os.path.basename(file_path)}",
                    text_color="#27ae60"
                )
                messagebox.showinfo(
                    "Sukses",
                    f"Laporan PDF berhasil dibuat!\n\n"
                    f"Lokasi: {file_path}\n\n"
                    f"File dapat dibuka dan dicetak menggunakan PDF reader."
                )
            else:
                self.download_status.configure(
                    text="❌ Gagal: Reportlab tidak tersedia",
                    text_color="#e74c3c"
                )
                messagebox.showerror(
                    "Error",
                    "Gagal membuat PDF. Pastikan reportlab sudah terinstall.\n"
                    "Install: pip install reportlab"
                )
        except Exception as e:
            self.download_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color="#e74c3c"
            )
            messagebox.showerror("Error", f"Gagal membuat PDF: {str(e)}")

    def download_text_report(self):
        """
        Download laporan sebagai file TXT
        File disimpan di folder exports/
        """
        try:
            # Buat nama file dengan timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = os.path.join(
                self.visualizer.export_folder,
                f'laporan_kesehatan_{timestamp}.txt'
            )

            # Generate dan simpan laporan
            self.visualizer.generate_report_text(save_path=file_path)

            self.download_status.configure(
                text=f"✅ TXT tersimpan: {os.path.basename(file_path)}",
                text_color="#27ae60"
            )
            messagebox.showinfo(
                "Sukses",
                f"Laporan teks berhasil dibuat!\n\n"
                f"Lokasi: {file_path}\n\n"
                f"File dapat dibuka dengan Notepad/Text editor."
            )
        except Exception as e:
            self.download_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color="#e74c3c"
            )
            messagebox.showerror("Error", f"Gagal membuat laporan: {str(e)}")

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


class PatientDialog(ctk.CTkToplevel):
    """
    Dialog untuk tambah/edit pasien

    Dialog ini bersifat MODAL - akan muncul di depan window utama
    dan user harus menyelesaikan input di dialog ini terlebih dahulu
    sebelum bisa berinteraksi dengan window utama kembali.
    """

    def __init__(self, parent, patient_id=None):
        super().__init__(parent)

        # ========================================
        # MODAL DIALOG BEHAVIOR
        # ========================================
        # Membuat dialog menjadi modal window:
        # 1. transient() - membuat dialog menjadi child window
        # 2. grab_set() - grab semua input event
        # 3. lift() - bawa dialog ke paling depan
        # 4. focus_set() - set focus ke dialog
        self.transient(parent)  # Jadikan dialog sebagai child window
        self.grab_set()  # Grab input event - user harus interaksi dengan dialog ini dulu

        self.patient_id = patient_id
        self.parent = parent  # Simpan reference ke parent window
        self.json_helper = JSONHelper()
        self.patient_crud = PatientCRUD()
        self.init_ui()
        if patient_id:
            self.load_patient_data()

        # Bawa dialog ke paling depan dan set focus
        self.lift()  # Bawa ke depan (z-order tertinggi)
        self.focus_set()  # Set focus ke dialog
        self.after(100, self._focus_dialog)  # Pastikan dialog benar-benar di depan

    def _focus_dialog(self):
        """Helper untuk memastikan dialog mendapat focus dan muncul di depan"""
        try:
            self.lift()  # Bawa ke paling depan
            self.focus_force()  # Force focus ke dialog
            self.attributes('-topmost', True)  # Set sebagai topmost window
            self.after(100, lambda: self.attributes('-topmost', False))  # Disable topmost setelah 100ms
        except:
            pass  # Dialog sudah di-destroy, abaikan

    def init_ui(self):
        """
        Inisialisasi UI dialog tambah/edit pasien

        CATATAN - AUTO-GENERATE USERNAME & PASSWORD:
        ===============================================
        Untuk pasien BARU, username dan password akan di-generate OTOMATIS:
        - Username: Nama pasien (lowercase, tanpa spasi)
        - Password: Nama + 4 digit terakhir nomor telepon

        Contoh:
        - Nama: "Budi Santoso", Telepon: "081234564383"
        - Username: "budisantoso"
        - Password: "budi4383"
        """
        title = "Edit Pasien" if self.patient_id else "Tambah Pasien Baru"
        self.title(title)
        self.geometry("500x650")

        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (250)
        y = (self.winfo_screenheight() // 2) - (325)
        self.geometry(f'500x650+{x}+{y}')

        # Main frame
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Info card untuk pasien baru tentang auto-generate username & password
        if not self.patient_id:
            info_card = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray25"))
            info_card.pack(fill="x", pady=(0, 15))

            info_text = (
                "💡 Username & Password akan di-generate otomatis:\n"
                "   • Username: Nama pasien (boleh ada spasi & uppercase)\n"
                "   • Password: Nama (lowercase) + 4 digit terakhir no. HP\n"
                "   • Umur dihitung otomatis dari tanggal lahir\n"
                "   Contoh: Budi Santoso + 08123456**4383** =\n"
                "     Username: Budi Santoso\n"
                "     Password: budi4383"
            )
            info_label = ctk.CTkLabel(
                info_card,
                text=info_text,
                font=ctk.CTkFont(size=11),
                justify="left"
            )
            info_label.pack(padx=15, pady=10)

        # Form fields
        self.name_entry = self.create_form_entry(main_frame, "Nama Lengkap:", "")

        # Tanggal lahir field
        birth_date_label = ctk.CTkLabel(main_frame, text="Tanggal Lahir:", font=ctk.CTkFont(size=13, weight="bold"))
        birth_date_label.pack(anchor="w", pady=(10, 5))

        self.birth_date_entry = ctk.CTkEntry(main_frame, placeholder_text="dd/mm/yyyy (contoh: 15/05/1990)")
        self.birth_date_entry.pack(fill="x", pady=(0, 15))

        # Info umur otomatis
        age_info_label = ctk.CTkLabel(
            main_frame,
            text="ℹ️ Umur akan dihitung otomatis dari tanggal lahir",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        age_info_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.phone_entry = self.create_form_entry(main_frame, "No. Telepon:", "08xxxxxxxxxx")

        # Gender
        gender_label = ctk.CTkLabel(main_frame, text="Jenis Kelamin:", font=ctk.CTkFont(size=13, weight="bold"))
        gender_label.pack(anchor="w", pady=(10, 5))
        self.gender_combo = ctk.CTkOptionMenu(main_frame, values=["Laki-laki", "Perempuan"])
        self.gender_combo.set("Laki-laki")
        self.gender_combo.pack(fill="x", pady=(0, 15))

        # Blood type
        blood_label = ctk.CTkLabel(main_frame, text="Golongan Darah:", font=ctk.CTkFont(size=13, weight="bold"))
        blood_label.pack(anchor="w", pady=(10, 5))

        blood_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        blood_frame.pack(fill="x", pady=(0, 15))

        self.blood_combo = ctk.CTkOptionMenu(blood_frame, values=["A", "B", "AB", "O"], width=100)
        self.blood_combo.set("A")
        self.blood_combo.pack(side="left", padx=(0, 10))

        self.rhesus_combo = ctk.CTkOptionMenu(blood_frame, values=["+", "-"], width=100)
        self.rhesus_combo.set("+")
        self.rhesus_combo.pack(side="left")

        # Address
        addr_label = ctk.CTkLabel(main_frame, text="Alamat:", font=ctk.CTkFont(size=13, weight="bold"))
        addr_label.pack(anchor="w", pady=(10, 5))
        self.address_text = ctk.CTkTextbox(main_frame, height=80)
        self.address_text.pack(fill="x", pady=(0, 15))

        # Username & Password - Hanya untuk edit pasien yang sudah ada
        if self.patient_id:
            # Username & Password fields hanya untuk edit
            self.username_entry = self.create_form_entry(main_frame, "Username:", "")
            self.password_entry = self.create_form_entry(main_frame, "Password:", "", show="*")
        else:
            # Untuk pasien baru, simpan referensi untuk generated credentials
            self.generated_username = None
            self.generated_password = None

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Batal",
            command=self.destroy,
            width=100,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Simpan",
            command=self.save_patient,
            width=100,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        save_btn.pack(side="right")

    def create_form_entry(self, parent, label, placeholder, show=None):
        """Helper untuk membuat form entry"""
        label_widget = ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=13, weight="bold"))
        label_widget.pack(anchor="w", pady=(10, 5))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, show=show)
        entry.pack(fill="x", pady=(0, 5))
        return entry

    def load_patient_data(self):
        """Load data pasien untuk edit"""
        patient = self.patient_crud.get_patient_by_id(self.patient_id)
        if patient:
            self.name_entry.insert(0, patient['name'])
            # Load tanggal lahir jika ada
            if 'birth_date' in patient and patient['birth_date']:
                self.birth_date_entry.insert(0, patient['birth_date'])
            self.phone_entry.insert(0, patient['phone'])
            self.gender_combo.set(patient['gender'])

            blood = patient['blood_type']
            if len(blood) > 1:
                self.blood_combo.set(blood[0])
                self.rhesus_combo.set(blood[1])

            self.address_text.insert("1.0", patient.get('address', ''))
            # Username & password hanya untuk edit, bukan create baru
            if hasattr(self, 'username_entry'):
                self.username_entry.insert(0, patient['username'])

    def save_patient(self):
        """
        Simpan data pasien (create atau update)

        CATATAN - AUTO-GENERATE CREDENTIALS & UMUR OTOMATIS:
        =====================================================
        Untuk pasien BARU (self.patient_id is None):
        - Username dan password akan di-generate OTOMATIS oleh PatientCRUD
        - Umur dihitung otomatis dari tanggal lahir
        - Format: Username = nama (boleh spasi & uppercase)
        - Format: Password = nama (lowercase) + 4 digit terakhir no. HP

        Untuk pasien yang sudah ada (edit):
        - Username dan password diambil dari form input
        """
        name = self.name_entry.get().strip()
        birth_date = self.birth_date_entry.get().strip()
        gender = self.gender_combo.get()
        phone = self.phone_entry.get().strip()
        blood_type = self.blood_combo.get() + self.rhesus_combo.get()
        address = self.address_text.get("1.0", "end").strip()

        # Validasi input dasar
        if not name:
            messagebox.showwarning("Error", "Nama harus diisi!")
            return

        # Validasi tanggal lahir (wajib diisi)
        if not birth_date:
            messagebox.showwarning("Error", "Tanggal lahir harus diisi!")
            return

        # Validasi format tanggal lahir
        try:
            from datetime import datetime
            datetime.strptime(birth_date, '%d/%m/%Y')
        except ValueError:
            messagebox.showwarning("Error", "Format tanggal lahir salah! Gunakan format: dd/mm/yyyy\nContoh: 15/05/1990")
            return

        # Validasi nomor telepon (minimal 4 digit untuk generate password)
        if not phone or len(phone) < 4:
            messagebox.showwarning("Error", "Nomor telepon harus diisi (minimal 4 digit)!")
            return

        # Untuk pasien baru, username & password akan di-generate otomatis
        # Untuk edit pasien, ambil dari form
        if self.patient_id:
            # Mode EDIT - ambil username dari form
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            if not username:
                messagebox.showwarning("Error", "Username harus diisi!")
                return

            patient_data = {
                'name': name,
                'birth_date': birth_date,  # Tanggal lahir untuk menghitung umur otomatis
                'gender': gender,
                'phone': phone,
                'blood_type': blood_type,
                'address': address,
                'username': username,
                'password': password if password else None
            }

            self.patient_crud.update_patient(self.patient_id, patient_data)
            messagebox.showinfo("Sukses", "Data pasien berhasil diupdate!")
        else:
            # Mode CREATE BARU - username & password di-generate otomatis
            # Generate untuk ditampilkan ke user
            phone_last_4 = phone[-4:]
            first_name = name.lower().split()[0] if ' ' in name else name.lower()

            generated_username = name  # Username boleh ada spasi & uppercase
            generated_password = f"{first_name}{phone_last_4}"

            patient_data = {
                'name': name,
                'birth_date': birth_date,  # Tanggal lahir untuk menghitung umur otomatis
                'gender': gender,
                'phone': phone,
                'blood_type': blood_type,
                'address': address
                # Username dan password TIDAK perlu disertakan
                # PatientCRUD akan meng-generate secara otomatis
            }

            # Buat pasien baru dengan auto-generate credentials
            new_patient = self.patient_crud.create_patient(patient_data)

            # Tampilkan credentials yang di-generate
            credentials_message = (
                f"✅ Pasien berhasil ditambahkan!\n\n"
                f"🔑 Username & Password yang di-generate:\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Username: {generated_username}\n"
                f"Password: {generated_password}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ Berikan informasi ini kepada pasien untuk login."
            )
            messagebox.showinfo("Sukses - Credentials Di-generate", credentials_message)

        self.destroy()


class DoctorDialog(ctk.CTkToplevel):
    """
    Dialog untuk tambah/edit dokter/bidan

    Dialog ini bersifat MODAL - akan muncul di depan window utama
    dan user harus menyelesaikan input di dialog ini terlebih dahulu
    sebelum bisa berinteraksi dengan window utama kembali.
    """

    def __init__(self, parent, username=None):
        super().__init__(parent)

        # ========================================
        # MODAL DIALOG BEHAVIOR
        # ========================================
        self.transient(parent)
        self.grab_set()

        self.username = username  # None untuk mode create, existing username untuk mode edit
        self.parent = parent
        self.doctor_crud = DoctorCRUD()
        self.init_ui()
        if username:
            self.load_doctor_data()

        # Bawa dialog ke paling depan dan set focus
        self.lift()
        self.focus_set()
        self.after(100, self._focus_dialog)

    def _focus_dialog(self):
        """Helper untuk memastikan dialog mendapat focus dan muncul di depan"""
        try:
            self.lift()
            self.focus_force()
            self.attributes('-topmost', True)
            self.after(100, lambda: self.attributes('-topmost', False))
        except:
            pass

    def init_ui(self):
        """
        Inisialisasi UI dialog tambah/edit dokter/bidan

        CATATAN - AUTO-GENERATE USERNAME & PASSWORD:
        ===============================================
        Untuk dokter/bidan BARU, username dan password akan di-generate OTOMATIS:
        - Username: Nama dokter/bidan (lowercase, BOLEH ADA SPASI)
        - Password: Nama + 4 digit terakhir nomor telepon

        Contoh:
        - Nama: "Dr. Andi Wijaya", Telepon: "081234564383"
        - Username: "dr. andi wijaya"
        - Password: "dr.4383"
        """
        title = "Edit Dokter/Bidan" if self.username else "Tambah Dokter/Bidan Baru"
        self.title(title)
        self.geometry("500x600")

        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (250)
        y = (self.winfo_screenheight() // 2) - (300)
        self.geometry(f'500x600+{x}+{y}')

        # Main frame
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Info card untuk dokter/bidan baru tentang auto-generate username & password
        if not self.username:
            info_card = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray25"))
            info_card.pack(fill="x", pady=(0, 15))

            info_text = (
                "💡 Username & Password akan di-generate otomatis:\n"
                "   • Username: Nama lengkap (boleh ada spasi & uppercase)\n"
                "   • Password: Nama (lowercase) + 4 digit terakhir no. HP\n"
                "   Contoh: Dr. Andi Wijaya + 08123456**4383** =\n"
                "     Username: Dr. Andi Wijaya\n"
                "     Password: dr.4383"
            )
            info_label = ctk.CTkLabel(
                info_card,
                text=info_text,
                font=ctk.CTkFont(size=11),
                justify="left"
            )
            info_label.pack(padx=15, pady=10)

        # Form fields
        self.name_entry = self.create_form_entry(main_frame, "Nama Lengkap:", "Dr. ...")
        self.phone_entry = self.create_form_entry(main_frame, "No. Telepon:", "08xxxxxxxxxx")

        # Role selection
        role_label = ctk.CTkLabel(main_frame, text="Role:", font=ctk.CTkFont(size=13, weight="bold"))
        role_label.pack(anchor="w", pady=(10, 5))
        self.role_combo = ctk.CTkOptionMenu(main_frame, values=["dokter", "bidan"])
        self.role_combo.set("dokter")
        self.role_combo.pack(fill="x", pady=(0, 15))

        # Specialization
        spec_label = ctk.CTkLabel(main_frame, text="Spesialisasi:", font=ctk.CTkFont(size=13, weight="bold"))
        spec_label.pack(anchor="w", pady=(10, 5))
        self.spec_entry = ctk.CTkEntry(main_frame, placeholder_text="Contoh: Umum, Anak, Kandungan, dll")
        self.spec_entry.pack(fill="x", pady=(0, 15))

        # Username & Password - Hanya untuk edit dokter yang sudah ada
        if self.username:
            self.password_entry = self.create_form_entry(main_frame, "Password Baru:", "", show="*")
        else:
            # Untuk dokter baru, simpan referensi untuk generated credentials
            self.generated_username = None
            self.generated_password = None

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Batal",
            command=self.destroy,
            width=100,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Simpan",
            command=self.save_doctor,
            width=100,
            fg_color="#27ae60",
            hover_color="#229954"
        )
        save_btn.pack(side="right")

    def create_form_entry(self, parent, label, placeholder, show=None):
        """Helper untuk membuat form entry"""
        label_widget = ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=13, weight="bold"))
        label_widget.pack(anchor="w", pady=(10, 5))

        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, show=show)
        entry.pack(fill="x", pady=(0, 5))
        return entry

    def load_doctor_data(self):
        """Load data dokter untuk edit"""
        doctor = self.doctor_crud.get_doctor_by_username(self.username)
        if doctor:
            self.name_entry.insert(0, doctor['name'])
            self.phone_entry.insert(0, doctor.get('phone', ''))
            self.role_combo.set(doctor['role'])
            self.spec_entry.insert(0, doctor.get('specialization', 'Umum'))

    def save_doctor(self):
        """
        Simpan data dokter/bidan (create atau update)

        CATATAN - AUTO-GENERATE CREDENTIALS:
        =====================================
        Untuk dokter/bidan BARU (self.username is None):
        - Username dan password akan di-generate OTOMATIS
        - Username: Nama lengkap (lowercase, boleh ada spasi)
        - Password: Nama + 4 digit terakhir nomor telepon

        Untuk dokter yang sudah ada (edit):
        - Password bisa diubah dari form input
        """
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        role = self.role_combo.get()
        specialization = self.spec_entry.get().strip()

        # Validasi input dasar
        if not name:
            messagebox.showwarning("Error", "Nama harus diisi!")
            return

        # Validasi nomor telepon (minimal 4 digit untuk generate password)
        if not phone or len(phone) < 4:
            messagebox.showwarning("Error", "Nomor telepon harus diisi (minimal 4 digit)!")
            return

        if not specialization:
            specialization = "Umum"

        # Untuk dokter baru, username & password akan di-generate otomatis
        # Untuk edit dokter, ambil password dari form jika ada
        if self.username:
            # Mode EDIT
            password = None
            if hasattr(self, 'password_entry'):
                password = self.password_entry.get().strip()

            doctor_data = {
                'name': name,
                'phone': phone,
                'role': role,
                'specialization': specialization
            }

            if password:
                doctor_data['password'] = password

            self.doctor_crud.update_doctor(self.username, doctor_data)
            messagebox.showinfo("Sukses", "Data dokter/bidan berhasil diupdate!")
        else:
            # Mode CREATE BARU - username & password di-generate otomatis
            # Generate untuk ditampilkan ke user
            phone_last_4 = phone[-4:]

            # Ambil nama depan saja untuk password (lowercase), hapus karakter khusus
            first_name_raw = name.split()[0] if ' ' in name else name
            first_name = ''.join(c for c in first_name_raw.lower() if c.isalnum())

            generated_username = name  # Username boleh ada spasi & uppercase
            generated_password = f"{first_name}{phone_last_4}"

            doctor_data = {
                'name': name,
                'phone': phone,
                'role': role,
                'specialization': specialization
                # Username dan password TIDAK perlu disertakan
                # DoctorCRUD akan meng-generate secara otomatis
            }

            # Buat dokter baru dengan auto-generate credentials
            new_doctor = self.doctor_crud.create_doctor(doctor_data)

            # Tampilkan credentials yang di-generate
            credentials_message = (
                f"✅ Dokter/Bidan berhasil ditambahkan!\n\n"
                f"🔑 Username & Password yang di-generate:\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Username: {generated_username}\n"
                f"Password: {generated_password}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ Berikan informasi ini untuk login."
            )
            messagebox.showinfo("Sukses - Credentials Di-generate", credentials_message)

        self.destroy()

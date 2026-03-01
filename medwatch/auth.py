"""
Modul Autentikasi
Menangani login dan verifikasi dokter dengan fullscreen support
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.json_helper import JSONHelper
import os


class AuthWindow(ctk.CTk):
    """Jendela autentikasi untuk login"""

    def __init__(self):
        super().__init__()
        self.json_helper = JSONHelper()
        self.pasien_ui = None
        self.dokter_ui = None
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        self.title("MedWatch - Login")
        self.geometry("500x500")

        # Center window
        self.center_window()

        # Bind ESC untuk toggle fullscreen
        self.bind("<Escape>", self.toggle_fullscreen)

        # Main frame dengan rounded corners
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="MEDWATCH",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title_label.pack(pady=(30, 5))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Sistem Monitoring Kesehatan",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 25))

        # Info fullscreen hint
        hint_label = ctk.CTkLabel(
            main_frame,
            text="💡 Tekan ESC untuk keluar fullscreen",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        hint_label.pack(pady=(0, 15))

        # Role selection
        role_label = ctk.CTkLabel(main_frame, text="Masuk sebagai:", font=ctk.CTkFont(size=14, weight="bold"))
        role_label.pack(pady=(10, 5), anchor="w")

        self.role_combo = ctk.CTkOptionMenu(main_frame, values=["Dokter", "Pasien"])
        self.role_combo.set("Dokter")
        self.role_combo.pack(pady=(0, 15), fill="x")

        # Username input
        username_label = ctk.CTkLabel(main_frame, text="Username:", font=ctk.CTkFont(size=14, weight="bold"))
        username_label.pack(pady=(10, 5), anchor="w")

        self.username_input = ctk.CTkEntry(main_frame, placeholder_text="Masukkan username")
        self.username_input.pack(pady=(0, 15), fill="x")

        # Password input
        password_label = ctk.CTkLabel(main_frame, text="Password:", font=ctk.CTkFont(size=14, weight="bold"))
        password_label.pack(pady=(10, 5), anchor="w")

        self.password_input = ctk.CTkEntry(main_frame, placeholder_text="Masukkan password", show="*")
        self.password_input.pack(pady=(0, 20), fill="x")

        # Bind Enter key untuk login
        self.password_input.bind("<Return>", lambda e: self.login())

        # Login button
        self.login_btn = ctk.CTkButton(
            main_frame,
            text="MASUK",
            command=self.login,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.login_btn.pack(pady=(15, 20), fill="x")

        # Akun demo info
        demo_frame = ctk.CTkFrame(main_frame, fg_color=("gray85", "gray20"))
        demo_frame.pack(fill="x", pady=(10, 0))

        demo_title = ctk.CTkLabel(
            demo_frame,
            text="Akun Demo:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        demo_title.pack(pady=(8, 3), anchor="w", padx=10)

        demo_info = ctk.CTkLabel(
            demo_frame,
            text="Dokter: dokter1 / dokter123   |   Pasien: pasien1 / pasien123",
            font=ctk.CTkFont(size=11)
        )
        demo_info.pack(pady=(0, 8), padx=10)

        # Copyright
        copyright_label = ctk.CTkLabel(
            main_frame,
            text="© 2024 MedWatch Healthcare System",
            font=ctk.CTkFont(size=10)
        )
        copyright_label.pack(side="bottom", pady=10)

    def center_window(self):
        """Center window di layar"""
        self.update_idletasks()
        width = 500
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_fullscreen(self, event=None):
        """
        Toggle fullscreen mode
        Dipanggil saat tombol ESC ditekan
        """
        current = self.attributes('-fullscreen')
        self.attributes('-fullscreen', not current)

    def login(self):
        """Proses login dengan username case-insensitive"""
        username = self.username_input.get().strip().lower()  # Ubah ke lowercase
        password = self.password_input.get().strip()
        role = self.role_combo.get().lower()

        if not username or not password:
            messagebox.showwarning("Error", "Username dan password harus diisi!")
            return

        # Load users data
        users = self.json_helper.load_users()

        # Check credentials (case-insensitive untuk username)
        user_found = False
        for user in users:
            if user['username'].lower() == username and user['password'] == password and user['role'] == role:
                user_found = True
                user_name = user.get('name', user['username'])
                break

        if user_found:
            messagebox.showinfo("Sukses", f"Selamat datang, {user_name}!")
            self.open_dashboard(role, username, user_name)
        else:
            messagebox.showerror("Error", "Username, password, atau role salah!")

    def open_dashboard(self, role, username, user_name):
        """Buka dashboard sesuai role dengan fullscreen"""
        # Set dashboard ke fullscreen sebelum close login
        if role == "dokter":
            from dokter_ui import DokterDashboard
            self.destroy()  # Destroy login window dulu!
            # Buka dashboard fullscreen
            self.dokter_ui = DokterDashboard(user_name)
            self.dokter_ui.attributes('-fullscreen', True)
            # Bind ESC sudah di init_ui dokter_ui
            self.dokter_ui.mainloop()
        else:
            from pasien_ui import PasienDashboard
            self.destroy()  # Destroy login window dulu!
            # Buka dashboard fullscreen
            self.pasien_ui = PasienDashboard(username)
            self.pasien_ui.attributes('-fullscreen', True)
            # Bind ESC sudah di init_ui pasien_ui
            self.pasien_ui.mainloop()

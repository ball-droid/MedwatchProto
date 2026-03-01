"""
Modul Autentikasi
Menangani login dan verifikasi dokter
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
        self.geometry("450x450")

        # Center window
        self.center_window()

        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="MEDWATCH",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Sistem Monitoring Kesehatan",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 20))

        # Role selection
        role_label = ctk.CTkLabel(main_frame, text="Masuk sebagai:", font=ctk.CTkFont(size=14))
        role_label.pack(pady=(10, 5), anchor="w")

        self.role_combo = ctk.CTkOptionMenu(main_frame, values=["Dokter", "Pasien"])
        self.role_combo.set("Dokter")
        self.role_combo.pack(pady=(0, 15), fill="x")

        # Username input
        username_label = ctk.CTkLabel(main_frame, text="Username:", font=ctk.CTkFont(size=14))
        username_label.pack(pady=(10, 5), anchor="w")

        self.username_input = ctk.CTkEntry(main_frame, placeholder_text="Masukkan username")
        self.username_input.pack(pady=(0, 15), fill="x")

        # Password input
        password_label = ctk.CTkLabel(main_frame, text="Password:", font=ctk.CTkFont(size=14))
        password_label.pack(pady=(10, 5), anchor="w")

        self.password_input = ctk.CTkEntry(main_frame, placeholder_text="Masukkan password", show="*")
        self.password_input.pack(pady=(0, 20), fill="x")

        # Bind Enter key
        self.password_input.bind("<Return>", lambda e: self.login())

        # Login button
        self.login_btn = ctk.CTkButton(
            main_frame,
            text="Masuk",
            command=self.login,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.login_btn.pack(pady=(10, 20), fill="x")

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
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def login(self):
        """Proses login"""
        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        role = self.role_combo.get().lower()

        if not username or not password:
            messagebox.showwarning("Error", "Username dan password harus diisi!")
            return

        # Load users data
        users = self.json_helper.load_users()

        # Check credentials
        user_found = False
        for user in users:
            if user['username'] == username and user['password'] == password and user['role'] == role:
                user_found = True
                user_name = user.get('name', username)
                break

        if user_found:
            messagebox.showinfo("Sukses", f"Selamat datang, {user_name}!")
            self.open_dashboard(role, user_name)
        else:
            messagebox.showerror("Error", "Username, password, atau role salah!")

    def open_dashboard(self, role, user_name):
        """Buka dashboard sesuai role"""
        self.destroy()  # Close login window

        if role == "dokter":
            from dokter_ui import DokterDashboard
            self.dokter_ui = DokterDashboard(user_name)
            self.dokter_ui.mainloop()
        else:
            from pasien_ui import PasienDashboard
            self.pasien_ui = PasienDashboard(user_name)
            self.pasien_ui.mainloop()

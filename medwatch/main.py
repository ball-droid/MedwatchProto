"""
 =============================================================================
 MEDWATCH - SISTEM MONITORING KESEHATAN
 =============================================================================

 Module: main.py
 Deskripsi: Entry point utama aplikasi
 Penulis: MedWatch Team

 Alur Program:
 -------------
 1. Import modul-modul yang diperlukan
 2. Konfigurasi tema aplikasi (warna, appearance mode)
 3. Membuat jendela autentikasi (login)
 4. Mengatur mode fullscreen
 5. Menjalankan main event loop

 Prinsip Clean Code:
 --------------------
 - Single Responsibility: Hanya mengatur inisialisasi aplikasi
 - Meaningful Names: Nama fungsi dan variabel jelas
 - Magic Numbers: Tidak ada, semua ada keterangan
 - DRY (Don't Repeat Yourself): Tidak ada duplikasi kode

 Prinsip Modular Programming:
 ---------------------------
 - Modularity: Aplikasi dibagi menjadi modul-modul terpisah
 - Low Coupling: main.py hanya tergantung pada AuthWindow
 - High Cohesion: Setiap modul memiliki fungsi spesifik
"""

import sys
import customtkinter as ctk
from auth import AuthWindow


def configure_application_theme():
    """
    Mengonfigurasi tema tampilan aplikasi

    Args:
        None

    Returns:
        None

    Alur:
    -----
    1. Set appearance mode (dark/light/system)
    2. Set default color theme (blue/green/dark-blue)

    Clean Code:
    -----------
    - Fungsi tunggal dengan satu tanggung jawab (SRP)
    - Nilai konstanta didefinisikan dengan jelas
    """
    # Mode gelap untuk kenyamanan mata
    # Alternatif: "System", "Dark", "Light"
    ctk.set_appearance_mode("Dark")

    # Tema warna biru sebagai identitas MedWatch
    # Alternatif: "blue", "green", "dark-blue"
    ctk.set_default_color_theme("blue")


def toggle_fullscreen_callback(window, event=None):
    """
    Callback untuk toggle mode fullscreen

    Args:
        window: Jendela yang akan di-toggle fullscreen-nya
        event: Event dari keyboard (opsional, untuk binding ESC)

    Returns:
        None

    Alur:
    -----
    1. Cek status fullscreen saat ini
    2. Toggle (aktifkan/matikan) mode fullscreen
    3. Esc → toggle fullscreen

    Modular Programming:
    --------------------
    - Fungsi terpisah untuk fungsi spesifik
    - Reusable di berbagai window
    """
    try:
        # Dapatkan status fullscreen saat ini (True/False)
        current_state = window.attributes('-fullscreen')

        # Toggle: True → False, False → True
        window.attributes('-fullscreen', not current_state)
    except Exception as e:
        # Handle error jika window sudah di-destroy
        print(f"Warning: Gagal toggle fullscreen: {e}")


def create_login_window():
    """
    Membuat dan mengembalikan jendela login

    Args:
        None

    Returns:
        AuthWindow: Object jendela login yang siap ditampilkan

    Alur:
    -----
    1. Instansiasi AuthWindow
    2. Atur mode fullscreen
    3. Binding tombol ESC untuk keluar fullscreen
    4. Return window object

    Clean Code:
    -----------
    - Fungsi murni tanpa side effect selain create object
    - Dependency injection: window dikembalikan ke caller
    """
    # Membuat jendela login
    login_window = AuthWindow()

    # Mengatur fullscreen sebagai default
    login_window.attributes('-fullscreen', True)

    # Binding ESC key untuk toggle fullscreen
    # Pengguna bisa keluar fullscreen dengan menekan ESC
    login_window.bind("<Escape>", lambda e: toggle_fullscreen_callback(login_window, e))

    return login_window


def main():
    """
    Fungsi utama aplikasi
    Entry point untuk menjalankan seluruh aplikasi MedWatch

    Args:
        None

    Returns:
        int: Exit code (0 = sukses, 1 = error)

    Alur Program Utama:
    -------------------
    1. Konfigurasi tema aplikasi
    2. Buat jendela login
    3. Masukkan ke main event loop
    4. Handle exception dan graceful exit

    Modular Programming:
    --------------------
    - main() hanya sebagai orchestrator
    - Logika detail didelegasikan ke modul lain
    - Mudah di-test (unit test possible)
    """
    try:
        # Langkah 1: Konfigurasi tema
        configure_application_theme()

        # Langkah 2: Buat jendela login
        login_window = create_login_window()

        # Langkah 3: Jalankan event loop
        # Program akan berjalan di sini sampai window di-close
        login_window.mainloop()

        # Exit code sukses
        return 0

    except KeyboardInterrupt:
        # Handle Ctrl+C untuk graceful exit
        print("\n[INFO] Aplikasi dihentikan oleh pengguna")
        return 0

    except Exception as e:
        # Handle exception tak terduga
        print(f"[ERROR] Terjadi kesalahan: {e}")
        return 1


if __name__ == "__main__":
    """
    Entry Point Guard
    -------------------
    Memastikan kode di bawah ini hanya jalan
    saat file dijalankan langsung (bukan saat di-import)
    """
    # Jalankan fungsi main dan ambil exit code
    exit_code = main()

    # Exit program dengan code yang sesuai
    sys.exit(exit_code)

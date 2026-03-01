"""
Modul Doctor CRUD
Create, Read, Update, Delete operations untuk data dokter/bidan

PENTING - FORMAT USERNAME & PASSWORD:
=====================================
Username dan password di-generate otomatis dengan format yang SAMA
seperti pasien:
- Username: Nama dokter/bidan (lowercase, tanpa spasi)
- Password: Nama + 4 digit terakhir nomor telepon

Contoh:
- Nama: "Dr. Andi Wijaya", Telepon: "081234564383"
- Username: "dr.andiwijaya"
- Password: "dr.4383"

Format Password: {nama_depan}{4_digit_terakhir_telepon}
"""

import os
import json
from utils.json_helper import JSONHelper


class DoctorCRUD:
    """
    Kelas untuk menangani CRUD dokter/bidan

    Sistem Auto-Generate Credentials:
    - Username dan password di-generate otomatis
    - Format sama seperti pasien untuk konsistensi
    """

    def __init__(self):
        self.json_helper = JSONHelper()
        self.users_file = os.path.join("data", "users.json")
        self.doctors_file = os.path.join("data", "doctors.json")

    def get_all_doctors(self):
        """Ambil semua data dokter/bidan dari users.json"""
        users = self.json_helper.load_users()
        # Filter hanya user dengan role dokter
        doctors = []
        for user in users:
            if user['role'] in ['dokter', 'bidan']:
                doctors.append(user)
        return doctors

    def get_doctor_by_username(self, username):
        """Ambil data dokter berdasarkan username"""
        users = self.json_helper.load_users()
        for user in users:
            if user['username'] == username and user['role'] in ['dokter', 'bidan']:
                return user
        return None

    def create_doctor(self, data):
        """
        Tambah dokter/bidan baru dengan auto-generate username/password

        SISTEM AUTO-GENERATE USERNAME & PASSWORD:
        ==========================================
        Username dan password di-generate otomatis berdasarkan:
        - Username: Nama dokter/bidan (lowercase, tanpa spasi)
        - Password: Nama + 4 digit terakhir nomor telepon

        Format SAMA seperti pasien untuk konsistensi sistem.

        Contoh:
        - Nama: "Dr. Andi Wijaya", Telepon: "081234564383"
        - Username: "dr.andiwijaya"
        - Password: "dr.4383"

        Args:
            data (dict): Data dokter baru (name, phone, specialization, etc.)
                        - Tidak perlu menyertakan 'username' dan 'password'
                        - Username dan password akan di-generate otomatis

        Returns:
            dict: Data dokter baru yang telah dibuat dengan kredensial
        """
        users = self.json_helper.load_users()

        # ========================================
        # AUTO-GENERATE USERNAME & PASSWORD
        # ========================================
        # Format: Nama dokter/bidan (boleh spasi, boleh uppercase)
        doctor_name = data['name'].strip()
        username = doctor_name  # Username boleh ada spasi & uppercase

        # ========================================
        # PENCEGAHAN DUPLIKASI USERNAME
        # ========================================
        # Cek apakah username sudah ada
        final_username = username
        counter = 2

        # Get existing usernames untuk cek duplikasi
        existing_usernames = [u['username'] for u in users]

        while final_username in existing_usernames:
            # Tambahkan angka di belakang jika duplikat
            final_username = f"{username} {counter}"
            counter += 1

        # Gunakan username yang sudah unik
        username = final_username

        # Format password: Nama (lowercase) + 4 digit terakhir nomor telepon
        # Contoh: "Dr. Andi Wijaya" + "081234564383" → "dr.4383"
        phone_number = data['phone'].strip()
        last_4_digits = phone_number[-4:] if len(phone_number) >= 4 else phone_number

        # Ambil nama depan saja untuk password (lowercase)
        # Hapus karakter khusus dari nama depan
        first_name_raw = doctor_name.split()[0] if ' ' in doctor_name else doctor_name
        first_name = ''.join(c for c in first_name_raw.lower() if c.isalnum())

        password = f"{first_name}{last_4_digits}"

        # Create doctor user account
        new_doctor = {
            'username': username,  # Auto-generate
            'password': password,   # Auto-generate
            'role': data.get('role', 'dokter'),  # dokter atau bidan
            'name': data['name'],
            'phone': data['phone'],
            'specialization': data.get('specialization', 'Umum')  # Spesialisasi
        }

        users.append(new_doctor)

        # Save users data
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return new_doctor

    def update_doctor(self, username, data):
        """
        Update data dokter/bidan

        Args:
            username (str): Username dokter yang akan diupdate
            data (dict): Data baru (name, phone, specialization, dll)

        Returns:
            bool: True jika berhasil
        """
        users = self.json_helper.load_users()

        for i, user in enumerate(users):
            if user['username'] == username and user['role'] in ['dokter', 'bidan']:
                users[i].update({
                    'name': data['name'],
                    'phone': data['phone'],
                    'specialization': data.get('specialization', 'Umum')
                })

                # Update password jika disediakan
                if data.get('password'):
                    users[i]['password'] = data['password']

                break

        # Save updated data
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return True

    def delete_doctor(self, username):
        """
        Hapus data dokter/bidan

        PENTING - DELETE CASCADE:
        =========================
        Ketika dokter dihapus:
        1. Akun dokter dari users.json dihapus
        2. Rekam medis yang dibuat oleh dokter TIDAK dihapus
           (karena merupakan data medis pasien yang penting)

        Args:
            username (str): Username dokter yang akan dihapus

        Returns:
            bool: True jika berhasil, False jika dokter tidak ditemukan
        """
        users = self.json_helper.load_users()

        # Cek apakah dokter ada
        doctor = self.get_doctor_by_username(username)
        if not doctor:
            return False

        # Remove doctor
        users = [u for u in users if not (u['username'] == username and u['role'] in ['dokter', 'bidan'])]

        # Save updated data
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return True

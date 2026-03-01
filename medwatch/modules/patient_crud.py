"""
Modul Patient CRUD
Create, Read, Update, Delete operations untuk data pasien

PENTING - SISTEM ID UNIK:
=========================
Setiap pasien memiliki ID unik yang otomatis di-generate oleh sistem.
ID unik ini mencegah tertukarnya data dan rekam medis antar pasien.

Manfaat ID Unik:
1. Mencegah tertukarnya rekam medis pasien dengan nama sama
2. Identifikasi pasien yang akurat dan unik
3. Referensi yang reliable untuk hubungan antar data (rekam medis, dll)

Contoh Implementasi:
- Pasien "Budi Santoso" dengan ID 1
- Pasien "Budi Santoso" dengan ID 2
-> Keduanya berbeda orang, sistem TIDAK akan tertukar karena ID unik
"""

import os
import json
from utils.json_helper import JSONHelper


class PatientCRUD:
    """
    Kelas untuk menangani CRUD pasien dengan sistem ID unik

    Sistem ID Unik:
    - ID di-generate otomatis (max ID + 1)
    - Setiap pasien memiliki ID yang berbeda
    - ID digunakan sebagai referensi utama untuk menghindari kebingungan
    """

    def __init__(self):
        self.json_helper = JSONHelper()
        self.patients_file = os.path.join("data", "patients.json")
        self.users_file = os.path.join("data", "users.json")

    def get_all_patients(self):
        """Ambil semua data pasien"""
        return self.json_helper.load_patients()

    def get_patient_by_id(self, patient_id):
        """Ambil data pasien berdasarkan ID"""
        patients = self.get_all_patients()
        for patient in patients:
            if patient['id'] == patient_id:
                return patient
        return None

    def create_patient(self, data):
        """
        Tambah pasien baru dengan ID unik otomatis dan auto-generate username/password

        SISTEM ID UNIK:
        ===============
        ID di-generate otomatis dengan formula: max(existing_id) + 1

        SISTEM AUTO-GENERATE USERNAME & PASSWORD:
        ==========================================
        Username dan password di-generate otomatis berdasarkan:
        - Username: Nama pasien (boleh spasi, boleh uppercase)
        - Password: Nama (lowercase) + 4 digit terakhir nomor telepon

        PENCEGAHAN DUPLIKASI USERNAME:
        ============================
        Jika username sudah ada, sistem akan menambahkan angka di belakang:
        - "Budi Santoso" sudah ada → "Budi Santoso 2"
        - "Budi Santoso 2" sudah ada → "Budi Santoso 3"
        dst.

        Contoh:
        - Nama: "Budi Santoso", Telepon: "081234564383"
        - Username: "Budi Santoso"
        - Password: "budi4383"

        Format Password: {nama_pasien}{4_digit_terakhir_telepon}

        Keuntungan:
        - Tidak ada duplikasi ID
        - Setiap pasien dapat di-identifikasi secara unik
        - Mencegah tertukarnya rekam medis antar pasien dengan nama sama
        - Username & password otomatis, mudah diingat oleh pasien
        - Username unik terjamin

        Args:
            data (dict): Data pasien baru (name, birth_date, gender, phone, etc.)
                        - Tidak perlu menyertakan 'username', 'password', 'age'
                        - Birth_date digunakan untuk menghitung umur otomatis

        Returns:
            dict: Data pasien baru yang telah dibuat dengan ID unik dan kredensial
        """
        patients = self.get_all_patients()

        # ========================================
        # GENERATE ID UNIK OTOMATIS
        # ========================================
        # Formula: ID baru = ID maksimum yang sudah ada + 1
        # Ini menjamin ID unik untuk setiap pasien baru
        if patients:
            new_id = max(p['id'] for p in patients) + 1
        else:
            new_id = 1  # Pasien pertama mendapat ID 1

        # ========================================
        # HITUNG UMUR DARI TANGGAL LAHIR
        # ========================================
        from datetime import datetime

        birth_date_str = data.get('birth_date', '').strip()
        if birth_date_str:
            try:
                # Parse tanggal lahir (format: dd/mm/yyyy)
                birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y')
                today = datetime.now()

                # Hitung umur
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except ValueError:
                # Jika format salah, gunakan umur dari input (jika ada) atau default 0
                age = data.get('age', 0)
        else:
            age = data.get('age', 0)

        # ========================================
        # AUTO-GENERATE USERNAME & PASSWORD
        # ========================================
        # Format: Nama pasien (boleh spasi, boleh uppercase)
        patient_name = data['name'].strip()
        username = patient_name  # Username boleh ada spasi & uppercase

        # ========================================
        # PENCEGAHAN DUPLIKASI USERNAME
        # ========================================
        # Cek apakah username sudah ada
        final_username = username
        counter = 2

        # Load existing users untuk cek duplikasi
        users = self.json_helper.load_users()
        existing_usernames = [u['username'] for u in users]

        while final_username in existing_usernames:
            # Tambahkan angka di belakang jika duplikat
            final_username = f"{username} {counter}"
            counter += 1

        # Gunakan username yang sudah unik
        username = final_username

        # Format password: Nama (lowercase) + 4 digit terakhir nomor telepon
        # Contoh: "Budi Santoso" + "081234564383" → "budi4383"
        phone_number = data['phone'].strip()
        last_4_digits = phone_number[-4:] if len(phone_number) >= 4 else phone_number

        # Ambil nama depan saja untuk password (bagi yang punya nama lebih dari 1 kata)
        first_name = patient_name.lower().split()[0] if ' ' in patient_name else patient_name.lower()
        password = f"{first_name}{last_4_digits}"

        # Create patient record
        new_patient = {
            'id': new_id,
            'name': data['name'],
            'age': age,  # Umur yang dihitung dari birth_date
            'birth_date': birth_date_str,  # Tanggal lahir (dd/mm/yyyy)
            'gender': data['gender'],
            'phone': data['phone'],
            'blood_type': data['blood_type'],
            'address': data.get('address', ''),
            'username': username,  # Auto-generate (dengan pengecekan duplikasi)
            'password': password   # Auto-generate
        }

        patients.append(new_patient)

        # Save patients data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        # Create user account for patient dengan kredensial yang sudah di-generate
        users = self.json_helper.load_users()
        new_user = {
            'username': username,  # Username yang sudah di-generate otomatis
            'password': password,   # Password yang sudah di-generate otomatis
            'role': 'pasien',
            'name': data['name']
        }
        users.append(new_user)

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return new_patient

    def update_patient(self, patient_id, data):
        """
        Update data pasien

        CATATAN - PERHITUNGAN UMUR OTOMATIS:
        =====================================
        Jika birth_date disediakan, umur akan dihitung ulang secara otomatis.
        Jika tidak ada birth_date, umur tetap menggunakan nilai existing.
        """
        from datetime import datetime

        patients = self.get_all_patients()

        for i, patient in enumerate(patients):
            if patient['id'] == patient_id:
                # Update data dasar
                patients[i]['name'] = data['name']
                patients[i]['gender'] = data['gender']
                patients[i]['phone'] = data['phone']
                patients[i]['blood_type'] = data['blood_type']
                patients[i]['address'] = data.get('address', '')
                patients[i]['username'] = data['username']

                # Update umur dari birth_date jika disediakan
                if 'birth_date' in data and data['birth_date']:
                    patients[i]['birth_date'] = data['birth_date']
                    try:
                        # Hitung ulang umur dari birth_date
                        birth_date = datetime.strptime(data['birth_date'], '%d/%m/%Y')
                        today = datetime.now()
                        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                        patients[i]['age'] = age
                    except ValueError:
                        # Jika format salah, gunakan umur existing
                        pass
                elif 'age' in data:
                    # Jika tidak ada birth_date tapi ada age field (backward compatibility)
                    patients[i]['age'] = data['age']

                # Update password if provided
                if data.get('password'):
                    self.update_user_password(patient['username'], data['password'])

                break

        # Save updated data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        return True

    def delete_patient(self, patient_id):
        """
        Hapus data pasien beserta semua rekam medisnya

        PENTING - DELETE CASCADE:
        =========================
        Ketika pasien dihapus, semua data yang terkait juga akan dihapus:
        1. Data pasien dari patients.json
        2. Akun user dari users.json
        3. SEMUA rekam medis pasien dari medical_records.json

        Ini mencegah data orphan (rekam medis tanpa pasien) dan menjaga
        integritas data sistem.

        Args:
            patient_id (int): ID unik pasien yang akan dihapus

        Returns:
            bool: True jika berhasil, False jika pasien tidak ditemukan
        """
        patients = self.get_all_patients()

        # Get username before deleting
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return False

        username = patient['username']

        # ========================================
        # STEP 1: Hapus Data Pasien
        # ========================================
        patients = [p for p in patients if p['id'] != patient_id]

        # Save updated data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        # ========================================
        # STEP 2: Hapus Akun User
        # ========================================
        users = self.json_helper.load_users()
        users = [u for u in users if u['username'] != username]

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        # ========================================
        # STEP 3: Hapus SEMUA Rekam Medis Pasien
        # ========================================
        # Load semua rekam medis
        records_file = os.path.join("data", "medical_records.json")
        with open(records_file, 'r') as f:
            records = json.load(f)

        # Filter: Hapus rekam medis yang milik pasien ini
        original_count = len(records)
        records = [r for r in records if r['patient_id'] != patient_id]
        deleted_count = original_count - len(records)

        # Save updated records
        with open(records_file, 'w') as f:
            json.dump(records, f, indent=4)

        # Logging jumlah rekam medis yang dihapus
        if deleted_count > 0:
            print(f"✅ {deleted_count} rekam medis pasien '{patient['name']}' juga dihapus")

        return True

    def update_user_password(self, username, new_password):
        """Update password user"""
        users = self.json_helper.load_users()

        for user in users:
            if user['username'] == username:
                user['password'] = new_password
                break

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

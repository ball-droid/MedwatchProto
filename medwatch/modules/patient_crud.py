"""
Modul Patient CRUD
Create, Read, Update, Delete operations untuk data pasien
"""

import os
import json
from utils.json_helper import JSONHelper


class PatientCRUD:
    """Kelas untuk menangani CRUD pasien"""

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
        """Tambah pasien baru"""
        patients = self.get_all_patients()

        # Generate new ID
        if patients:
            new_id = max(p['id'] for p in patients) + 1
        else:
            new_id = 1

        # Create patient record
        new_patient = {
            'id': new_id,
            'name': data['name'],
            'age': data['age'],
            'gender': data['gender'],
            'phone': data['phone'],
            'blood_type': data['blood_type'],
            'address': data.get('address', ''),
            'username': data['username']
        }

        patients.append(new_patient)

        # Save patients data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        # Create user account for patient
        users = self.json_helper.load_users()
        new_user = {
            'username': data['username'],
            'password': data['password'],
            'role': 'pasien',
            'name': data['name']
        }
        users.append(new_user)

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

        return new_patient

    def update_patient(self, patient_id, data):
        """Update data pasien"""
        patients = self.get_all_patients()

        for i, patient in enumerate(patients):
            if patient['id'] == patient_id:
                patients[i].update({
                    'name': data['name'],
                    'age': data['age'],
                    'gender': data['gender'],
                    'phone': data['phone'],
                    'blood_type': data['blood_type'],
                    'address': data.get('address', ''),
                    'username': data['username']
                })

                # Update password if provided
                if data.get('password'):
                    self.update_user_password(patient['username'], data['password'])

                break

        # Save updated data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        return True

    def delete_patient(self, patient_id):
        """Hapus data pasien"""
        patients = self.get_all_patients()

        # Get username before deleting
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return False

        username = patient['username']

        # Remove patient
        patients = [p for p in patients if p['id'] != patient_id]

        # Save updated data
        with open(self.patients_file, 'w') as f:
            json.dump(patients, f, indent=4)

        # Remove user account
        users = self.json_helper.load_users()
        users = [u for u in users if u['username'] != username]

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)

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

"""
Modul Medical Record
Menangani operasi rekam medis pasien
"""

import os
import json
from datetime import datetime
from utils.json_helper import JSONHelper


class MedicalRecordManager:
    """Kelas untuk menangani rekam medis"""

    def __init__(self):
        self.json_helper = JSONHelper()
        self.records_file = os.path.join("data", "medical_records.json")
        self.patients_file = os.path.join("data", "patients.json")

    def get_all_records(self):
        """Ambil semua rekam medis dengan nama pasien"""
        records = self.json_helper.load_medical_records()
        patients = self.json_helper.load_patients()

        # Create patient name mapping
        patient_names = {p['id']: p['name'] for p in patients}

        # Add patient name to each record
        for record in records:
            record['patient_name'] = patient_names.get(record['patient_id'], 'Unknown')

        return records

    def get_patient_records(self, patient_id):
        """Ambil rekam medis berdasarkan ID pasien"""
        all_records = self.get_all_records()
        return [r for r in all_records if r['patient_id'] == patient_id]

    def create_record(self, data):
        """Tambah rekam medis baru"""
        records = self.json_helper.load_medical_records()

        # Generate new ID
        if records:
            new_id = max(r['id'] for r in records) + 1
        else:
            new_id = 1

        # Create new record
        new_record = {
            'id': new_id,
            'patient_id': data['patient_id'],
            'date': data['date'],
            'diagnosis': data['diagnosis'],
            'medications': data.get('medications', ''),
            'notes': data.get('notes', ''),
            'doctor': data['doctor']
        }

        records.append(new_record)

        # Save to file
        with open(self.records_file, 'w') as f:
            json.dump(records, f, indent=4)

        return new_record

    def update_record(self, record_id, data):
        """Update rekam medis"""
        records = self.json_helper.load_medical_records()

        for i, record in enumerate(records):
            if record['id'] == record_id:
                records[i].update(data)
                break

        # Save to file
        with open(self.records_file, 'w') as f:
            json.dump(records, f, indent=4)

        return True

    def delete_record(self, record_id):
        """Hapus rekam medis"""
        records = self.json_helper.load_medical_records()
        records = [r for r in records if r['id'] != record_id]

        # Save to file
        with open(self.records_file, 'w') as f:
            json.dump(records, f, indent=4)

        return True

    def get_records_by_diagnosis(self, diagnosis_keyword):
        """Cari rekam medis berdasarkan diagnosis"""
        records = self.get_all_records()
        return [
            r for r in records
            if diagnosis_keyword.lower() in r['diagnosis'].lower()
        ]

    def get_records_by_date_range(self, start_date, end_date):
        """Ambil rekam medis dalam rentang tanggal"""
        records = self.get_all_records()
        return [
            r for r in records
            if start_date <= r['date'] <= end_date
        ]

    def get_diagnosis_statistics(self):
        """Hitung statistik diagnosis"""
        records = self.json_helper.load_medical_records()
        stats = {}

        for record in records:
            diagnosis = record['diagnosis']
            stats[diagnosis] = stats.get(diagnosis, 0) + 1

        # Sort by count
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

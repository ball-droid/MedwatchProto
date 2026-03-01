"""
Modul Drug Data
Database obat dengan format dictionary untuk fast search
"""

import os
import json
from utils.json_helper import JSONHelper


class DrugDataManager:
    """Kelas untuk menangani data obat dengan format dictionary"""

    def __init__(self):
        self.json_helper = JSONHelper()

    def get_all_drugs(self):
        """Ambil semua data obat sebagai list"""
        return self.json_helper.get_drug_list()

    def get_drugs_dict(self):
        """
        Ambil semua data obat sebagai dictionary (key: lowercase name)
        Jika file JSON format list, otomatis konversi ke dict
        """
        drugs = self.json_helper.load_drugs()

        # Jika masih format list, konversi ke dict
        if isinstance(drugs, list):
            drugs_dict = {}
            for drug in drugs:
                key = drug['name'].lower()
                drugs_dict[key] = drug
            return drugs_dict

        return drugs

    def get_drug_by_name(self, name):
        """Ambil data obat berdasarkan nama (O(1) lookup)"""
        drugs = self.get_drugs_dict()  # Pastikan dict format
        name_lower = name.lower().strip()

        # Direct match
        if name_lower in drugs:
            return drugs[name_lower]

        # Search in aliases
        for drug in drugs.values():
            if 'aliases' in drug:
                for alias in drug['aliases']:
                    if name_lower == alias.lower():
                        return drug

        # Partial match
        for drug in drugs.values():
            if name_lower in drug['name'].lower():
                return drug

        return None

    def get_drug_by_id(self, drug_id):
        """Ambil obat berdasarkan ID"""
        drugs = self.get_all_drugs()
        for drug in drugs:
            if drug['id'] == drug_id:
                return drug
        return None

    def get_drugs_by_category(self, category):
        """Ambil obat berdasarkan kategori"""
        drugs = self.get_all_drugs()
        return [d for d in drugs if category.lower() in d['category'].lower()]

    def get_all_categories(self):
        """Ambil semua kategori obat yang unik"""
        drugs = self.get_all_drugs()
        categories = set(d['category'] for d in drugs)
        return sorted(list(categories))

    def get_drugs_by_tag(self, tag):
        """Cari obat berdasarkan tag"""
        drugs = self.get_all_drugs()
        tag_lower = tag.lower()
        return [
            d for d in drugs
            if 'tags' in d and any(tag_lower in t.lower() for t in d['tags'])
        ]

    def add_drug(self, drug_data):
        """Tambah obat baru ke dictionary"""
        drugs = self.get_drugs_dict()

        # Generate new ID
        if drugs:
            new_id = max(d['id'] for d in drugs.values()) + 1
        else:
            new_id = 1

        # Create lowercase key for dictionary
        name_key = drug_data['name'].lower().strip()

        new_drug = {
            'id': new_id,
            'name': drug_data['name'],
            'aliases': drug_data.get('aliases', []),
            'category': drug_data['category'],
            'dosage': drug_data['dosage'],
            'indication': drug_data['indication'],
            'side_effects': drug_data['side_effects'],
            'warnings': drug_data['warnings'],
            'contraindications': drug_data.get('contraindications', ''),
            'price': drug_data.get('price', 0),
            'tags': drug_data.get('tags', [])
        }

        drugs[name_key] = new_drug
        self.json_helper.save_drugs(drugs)

        return new_drug

    def update_drug(self, drug_id, drug_data):
        """Update data obat"""
        drugs = self.get_drugs_dict()

        # Find and update
        for key, drug in drugs.items():
            if drug['id'] == drug_id:
                # Keep the original key if name unchanged, else update key
                old_key = key
                new_key = drug_data['name'].lower().strip()

                updated_drug = {
                    'id': drug_id,
                    'name': drug_data['name'],
                    'aliases': drug_data.get('aliases', drug.get('aliases', [])),
                    'category': drug_data.get('category', drug['category']),
                    'dosage': drug_data.get('dosage', drug['dosage']),
                    'indication': drug_data.get('indication', drug['indication']),
                    'side_effects': drug_data.get('side_effects', drug['side_effects']),
                    'warnings': drug_data.get('warnings', drug['warnings']),
                    'contraindications': drug_data.get('contraindications', drug.get('contraindications', '')),
                    'price': drug_data.get('price', drug.get('price', 0)),
                    'tags': drug_data.get('tags', drug.get('tags', []))
                }

                # Remove old key and add new key if name changed
                if old_key != new_key:
                    del drugs[old_key]

                drugs[new_key] = updated_drug
                self.json_helper.save_drugs(drugs)
                return True

        return False

    def delete_drug(self, drug_id):
        """Hapus obat dari dictionary"""
        drugs = self.get_drugs_dict()

        # Find and remove
        for key, drug in list(drugs.items()):
            if drug['id'] == drug_id:
                del drugs[key]
                self.json_helper.save_drugs(drugs)
                return True

        return False

    def search_drugs(self, keyword):
        """
        Cari obat berdasarkan keyword (enhanced search)
        Mencari di: name, aliases, category, indication, tags
        Menggunakan fungsi dari json_helper untuk konsistensi
        """
        return self.json_helper.search_drugs(keyword)

    def get_drug_interactions(self, drug_names):
        """Cek interaksi antar obat"""
        interactions = []

        # Common drug interactions database
        common_interactions = {
            'paracetamol': ['warfarin', 'carbamazepine'],
            'ibuprofen': ['aspirin', 'warfarin', 'corticosteroids'],
            'aspirin': ['warfarin', 'ibuprofen', 'corticosteroids'],
            'amoxicillin': ['allopurinol', 'warfarin'],
            'metformin': ['furosemide', 'corticosteroids'],
            'ciprofloxacin': ['theophylline', 'warfarin'],
            'simvastatin': ['gemfibrozil', 'clarithromycin'],
        }

        # Normalize drug names
        drug_names_lower = []
        for drug_name in drug_names:
            drug = self.get_drug_by_name(drug_name)
            if drug:
                drug_names_lower.append(drug['name'].lower())
            else:
                drug_names_lower.append(drug_name.lower())

        for drug in drug_names_lower:
            if drug in common_interactions:
                for interacting_drug in common_interactions[drug]:
                    if interacting_drug in drug_names_lower:
                        interactions.append({
                            'drug1': drug,
                            'drug2': interacting_drug,
                            'severity': 'Moderate to Severe',
                            'description': f"Potensi interaksi antara {drug} dan {interacting_drug}"
                        })

        return interactions

    def get_popular_drugs(self, limit=10):
        """Ambil obat populer (berdasarkan harga/usage)"""
        drugs = self.get_all_drugs()
        # Sort by price (as popularity indicator)
        return sorted(drugs, key=lambda x: x.get('price', 0), reverse=True)[:limit]

    def get_affordable_drugs(self, limit=10):
        """Ambil obat termurah"""
        drugs = self.get_all_drugs()
        return sorted(drugs, key=lambda x: x.get('price', float('inf')))[:limit]

"""
Modul Drug Recommendation
Sistem rekomendasi obat berdasarkan gejala dengan algoritma pengecekan kecocokan

@author: MedWatch Team
@maintained: Mahasiswa
@description:
    Modul ini berfungsi untuk:
    1. Merekomendasikan obat berdasarkan gejala yang diinput
    2. Mengecek apakah obat cocok untuk kondisi pasien
    3. Menampilkan efek samping dan peringatan
    4. Memberikan skor kecocokan (suitability score)
"""

import os
import json
from utils.json_helper import JSONHelper


class DrugRecommender:
    """
    Kelas untuk memberikan rekomendasi obat berdasarkan gejala
    dengan algoritma pengecekan kecocokan obat
    """

    # Pesan disclaimer yang wajib ditampilkan
    DISCLAIMER = (
        "\n"
        "═══════════════════════════════════════════════════════════════\n"
        "⚠️  PERHATIAN PENTING ⚠️\n"
        "═══════════════════════════════════════════════════════════════\n"
        "Hasil rekomendasi ini hanya untuk INFORMASI dan EDUKASI.\n"
        "Untuk diagnosis yang akurat dan pengobatan yang tepat, \n"
        "harap KONSULTASIKAN dengan DOKTER atau TENAGA KESEHATAN PROFESSIONAL.\n"
        "═══════════════════════════════════════════════════════════════\n"
    )

    def __init__(self):
        """Constructor: inisialisasi variabel yang dibutuhkan"""
        self.json_helper = JSONHelper()
        # Import drug_manager secara dinamis untuk avoid circular import
        self.drug_manager = __import__('modules.drug_data', fromlist=['DrugDataManager']).DrugDataManager()

        # Mapping gejala ke obat (database gejala-obat)
        # Format: 'gejala': ['Nama Obat 1', 'Nama Obat 2', ...]
        self.symptom_drug_map = {
            # ==================== GEJALA DEMAM & SAKIT KEPALA ====================
            'demam': ['Paracetamol', 'Ibuprofen'],
            'sakit kepala': ['Paracetamol', 'Ibuprofen', 'Aspirin'],
            'headache': ['Paracetamol', 'Ibuprofen'],
            'pilek': ['Paracetamol', 'Cetirizine', 'Chlorpheniramine'],
            'flu': ['Paracetamol', 'Vitamin C'],
            'influenza': ['Paracetamol', 'Vitamin C', 'Zinc'],

            # ==================== GEJALA BATUK ====================
            'batuk kering': ['Dextromethorphan', 'Cetirizine'],
            'batuk berdahak': ['Ambroxol', 'Bromhexine', 'Guaifenesin'],
            'batuk': ['Ambroxol', 'Dextromethorphan'],
            'sesak': ['Salbutamol'],
            'sesak napas': ['Salbutamol'],
            'asma': ['Salbutamol', 'Theophylline', 'Budesonide'],
            'radang tenggorokan': ['Amoxicillin', 'Faringosept', 'Paracetamol'],
            'sakit tenggorokan': ['Faringosept', 'Paracetamol'],

            # ==================== GEJALA ALERGI ====================
            'alergi': ['Cetirizine', 'Loratadine', 'Chlorpheniramine'],
            'gatal': ['Cetirizine', 'Loratadine', 'Chlorpheniramine', 'Dexchlorpheniramine'],
            'biduran': ['Cetirizine', 'Loratadine', 'Fexofenadine'],
            'ruam kulit': ['Cetirizine', 'Loratadine'],

            # ==================== GEJALA MASALAH PENCERNAAN ====================
            'maag': ['Omeprazole', 'Ranitidine', 'Antacida'],
            'asam lambung': ['Omeprazole', 'Ranitidine', 'Famotidine', 'Antacida'],
            'heartburn': ['Omeprazole', 'Antacida'],
            'diare': ['Loperamide', 'ORS'],
            'mencret': ['Loperamide', 'ORS'],
            'mual': ['Metoclopramide', 'Domperidone', 'Omeprazole'],
            'muntah': ['Metoclopramide', 'Domperidone', 'Ondansetron'],
            'kembung': ['Domperidone', 'Simetikon'],
            'sembelit': ['Vitamin C', 'Fiber'],

            # ==================== GEJALA NYERI ====================
            'nyeri otot': ['Ibuprofen', 'Diclofenac', 'Meloxicam'],
            'nyeri sendi': ['Diclofenac', 'Meloxicam', 'Ibuprofen'],
            'nyeri haid': ['Mefenamic Acid', 'Ibuprofen'],
            'sakit gigi': ['Paracetamol', 'Ibuprofen'],
            'nyeri': ['Ibuprofen', 'Paracetamol', 'Tramadol'],
            'sakit': ['Paracetamol', 'Ibuprofen'],

            # ==================== GEJALA INFEKSI ====================
            'infeksi bakteri': ['Amoxicillin', 'Ciprofloxacin', 'Cefadroxil', 'Azithromycin'],
            'infeksi': ['Amoxicillin', 'Ciprofloxacin'],
            'luka': ['Betadine', 'Antibiotik'],  # Betadine perlu ditambahkan ke drugs
            'radang': ['Ibuprofen', 'Dexamethasone'],

            # ==================== GEJALA KULIT ====================
            'jerawat': ['Clindamycin Topical', 'Benzoyl Peroxide', 'Salicylic Acid', 'Doxycycline', 'Zinc'],
            'acne': ['Clindamycin Topical', 'Benzoyl Peroxide'],
            'jamur': ['Clotrimazole', 'Miconazole', 'Ketoconazole'],
            'jamur kulit': ['Clotrimazole', 'Miconazole', 'Ketoconazole'],
            'panu': ['Clotrimazole', 'Ketoconazole', 'Salicylic Acid'],
            'kutu air': ['Clotrimazole', 'Miconazole'],
            'eksem': ['Desonide', 'Cetirizine'],

            # ==================== GEJALA VITAL & UMUM ====================
            'lemas': ['Vitamin C', 'Multivitamin', 'Ferrous Sulfate', 'Vitamin B Complex'],
            'kekurangan vitamin': ['Multivitamin', 'Vitamin C', 'Vitamin B Complex'],
            'daya tahan tubuh': ['Vitamin C', 'Multivitamin', 'Zinc', 'Echinacea'],
            'tulang': ['Calcium', 'Vitamin D'],
            'osteoporosis': ['Calcium', 'Vitamin D'],
            'anemia': ['Ferrous Sulfate', 'Folic Acid'],
            'kurang darah': ['Ferrous Sulfate', 'Sangobion'],

            # ==================== GEJALA HIPERTENSI ====================
            'darah tinggi': ['Amlodipine', 'Losartan', 'Captopril', 'Bisoprolol'],
            'hipertensi': ['Amlodipine', 'Losartan', 'Captopril', 'Bisoprolol', 'Hydrochlorothiazide'],
            'tekanan darah': ['Amlodipine', 'Losartan'],
            'jantung': ['Amlodipine', 'Bisoprolol'],

            # ==================== GEJALA DIABETES ====================
            'diabetes': ['Metformin', 'Glipizide', 'Glibenclamide', 'Sitagliptin'],
            'kencing manis': ['Metformin', 'Glipizide', 'Glibenclamide'],
            'gula darah': ['Metformin', 'Glipizide', 'Glibenclamide'],
            'gula darah tinggi': ['Metformin', 'Sitagliptin'],
            'insulin': ['Metformin', 'Sitagliptin'],

            # ==================== GEJALA KOLESTEROL ====================
            'kolesterol': ['Simvastatin', 'Atorvastatin', 'Fenofibrate'],
            'kolesterol tinggi': ['Simvastatin', 'Atorvastatin'],
            'lemak darah': ['Simvastatin', 'Fenofibrate'],
            'trigliserida': ['Fenofibrate', 'Atorvastatin'],

            # ==================== GEJALA ASAM URAT ====================
            'asam urat': ['Allopurinol', 'Colchicine'],
            'nyeri sendi karena asam urat': ['Colchicine', 'Ibuprofen'],
        }

    def calculate_suitability_score(self, drug, symptoms, patient_conditions=None):
        """
        Menghitung skor kecocokan obat dengan gejala dan kondisi pasien

        Args:
            drug: dict data obat
            symptoms: list gejala pasien
            patient_conditions: list kondisi medis existing pasien (opsional)

        Returns:
            dict dengan keys:
                - score: float (0-100), semakin tinggi semakin cocok
                - status: str ('COCOK', 'HATI-HATI', 'TIDAK COCOK')
                - warnings: list peringatan
                - side_effects: list efek samping yang mungkin terjadi
                - matched_symptoms: list gejala yang cocok dengan obat
        """
        score = 50  # Skor dasar
        warnings = []
        matched_symptoms = []
        side_effects = []

        # 1. Cek kecocokan dengan gejala
        drug_indication = drug['indication'].lower()
        drug_tags = [t.lower() for t in drug.get('tags', [])]

        for symptom in symptoms:
            symptom_lower = symptom.lower().strip()
            # Cek apakah gejala ada di indikasi atau tags
            if (symptom_lower in drug_indication or
                any(symptom_lower in tag for tag in drug_tags)):
                matched_symptoms.append(symptom)
                score += 15  # Tambah skor jika gejala cocok

        # 2. Cek kontraindikasi dengan kondisi pasien
        if patient_conditions:
            for condition in patient_conditions:
                condition_lower = condition.lower()
                contraindications = drug.get('contraindications', '').lower()

                if condition_lower in contraindications:
                    score -= 50  # Kurangi banyak jika ada kontraindikasi
                    warnings.append(
                        f"⛔ KONTRAINDIKASI: {drug['name']} TIDAK dianjurkan untuk pasien dengan {condition}"
                    )

                # Cek peringatan khusus berdasarkan kondisi
                if condition_lower == 'asma' and 'nsaid' in drug['category'].lower():
                    score -= 20
                    warnings.append(
                        f"⚠️ HATI-HATI: {drug['name']} dapat memicu serangan asma"
                    )

                if condition_lower in ['maag', 'ulkus', 'asam lambung'] and 'nsaid' in drug['category'].lower():
                    score -= 25
                    warnings.append(
                        f"⚠️ HATI-HATI: {drug['name']} dapat memperburuk maag/ulkus"
                    )

                if condition_lower in ['ginjal', 'gagal ginjal'] and drug.get('severity') == 'high':
                    score -= 30
                    warnings.append(
                        f"⚠️ HATI-HATI: {drug['name']} perlu penyesuaian dosis untuk gangguan ginjal"
                    )

                if condition_lower in ['hati', 'gagal hati'] and drug.get('severity') == 'high':
                    score -= 30
                    warnings.append(
                        f"⚠️ HATI-HATI: {drug['name']} perlu penyesuaian dosis untuk gangguan hati"
                    )

                if condition_lower == 'hamil' and drug.get('requires_prescription', False):
                    score -= 40
                    warnings.append(
                        f"⚠️ HATI-HATI: {drug['name']} sebaiknya dikonsultasikan dengan dokter untuk ibu hamil"
                    )

        # 3. Cek tingkat keparahan obat (severity)
        severity = drug.get('severity', 'low')
        if severity == 'high':
            score -= 10
            warnings.append(
                f"⚠️ INFO: {drug['name']} termasuk obat keras, memerlukan resep dokter"
            )
        elif severity == 'medium':
            score -= 5

        # 4. Cek efek samping dari obat
        if drug.get('side_effects'):
            # Tampilkan efek samping utama
            side_effects_list = drug['side_effects'].split(',')
            side_effects = [s.strip() for s in side_effects_list[:3]]  # Ambil 3 teratas

        # 5. Pastikan skor dalam range 0-100
        score = max(0, min(100, score))

        # 6. Tentukan status kecocokan
        if score >= 70:
            status = "✅ COCOK"
        elif score >= 40:
            status = "⚠️ HATI-HATI"
        else:
            status = "❌ TIDAK COCOK"

        return {
            'score': score,
            'status': status,
            'warnings': warnings,
            'side_effects': side_effects,
            'matched_symptoms': matched_symptoms
        }

    def recommend(self, symptoms, patient_conditions=None):
        """
        Berikan rekomendasi obat berdasarkan gejala dengan algoritma kecocokan

        Args:
            symptoms: String gejala (dipisahkan koma) atau list gejala
            patient_conditions: List kondisi medis pasien (opsional)
                Contoh: ['asma', 'maag', 'ginjal']

        Returns:
            List of recommended drugs dengan detail dan skor kecocokan
        """
        # Parse gejala jika input berupa string
        if isinstance(symptoms, str):
            symptom_list = [s.strip().lower() for s in symptoms.split(',')]
        else:
            symptom_list = [s.lower() for s in symptoms]

        # Cari obat yang cocok berdasarkan mapping gejala
        drug_recommendations = {}  # format: {drug_name: [matched_symptoms]}
        for symptom in symptom_list:
            # Cari gejala yang mirip (fuzzy match)
            for key, drugs in self.symptom_drug_map.items():
                if symptom in key or key in symptom:
                    for drug in drugs:
                        if drug not in drug_recommendations:
                            drug_recommendations[drug] = []
                        if symptom not in drug_recommendations[drug]:
                            drug_recommendations[drug].append(symptom)

        # Jika tidak ada yang cocok, cari berdasarkan keyword di indication/tags
        if not drug_recommendations:
            drugs_dict = self.drug_manager.get_drugs_dict()
            for drug in drugs_dict.values():
                for symptom in symptom_list:
                    if (symptom in drug['indication'].lower() or
                        any(symptom in tag.lower() for tag in drug.get('tags', []))):
                        if drug['name'] not in drug_recommendations:
                            drug_recommendations[drug['name']] = []
                        drug_recommendations[drug['name']].append(symptom)

        # Hitung skor kecocokan untuk setiap obat
        drugs_dict = self.drug_manager.get_drugs_dict()
        results = []

        for drug_name, matched_symptoms in drug_recommendations.items():
            # Cari detail obat dari dictionary
            drug_detail = self.get_drug_detail(drugs_dict, drug_name)

            if drug_detail:
                # Hitung skor kecocokan
                suitability = self.calculate_suitability_score(
                    drug_detail,
                    symptom_list,
                    patient_conditions or []
                )

                results.append({
                    'name': drug_detail['name'],
                    'category': drug_detail['category'],
                    'dosage': drug_detail['dosage'],
                    'indication': drug_detail['indication'],
                    'side_effects': drug_detail['side_effects'],
                    'warnings': drug_detail['warnings'],
                    'contraindications': drug_detail.get('contraindications', ''),
                    'price': drug_detail.get('price', 0),
                    'severity': drug_detail.get('severity', 'low'),
                    'requires_prescription': drug_detail.get('requires_prescription', False),
                    # Data dari algoritma
                    'matched_symptoms': ', '.join(matched_symptoms),
                    'suitability_score': suitability['score'],
                    'suitability_status': suitability['status'],
                    'suitability_warnings': suitability['warnings'],
                    'potential_side_effects': suitability['side_effects']
                })
            else:
                # Default info jika obat tidak ada di database
                results.append({
                    'name': drug_name,
                    'category': 'Umum',
                    'dosage': 'Sesuai resep dokter',
                    'indication': f'Meredakan: {", ".join(matched_symptoms)}',
                    'side_effects': 'Konsumsi sesuai dosis yang dianjurkan',
                    'warnings': 'Konsultasikan dengan dokter',
                    'contraindications': '-',
                    'price': 0,
                    'severity': 'unknown',
                    'requires_prescription': True,
                    'matched_symptoms': ', '.join(matched_symptoms),
                    'suitability_score': 50,
                    'suitability_status': '⚠️ HATI-HATI',
                    'suitability_warnings': ['⚠️ Obat ini tidak lengkap datanya, konsultasikan dengan dokter'],
                    'potential_side_effects': []
                })

        # Sort berdasarkan skor kecocokan (tertinggi dulu)
        results.sort(key=lambda x: x['suitability_score'], reverse=True)

        return results

    def format_recommendation_text(self, symptoms, recommendations):
        """
        Format hasil rekomendasi menjadi teks yang mudah dibaca

        Args:
            symptoms: string gejala
            recommendations: list hasil rekomendasi dari fungsi recommend()

        Returns:
            string teks yang sudah diformat
        """
        result_text = f"{'='*65}\n"
        result_text += f"  HASIL REKOMENDASI OBAT\n"
        result_text += f"  Gejala: {symptoms}\n"
        result_text += f"{'='*65}\n\n"

        if not recommendations:
            result_text += "❌ Tidak ditemukan rekomendasi obat untuk gejala tersebut.\n"
            result_text += "   Silakan konsultasi dengan dokter untuk diagnosis lebih lanjut.\n"
        else:
            # Tambahkan disclaimer
            result_text += self.DISCLAIMER + "\n"

            for i, rec in enumerate(recommendations, 1):
                result_text += f"\n{'─'*65}\n"
                result_text += f"  #{i} - {rec['name']}\n"
                result_text += f"{'─'*65}\n"
                result_text += f"  Status Kecocokan: {rec['suitability_status']} "
                result_text += f"(Skor: {rec['suitability_score']}/100)\n"
                result_text += f"  Kategori: {rec['category']}\n"
                result_text += f"  Dosis: {rec['dosage']}\n"
                result_text += f"  Indikasi: {rec['indication']}\n"

                # Tampilkan gejala yang cocok
                if rec['matched_symptoms']:
                    result_text += f"  Cocok untuk: {rec['matched_symptoms']}\n"

                # Tampilkan efek samping yang mungkin
                if rec['potential_side_effects']:
                    result_text += f"  Efek Samping: {', '.join(rec['potential_side_effects'])}\n"
                else:
                    result_text += f"  Efek Samping: {rec['side_effects']}\n"

                # Tampilkan peringatan khusus dari algoritma
                if rec['suitability_warnings']:
                    result_text += f"\n  ⚠️ PERINGATAN KHUSUS:\n"
                    for warning in rec['suitability_warnings']:
                        result_text += f"     {warning}\n"

                # Peringatan umum dari obat
                result_text += f"  Peringatan: {rec['warnings']}\n"

                # Tampilkan apakah butuh resep
                if rec['requires_prescription']:
                    result_text += f"  📝 Memerlukan resep dokter\n"

                # Harga
                if rec['price'] > 0:
                    result_text += f"  Harga estimasi: Rp {rec['price']:,}\n"

            # Tambahkan penutup
            result_text += f"\n{'='*65}\n"
            result_text += "  INGAT: Selalu konsultasikan dengan dokter atau tenaga medis\n"
            result_text += "  sebelum mengonsumsi obat-obatan.\n"
            result_text += f"{'='*65}\n"

        return result_text

    def get_drug_detail(self, drugs_dict, name):
        """
        Ambil detail obat dari dictionary (O(1) lookup)

        Args:
            drugs_dict: dictionary obat (atau list untuk backward compatibility)
            name: nama obat yang dicari

        Returns:
            dict data obat atau None jika tidak ditemukan
        """
        # Handle jika drugs_dict adalah list (backward compatibility)
        if isinstance(drugs_dict, list):
            for drug in drugs_dict:
                if name.lower() in drug['name'].lower():
                    return drug
            return None

        name_lower = name.lower().strip()

        # Direct match (paling cepat)
        if isinstance(drugs_dict, dict) and name_lower in drugs_dict:
            return drugs_dict[name_lower]

        # Search in aliases
        for drug in drugs_dict.values():
            if 'aliases' in drug:
                for alias in drug['aliases']:
                    if name_lower == alias.lower():
                        return drug

        # Partial match
        for drug in drugs_dict.values():
            if name_lower in drug['name'].lower():
                return drug

        return None

    def search_drugs(self, keyword):
        """
        Search drugs by keyword (nama, kategori, indikasi, tags)

        Args:
            keyword: kata kunci pencarian

        Returns:
            list of drug dicts
        """
        return self.drug_manager.search_drugs(keyword)

    def get_alternatives(self, drug_name):
        """
        Dapatkan alternatif obat berdasarkan kategori yang sama

        Args:
            drug_name: nama obat yang ingin dicari alternatifnya

        Returns:
            list obat alternatif
        """
        drug = self.drug_manager.get_drug_by_name(drug_name)

        if not drug:
            return []

        drugs_dict = self.drug_manager.get_drugs_dict()

        # Handle jika drugs_dict adalah list
        if isinstance(drugs_dict, list):
            return [
                d for d in drugs_dict
                if d['category'] == drug['category'] and d['name'].lower() != drug['name'].lower()
            ]

        alternatives = []

        for d in drugs_dict.values():
            if (d['category'] == drug['category'] and
                d['name'].lower() != drug['name'].lower()):
                alternatives.append(d)

        return alternatives

    def check_drug_interactions(self, drug_list):
        """
        Cek interaksi antar obat

        Args:
            drug_list: list nama obat yang akan dikonsumsi bersama

        Returns:
            list interaksi yang ditemukan
        """
        interactions = []

        # Database interaksi obat (simplified)
        interaction_db = {
            'paracetamol': ['warfarin', 'carbamazepine'],
            'ibuprofen': ['aspirin', 'warfarin', 'corticosteroids', 'antihypertensive'],
            'aspirin': ['warfarin', 'ibuprofen', 'corticosteroids'],
            'amoxicillin': ['allopurinol', 'warfarin', 'oral contraceptives'],
            'metformin': ['furosemide', 'corticosteroids', 'diuretics'],
            'ciprofloxacin': ['theophylline', 'warfarin', 'tizanidine'],
            'simvastatin': ['gemfibrozil', 'clarithromycin', 'itraconazole'],
            'digoxin': ['amiodarone', 'quinidine', 'verapamil'],
        }

        drug_list_lower = [d.lower() for d in drug_list]

        for drug in drug_list_lower:
            if drug in interaction_db:
                for interacting_drug in interaction_db[drug]:
                    if interacting_drug in drug_list_lower:
                        interactions.append({
                            'drug1': drug,
                            'drug2': interacting_drug,
                            'severity': 'Medium to High',
                            'description': f"⚠️ Potensi interaksi antara {drug} dan {interacting_drug}"
                        })

        return interactions

    def get_all_categories(self):
        """Get all drug categories"""
        return self.drug_manager.get_all_categories()

    def get_drug_by_name(self, name):
        """Get drug by name using dictionary lookup"""
        return self.drug_manager.get_drug_by_name(name)

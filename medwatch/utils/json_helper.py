"""
JSON Helper Module
Helper functions untuk operasi JSON dengan format dictionary untuk drug data
@author: MedWatch Team
@maintained: Mahasiswa
"""

import os
import json


class JSONHelper:
    """
    Kelas helper untuk operasi JSON
    Menangani pembacaan dan penulisan data ke file JSON
    """

    def __init__(self, base_dir="data"):
        """Constructor: inisialisasi path direktori data"""
        self.base_dir = base_dir
        self.ensure_data_files()

    def ensure_data_files(self):
        """
        Membuat file data jika belum ada
        Termasuk data default untuk users, patients, medical records, dan drugs
        """
        # Buat folder data jika belum ada
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        # Data default untuk setiap file
        default_files = {
            'users.json': [
                {'username': 'dokter1', 'password': 'dokter123', 'role': 'dokter', 'name': 'Dr. Andi Wijaya'},
                {'username': 'dokter2', 'password': 'dokter123', 'role': 'dokter', 'name': 'Dr. Sari Pertiwi'},
                {'username': 'pasien1', 'password': 'pasien123', 'role': 'pasien', 'name': 'Budi Santoso'},
                {'username': 'pasien2', 'password': 'pasien123', 'role': 'pasien', 'name': 'Siti Rahayu'},
            ],
            'patients.json': [
                {
                    'id': 1, 'name': 'Budi Santoso', 'age': 35, 'gender': 'Laki-laki',
                    'phone': '08123456789', 'blood_type': 'A+', 'address': 'Jl. Merdeka No. 123, Jakarta',
                    'username': 'pasien1', 'conditions': ['asma']  # kondisi medis existing
                },
                {
                    'id': 2, 'name': 'Siti Rahayu', 'age': 28, 'gender': 'Perempuan',
                    'phone': '08234567890', 'blood_type': 'O+', 'address': 'Jl. Sudirman No. 45, Bandung',
                    'username': 'siti123', 'conditions': []
                },
            ],
            'medical_records.json': [
                {
                    'id': 1, 'patient_id': 1, 'date': '2024-01-15',
                    'diagnosis': 'Demam berdarah', 'medications': 'Paracetamol 500mg, Elektrolik',
                    'notes': 'Pasien dirawat inap 3 hari', 'doctor': 'Dr. Andi Wijaya'
                },
                {
                    'id': 2, 'patient_id': 2, 'date': '2024-02-10',
                    'diagnosis': 'Influenza', 'medications': 'Paracetamol 500mg, Vitamin C',
                    'notes': 'Istirahat cukup', 'doctor': 'Dr. Andi Wijaya'
                },
            ],
            # ==================== DATABASE OBAT (FORMAT DICTIONARY) ====================
            # Key: nama obat lowercase untuk O(1) lookup (pencarian cepat)
            # Setiap obat memiliki: id, name, aliases, category, dosage, indication,
            #                         side_effects, warnings, contraindications, price, tags, severity
            'drugs.json': {
                # ==================== OBAT DEMAM & SAKIT KEPALA ====================
                'paracetamol': {
                    'id': 1, 'name': 'Paracetamol',
                    'aliases': ['parasetamol', 'panadol', 'tamiflu', 'biogesic', 'sanmol', 'termorex'],
                    'category': 'Analgesik & Antipiretik',
                    'dosage': '500mg, 3-4x sehari (maksimal 4g/hari untuk dewasa)',
                    'indication': 'demam sakit kepala nyeri ringan influenza nyeri otot',
                    'side_effects': 'Jarang, ruam kulit pada dosis tinggi, kerusakan hati jika overdosis',
                    'warnings': 'Hati-hati pada pasien gangguan hati, jangan konsumsi alkohol',
                    'contraindications': 'Hipersensitif terhadap paracetamol, gangguan hati berat',
                    'price': 5000, 'tags': ['demam', 'sakit kepala', 'nyeri', 'flu', 'influenza'],
                    'severity': 'low', 'requires_prescription': False
                },
                'ibuprofen': {
                    'id': 2, 'name': 'Ibuprofen',
                    'aliases': ['advil', 'motrin', 'brufen', 'proris'],
                    'category': 'NSAID (Anti-inflammatory)',
                    'dosage': '200-400mg, 2-3x sehari sesudah makan',
                    'indication': 'nyeri sedang radang demam nyeri otot sakit gigi nyeri sendi',
                    'side_effects': 'Mual, sakit kepala, gangguan lambung, maag, pusing',
                    'warnings': 'Hati-hati pada pasien maag, asma, ginal, usia lanjut',
                    'contraindications': 'Ulkus peptik, gangguan ginjal berat, hamil trimester 3',
                    'price': 8000, 'tags': ['nyeri', 'demam', 'radang', 'nyeri otot', 'sakit gigi', 'nyeri sendi'],
                    'severity': 'medium', 'requires_prescription': False
                },
                'aspirin': {
                    'id': 3, 'name': 'Aspirin',
                    'aliases': ['asam asetilsalisilat', 'aspilet', 'cardipirin'],
                    'category': 'NSAID & Antiplatelet',
                    'dosage': '300-600mg, 3-4x sehari (untuk nyeri), 80-100mg (untuk jantung)',
                    'indication': 'sakit kepala demam nyeri ringan pencegahan serangan jantung',
                    'side_effects': 'Irritasi lambung, tinitus (telinga berdenging), perdarahan',
                    'warnings': 'Hati-hati pada pasien maag, tidak untuk anak <12 tahun (sindrom Reye)',
                    'contraindications': 'Ulkus aktif, hemofilia, anak <12 tahun, ibu menyusui',
                    'price': 6000, 'tags': ['sakit kepala', 'demam', 'nyeri', 'jantung'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'mefenamic_acid': {
                    'id': 4, 'name': 'Mefenamic Acid',
                    'aliases': ['ponstan', 'mefenamat', 'ponstan'],
                    'category': 'NSAID',
                    'dosage': '500mg, 3x sehari sesudah makan',
                    'indication': 'nyeri haid nyeri ringan sedang sakit kepala',
                    'side_effects': 'Mual, diare, ruam kulit, pusing',
                    'warnings': 'Hati-hati pada pasien maag, dapat menyebabkan perdarahan lambung',
                    'contraindications': 'Ulkus peptik, gangguan ginjal',
                    'price': 9000, 'tags': ['nyeri haid', 'nyeri', 'haid', 'menstruasi'],
                    'severity': 'medium', 'requires_prescription': False
                },
                'diclofenac': {
                    'id': 5, 'name': 'Diclofenac',
                    'aliases': ['cataflam', 'voltaren', 'na-diclofenac', 'kaltrofen'],
                    'category': 'NSAID',
                    'dosage': '50mg, 2-3x sehari (tablet), 1-2x sehari (injeksi)',
                    'indication': 'nyeri sendi radang nyeri otot sakit punggung nyeri pasca operasi',
                    'side_effects': 'Sakit maag, pusing, mual, diare, kerusakan ginjal',
                    'warnings': 'Hati-hati pada pasien maag dan ginjal',
                    'contraindications': 'Ulkus peptik, gagal jantung, hamil trimester 3',
                    'price': 10000, 'tags': ['nyeri', 'radang', 'nyeri sendi', 'nyeri otot', 'sendi'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'meloxicam': {
                    'id': 6, 'name': 'Meloxicam',
                    'aliases': ['moxicam', 'melox'],
                    'category': 'NSAID (COX-2 Inhibitor)',
                    'dosage': '7.5-15mg, 1x sehari',
                    'indication': 'nyeri sendi radang sendi osteoartritis rheumatoid arthritis',
                    'side_effects': 'Mual, sakit kepala, pusing, edema',
                    'warnings': 'Hati-hati pada pasien jantung dan ginjal',
                    'contraindications': 'Ulkus peptik, gagal jantung',
                    'price': 15000, 'tags': ['nyeri sendi', 'radang sendi', 'artritis', 'sendi'],
                    'severity': 'medium', 'requires_prescription': True
                },

                # ==================== ANTIBIOTIK ====================
                'amoxicillin': {
                    'id': 7, 'name': 'Amoxicillin',
                    'aliases': ['amoxil', 'amoxan', 'yusimox', 'hopacil'],
                    'category': 'Antibiotik (Penisilin)',
                    'dosage': '500mg, 3x sehari selama 5-7 hari',
                    'indication': 'infeksi bakteri ispa uti kulit radang tenggorokan infeksi telinga',
                    'side_effects': 'Mual, diare, ruam kulit, alergi',
                    'warnings': 'Selesaikan dosis penuh meski gejala membaik, bisa menyebabkan diare',
                    'contraindications': 'Hipersensitif terhadap penisilin, mononukleosis',
                    'price': 12000, 'tags': ['infeksi', 'bakteri', 'radang', 'ISPA', 'tenggorokan', 'telinga'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'amoxicillin_clavulanate': {
                    'id': 8, 'name': 'Amoxicillin-Clavulanate',
                    'aliases': ['augmentin', 'yusimox forte', 'hopacil forte'],
                    'category': 'Antibiotik (Penisilin + Inhibitor Beta-laktamase)',
                    'dosage': '500mg/125mg, 3x sehari',
                    'indication': 'infeksi bakteri berat sinusitis pneumonia infeksi saluran kemih',
                    'side_effects': 'Diare lebih sering, mual, ruam kulit',
                    'warnings': 'Risiko diare lebih tinggi, hati-hati pada gangguan hati',
                    'contraindications': 'Hipersensitif terhadap penisilin',
                    'price': 20000, 'tags': ['infeksi', 'bakteri', 'sinusitis', 'pneumonia'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'ciprofloxacin': {
                    'id': 9, 'name': 'Ciprofloxacin',
                    'aliases': ['cipro', 'baquinor', 'ciproflox'],
                    'category': 'Antibiotik (Fluorokuinolon)',
                    'dosage': '500mg, 2x sehari',
                    'indication': 'infeksi saluran kemih infeksi berat iska diarrhea bakteri',
                    'side_effects': 'Mual, pusing, ruam, sensitif terhadap sinar matahari',
                    'warnings': 'Hindari sinar matahari berlebih, bisa menyebabkan tendonitis',
                    'contraindications': 'Hamil, anak <18 tahun, epilepsi',
                    'price': 15000, 'tags': ['infeksi', 'bakteri', 'ISKA', 'UTI', 'saluran kemih'],
                    'severity': 'high', 'requires_prescription': True
                },
                'cefadroxil': {
                    'id': 10, 'name': 'Cefadroxil',
                    'aliases': ['cefadro', 'cefadrox', 'duricef'],
                    'category': 'Antibiotik (Sefalosporin Generasi 1)',
                    'dosage': '500mg, 2x sehari',
                    'indication': 'infeksi kulit infeksi saluran kemih radang tenggorokan',
                    'side_effects': 'Mual, diare, ruam kulit',
                    'warnings': 'Hati-hati pada pasien alergi penisilin (cross-reactivity)',
                    'contraindications': 'Hipersensitif terhadap sefalosporin',
                    'price': 13000, 'tags': ['infeksi', 'bakteri', 'kulit', 'UTI'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'azithromycin': {
                    'id': 11, 'name': 'Azithromycin',
                    'aliases': ['azitral', 'zithromax', 'azomax'],
                    'category': 'Antibiotik (Makrolida)',
                    'dosage': '500mg hari pertama, lalu 250mg/hari selama 4 hari',
                    'indication': 'infeksi saluran napas radang tenggorokan pneumonia',
                    'side_effects': 'Mual, diare, sakit perut',
                    'warnings': 'Hati-hati pada gangguan hati',
                    'contraindications': 'Hipersensitif terhadap makrolida',
                    'price': 18000, 'tags': ['infeksi', 'napas', 'tenggorokan', 'pneumonia'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'doxycycline': {
                    'id': 12, 'name': 'Doxycycline',
                    'aliases': ['doxy', 'doxycin', 'vibramycin'],
                    'category': 'Antibiotik (Tetrasiklin)',
                    'dosage': '100mg, 2x sehari',
                    'indication': 'jerawat infeksi malaria klamidia malaria',
                    'side_effects': 'Fotosensitivitas, mual, diare, esofagitis',
                    'warnings': 'Hindari sinar matahari, minum banyak air, jangan berbaring setelah minum',
                    'contraindications': 'Hamil, anak <8 tahun, menyusui',
                    'price': 8000, 'tags': ['jerawat', 'infeksi', 'malaria', 'kulit'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'metronidazole': {
                    'id': 13, 'name': 'Metronidazole',
                    'aliases': ['flagyl', 'metronid', 'agifloc'],
                    'category': 'Antibiotik & Antiprotozoa',
                    'dosage': '500mg, 3x sehari',
                    'indication': 'infeksi parasit diarrhea amubiasis vaginitis trichomonas',
                    'side_effects': 'Mual, metal taste (rasa logam di mulut), tidak boleh minum alkohol',
                    'warnings': 'JANGAN minum alkohol saat konsumsi (efek disulfiram)',
                    'contraindications': 'Trimester pertama kehamilan',
                    'price': 7000, 'tags': ['parasit', 'diare', 'amubiasis', 'vagina'],
                    'severity': 'high', 'requires_prescription': True
                },

                # ==================== OBAT BATUK & TENGGOROKAN ====================
                'ambroxol': {
                    'id': 14, 'name': 'Ambroxol',
                    'aliases': ['mucos', 'bisoltus', 'ambrolex'],
                    'category': 'Mukolitik (Pengencer Dahak)',
                    'dosage': '30mg, 3x sehari',
                    'indication': 'batuk berdahak dahak kental sulit keluar',
                    'side_effects': 'Mual, diare, nyeri lambung',
                    'warnings': 'Hati-hati pada pasien tukak lambung',
                    'contraindications': 'Hipersensitif terhadap ambroxol',
                    'price': 7000, 'tags': ['batuk', 'batuk berdahak', 'dahak', 'lendir'],
                    'severity': 'low', 'requires_prescription': False
                },
                'dextromethorphan': {
                    'id': 15, 'name': 'Dextromethorphan',
                    'aliases': ['dekstrometorfan', 'obat batuk kering', 'hit'],  # hit = herba in plus
                    'category': 'Antitusif (Penekan Batuk)',
                    'dosage': '10-20mg, 3-4x sehari',
                    'indication': 'batuk kering non-produktif batuk tanpa dahak',
                    'side_effects': 'Mengantuk, pusing, mual, konstipasi',
                    'warnings': 'Tidak untuk batuk berdahak, hati-hati overdosis',
                    'contraindications': 'Sedang minum MAOI, asma berat',
                    'price': 8500, 'tags': ['batuk', 'batuk kering', 'kering'],
                    'severity': 'low', 'requires_prescription': False
                },
                'bromhexine': {
                    'id': 16, 'name': 'Bromhexine',
                    'aliases': ['bisolvon', 'bromhex'],
                    'category': 'Mukolitik',
                    'dosage': '8mg, 3x sehari',
                    'indication': 'batuk berdahak dahak kental',
                    'side_effects': 'Mual, sakit kepala, pusing',
                    'warnings': 'Hati-hati pada pasien maag',
                    'contraindications': 'Hipersensitif',
                    'price': 7500, 'tags': ['batuk', 'batuk berdahak', 'dahak'],
                    'severity': 'low', 'requires_prescription': False
                },
                'guaifenesin': {
                    'id': 17, 'name': 'Guaifenesin',
                    'aliases': ['guaifenesin', 'expectorant'],
                    'category': 'Ekspektoran (Pelancar Dahak)',
                    'dosage': '200-400mg, 4x sehari',
                    'indication': 'batuk berdahak pilek flu',
                    'side_effects': 'Mual, muntah, pusing',
                    'warnings': 'Hati-hati pada pasien asma',
                    'contraindications': 'Hipersensitif',
                    'price': 6500, 'tags': ['batuk', 'dahak', 'pilek', 'flu'],
                    'severity': 'low', 'requires_prescription': False
                },
                'faringosept': {
                    'id': 18, 'name': 'Faringosept',
                    'aliases': ['faringosept', 'lozenges'],
                    'category': 'Antiseptik Tenggorokan',
                    'dosage': '1 tablet, 4-5x sehari (hisap)',
                    'indication': 'sakit tenggorokan radang tenggorokan faringitis',
                    'side_effects': 'Jarang, iritasi ringan',
                    'warnings': 'Jangan langsung ditelah setelah hisap',
                    'contraindications': 'Hipersensitif',
                    'price': 4000, 'tags': ['tenggorokan', 'radang', 'faringitis', 'sakitt tenggorokan'],
                    'severity': 'low', 'requires_prescription': False
                },

                # ==================== OBAT ALERGI ====================
                'cetirizine': {
                    'id': 19, 'name': 'Cetirizine',
                    'aliases': ['ctrizine', 'zyrtec', 'allerzit', 'incizine'],
                    'category': 'Antihistamin Generasi 2',
                    'dosage': '10mg, 1x sehari (malam hari)',
                    'indication': 'alergi rhinitis alergi gatal biduran pilek alergi',
                    'side_effects': 'Mengantuk (jarang), mulut kering, kelelahan, sakit kepala',
                    'warnings': 'Hati-hati saat mengemudi atau operasi mesin',
                    'contraindications': 'Gagal ginjal berat, hipersensitif',
                    'price': 6000, 'tags': ['alergi', 'gatal', 'biduran', 'pilek', 'rhinitis'],
                    'severity': 'low', 'requires_prescription': False
                },
                'loratadine': {
                    'id': 20, 'name': 'Loratadine',
                    'aliases': ['claritin', 'allerta', 'loratin'],
                    'category': 'Antihistamin Generasi 2',
                    'dosage': '10mg, 1x sehari',
                    'indication': 'alergi gatal biduran rhinitis rinitis alergi',
                    'side_effects': 'Sakit kepala, mulut kering, kelelahan',
                    'warnings': 'Dapat menyebabkan kantuk pada beberapa orang',
                    'contraindications': 'Hipersensitif',
                    'price': 7000, 'tags': ['alergi', 'gatal', 'biduran', 'rhinitis'],
                    'severity': 'low', 'requires_prescription': False
                },
                'chlorpheniramine': {
                    'id': 21, 'name': 'Chlorpheniramine Maleate (CTM)',
                    'aliases': ['ctm', 'chlorphen', 'allergenta'],
                    'category': 'Antihistamin Generasi 1',
                    'dosage': '4mg, 3-4x sehari',
                    'indication': 'alergi gatal biduran pilek',
                    'side_effects': 'MENGANTUK berat, mulut kering, pandangan kabur',
                    'warnings': 'Sangat menyebabkan kantuk, jangan mengemudi',
                    'contraindications': 'Glakoma, BPH, asma',
                    'price': 3000, 'tags': ['alergi', 'gatal', 'biduran', 'pilek'],
                    'severity': 'low', 'requires_prescription': False
                },
                'dexchlorpheniramine': {
                    'id': 22, 'name': 'Dexchlorpheniramine',
                    'aliases': ['dexchlor', 'sch'],
                    'category': 'Antihistamin',
                    'dosage': '2mg, 3x sehari',
                    'indication': 'alergi gatal pilek',
                    'side_effects': 'Mengantuk, mulut kering',
                    'warnings': 'Hati-hati saat mengemudi',
                    'contraindications': 'Hipersensitif',
                    'price': 5000, 'tags': ['alergi', 'gatal', 'pilek'],
                    'severity': 'low', 'requires_prescription': False
                },
                'fexofenadine': {
                    'id': 23, 'name': 'Fexofenadine',
                    'aliases': ['telfast', 'allegra', 'fexo'],
                    'category': 'Antihistamin Generasi 3',
                    'dosage': '120-180mg, 1x sehari',
                    'indication': 'alergi rhinitis gatal biduran',
                    'side_effects': 'Sakit kepala, mual, pusing',
                    'warnings': 'Minimal efek kantuk',
                    'contraindications': 'Hipersensitif',
                    'price': 12000, 'tags': ['alergi', 'rhinitis', 'gatal', 'biduran'],
                    'severity': 'low', 'requires_prescription': False
                },
                'ketotifen': {
                    'id': 24, 'name': 'Ketotifen',
                    'aliases': ['ketotifen', 'posifen'],
                    'category': 'Antihistamin & Mast Cell Stabilizer',
                    'dosage': '1mg, 2x sehari',
                    'indication': 'alergi gatal asma alergi preventif',
                    'side_effects': 'Mengantuk, penambahan berat badan',
                    'warnings': 'Efek muncul setelah beberapa minggu',
                    'contraindications': 'Hipersensitif',
                    'price': 8000, 'tags': ['alergi', 'gatal', 'asma'],
                    'severity': 'low', 'requires_prescription': True
                },

                # ==================== OBAT LAMBUNG & PENCERNAAN ====================
                'omeprazole': {
                    'id': 25, 'name': 'Omeprazole',
                    'aliases': ['promil', 'prolac', 'loxigamma'],
                    'category': 'PPI (Proton Pump Inhibitor)',
                    'dosage': '20mg, 1x sehari sebelum makan (pagi)',
                    'indication': 'gerd maag tukak lambung asam lambung heartburn',
                    'side_effects': 'Sakit kepala, diare, konstipasi',
                    'warnings': 'Gunakan sesuai durasi yang dianjurkan, jangan jangka panjang',
                    'contraindications': 'Hipersensitif terhadap omeprazole',
                    'price': 10000, 'tags': ['maag', 'asam lambung', 'GERD', 'tukak', 'heartburn'],
                    'severity': 'low', 'requires_prescription': False
                },
                'esomeprazole': {
                    'id': 26, 'name': 'Esomeprazole',
                    'aliases': ['nexium', 'nexium'],
                    'category': 'PPI',
                    'dosage': '20-40mg, 1x sehari',
                    'indication': 'gerd maag tukak lambung asam lambung',
                    'side_effects': 'Sakit kepala, diare, kram perut',
                    'warnings': 'Hati-hati penggunaan jangka panjang',
                    'contraindications': 'Hipersensitif',
                    'price': 15000, 'tags': ['maag', 'asam lambung', 'GERD'],
                    'severity': 'low', 'requires_prescription': True
                },
                'ranitidine': {
                    'id': 27, 'name': 'Ranitidine',
                    'aliases': ['zanid', 'gastrid', 'ranitin'],
                    'category': 'H2 Blocker (Antagonis H2)',
                    'dosage': '150mg, 2x sehari',
                    'indication': 'maag asam lambung tukak lambung heartburn',
                    'side_effects': 'Sakit kepala, pusing, kelelahan',
                    'warnings': 'Hati-hati pada pasien ginjal',
                    'contraindications': 'Hipersensitif',
                    'price': 8000, 'tags': ['maag', 'asam lambung', 'heartburn'],
                    'severity': 'low', 'requires_prescription': False
                },
                'famotidine': {
                    'id': 28, 'name': 'Famotidine',
                    'aliases': ['pepcid', 'famo'],
                    'category': 'H2 Blocker',
                    'dosage': '20-40mg, 2x sehari',
                    'indication': 'maag asam lambung tukak lambung',
                    'side_effects': 'Sakit kepala, pusing, konstipasi',
                    'warnings': 'Hati-hati pada gangguan ginjal',
                    'contraindications': 'Hipersensitif',
                    'price': 10000, 'tags': ['maag', 'asam lambung'],
                    'severity': 'low', 'requires_prescription': False
                },
                'antacida': {
                    'id': 29, 'name': 'Antacida (Mg(OH)2 + Al(OH)3)',
                    'aliases': ['mylanta', 'maalox', 'promag'],
                    'category': 'Antasida',
                    'dosage': '1-2 tablet, 3-4x sehari sesudah makan',
                    'indication': 'maag asam lambung heartburn kembung',
                    'side_effects': 'Konstipasi (Al) atau diare (Mg)',
                    'warnings': 'Hati-hati pada pasien ginjal',
                    'contraindications': 'Hipersensitif',
                    'price': 5000, 'tags': ['maag', 'asam lambung', 'heartburn', 'kembung'],
                    'severity': 'low', 'requires_prescription': False
                },
                'metoclopramide': {
                    'id': 30, 'name': 'Metoclopramide',
                    'aliases': ['primperan', 'metoclo', 'clopramide'],
                    'category': 'Prokinetik (Antiemetik)',
                    'dosage': '10mg, 3x sehari sebelum makan',
                    'indication': 'mual muntah gangguan lambung rasa penuh di perut',
                    'side_effects': 'Kantuk, pusing, tremor, ekstrapiramidal',
                    'warnings': 'Hati-hati penggunaan jangka panjang, bisa menyebabkan diskinesia',
                    'contraindications': 'Epilepsi, feokromositoma',
                    'price': 6000, 'tags': ['mual', 'muntah', 'lambung', 'maag'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'domperidone': {
                    'id': 31, 'name': 'Domperidone',
                    'aliases': ['motilium', 'domperon', 'emedom'],
                    'category': 'Prokinetik',
                    'dosage': '10mg, 3x sehari sebelum makan',
                    'indication': 'mual muntah rasa penuh di perut kembung',
                    'side_effects': 'Kram perut, diare, pusing',
                    'warnings': 'Hati-hati pada penyakit jantung',
                    'contraindications': 'Prolaktinoma, gangguan hati berat',
                    'price': 8000, 'tags': ['mual', 'muntah', 'kembung', 'lambung'],
                    'severity': 'low', 'requires_prescription': False
                },
                'loperamide': {
                    'id': 32, 'name': 'Loperamide',
                    'aliases': ['imodium', 'diatab', 'diarstop'],
                    'category': 'Antidiare',
                    'dosage': '2mg awal, lalu 1mg setiap buang air besar (maks 16mg/hari)',
                    'indication': 'diare akut diare',
                    'side_effects': 'Sembelit, pusing, keringat berlebih',
                    'warnings': 'Tidak untuk diare infeksius/bakteri (hanya simtomatik)',
                    'contraindications': 'Kolitis ulserativa, diare berdarah',
                    'price': 5000, 'tags': ['diare', 'mencret'],
                    'severity': 'low', 'requires_prescription': False
                },
                'ors': {
                    'id': 33, 'name': 'Oralit (ORS)',
                    'aliases': ['ors', 'oralit', 'electrolyte'],
                    'category': 'Rehidrasi Oral',
                    'dosage': '1 sachet larut dalam 200ml air, minum sesering mungkin',
                    'indication': 'diare dehidrasi kekurangan cairan',
                    'side_effects': 'Jarang',
                    'warnings': 'Larutkan dengan air matang, jangan dengan air gula',
                    'contraindications': '-',
                    'price': 2000, 'tags': ['diare', 'dehidrasi', 'cairan'],
                    'severity': 'low', 'requires_prescription': False
                },

                # ==================== VITAMIN & SUPELEMEN ====================
                'vitamin_c': {
                    'id': 34, 'name': 'Vitamin C',
                    'aliases': ['askorbat', 'vit c', 'ascorbic acid', 'holocare'],
                    'category': 'Vitamin (Asam Askorbat)',
                    'dosage': '500-1000mg, 1-2x sehari',
                    'indication': 'suplemen daya tahan tubuh lemas kekurangan vitamin sariawan',
                    'side_effects': 'Diare pada dosis tinggi, batu ginjal (jarang)',
                    'warnings': 'Hati-hati pada pasien batu ginjal',
                    'contraindications': 'Hipersensitif terhadap vitamin C',
                    'price': 3000, 'tags': ['vitamin', 'daya tahan tubuh', 'lemas', 'sariawan'],
                    'severity': 'low', 'requires_prescription': False
                },
                'vitamin_b_complex': {
                    'id': 35, 'name': 'Vitamin B Complex',
                    'aliases': ['vit b', 'b complex', 'neurobion'],
                    'category': 'Vitamin B Kompleks',
                    'dosage': '1 tablet, 1-3x sehari',
                    'indication': 'lemas saraf kejepit kekurangan vitamin b neuritis',
                    'side_effects': 'Urine kuning, mual',
                    'warnings': 'Urine berwarna kuning adalah normal',
                    'contraindications': 'Hipersensitif',
                    'price': 5000, 'tags': ['vitamin', 'lemas', 'saraf', 'neuritis'],
                    'severity': 'low', 'requires_prescription': False
                },
                'multivitamin': {
                    'id': 36, 'name': 'Multivitamin',
                    'aliases': ['sangobion', 'imboost', 'stimuno', 'profertil'],
                    'category': 'Multivitamin',
                    'dosage': '1 kapsul/tablet, 1x sehari',
                    'indication': 'lemas daya tahan tubuh rendah kekurangan vitamin',
                    'side_effects': 'Jarang',
                    'warnings': 'Hati-hati pada penggunaan jangka panjang',
                    'contraindications': 'Hipersensitif',
                    'price': 8000, 'tags': ['vitamin', 'daya tahan tubuh', 'lemas', 'kekebalan'],
                    'severity': 'low', 'requires_prescription': False
                },
                'vitamin_d': {
                    'id': 37, 'name': 'Vitamin D',
                    'aliases': ['vit d', 'calciferol', 'vitamin d3'],
                    'category': 'Vitamin D',
                    'dosage': '400-1000 IU, 1-2x sehari',
                    'indication': 'tulang rapuh osteoporosis kekurangan vitamin d',
                    'side_effects': 'Mual, lemah, pusing',
                    'warnings': 'Hati-hati overdosis (hiperkalsemia)',
                    'contraindications': 'Hiperkalsemia',
                    'price': 7000, 'tags': ['tulang', 'osteoporosis', 'vitamin', 'kalsium'],
                    'severity': 'low', 'requires_prescription': False
                },
                'vitamin_e': {
                    'id': 38, 'name': 'Vitamin E',
                    'aliases': ['vit e', 'tocopherol', 'evion'],
                    'category': 'Vitamin E (Antioksidan)',
                    'dosage': '200-400 IU, 1x sehari',
                    'indication': 'antioksidan kulit kering kesuburan',
                    'side_effects': 'Mual, diare, kram perut',
                    'warnings': 'Hati-hati pada pasien jantung',
                    'contraindications': 'Hipersensitif',
                    'price': 6000, 'tags': ['vitamin', 'kulit', 'antioksidan'],
                    'severity': 'low', 'requires_prescription': False
                },
                'calcium': {
                    'id': 39, 'name': 'Calcium + Vitamin D',
                    'aliases': ['kalsium', 'calci', 'calci-s'],
                    'category': 'Suplemen Kalsium',
                    'dosage': '500-1000mg, 2x sehari',
                    'indication': 'tulang rapuh osteoporosis kekurangan kalsium',
                    'side_effects': 'Konstipasi, kembung',
                    'warnings': 'Hati-hati pada pasien batu ginjal',
                    'contraindications': 'Hiperkalsemia',
                    'price': 8000, 'tags': ['tulang', 'osteoporosis', 'kalsium'],
                    'severity': 'low', 'requires_prescription': False
                },
                'ferrous_sulfate': {
                    'id': 40, 'name': 'Ferrous Sulfate',
                    'aliases': ['tambah darah', 'sangobion', 'ferrum'],
                    'category': 'Suplemen Zat Besi',
                    'dosage': '200mg, 2-3x sehari',
                    'indication': 'anemia kurang darah kekurangan zat besi',
                    'side_effects': 'Feses hitam, konstipasi, mual',
                    'warnings': 'Ambil dengan makanan, feses hitam adalah normal',
                    'contraindications': 'Hemosiderosis, hemokromatosis',
                    'price': 5000, 'tags': ['anemia', 'kurang darah', 'zat besi'],
                    'severity': 'low', 'requires_prescription': False
                },
                'folic_acid': {
                    'id': 41, 'name': 'Folic Acid (Asam Folat)',
                    'aliases': ['asam folat', 'folat', 'folin'],
                    'category': 'Vitamin B9',
                    'dosage': '400mcg, 1x sehari',
                    'indication': 'anemia kurang darah kehamilan',
                    'side_effects': 'Jarang, ruam kulit',
                    'warnings': 'Penting untuk ibu hamil',
                    'contraindications': 'Hipersensitif',
                    'price': 4000, 'tags': ['anemia', 'kehamilan', 'vitamin'],
                    'severity': 'low', 'requires_prescription': False
                },
                'zinc': {
                    'id': 42, 'name': 'Zinc (Seng)',
                    'aliases': ['zink', 'seng', 'zinc sulphate'],
                    'category': 'Mineral',
                    'dosage': '20-50mg, 1x sehari',
                    'indication': 'daya tahan tubuh luka jerawat',
                    'side_effects': 'Mual, muntah, rasa logam',
                    'warnings': 'Hati-hati penggunaan jangka panjang',
                    'contraindications': 'Hipersensitif',
                    'price': 6000, 'tags': ['daya tahan tubuh', 'luka', 'jerawat'],
                    'severity': 'low', 'requires_prescription': False
                },
                'fish_oil': {
                    'id': 43, 'name': 'Fish Oil (Minyak Ikan)',
                    'aliases': ['omega-3', 'minyak ikan', 'omega 3'],
                    'category': 'Suplemen Omega-3',
                    'dosage': '1000mg, 2-3x sehari',
                    'indication': 'jantung kolesterol antiinflamasi',
                    'side_effects': 'Bau amis, sendawa, diare',
                    'warnings': 'Hati-hati pada pasien yang akan operasi',
                    'contraindications': 'Alergi ikan',
                    'price': 10000, 'tags': ['jantung', 'kolesterol', 'omega'],
                    'severity': 'low', 'requires_prescription': False
                },

                # ==================== OBAT HIPERTENSI & JANTUNG ====================
                'amlodipine': {
                    'id': 44, 'name': 'Amlodipine',
                    'aliases': ['norvasc', 'amlong', 'amlodip', 'vascal'],
                    'category': 'Antagonis Kalsium (CCB)',
                    'dosage': '5-10mg, 1x sehari',
                    'indication': 'hipertensi darah tinggi angina pektoris sakit dada',
                    'side_effects': 'Sakit kepala, edema perifer (bengkak kaki), pusing, flushing',
                    'warnings': 'Hati-hati pada gagal jantung',
                    'contraindications': 'Hipersensitif, syok kardiogenik',
                    'price': 12000, 'tags': ['hipertensi', 'darah tinggi', 'tekanan darah', 'jantung'],
                    'severity': 'high', 'requires_prescription': True
                },
                'nifedipine': {
                    'id': 45, 'name': 'Nifedipine',
                    'aliases': ['adalat', 'nifedip', 'corinfar'],
                    'category': 'Antagonis Kalsium',
                    'dosage': '10-20mg, 2-3x sehari',
                    'indication': 'hipertensi darah tinggi angina',
                    'side_effects': 'Pusing, flushing, sakit kepala',
                    'warnings': 'Hati-hati, bisa menyebabkan hipotensi berat',
                    'contraindications': 'Hipersensitif',
                    'price': 10000, 'tags': ['hipertensi', 'darah tinggi'],
                    'severity': 'high', 'requires_prescription': True
                },
                'captopril': {
                    'id': 46, 'name': 'Captopril',
                    'aliases': ['kapoten', 'ace inhibitor'],
                    'category': 'ACE Inhibitor',
                    'dosage': '12.5-25mg, 2-3x sehari',
                    'indication': 'hipertensi darah tinggi gagal jantung',
                    'side_effects': 'Batuk kering, pusing, hipotensi, hiperkalemia',
                    'warnings': 'Hati-hati pada gangguan ginjal, bisa menyebabkan batuk',
                    'contraindications': 'Hamil, angioedema',
                    'price': 8000, 'tags': ['hipertensi', 'darah tinggi', 'jantung'],
                    'severity': 'high', 'requires_prescription': True
                },
                'losartan': {
                    'id': 47, 'name': 'Losartan',
                    'aliases': ['cozaar', 'losart', 'losa'],
                    'category': 'ARB (Angiotensin Receptor Blocker)',
                    'dosage': '50mg, 1x sehari',
                    'indication': 'hipertensi darah tinggi ginjal diabetic',
                    'side_effects': 'Pusing, hiperkalemia',
                    'warnings': 'Hati-hati pada gangguan ginjal',
                    'contraindications': 'Hamil',
                    'price': 15000, 'tags': ['hipertensi', 'darah tinggi'],
                    'severity': 'high', 'requires_prescription': True
                },
                'hydrochlorothiazide': {
                    'id': 48, 'name': 'Hydrochlorothiazide (HCT)',
                    'aliases': ['hct', 'diuretik', 'hidroklorotiazid'],
                    'category': 'Diuretik Tiazid',
                    'dosage': '12.5-25mg, 1x sehari',
                    'indication': 'hipertensi darah tinggi edema',
                    'side_effects': 'Peningkatan urinasi, hipokalemia, pusing',
                    'warnings': 'Hati-hati pada gangguan ginjal',
                    'contraindications': 'Anuria, hipersensitif',
                    'price': 5000, 'tags': ['hipertensi', 'darah tinggi', 'banyak kencing'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'bisoprolol': {
                    'id': 49, 'name': 'Bisoprolol',
                    'aliases': ['concor', 'bisoprol'],
                    'category': 'Beta Blocker',
                    'dosage': '5-10mg, 1x sehari',
                    'indication': 'hipertensi darah tinggi jantung',
                    'side_effects': 'Pusing, lemas, bradikardia, cold extremities',
                    'warnings': 'Jangan stop tiba-tiba, turunkan dosis bertahap',
                    'contraindications': 'Asma, bradikardia, gagal jantung dekompensasi',
                    'price': 15000, 'tags': ['hipertensi', 'darah tinggi', 'jantung'],
                    'severity': 'high', 'requires_prescription': True
                },

                # ==================== OBAT DIABETES ====================
                'metformin': {
                    'id': 50, 'name': 'Metformin',
                    'aliases': ['diabex', 'glucophage', 'dimethyl', 'metfor'],
                    'category': 'Antidiabetik Oral (Biguanid)',
                    'dosage': '500mg, 2-3x sehari sesudah makan',
                    'indication': 'diabetes tipe 2 kencing manis gula darah tinggi insulin resistance',
                    'side_effects': 'Mual, diare, gangguan pencernaan, asidosis laktik (jarang)',
                    'warnings': 'Henti sebelum operasi atau pemeriksaan kontras',
                    'contraindications': 'Gagal ginjal, asidosis laktik, alkoholisme',
                    'price': 15000, 'tags': ['diabetes', 'kencing manis', 'gula darah', 'insulin'],
                    'severity': 'high', 'requires_prescription': True
                },
                'glipizide': {
                    'id': 51, 'name': 'Glipizide',
                    'aliases': ['minidiab', 'glipizid'],
                    'category': 'Antidiabetik Oral (Sulfonylurea)',
                    'dosage': '5mg, 1-2x sehari',
                    'indication': 'diabetes tipe 2 gula darah tinggi',
                    'side_effects': 'Hipoglikemia, mual, berat badan naik',
                    'warnings': 'Rutin cek gula darah, waspada hipoglikemia',
                    'contraindications': 'Diabetes tipe 1',
                    'price': 13000, 'tags': ['diabetes', 'kencing manis', 'gula darah'],
                    'severity': 'high', 'requires_prescription': True
                },
                'glibenclamide': {
                    'id': 52, 'name': 'Glibenclamide',
                    'aliases': ['daonil', 'gliben', 'ukal'],
                    'category': 'Antidiabetik Oral (Sulfonylurea)',
                    'dosage': '5mg, 1-2x sehari',
                    'indication': 'diabetes tipe 2 kencing manis',
                    'side_effects': 'Hipoglikemia, mual',
                    'warnings': 'Waspada hipoglikemia',
                    'contraindications': 'Diabetes tipe 1',
                    'price': 10000, 'tags': ['diabetes', 'kencing manis', 'gula darah'],
                    'severity': 'high', 'requires_prescription': True
                },
                'sitagliptin': {
                    'id': 53, 'name': 'Sitagliptin',
                    'aliases': ['januvia', 'sitaglipt'],
                    'category': 'DPP-4 Inhibitor',
                    'dosage': '100mg, 1x sehari',
                    'indication': 'diabetes tipe 2',
                    'side_effects': 'Sakit kepala, infeksi saluran napas',
                    'warnings': 'Hati-hati pada gangguan ginjal',
                    'contraindications': 'Hipersensitif',
                    'price': 35000, 'tags': ['diabetes', 'kencing manis'],
                    'severity': 'medium', 'requires_prescription': True
                },

                # ==================== OBAT KOLESTEROL ====================
                'simvastatin': {
                    'id': 54, 'name': 'Simvastatin',
                    'aliases': ['cholestin', 'liponorm', 'simvo'],
                    'category': 'Statin',
                    'dosage': '10-40mg, 1x sehari malam',
                    'indication': 'kolesterol tinggi kolesterol ldl trigliserida',
                    'side_effects': 'Sakit kepala, nyeri otot, gangguan hati',
                    'warnings': 'Cek fungsi hati berkala, waspada nyeri otot',
                    'contraindications': 'Penyakit hati aktif, kehamilan',
                    'price': 12000, 'tags': ['kolesterol', 'lemak darah', 'trigliserida'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'atorvastatin': {
                    'id': 55, 'name': 'Atorvastatin',
                    'aliases': ['lipitor', 'atorva', 'atocor'],
                    'category': 'Statin',
                    'dosage': '10-80mg, 1x sehari',
                    'indication': 'kolesterol tinggi kolesterol',
                    'side_effects': 'Nyeri otot, mual, diare',
                    'warnings': 'Cek fungsi hati berkala',
                    'contraindications': 'Penyakit hati',
                    'price': 20000, 'tags': ['kolesterol', 'lemak darah'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'fenofibrate': {
                    'id': 56, 'name': 'Fenofibrate',
                    'aliases': ['fenofib', 'lipanthyl'],
                    'category': 'Fibrat',
                    'dosage': '160mg, 1x sehari',
                    'indication': 'kolesterol tinggi trigliserida tinggi',
                    'side_effects': 'Mual, pusing, gangguan hati',
                    'warnings': 'Cek fungsi hati',
                    'contraindications': 'Gagal ginjal, penyakit hati',
                    'price': 18000, 'tags': ['kolesterol', 'trigliserida'],
                    'severity': 'medium', 'requires_prescription': True
                },

                # ==================== OBAT ASMA & SALURAN NAPAS ====================
                'salbutamol': {
                    'id': 57, 'name': 'Salbutamol',
                    'aliases': ['ventolin', 'albuterol', 'salbu'],
                    'category': 'Bronkodilator (Beta-2 Agonis)',
                    'dosage': '2-4mg tablet 3x sehari atau 1-2 puff inhaler saat needed',
                    'indication': 'asma sesak napas bronkitis asma bronkial',
                    'side_effects': 'Gemetar, pusing, jantung berdebar, sakit kepala',
                    'warnings': 'Hati-hati pada pasien jantung, hipertiroid',
                    'contraindications': 'Hipersensitif',
                    'price': 15000, 'tags': ['asma', 'sesak', 'bronkitis', 'sesak napas'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'theophylline': {
                    'id': 58, 'name': 'Theophylline',
                    'aliases': ['theophyl', 'quibron'],
                    'category': 'Bronkodilator',
                    'dosage': '100-200mg, 2-3x sehari',
                    'indication': 'asma bronkitis sesak napas',
                    'side_effects': 'Mual, pusing, insomnia, takikardia',
                    'warnings': 'Hati-hati pada penyakit jantung dan epilepsi',
                    'contraindications': 'Hipersensitif',
                    'price': 10000, 'tags': ['asma', 'sesak', 'bronkitis'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'budesonide': {
                    'id': 59, 'name': 'Budesonide',
                    'aliases': ['pulmicort', 'bude'],
                    'category': 'Kortikosteroid Inhalasi',
                    'dosage': '1-2 puff, 2x sehari',
                    'indication': 'asma bronkitis radang saluran napas',
                    'side_effects': 'Kandidiasis mulut, batuk',
                    'warnings': 'Berkumur setelah inhalasi',
                    'contraindications': 'Hipersensitif',
                    'price': 25000, 'tags': ['asma', 'radang', 'bronkitis'],
                    'severity': 'medium', 'requires_prescription': True
                },

                # ==================== ANALGESIK NARKOTIK (HARUS DENGAN RESEP) ====================
                'tramadol': {
                    'id': 60, 'name': 'Tramadol',
                    'aliases': ['tramal', 'trama'],
                    'category': 'Analgesik Opioid',
                    'dosage': '50-100mg, 4-6x sehari',
                    'indication': 'nyeri sedang berat nyeri pasca operasi',
                    'side_effects': 'Mual, pusing, kantuk, konstipasi',
                    'warnings': 'Dapat menyebabkan ketergantungan, hati-hati saat mengemudi',
                    'contraindications': 'Epilepsi, overdosis opioid',
                    'price': 15000, 'tags': ['nyeri', 'nyeri berat', 'sakit'],
                    'severity': 'high', 'requires_prescription': True
                },

                # ==================== OBAT TOKSISITAS ====================
                'ondansetron': {
                    'id': 61, 'name': 'Ondansetron',
                    'aliases': ['zofran', 'ondan', 'emetron'],
                    'category': 'Antiemetik (Anti Muntah)',
                    'dosage': '4-8mg, 2-3x sehari',
                    'indication': 'mual muntah kemoterapi pasca operasi',
                    'side_effects': 'Sakit kepala, konstipasi, pusing',
                    'warnings': 'Hati-hati pada gangguan hati',
                    'contraindications': 'Hipersensitif',
                    'price': 12000, 'tags': ['mual', 'muntah', 'kemoterapi'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'dexamethasone': {
                    'id': 62, 'name': 'Dexamethasone',
                    'aliases': ['dexa', 'dexa', 'cortenema'],
                    'category': 'Kortikosteroid',
                    'dosage': '0.5-5mg, 1-4x sehari',
                    'indication': 'alergi berat radang asma',
                    'side_effects': 'Peningkatan nafsu makan, insomnia, ulkus',
                    'warnings': 'Jangan stop tiba-tiba, turunkan dosis bertahap',
                    'contraindications': 'Infeksi jamur sistemik',
                    'price': 5000, 'tags': ['alergi', 'radang', 'asma'],
                    'severity': 'high', 'requires_prescription': True
                },
                'prednisone': {
                    'id': 63, 'name': 'Prednisone',
                    'aliases': ['prednis', 'prednison'],
                    'category': 'Kortikosteroid',
                    'dosage': '5-60mg/hari, tergantung kondisi',
                    'indication': 'alergi radang asma autoimun',
                    'side_effects': 'Peningkatan berat, osteoporosis, hiperglikemia',
                    'warnings': 'Tapering dosis bertahap, jangan stop tiba-tiba',
                    'contraindications': 'Infeksi jamur sistemik',
                    'price': 8000, 'tags': ['alergi', 'radang', 'asma', 'autoimun'],
                    'severity': 'high', 'requires_prescription': True
                },

                # ==================== OBAT KULIT ====================
                'clotrimazole': {
                    'id': 64, 'name': 'Clotrimazole',
                    'aliases': ['canesten', 'clotri', 'fungal'],
                    'category': 'Antijamur Topikal',
                    'dosage': 'Oles 2-3x sehari',
                    'indication': 'jamur kulit panu kutu air candidiasis',
                    'side_effects': 'Iritasi ringan, gatal',
                    'warnings': 'Gunakan sampai sembuh, lanjutkan 1 minggu setelah sembuh',
                    'contraindications': 'Hipersensitif',
                    'price': 15000, 'tags': ['jamur', 'kulit', 'panu', 'kutu air'],
                    'severity': 'low', 'requires_prescription': False
                },
                'miconazole': {
                    'id': 65, 'name': 'Miconazole',
                    'aliases': ['micatin', 'mico', 'daktarin'],
                    'category': 'Antijamur Topikal',
                    'dosage': 'Oles 2x sehari',
                    'indication': 'jamur kulit panu kutu air',
                    'side_effects': 'Iritasi, burning',
                    'warnings': 'Hindari kontak dengan mata',
                    'contraindications': 'Hipersensitif',
                    'price': 18000, 'tags': ['jamur', 'kulit', 'panu'],
                    'severity': 'low', 'requires_prescription': False
                },
                'ketoconazole': {
                    'id': 66, 'name': 'Ketoconazole',
                    'aliases': ['keto', 'nizoral', 'ketoconazol'],
                    'category': 'Antijamur Topikal & Sistemik',
                    'dosage': 'Topikal: oles 1-2x sehari, Sistemik: 200mg/hari',
                    'indication': 'jamur kulit panu ketombe',
                    'side_effects': 'Iritasi, gangguan hati (formulasi sistemik)',
                    'warnings': 'Formulasi sistemik hati-hati pada gangguan hati',
                    'contraindications': 'Hipersensitif',
                    'price': 20000, 'tags': ['jamur', 'kulit', 'panu', 'ketombe'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'salicylic_acid': {
                    'id': 67, 'name': 'Salicylic Acid (Asam Salisilat)',
                    'aliases': ['salsil', 'asam salisilat'],
                    'category': 'Keratolitik',
                    'dosage': 'Oles 1-2x sehari',
                    'indication': 'jerawat kapalan kutil psoriasis',
                    'side_effects': 'Iritasi, kering, mengelupas',
                    'warnings': 'Jangan gunakan pada kulit luka/iritasi',
                    'contraindications': 'Hipersensitif, diabetes',
                    'price': 10000, 'tags': ['jerawat', 'kutil', 'kapalan'],
                    'severity': 'low', 'requires_prescription': False
                },
                'benzoyl_peroxide': {
                    'id': 68, 'name': 'Benzoyl Peroxide',
                    'aliases': ['benzac', 'benzo', 'oxy'],
                    'category': 'Anti-Jerawat',
                    'dosage': 'Oles 1-2x sehari',
                    'indication': 'jerawat acne komedo',
                    'side_effects': 'Kering, iritasi, kemerahan',
                    'warnings': 'Hindari sinar matahari, bisa memutihkan pakaian',
                    'contraindications': 'Hipersensitif',
                    'price': 15000, 'tags': ['jerawat', 'acne', 'komedo'],
                    'severity': 'low', 'requires_prescription': False
                },
                'clindamycin_topical': {
                    'id': 69, 'name': 'Clindamycin Topical',
                    'aliases': ['clinda', 'dalacin'],
                    'category': 'Antibiotik Topikal',
                    'dosage': 'Oles 2x sehari',
                    'indication': 'jerawat acne',
                    'side_effects': 'Iritasi, kering, kolitis (jarang)',
                    'warnings': 'Hati-hati penggunaan jangka panjang',
                    'contraindications': 'Hipersensitif',
                    'price': 20000, 'tags': ['jerawat', 'acne'],
                    'severity': 'low', 'requires_prescription': True
                },
                'desonide': {
                    'id': 70, 'name': 'Desonide',
                    'aliases': ['deson', 'desonide'],
                    'category': 'Kortikosteroid Topikal',
                    'dosage': 'Oles 2-3x sehari',
                    'indication': 'radang kulit gatal eksem dermatitis',
                    'side_effects': 'Iritasi, penipisan kulit',
                    'warnings': 'Jangan gunakan jangka panjang',
                    'contraindications': 'Hipersensitif',
                    'price': 18000, 'tags': ['radang', 'gatal', 'eksem', 'dermatitis'],
                    'severity': 'low', 'requires_prescription': True
                },

                # ==================== OBAT LAINNYA ====================
                'orlistat': {
                    'id': 71, 'name': 'Orlistat',
                    'aliases': ['xenical', 'alli', 'orli'],
                    'category': 'Anti-Obesitas',
                    'dosage': '120mg, 3x sehari dengan makan',
                    'indication': 'obesitas penurunan berat badan',
                    'side_effects': 'Diare berminyak, flatus, inkontinesia fekal',
                    'warnings': 'Hati-hati pada gangguan penyerapan',
                    'contraindications': 'Sindrom malabsorpsi, kolestasis',
                    'price': 45000, 'tags': ['obesitas', 'diet', 'berat badan'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'sildenafil': {
                    'id': 72, 'name': 'Sildenafil',
                    'aliases': ['viagra', 'silden', 'egra'],
                    'category': 'Inhibitor PDE-5',
                    'dosage': '25-100mg, 1 jam sebelum aktivitas seksual',
                    'indication': 'disfungsi ereksi pulmonary hypertension',
                    'side_effects': 'Sakit kepala, flushing, gangguan penglihatan',
                    'warnings': 'JANGAN gunakan dengan nitrat, dapat menyebabkan hipotensi berat',
                    'contraindications': 'Penggunaan nitrat, gagal jantung',
                    'price': 80000, 'tags': ['ereksi', 'disfungsi ereksi', 'ed'],
                    'severity': 'high', 'requires_prescription': True
                },
                'tamsulosin': {
                    'id': 73, 'name': 'Tamsulosin',
                    'aliases': ['tamsu', 'flomax', 'harnal'],
                    'category': 'Alpha Blocker',
                    'dosage': '0.4mg, 1x sehari',
                    'indication': 'bph pembesaran prostat sulit kencing',
                    'side_effects': 'Pusing, hipotensi, ejakulasi retrograde',
                    'warnings': 'Berdiri perlahan saat bangun',
                    'contraindications': 'Hipersensitif',
                    'price': 20000, 'tags': ['prostat', 'bph', 'kencing'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'finasteride': {
                    'id': 74, 'name': 'Finasteride',
                    'aliases': ['finas', 'propecia', 'proscar'],
                    'category': 'Inhibitor 5-alpha Reduktase',
                    'dosage': '1-5mg, 1x sehari',
                    'indication': 'kebotakan bph prostat',
                    'side_effects': 'Impotensi, ginekomastia, penurunan libido',
                    'warnings': 'Hati-hati pada wanita hamil (jangan sentuh tablet)',
                    'contraindications': 'Hamil',
                    'price': 25000, 'tags': ['kebotakan', 'rambut', 'prostat'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'allopurinol': {
                    'id': 75, 'name': 'Allopurinol',
                    'aliases': ['allo', 'zyloric', 'puric'],
                    'category': 'Inhibitor Xantin Oksidase',
                    'dosage': '100-300mg, 1x sehari',
                    'indication': 'asam urat hiperurisemia batu ginjal',
                    'side_effects': 'Mual, ruam, sindrom stevens-johnson',
                    'warnings': 'Minum banyak air, waspada reaksi kulit',
                    'contraindications': 'Hipersensitif',
                    'price': 10000, 'tags': ['asam urat', 'uric acid', 'nyeri sendi'],
                    'severity': 'medium', 'requires_prescription': True
                },
                'colchicine': {
                    'id': 76, 'name': 'Colchicine',
                    'aliases': ['colchi', 'kolhisin'],
                    'category': 'Anti-Gout',
                    'dosage': '0.5-1mg, 2-3x sehari',
                    'indication': 'asam urat serangan asam urat',
                    'side_effects': 'Mual, diare, kerusakan otot',
                    'warnings': 'Hati-hati pada gangguan ginjal',
                    'contraindications': 'Gagal ginjal berat',
                    'price': 8000, 'tags': ['asam urat', 'nyeri sendi'],
                    'severity': 'high', 'requires_prescription': True
                },
            }
        }

        # Buat file jika belum ada
        for filename, default_content in default_files.items():
            filepath = os.path.join(self.base_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, indent=4, ensure_ascii=False)

    def load_json(self, filename):
        """Load data dari file JSON"""
        filepath = os.path.join(self.base_dir, filename)

        if not os.path.exists(filepath):
            return {} if filename == 'drugs.json' else []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} if filename == 'drugs.json' else []

    def save_json(self, filename, data):
        """Simpan data ke file JSON"""
        filepath = os.path.join(self.base_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_users(self):
        """Load data users"""
        return self.load_json('users.json')

    def load_patients(self):
        """Load data pasien"""
        return self.load_json('patients.json')

    def load_medical_records(self):
        """Load data rekam medis"""
        return self.load_json('medical_records.json')

    def load_drugs(self):
        """
        Load data obat sebagai dictionary
        Returns: dict dengan key = lowercase drug name
        """
        return self.load_json('drugs.json')

    def get_drug_list(self):
        """
        Get drugs as list untuk backward compatibility
        Returns: list of drug dictionaries
        """
        drugs_dict = self.load_drugs()
        return list(drugs_dict.values()) if isinstance(drugs_dict, dict) else drugs_dict

    def save_users(self, users):
        """Simpan data users"""
        self.save_json('users.json', users)

    def save_patients(self, patients):
        """Simpan data pasien"""
        self.save_json('patients.json', patients)

    def save_medical_records(self, records):
        """Simpan data rekam medis"""
        self.save_json('medical_records.json', records)

    def save_drugs(self, drugs):
        """Simpan data obat"""
        self.save_json('drugs.json', drugs)

    def search_drugs(self, keyword):
        """
        Cari obat berdasarkan keyword (search function)
        Mencari di: name, aliases, category, indication, tags
        """
        drugs = self.load_drugs()
        if not isinstance(drugs, dict):
            return []

        keyword = keyword.lower().strip()
        results = []

        for key, drug in drugs.items():
            # Search in name
            if keyword in drug['name'].lower():
                results.append(drug)
                continue

            # Search in aliases
            if 'aliases' in drug:
                for alias in drug['aliases']:
                    if keyword in alias.lower():
                        results.append(drug)
                        break
                else:
                    continue
                continue

            # Search in category
            if keyword in drug['category'].lower():
                results.append(drug)
                continue

            # Search in indication
            if keyword in drug['indication'].lower():
                results.append(drug)
                continue

            # Search in tags
            if 'tags' in drug:
                for tag in drug['tags']:
                    if keyword in tag.lower():
                        results.append(drug)
                        break

        return results

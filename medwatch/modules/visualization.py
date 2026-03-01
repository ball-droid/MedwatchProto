"""
Modul Visualization
Visualisasi tren penyakit dan statistik dengan fitur download

@author: MedWatch Team
@maintained: Mahasiswa
@description:
    Modul ini menangani:
    1. Visualisasi data medis dalam bentuk grafik
    2. Export grafik ke file (PNG/PDF) untuk dicetak
    3. Generate laporan dalam bentuk teks/PDF
"""

import os
import json
from collections import Counter
from datetime import datetime
from utils.json_helper import JSONHelper

# Cek ketersediaan matplotlib
try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    import matplotlib
    matplotlib.use('Agg')  # Untuk save file tanpa GUI
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Cek ketersediaan reportlab untuk PDF
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class DiseaseTrendVisualizer:
    """
    Kelas untuk visualisasi tren penyakit
    Menyediakan fungsi untuk membuat grafik dan export ke file
    """

    def __init__(self):
        """Constructor: inisialisasi json_helper"""
        self.json_helper = JSONHelper()

        # Folder untuk menyimpan file export
        self.export_folder = "exports"
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

    def get_statistics(self):
        """
        Ambil statistik penyakit dari rekam medis

        Returns:
            dict: {nama_penyakit: jumlah_kasus}
        """
        records = self.json_helper.load_medical_records()
        stats = {}

        for record in records:
            diagnosis = record['diagnosis']
            stats[diagnosis] = stats.get(diagnosis, 0) + 1

        # Sort berdasarkan jumlah (terbanyak dulu)
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def get_monthly_statistics(self, year=None):
        """
        Ambil statistik penyakit per bulan

        Args:
            year: filter tahun (opsional)

        Returns:
            dict: {YYYY-MM: {penyakit: jumlah}}
        """
        records = self.json_helper.load_medical_records()
        monthly_data = {}

        for record in records:
            try:
                date_obj = datetime.strptime(record['date'], '%Y-%m-%d')
                if year and date_obj.year != year:
                    continue

                month_key = date_obj.strftime('%Y-%m')
                if month_key not in monthly_data:
                    monthly_data[month_key] = {}

                diagnosis = record['diagnosis']
                monthly_data[month_key][diagnosis] = monthly_data[month_key].get(diagnosis, 0) + 1
            except ValueError:
                continue

        return monthly_data

    def get_top_diseases(self, limit=10):
        """
        Ambil penyakit teratas berdasarkan jumlah kasus

        Args:
            limit: jumlah penyakit yang ingin diambil

        Returns:
            dict: {nama_penyakit: jumlah_kasus}
        """
        stats = self.get_statistics()
        return dict(list(stats.items())[:limit])

    def get_patient_age_distribution(self):
        """
        Ambil distribusi usia pasien

        Returns:
            dict: {range_usia: jumlah}
        """
        patients = self.json_helper.load_patients()

        age_groups = {
            '0-12': 0,
            '13-18': 0,
            '19-35': 0,
            '36-50': 0,
            '51-65': 0,
            '65+': 0
        }

        for patient in patients:
            age = patient.get('age', 0)
            if age <= 12:
                age_groups['0-12'] += 1
            elif age <= 18:
                age_groups['13-18'] += 1
            elif age <= 35:
                age_groups['19-35'] += 1
            elif age <= 50:
                age_groups['36-50'] += 1
            elif age <= 65:
                age_groups['51-65'] += 1
            else:
                age_groups['65+'] += 1

        return age_groups

    def get_blood_type_distribution(self):
        """
        Ambil distribusi golongan darah pasien

        Returns:
            dict: {golongan_darah: jumlah}
        """
        patients = self.json_helper.load_patients()

        blood_types = Counter([p.get('blood_type', 'Unknown') for p in patients])

        return dict(blood_types)

    def create_disease_chart(self, save_path=None):
        """
        Buat grafik penyakit teratas dan simpan ke file

        Args:
            save_path: path file untuk menyimpan grafik (opsional)

        Returns:
            str: path file yang disimpan atau None jika gagal
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        # Buat figure dengan ukuran A4 landscape
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))

        # Get data
        top_diseases = self.get_top_diseases(10)
        age_dist = self.get_patient_age_distribution()

        # Plot 1: Bar chart penyakit teratas
        diseases = list(top_diseases.keys())
        counts = list(top_diseases.values())

        bars = ax1.barh(diseases, counts, color='#3498db')
        ax1.set_xlabel('Jumlah Kasus', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Penyakit', fontsize=12, fontweight='bold')
        ax1.set_title('10 Penyakit Teratas', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()

        # Tambah value label di setiap bar
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=10)

        # Grid untuk ax1
        ax1.grid(axis='x', alpha=0.3)

        # Plot 2: Pie chart distribusi usia
        if sum(age_dist.values()) > 0:
            labels = list(age_dist.keys())
            sizes = list(age_dist.values())
            colors_chart = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

            explode = [0.1 if i == 0 else 0 for i in range(len(sizes))]  # Highlight pie terbesar

            wedges, texts, autotexts = ax2.pie(
                sizes,
                explode=explode,
                labels=labels,
                autopct='%1.1f%%',
                colors=colors_chart,
                startangle=90,
                textprops={'fontsize': 11, 'fontweight': 'bold'}
            )
            ax2.set_title('Distribusi Usia Pasien', fontsize=14, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center', fontsize=14)

        # Judul utama
        fig.suptitle('LAPORAN STATISTIK KESEHATAN\nMedWatch Healthcare System',
                     fontsize=16, fontweight='bold')

        # Timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        fig.text(0.5, 0.02, f'Dicetak: {timestamp}', ha='center', fontsize=10, style='italic')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Tentukan path penyimpanan
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.export_folder, f'laporan_kesehatan_{timestamp}.png')

        # Simpan ke file
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return save_path

    def create_monthly_trend_chart(self, year=None, save_path=None):
        """
        Buat grafik tren bulanan penyakit dan simpan ke file

        Args:
            year: filter tahun (opsional)
            save_path: path file untuk menyimpan (opsional)

        Returns:
            str: path file yang disimpan atau None
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        monthly_data = self.get_monthly_statistics(year)

        if not monthly_data:
            return None

        # Buat figure
        fig, ax = plt.subplots(figsize=(14, 8))

        # Get all unique diagnoses
        all_diagnoses = set()
        for month_data in monthly_data.values():
            all_diagnoses.update(month_data.keys())

        # Ambil top 5 penyakit
        top_diseases = self.get_top_diseases(5).keys()

        # Plot lines untuk top diseases
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

        for i, disease in enumerate(top_diseases):
            if disease in all_diagnoses:
                months = sorted(monthly_data.keys())
                counts = [monthly_data[m].get(disease, 0) for m in months]

                ax.plot(months, counts, marker='o', label=disease,
                       color=colors[i % len(colors)], linewidth=2, markersize=8)

        ax.set_xlabel('Bulan', fontsize=12, fontweight='bold')
        ax.set_ylabel('Jumlah Kasus', fontsize=12, fontweight='bold')
        title_year = f'Tahun {year}' if year else 'Semua Tahun'
        ax.set_title(f'Tren Bulanan Penyakit - {title_year}', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')

        # Judul utama
        fig.suptitle('TREN PENYAKIT BULANAN\nMedWatch Healthcare System',
                     fontsize=16, fontweight='bold')

        # Timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        fig.text(0.5, 0.02, f'Dicetak: {timestamp}', ha='center', fontsize=10, style='italic')

        plt.tight_layout(rect=[0, 0.03, 1, 0.93])

        # Simpan
        if save_path is None:
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.export_folder, f'tren_bulanan_{timestamp_str}.png')

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return save_path

    def create_blood_type_chart(self, save_path=None):
        """
        Buat grafik distribusi golongan darah dan simpan ke file

        Args:
            save_path: path file untuk menyimpan (opsional)

        Returns:
            str: path file yang disimpan atau None
        """
        if not MATPLOTLIB_AVAILABLE:
            return None

        blood_dist = self.get_blood_type_distribution()

        # Buat figure
        fig, ax = plt.subplots(figsize=(10, 8))

        if blood_dist:
            labels = list(blood_dist.keys())
            sizes = list(blood_dist.values())
            colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#34495e']

            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                colors=colors[:len(labels)],
                startangle=90,
                textprops={'fontsize': 12, 'fontweight': 'bold'}
            )

            # Tambah legend dengan jumlah
            legend_labels = [f'{label}: {size} pasien' for label, size in zip(labels, sizes)]
            ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 0, 0.5, 1))

            ax.set_title('Distribusi Golongan Darah Pasien', fontsize=14, fontweight='bold', pad=20)
        else:
            ax.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center', fontsize=14)

        # Judul
        fig.suptitle('DISTRIBUSI GOLONGAN DARAH\nMedWatch Healthcare System',
                     fontsize=16, fontweight='bold')

        # Timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
        fig.text(0.5, 0.02, f'Dicetak: {timestamp}', ha='center', fontsize=10, style='italic')

        plt.tight_layout(rect=[0, 0.03, 1, 0.9])

        # Simpan
        if save_path is None:
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(self.export_folder, f'golongan_darah_{timestamp_str}.png')

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return save_path

    def show_trend_chart(self):
        """
        Tampilkan grafik tren penyakit (untuk live preview)
        Jika matplotlib tidak tersedia, tampilkan laporan teks
        """
        if not MATPLOTLIB_AVAILABLE:
            self.show_trend_text_report()
            return

        # Import untuk display GUI dengan backend yang benar
        import matplotlib
        matplotlib.use('tkagg')  # Fix: gunakan 'tkagg' bukan 'default'
        import matplotlib.pyplot as plt

        # Create figure dengan subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Get top diseases
        top_diseases = self.get_top_diseases(10)

        # Plot 1: Bar chart of top diseases
        diseases = list(top_diseases.keys())
        counts = list(top_diseases.values())

        bars = ax1.barh(diseases, counts, color='#3498db')
        ax1.set_xlabel('Jumlah Kasus')
        ax1.set_ylabel('Penyakit')
        ax1.set_title('10 Penyakit Teratas', fontweight='bold')
        ax1.invert_yaxis()

        # Add value labels
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(count), va='center', fontsize=10)

        # Plot 2: Age distribution pie chart
        age_dist = self.get_patient_age_distribution()

        if sum(age_dist.values()) > 0:
            labels = list(age_dist.keys())
            sizes = list(age_dist.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

            ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax2.set_title('Distribusi Usia Pasien', fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'Tidak ada data', ha='center', va='center')

        fig.tight_layout()
        plt.show()

    def show_trend_text_report(self):
        """Tampilkan laporan teks jika matplotlib tidak tersedia"""
        print(self.generate_report_text())

    def generate_report_text(self, save_path=None):
        """
        Generate laporan dalam bentuk teks

        Args:
            save_path: path file untuk menyimpan (opsional)

        Returns:
            str: isi laporan
        """
        report = []
        report.append("="*60)
        report.append("LAPORAN STATISTIK KESEHATAN")
        report.append("MedWatch Healthcare System")
        report.append("="*60)
        report.append(f"Dicetak: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append("")

        # Statistik penyakit
        report.append("PENYAKIT TERBANYAK:")
        report.append("-"*40)
        top_diseases = self.get_top_diseases(15)
        for i, (disease, count) in enumerate(top_diseases.items(), 1):
            report.append(f"{i:2d}. {disease}: {count} kasus")
        report.append("")

        # Distribusi usia
        report.append("DISTRIBUSI USIA PASIEN:")
        report.append("-"*40)
        age_dist = self.get_patient_age_distribution()
        for age_group, count in age_dist.items():
            report.append(f"{age_group}: {count} pasien")
        report.append("")

        # Distribusi golongan darah
        report.append("DISTRIBUSI GOLONGAN DARAH:")
        report.append("-"*40)
        blood_dist = self.get_blood_type_distribution()
        for blood_type, count in sorted(blood_dist.items()):
            report.append(f"{blood_type}: {count} pasien")
        report.append("")

        # Total pasien dan rekam medis
        patients = self.json_helper.load_patients()
        records = self.json_helper.load_medical_records()
        report.append("RINGKASAN DATA:")
        report.append("-"*40)
        report.append(f"Total Pasien: {len(patients)}")
        report.append(f"Total Rekam Medis: {len(records)}")
        report.append("")

        report.append("="*60)
        report.append("Disclaimer: Laporan ini hanya untuk tujuan informasi.")
        report.append("Untuk keputusan medis, konsultasikan dengan dokter.")
        report.append("="*60)

        report_text = "\n".join(report)

        # Simpan ke file jika path diberikan
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
        elif save_path is None:
            # Default save
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_path = os.path.join(self.export_folder, f'laporan_kesehatan_{timestamp}.txt')
            with open(default_path, 'w', encoding='utf-8') as f:
                f.write(report_text)

        return report_text

    def export_to_pdf(self, output_path=None):
        """
        Export laporan ke PDF yang siap dicetak

        Args:
            output_path: path file PDF (opsional)

        Returns:
            str: path file PDF yang dibuat atau None jika gagal
        """
        if not REPORTLAB_AVAILABLE:
            return None

        # Tentukan path output
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.export_folder, f'laporan_kesehatan_{timestamp}.pdf')

        # Buat PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=30, leftMargin=30,
                               topMargin=30, bottomMargin=30)

        # Container untuk elemen PDF
        elements = []

        # Styles
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            spaceAfter=30
        )

        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=10
        )

        # Judul
        elements.append(Paragraph("LAPORAN STATISTIK KESEHATAN", title_style))
        elements.append(Paragraph("MedWatch Healthcare System", subtitle_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Dicetak: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                                   styles['Normal']))
        elements.append(Spacer(1, 20))

        # Statistik penyakit
        elements.append(Paragraph("Penyakit Terbanyak", header_style))
        top_diseases = self.get_top_diseases(15)

        # Buat tabel
        table_data = [['No', 'Penyakit', 'Jumlah Kasus']]
        for i, (disease, count) in enumerate(top_diseases.items(), 1):
            table_data.append([str(i), disease, str(count)])

        table = Table(table_data, colWidths=[0.5*inch, 4*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Distribusi usia
        elements.append(Paragraph("Distribusi Usia Pasien", header_style))
        age_dist = self.get_patient_age_distribution()

        age_data = [['Kelompok Usia', 'Jumlah Pasien']]
        for age_group, count in age_dist.items():
            age_data.append([age_group, str(count)])

        age_table = Table(age_data, colWidths=[2*inch, 2*inch])
        age_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ]))
        elements.append(age_table)
        elements.append(Spacer(1, 20))

        # Distribusi golongan darah
        elements.append(Paragraph("Distribusi Golongan Darah", header_style))
        blood_dist = self.get_blood_type_distribution()

        blood_data = [['Golongan Darah', 'Jumlah Pasien']]
        for blood_type, count in sorted(blood_dist.items()):
            blood_data.append([blood_type, str(count)])

        blood_table = Table(blood_data, colWidths=[2*inch, 2*inch])
        blood_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ]))
        elements.append(blood_table)
        elements.append(Spacer(1, 30))

        # Summary
        patients = self.json_helper.load_patients()
        records = self.json_helper.load_medical_records()

        summary_data = [
            ['Ringkasan Data', ''],
            ['Total Pasien', str(len(patients))],
            ['Total Rekam Medis', str(len(records))],
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 30))

        # Disclaimer
        disclaimer = (
            "Disclaimer: Laporan ini hanya untuk tujuan informasi. "
            "Untuk keputusan medis, konsultasikan dengan dokter."
        )
        elements.append(Paragraph(disclaimer, styles['Italic']))
        elements.append(Spacer(1, 10))

        # Footer
        footer = f"Laporan dibuat oleh MedWatch Healthcare System pada {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        elements.append(Paragraph(footer, styles['Normal']))

        # Build PDF
        doc.build(elements)

        return output_path

    def get_all_export_methods(self):
        """
        Get semua metode export yang tersedia

        Returns:
            dict: {nama_metode: tersedia (bool)}
        """
        return {
            'PNG (Grafik)': MATPLOTLIB_AVAILABLE,
            'PDF (Laporan)': REPORTLAB_AVAILABLE,
            'TXT (Teks)': True
        }

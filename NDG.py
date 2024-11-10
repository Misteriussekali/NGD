# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kkN-wxqq3PlHdnGJEV-ZV_A2Pxdo7aJs
"""

import random
import pandas as pd
import ipywidgets as widgets
import streamlit
from IPython.display import display
from datetime import datetime

# Widget untuk memilih jenis data
data_type_widget = widgets.Dropdown(
    options=['Tidak ada pilihan', 'Time Series', 'Cross Section'],
    value='Tidak ada pilihan',
    description='Jenis Data:'
)

# Widget untuk memilih frekuensi (bulanan atau tahunan) dan tahun awal jika memilih time series
frequency_widget = widgets.Dropdown(
    options=['Bulanan', 'Tahunan'],
    value='Bulanan',
    description='Frekuensi:'
)

start_year_widget = widgets.IntText(
    value=2020,
    description="Tahun Awal:"
)

# Widget untuk input "Besar Batas yang Diharapkan" dan "Banyak Proses"
expected_limit_widget = widgets.IntText(
    value=10,
    description="Besar Batas:"
)

repeat_process_widget = widgets.IntText(
    value=5,
    description="Banyak Proses:"
)

# Tombol untuk melakukan generate angka
generate_button = widgets.Button(
    description="Generate Angka"
)

# Widget untuk memasukkan nama file untuk ekspor
file_name_widget = widgets.Text(
    value=f"hasil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    description="Nama File:"
)

# Tombol untuk mengekspor hasil ke Excel
export_button = widgets.Button(
    description="Export ke Excel"
)

# Output untuk menampilkan hasil
output = widgets.Output()

# Variabel untuk menyimpan hasil generate
results = []

# Fungsi untuk mengatur visibilitas widget berdasarkan pilihan jenis data
def on_data_type_change(change):
    if change['new'] == 'Time Series':
        frequency_widget.layout.display = 'block'
        start_year_widget.layout.display = 'block'
        repeat_process_widget.layout.display = 'block'
        generate_button.layout.display = 'block'
        expected_limit_widget.layout.display = 'block'
        file_name_widget.layout.display = 'block'
        export_button.layout.display = 'block'
    elif change['new'] == 'Cross Section':
        frequency_widget.layout.display = 'none'
        start_year_widget.layout.display = 'none'
        repeat_process_widget.layout.display = 'block'
        generate_button.layout.display = 'block'
        expected_limit_widget.layout.display = 'block'
        file_name_widget.layout.display = 'block'
        export_button.layout.display = 'block'
    else:
        frequency_widget.layout.display = 'none'
        start_year_widget.layout.display = 'none'
        repeat_process_widget.layout.display = 'none'
        generate_button.layout.display = 'none'
        expected_limit_widget.layout.display = 'none'
        file_name_widget.layout.display = 'none'
        export_button.layout.display = 'none'

# Hubungkan fungsi dengan widget data_type_widget
data_type_widget.observe(on_data_type_change, names='value')

# Fungsi untuk melakukan generate angka ketika tombol diklik
def on_button_click(b):
    global results  # Menggunakan variabel global untuk menyimpan hasil
    results = []  # Reset hasil setiap kali tombol diklik

    with output:
        output.clear_output()  # Hapus output sebelumnya
        expected_limit = expected_limit_widget.value  # Ambil nilai dari widget Besar Batas
        repeat_process = repeat_process_widget.value  # Ambil nilai dari widget Banyak Proses

        # Tentukan persentase pengurangan awal 87%
        percentage = 87

        # Kurangi 1% untuk setiap digit lebih dari dua
        num_digits = len(str(expected_limit))
        if num_digits > 2:
            percentage -= (num_digits - 2)

        # Hitung nilai setelah dikurangi persentase yang sesuai
        adjusted_limit = expected_limit * (percentage / 100)

        # Tentukan jumlah pengulangan berdasarkan adjusted_limit
        repeat_count = round((adjusted_limit * 2) / 5)

        start_year = start_year_widget.value  # Tahun awal
        frequency = frequency_widget.value  # Frekuensi (bulanan atau tahunan)

        # Lakukan proses generate dan penjumlahan berulang kali sesuai repeat_process
        for i in range(repeat_process):
            # Generate angka acak 1-5 sebanyak repeat_count kali
            generated_numbers = [random.randint(1, 5) for _ in range(repeat_count)]
            total_sum = sum(generated_numbers)  # Hitung total dari angka yang di-generate

            # Tambahkan hasil dan waktu sesuai pilihan frekuensi
            if data_type_widget.value == 'Time Series':
                if frequency == 'Tahunan':
                    time_label = f"{start_year + i}"  # Tahun
                elif frequency == 'Bulanan':
                    year = start_year + (i // 12)  # Menambah tahun setiap 12 bulan
                    month = (i % 12) + 1  # Mengatur bulan dari 1 sampai 12
                    time_label = f"{year}-{month:02d}"  # Format tahun-bulan
            else:
                time_label = f"{i+1}"  # Urutan untuk cross section atau tanpa pilihan

            results.append((time_label, total_sum))

        # Tampilkan hasil setiap proses
        print("Hasil setiap proses:")
        for time_label, total in results:
            print(f"{time_label}: {total}")

# Fungsi untuk mengekspor hasil ke Excel
def export_to_excel(b):
    if results:
        df = pd.DataFrame(results, columns=["Waktu", "Total"])
        file_name = file_name_widget.value
        df.to_excel(file_name, index=False)
        with output:
            print(f"Hasil berhasil diekspor ke file: {file_name}")
    else:
        with output:
            print("Tidak ada data untuk diekspor. Silakan generate data terlebih dahulu.")

# Hubungkan fungsi dengan tombol
generate_button.on_click(on_button_click)
export_button.on_click(export_to_excel)

# Awalnya sembunyikan widget yang hanya relevan untuk pilihan tertentu
frequency_widget.layout.display = 'none'
start_year_widget.layout.display = 'none'
repeat_process_widget.layout.display = 'none'
generate_button.layout.display = 'none'
expected_limit_widget.layout.display = 'none'
file_name_widget.layout.display = 'none'
export_button.layout.display = 'none'

# Tampilkan semua widget
display(data_type_widget, frequency_widget, start_year_widget, expected_limit_widget, repeat_process_widget, generate_button, file_name_widget, export_button, output)
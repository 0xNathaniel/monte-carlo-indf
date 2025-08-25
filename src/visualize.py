import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os # <-- Tambahkan library os untuk mengelola direktori

# --------------------------------------------------------------------------
# 1. DEFINISIKAN PARAMETER UTAMA
# --------------------------------------------------------------------------
CSV_FILE_PATH = '../data/monte_carlo_sotp_results.csv'
STATS_OUTPUT_PATH = '../data/monte_carlo_statistics.py' # <-- Path file output statistik
VISUALIZATION_OUTPUT_PATH = '../data/sotp_monte_carlo_visualization.png' # <-- Path file output visualisasi

CURRENT_PRICE = 7700
BULL_SCENARIO_THRESHOLD = 11500

try:
    # Baca file hasil simulasi
    df = pd.read_csv(CSV_FILE_PATH)
    results_series = df['Projected_Share_Price_INDF']
    
    # Hapus nilai-nilai ekstrem atau tidak valid (misalnya, negatif)
    results_series = results_series[results_series > 0]

    # --------------------------------------------------------------------------
    # 3. HITUNG STATISTIK LENGKAP
    # --------------------------------------------------------------------------
    trials = len(results_series)
    target_price_mean = results_series.mean()
    percentile_25 = results_series.quantile(0.25)
    median_price = results_series.median()
    percentile_75 = results_series.quantile(0.75)
    std_dev = results_series.std()
    
    coeff_variation = std_dev / target_price_mean if target_price_mean != 0 else 0
    skewness = results_series.skew()
    kurtosis = results_series.kurtosis()
    
    mean_upside_percent = ((target_price_mean - CURRENT_PRICE) / CURRENT_PRICE) * 100
    percent_above_10_upside = (results_series > (CURRENT_PRICE * 1.10)).mean() * 100
    percent_bull_scenario = (results_series > BULL_SCENARIO_THRESHOLD).mean() * 100

    # Siapkan data untuk ditampilkan di console
    stats_data = {
        "Statistic": [
            "Trials", "Target Price (Mean)", "Mean upside%", "25th percentile", 
            "Median", "75th percentile", "Standard deviation", 
            "Coefficient of Variation", "Skewness", "Kurtosis",
            "% above 10% upside", f"% bull scenario (> Rp {BULL_SCENARIO_THRESHOLD:,})"
        ],
        "Value": [
            f"{trials:,}", f"Rp {target_price_mean:,.0f}", f"{mean_upside_percent:.2f}%",
            f"Rp {percentile_25:,.0f}", f"Rp {median_price:,.0f}", f"Rp {percentile_75:,.0f}",
            f"Rp {std_dev:,.0f}", f"{coeff_variation:.2f}", f"{skewness:.2f}",
            f"{kurtosis:.2f}", f"{percent_above_10_upside:.2f}%", f"{percent_bull_scenario:.2f}%"
        ]
    }
    stats_df = pd.DataFrame(stats_data)

    print("--- Analisis Statistik Hasil Simulasi Monte Carlo ---")
    print(stats_df.to_string(index=False))

    # --------------------------------------------------------------------------
    # >>>>> BLOK KODE BARU UNTUK MENYIMPAN STATISTIK <<<<<
    # --------------------------------------------------------------------------
    
    # Pastikan direktori ../data ada
    output_dir = os.path.dirname(STATS_OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Siapkan konten yang akan ditulis ke file .py
    stats_py_content = f"""
# --- Hasil Statistik Simulasi Monte Carlo ---
# File ini dihasilkan secara otomatis.

TRIALS = {trials}
TARGET_PRICE_MEAN = {target_price_mean}
MEAN_UPSIDE_PERCENT = {mean_upside_percent}
PERCENTILE_25 = {percentile_25}
MEDIAN = {median_price}
PERCENTILE_75 = {percentile_75}
STANDARD_DEVIATION = {std_dev}
COEFFICIENT_OF_VARIATION = {coeff_variation}
SKEWNESS = {skewness}
KURTOSIS = {kurtosis}
PERCENT_ABOVE_10_UPSIDE = {percent_above_10_upside}
PERCENT_BULL_SCENARIO = {percent_bull_scenario}
"""
    
    # Tulis string ke dalam file .py
    with open(STATS_OUTPUT_PATH, 'w') as f:
        f.write(stats_py_content)
        
    print(f"\nHasil statistik telah disimpan di '{STATS_OUTPUT_PATH}'")

    # --------------------------------------------------------------------------
    # 4. BUAT VISUALISASI HISTOGRAM
    # --------------------------------------------------------------------------
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Buat histogram dan warnai barnya
    counts, bins, patches = ax.hist(results_series, bins=75, alpha=0.1, color='#04549b')
    ax.clear() # Hapus histogram awal agar bisa digambar ulang dengan warna
    
    bin_centers = (bins[:-1] + bins[1:]) / 2
    for i in range(len(bin_centers)):
        bar_color = '#fe5a5b'
        if bin_centers[i] > BULL_SCENARIO_THRESHOLD:
            bar_color = '#ffc107'
        elif bin_centers[i] > CURRENT_PRICE:
            bar_color = '#04549b'
        ax.bar(bin_centers[i], counts[i], width=(bins[i+1]-bins[i])*0.9, color=bar_color, alpha=0.8)

    # Tambahkan kembali KDE plot
    sns.kdeplot(results_series, ax=ax, color='black', linewidth=1.5)

    # Tambahkan garis vertikal untuk statistik penting
    ax.axvline(target_price_mean, color='black', linestyle='--', linewidth=2, label=f'Target Harga Rata-Rata: Rp {target_price_mean:,.0f}')
    ax.axvline(CURRENT_PRICE, color='red', linestyle='-', linewidth=2, label=f'Harga Saat Ini: Rp {CURRENT_PRICE:,.0f}')

    # Kustomisasi Plot
    ax.set_title('Distribusi Probabilitas Valuasi SOTP INDF (Monte Carlo Simulation)', fontsize=18, fontweight='bold')
    ax.set_xlabel('Target Harga per Saham (Rp)', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.legend()
    
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(VISUALIZATION_OUTPUT_PATH)
    
    print(f"\nVisualisasi telah disimpan sebagai '{VISUALIZATION_OUTPUT_PATH}'")

except FileNotFoundError:
    print(f"ERROR: File '{CSV_FILE_PATH}' tidak ditemukan. Pastikan file tersebut berada di direktori yang benar.")
except Exception as e:
    print(f"Terjadi error: {e}")
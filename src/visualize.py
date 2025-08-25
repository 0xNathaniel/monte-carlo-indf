import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 

CSV_FILE_PATH = '../data/monte_carlo_sotp_results.csv'
STATS_OUTPUT_PATH = '../data/monte_carlo_statistics.csv'
VISUALIZATION_OUTPUT_PATH = '../data/sotp_monte_carlo_visualization.png'

CURRENT_PRICE = 7700
BULL_SCENARIO_THRESHOLD = 11500

try:
    df = pd.read_csv(CSV_FILE_PATH)
    results_series = df['Projected_Share_Price_INDF']
    
    # Filter out negative values
    results_series = results_series[results_series > 0]

    # Calculate statistics
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

    print("--- Monte Carlo Simulation Statistical Analysis ---")
    print(stats_df.to_string(index=False))

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(STATS_OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    stats_py_content = f"""
# --- Monte Carlo Simulation Statistical Results ---
# This file is generated automatically.

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
    
    with open(STATS_OUTPUT_PATH, 'w') as f:
        f.write(stats_py_content)
        
    print(f"\nStatistical results have been saved to '{STATS_OUTPUT_PATH}'")


    # Create simple visualization with white background
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set clean white background
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Calculate histogram
    counts, bins, patches = ax.hist(results_series, bins=75, alpha=0.1, color='#105c9c')
    ax.clear()
    
    # Create histogram with color coding
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_width = bins[1] - bins[0]
    
    for i in range(len(bin_centers)):
        bar_color = '#fe5a5b'  # Red for below current price
        if bin_centers[i] > BULL_SCENARIO_THRESHOLD:
            bar_color = '#ffc107'  # Yellow for bull scenario
        elif bin_centers[i] > CURRENT_PRICE:
            bar_color = '#105c9c'  # New blue for above current price
        
        ax.bar(bin_centers[i], counts[i], width=bin_width*0.9, 
               color=bar_color, alpha=0.8)

    # Remove vertical lines (mean target, current price, median)
    # Keeping only the histogram bars for cleaner look
    
    # Remove title on x and y axis (no set_xlabel and set_ylabel)
    
    # Format X axis with thousand separators and horizontal rotation
    def format_rupiah(x, p):
        return f'Rp {int(x):,}'
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(format_rupiah))
    
    # Remove grid
    ax.grid(False)
    
    # Add simplified summary statistics in top right with requested metrics
    stats_text = f'''Statistics Summary:
Target Price Mean: Rp {target_price_mean:,.0f}
Mean Upside: {mean_upside_percent:.1f}%
10% Upside: {percent_above_10_upside:.1f}%
Bull Scenario: {percent_bull_scenario:.1f}%'''
    
    # Position text box for key statistics in top right
    ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, 
                     edgecolor='black', linewidth=1),
            fontsize=9, fontweight='normal', color='black')
    
    # Style ticks - horizontal price labels (rotation=0)
    ax.tick_params(axis='both', which='major', labelsize=10, colors='black')
    ax.tick_params(axis='x', rotation=0)  # Horizontal
    
    # Simple black border - remove top and right axis lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_edgecolor('black')
    ax.spines['left'].set_linewidth(1)
    ax.spines['bottom'].set_edgecolor('black')
    ax.spines['bottom'].set_linewidth(1)
    
    plt.tight_layout()
    plt.savefig(VISUALIZATION_OUTPUT_PATH, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"\nSimple visualization has been saved as '{VISUALIZATION_OUTPUT_PATH}'")

except FileNotFoundError:
    print(f"ERROR: File '{CSV_FILE_PATH}' not found. Please ensure the file is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")
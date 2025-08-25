import numpy as np
import pandas as pd
import variables

""" Monte Carlo Simulation """
NUM_ITERATIONS = 10000
results = []

for i in range(NUM_ITERATIONS):
    # Mengambil sampel acak dari distribusi normal
    current_wacc = np.random.normal(loc=variables.WACC_MEAN, scale=variables.WACC_STD_DEV)
    current_g = np.random.normal(loc=variables.G_MEAN, scale=variables.G_STD_DEV)
    current_bogasari_multiple = np.random.normal(loc=variables.BOGASARI_EV_EBIT_MEAN, scale=variables.BOGASARI_EV_EBIT_STD_DEV)
    current_distribution_multiple = np.random.normal(loc=variables.DISTRIBUTION_EV_EBIT_MEAN, scale=variables.DISTRIBUTION_EV_EBIT_STD_DEV)
    current_holding_discount = np.random.normal(loc=variables.HOLDING_DISCOUNT_MEAN, scale=variables.HOLDING_DISCOUNT_STD_DEV)

    # Memastikan kondisi matematis terpenuhi
    if current_g >= current_wacc or current_bogasari_multiple < 0 or current_distribution_multiple < 0 or current_holding_discount < 0:
        continue
    
    """ DCF """
    # Menghitung Enterprise Value ICBP
    pv_fcf = sum([fcf / ((1 + current_wacc) ** (j + 1)) for j, fcf in enumerate(variables.FCF_BASE_PROJECTIONS)])
    last_fcf = variables.FCF_BASE_PROJECTIONS[-1]
    terminal_value = (last_fcf * (1 + current_g)) / (current_wacc - current_g)
    pv_terminal_value = terminal_value / ((1 + current_wacc) ** len(variables.FCF_BASE_PROJECTIONS))
    dcf_pv = pv_fcf + pv_terminal_value
    
    # Menghitung Equity Value ICBP (sesuai formula awal Anda)
    dcf_ev = dcf_pv - variables.TOTAL_NET_DEBT

    """ Multiples """
    bogasari_ev = variables.BOGASARI_EBIT * current_bogasari_multiple
    distribution_ev = variables.DISTRIBUTION_EBIT * current_distribution_multiple
    
    """ Monte Carlo Iteration Result """
    # Menggunakan formula SOTP sesuai permintaan Anda
    result = (1 - current_holding_discount) * (dcf_ev + bogasari_ev + distribution_ev + variables.AGRIBUSINESS_EV) / variables.SHARES_OUTSTANDING
    results.append(result)

""" Save Result """
results_df = pd.DataFrame(results, columns=['Projected_Share_Price_INDF'])
results_df.to_csv('../data/monte_carlo_sotp_results.csv', index=False)

print(f"Simulasi selesai. {len(results)} hasil valuasi telah disimpan di '../data/monte_carlo_sotp_results.csv'")
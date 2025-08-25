import numpy as np
import pandas as pd

import variables

""" Monte Carlo Simulation """
NUM_ITERATIONS          = 10000
results                 = []

simulated_wacc      = np.random.choice(variables.WACC_LIST, size=NUM_ITERATIONS, p=variables.WEIGHTS)
simulated_g         = np.random.choice(variables.G_LIST, size=NUM_ITERATIONS, p=variables.WEIGHTS)
holding_discount    = np.random.choice(variables.HOLDING_DISCOUNT, size=NUM_ITERATIONS, p=variables.HOLDING_DISCOUNT_WEIGHT)

simulated_bogasari_ev_ebit      = np.random.choice(variables.BOGASARI_EV_EBIT, size=NUM_ITERATIONS, p=variables.WEIGHTS)
simulated_distribution_ev_ebit  = np.random.choice(variables.DISTRIBUTION_EV_EBIT, size=NUM_ITERATIONS, p=variables.WEIGHTS)

for i in range(NUM_ITERATIONS):
    """ DCF """
    if simulated_g[i] >= simulated_wacc[i]:
        continue
    
    # Count PV of FCF
    pv_fcf              = sum([fcf / ((1 + simulated_wacc[i]) ** (j + 1)) for j, fcf in enumerate(variables.FCF_BASE_PROJECTIONS)])
    # Count Terminal Value
    last_fcf            = variables.FCF_BASE_PROJECTIONS[-1]
    terminal_value      = (last_fcf * (1 + simulated_g[i])) / (simulated_wacc[i] - simulated_g[i])
    pv_terminal_value   = terminal_value / ((1 + simulated_wacc[i]) ** len(variables.FCF_BASE_PROJECTIONS))
    
    dcf_pv              = pv_fcf + pv_terminal_value
    dcf_ev              = dcf_pv - variables.TOTAL_NET_DEBT

    """ Multiples """
    bogasari_ev         = variables.BOGASARI_EBIT * simulated_bogasari_ev_ebit[i]
    distribution_ev     = variables.DISTRIBUTION_EBIT * simulated_distribution_ev_ebit[i]
    
    """ Monte Carlo Iteration Result """
    result              = (1 - holding_discount[i]) * (dcf_ev + bogasari_ev + distribution_ev + variables.AGRIBUSINESS_EV) // variables.SHARES_OUTSTANDING
    results.append(result)



""" Save Result """
results_df = pd.DataFrame(results, columns=['Projected_Share_Price_INDF'])
results_df.to_csv('../data/monte_carlo_sotp_results.csv', index=False)
"""
INDF Stock Price Monte Carlo Simulation
via SOTP Valuation of
1. ICBP DCF
2. Bogasari and Distribution EV/EBIT Multiple
3. Agribusiness EV Ownership Calculation
"""

""" Base Inputs """
FCF_BASE_PROJECTIONS    = [11407755, 11617793, 12197554, 12806424, 13445846] # ICBP FCF Projections
TOTAL_NET_DEBT          = 20239000  # ICBP Net Debt

BOGASARI_EBIT           = 2567040   # 2024 EBIT
DISTRIBUTION_EBIT       = 490000    # 2024 EBIT 
AGRIBUSINESS_EV         = 11107642  # 2024 Total Weighted EV



""" DCF Random Variables """
WACC_LIST               = [0.0914, 0.0964, 0.1014, 0.1064, 0.1114]
G_LIST                  = [0.02, 0.025, 0.03, 0.035, 0.04]

""" Bogasari Multiple Random Variables """
BOGASARI_EV_EBIT        = [7.045, 7.545, 8.045, 8.545, 9.045]

""" Distribution Multiple Random Variables """
DISTRIBUTION_EV_EBIT    = [7.96, 8.46, 8.96, 9.46, 9.96]

WEIGHTS                 = [0.10, 0.20, 0.40, 0.20, 0.10]

""" SOTP Random Variables """
HOLDING_DISCOUNT        = [0.55, 0.5, 0.45]
HOLDING_DISCOUNT_WEIGHT = [0.3, 0.4, 0.3]

SHARES_OUTSTANDING      = 8780  # INDF Shares Oustanding
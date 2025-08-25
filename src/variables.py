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

""" DCF Random Variables (Normal Distribution) """
WACC_MEAN               = 0.1014
WACC_STD_DEV            = 0.005

G_MEAN                  = 0.03
G_STD_DEV               = 0.005

""" Bogasari Multiple Random Variables (Normal Distribution) """
BOGASARI_EV_EBIT_MEAN   = 8.045
BOGASARI_EV_EBIT_STD_DEV= 0.5

""" Distribution Multiple Random Variables (Normal Distribution) """
DISTRIBUTION_EV_EBIT_MEAN   = 8.96
DISTRIBUTION_EV_EBIT_STD_DEV= 0.5

""" SOTP Random Variables (Normal Distribution) """
HOLDING_DISCOUNT_MEAN     = 0.5
HOLDING_DISCOUNT_STD_DEV  = 0.025

SHARES_OUTSTANDING      = 8780  # INDF Shares Outstanding (disesuaikan)
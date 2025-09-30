def simulate_etf_investment(
    monthly_investment=200,
    annual_return_rate=0.07,
    holding_years=10,
    regime="PEA",  # or "CTO"
    flat_tax_rate=0.30,
    social_charges_rate=0.172,
    final_salary_withdrawal=False
):
    """
    Simulates ETF investment with monthly contributions, annual compounding and taxation.

    Parameters:
    - monthly_investment (float): Monthly amount invested
    - annual_return_rate (float): Annualized return (e.g. 0.07 = 7%)
    - holding_years (int): Investment duration in years
    - regime (str): 'PEA' or 'CTO'
    - flat_tax_rate (float): Tax rate for CTO (30%)
    - social_charges_rate (float): Social charges for CTO (17.2%)
    - final_salary_withdrawal (bool): If True, includes gain as gross income

    Returns:
    - dict: with total invested, final value, taxes paid, and net gain
    """
    months = holding_years * 12
    monthly_return = (1 + annual_return_rate) ** (1 / 12) - 1
    values = []
    total_invested = 0
    current_value = 0

    for month in range(months):
        current_value = current_value * (1 + monthly_return) + monthly_investment
        total_invested += monthly_investment
        values.append(current_value)

    gain = current_value - total_invested

    if regime == "PEA": 
        tax = gain * social_charges_rate if holding_years >= 5 else gain * (flat_tax_rate + social_charges_rate)
    else:  # CTO
        tax = gain * flat_tax_rate

    net_gain = gain - tax
    final_value = total_invested + net_gain

    return {
        "Total invested (€)": round(total_invested),
        "Gross value after compounding (€)": round(current_value),
        "Capital gain (€)": round(gain),
        "Taxes paid (€)": round(tax),
        "Net gain (€)": round(net_gain),
        "Final value after tax (€)": round(final_value)
    }

if __name__ == "__main__":
    # Example usage
    results_pea = simulate_etf_investment(regime="PEA", holding_years=20)
    results_cto = simulate_etf_investment(regime="CTO", holding_years=20)

    print("PEA Investment Results:")
    for key, value in results_pea.items():
        print(f"{key}: {value} €")
    print("\nCTO Investment Results:")
    for key, value in results_cto.items():
        print(f"{key}: {value} €")


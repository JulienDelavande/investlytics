import numpy as np
def simulate_rental_investment(
    property_price=300_000,
    down_payment=50_000,
    loan_rate=0.02,
    loan_years=20,
    rental_income_monthly=1_300,
    annual_charges_fixed=3_000,
    annual_property_tax=1_000,
    annual_vacancy_rate=0.08,
    furnishing_cost=10_000,
    notary_and_agency_fees=15_000,
    amortization_years_building=30,
    amortization_years_furniture=7,
    amortization_years_fees=5,
    is_furnished=True,
    regime="LMNP",  # "LMNP" or "nue"
    income_tax_rate=0.3,
    social_charges_rate=0.172,
    property_value_growth=0.02,
    holding_period=10,
    notary_fees_rate=0.08
):
    loan_amount = property_price - down_payment
    months = loan_years * 12
    monthly_rate = loan_rate / 12
    monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
    total_loan_interest = monthly_payment * months - loan_amount

    annual_rent = rental_income_monthly * 12 * (1 - annual_vacancy_rate)

    building_value = property_price * 0.85
    amort_building = building_value / amortization_years_building
    amort_furniture = furnishing_cost / amortization_years_furniture if is_furnished else 0
    amort_fees = notary_and_agency_fees / amortization_years_fees

    total_rent_collected = 0
    total_charges = 0
    total_taxes = 0
    total_amortization = 0
    total_deductions_on_salary = 0
    total_tax_savings_on_salary = 0
    total_out_of_pocket = 0

    for year in range(1, holding_period + 1):
        rent = annual_rent
        charges = annual_charges_fixed + annual_property_tax
        amort_this_year = amort_building + amort_furniture + amort_fees if is_furnished else 0
        total_amortization += amort_this_year

        taxable_income = rent - charges
        tax = 0
        salary_deduction = 0
        tax_savings = 0

        if regime == "LMNP" and is_furnished:
            taxable_income -= amort_this_year
            taxable_income = max(taxable_income, 0)
            tax = taxable_income * (income_tax_rate + social_charges_rate)
        elif regime == "nue":
            result = taxable_income - loan_rate * loan_amount
            if result < 0:
                max_offset = 10700
                salary_deduction = min(abs(result), max_offset)
                tax_savings = salary_deduction * income_tax_rate
                tax = 0
            else:
                tax = result * (income_tax_rate + social_charges_rate)

        annual_credit_payment = monthly_payment * 12
        out_of_pocket_this_year = annual_credit_payment + charges + tax - rent
        total_out_of_pocket += out_of_pocket_this_year

        total_rent_collected += rent
        total_charges += charges
        total_taxes += tax
        total_deductions_on_salary += salary_deduction
        total_tax_savings_on_salary += tax_savings

    resale_price = property_price * ((1 + property_value_growth) ** holding_period)
    gross_capital_gain = resale_price - property_price
    tax_on_gain = 0 if holding_period >= 22 else gross_capital_gain * 0.362
    notary_fees = property_price * notary_fees_rate

    net_gain = (
        total_rent_collected
        - total_charges
        - total_taxes
        + resale_price
        - tax_on_gain
        - notary_fees
        - loan_amount
        - total_loan_interest
        + total_tax_savings_on_salary
    )

    total_value = net_gain + down_payment

    return {
        "Total rent collected (€)": round(total_rent_collected),
        "Total charges (€)": round(total_charges),
        "Total taxes on rent (€)": round(total_taxes),
        "Deductions on salary (nue only) (€)": round(total_deductions_on_salary),
        "Tax savings on salary (nue only) (€)": round(total_tax_savings_on_salary),
        "Total amortization (LMNP) (€)": round(total_amortization),
        "Resale price (€)": round(resale_price),
        "Tax on capital gain (€)": round(tax_on_gain),
        "Total interest paid (€)": round(total_loan_interest),
        "Monthly loan payment (€)": round(monthly_payment),
        "Net gain after holding period (€)": round(net_gain),
        "Total value after period (net gain + down payment) (€)": round(total_value),
        "Total out-of-pocket cost (€)": round(total_out_of_pocket),
        "Avg out-of-pocket per month (€)": round(total_out_of_pocket / (holding_period * 12)),
    }

if __name__ == "__main__":
    # Poitier
    property_price = 160_000
    down_payment = 50_000
    rental_income_monthly = 1000
    loan_rate = 0.03
    loan_years = 20
    annual_charges_fixed = 2500
    annual_property_tax = 800
    annual_vacancy_rate = 0.06
    furnishing_cost = 7_000
    notary_and_agency_fees = 12_000

    property_price = 270_000
    down_payment = 50_000
    loan_rate = 0.03
    loan_years = 20
    rental_income_monthly = 1_250
    annual_charges_fixed = 3_000
    annual_property_tax = 1_000
    annual_vacancy_rate = 0.06
    furnishing_cost = 8_000
    notary_and_agency_fees = 15_000
    holding_period = 15


    # Example usage
    results_lmnp = simulate_rental_investment(
        property_price=property_price,
        down_payment=down_payment,
        rental_income_monthly=rental_income_monthly,
        loan_rate=loan_rate,
        loan_years=loan_years,
        annual_charges_fixed=annual_charges_fixed,
        annual_property_tax=annual_property_tax,
        annual_vacancy_rate=annual_vacancy_rate,
        furnishing_cost=furnishing_cost,
        notary_and_agency_fees=notary_and_agency_fees,
        regime="LMNP",
        is_furnished=True
    )
    results_nue = simulate_rental_investment(
        property_price=property_price,
        down_payment=down_payment,
        rental_income_monthly=rental_income_monthly,
        loan_rate=loan_rate,
        loan_years=loan_years,
        annual_charges_fixed=annual_charges_fixed,
        annual_property_tax=annual_property_tax,
        annual_vacancy_rate=annual_vacancy_rate,
        furnishing_cost=furnishing_cost,
        notary_and_agency_fees=notary_and_agency_fees,
        regime="nue",
        is_furnished=False
    )
    print("Results for LMNP (Furnished):")
    for key, value in results_lmnp.items():
        print(f"{key}: {value}")
    print("\nResults for Nue (Unfurnished):")
    for key, value in results_nue.items():
        print(f"{key}: {value}")

# payroll_agent.py

# -------------------------------
# Step 0: Imports
# -------------------------------
from datetime import date

# -------------------------------
# Step 1: Constants
# -------------------------------
BIWEEKLY_PERIODS = 26
STATE_TAX_RATES = {
    "AL": 0.05, "AK": 0.0, "AZ": 0.0454, "AR": 0.05, "CA": 0.08, "CO": 0.0463,
    "CT": 0.069, "DE": 0.066, "FL": 0.0, "GA": 0.0575, "HI": 0.08, "ID": 0.068,
    "IL": 0.0495, "IN": 0.0323, "IA": 0.0853, "KS": 0.057, "KY": 0.05, "LA": 0.06,
    "ME": 0.0715, "MD": 0.0575, "MA": 0.05, "MI": 0.0425, "MN": 0.0985, "MS": 0.05,
    "MO": 0.054, "MT": 0.069, "NE": 0.0684, "NV": 0.0, "NH": 0.0, "NJ": 0.0575,
    "NM": 0.049, "NY": 0.065, "NC": 0.0525, "ND": 0.029, "OH": 0.04997, "OK": 0.05,
    "OR": 0.099, "PA": 0.0307, "RI": 0.059, "SC": 0.07, "SD": 0.0, "TN": 0.0,
    "TX": 0.0, "UT": 0.0495, "VT": 0.0875, "VA": 0.0575, "WA": 0.0, "WV": 0.065,
    "WI": 0.0765, "WY": 0.0
}
SOCIAL_SECURITY_RATE = 0.062
MEDICARE_RATE = 0.0145

# -------------------------------
# Step 2: Federal Tax Brackets (2025, biweekly)
# -------------------------------
FEDERAL_BRACKETS_BIWEEKLY = [
    (458, 0.10),
    (1865, 0.12),
    (3978, 0.22),
    (7584, 0.24),
    (9630, 0.32),
    (24073, 0.35),
    (float('inf'), 0.37)
]

# -------------------------------
# Step 3: Helper Functions
# -------------------------------
def calculate_federal_tax(taxable_income):
    tax = 0
    prev_limit = 0

    for limit, rate in FEDERAL_BRACKETS_BIWEEKLY:
        if taxable_income <= limit:
            tax += (taxable_income - prev_limit) * rate
            break
        else:
            tax += (limit - prev_limit) * rate
            prev_limit = limit

    return tax


def calculate_state_tax(taxable_income, state):
    rate = STATE_TAX_RATES.get(state.upper(), 0)
    return taxable_income * rate

# -------------------------------
# Step 4: Main Payroll Calculation
# -------------------------------
def generate_biweekly_payslip(name, annual_salary, employee_401k_pct, state):
    biweekly_gross = annual_salary / BIWEEKLY_PERIODS
    employee_401k = biweekly_gross * (employee_401k_pct / 100)
    taxable_income = biweekly_gross - employee_401k

    federal_tax = calculate_federal_tax(taxable_income)
    social_security = taxable_income * SOCIAL_SECURITY_RATE
    medicare = taxable_income * MEDICARE_RATE
    state_tax = calculate_state_tax(taxable_income, state)

    net_pay = taxable_income - (federal_tax + social_security + medicare + state_tax)

    payslip = {
        "Name": name,
        "Gross Pay": round(biweekly_gross, 2),
        "401k Deduction": round(employee_401k, 2),
        "Federal Tax": round(federal_tax, 2),
        "Social Security": round(social_security, 2),
        "Medicare": round(medicare, 2),
        "State Tax": round(state_tax, 2),
        "Net Pay": round(net_pay, 2)
    }
    return payslip

# -------------------------------
# Step 5: Example Usage
# -------------------------------
if __name__ == "__main__":
#    name = "Arif Shaik"
#    annual_salary = 65000
#    employee_401k_pct = 6
#    state = "CA"
    name = input("Enter employee name: ")
    annual_salary = float(input("Enter annual salary (USD): "))
    employee_401k_pct = float(input("Enter 401k deduction %: "))
    state = input("Enter state (e.g., AR): ")

    payslip = generate_biweekly_payslip(name, annual_salary, employee_401k_pct, state)

    print("\n--- Biweekly Payslip ---")
    for key, value in payslip.items():
        print(f"{key}: ${value}")

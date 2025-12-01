
# Constants for California electricity rates
CA_AVG_RATE = 0.30  # $0.30 per kWh (California average)
PGE_SLO_RATE = 0.32  # Adjust based on actual PGE rate for SLO
DAYS = 365


def total_cost_savings(data, rate_per_kwh=CA_AVG_RATE):


    total_kwh = sum(energy.goldtree + energy.housing for energy in data)
    total_savings = total_kwh * rate_per_kwh
    days_analyzed = len(data)

    return {
        'total_kwh_produced': total_kwh,
        'total_savings': total_savings,
        'days_analyzed': days_analyzed,
        'rate_used': rate_per_kwh
    }


def monthly_savings_breakdown(data, rate_per_kwh=CA_AVG_RATE):

    monthly_data = {}
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Group data by month
    for energy in data:
        key = (energy.year, energy.month)
        if key not in monthly_data:
            monthly_data[key] = {
                'total_kwh': 0,
                'days': 0
            }
        monthly_data[key]['total_kwh'] += (energy.gold + energy.housing)
        monthly_data[key]['days'] += 1

    # Calculate savings for each month
    monthly_savings = {}
    for (year, month), data_dict in sorted(monthly_data.items()):
        month_label = f"{year}-{month_names[month - 1]}"
        total_kwh = data_dict['total_kwh']
        savings = total_kwh * rate_per_kwh

        monthly_savings[month_label] = {
            'total_kwh': total_kwh,
            'total_savings': savings,
            'days_recorded': data_dict['days'],
            'avg_daily_kwh': total_kwh / data_dict['days'],
            'avg_daily_savings': savings / data_dict['days']
        }

    return monthly_savings


def yearly_savings_projection(data, rate_per_kwh=CA_AVG_RATE):
    total_kwh = sum(energy.gold + energy.housing for energy in data)
    days_analyzed = len(data)

    # Calculate daily average
    avg_daily_kwh = total_kwh / days_analyzed
    avg_daily_savings = avg_daily_kwh * rate_per_kwh

    #  Yearly Analysis (365 days)
    projected_annual_kwh = avg_daily_kwh * DAYS
    projected_annual_savings = projected_annual_kwh * rate_per_kwh

    # Calculate based on 500 days of data

    months_in_data = days_analyzed / 30.44  # Average days per month
    projected_12_month_kwh = (total_kwh / days_analyzed) * DAYS
    projected_12_month_savings = projected_12_month_kwh * rate_per_kwh

    return {
        'days_analyzed': days_analyzed,
        'avg_daily_kwh': avg_daily_kwh,
        'avg_daily_savings': avg_daily_savings,
        'projected_annual_kwh': projected_annual_kwh,
        'projected_annual_savings': projected_annual_savings,
        'rate_used': rate_per_kwh
    }


def pge_comparison(data, solar_rate=CA_AVG_RATE, pge_rate=PGE_SLO_RATE):

    total_kwh = sum(energy.gold + energy.housing for energy in data)
    days_analyzed = len(data)

    # What Cal Poly saved with solar
    solar_savings = total_kwh * solar_rate

    # What Cal Poly would have paid PG&E for same energy
    pge_cost = total_kwh * pge_rate

    # Additional savings from avoiding PG&E's higher rate
    additional_savings = pge_cost - solar_savings

    # Project to annual
    avg_daily_kwh = total_kwh / days_analyzed
    annual_kwh = avg_daily_kwh * DAYS

    annual_solar_value = annual_kwh * solar_rate
    annual_pge_cost = annual_kwh * pge_rate
    annual_savings_vs_pge = annual_pge_cost - annual_solar_value

    return {
        'total_kwh_produced': total_kwh,
        'days_analyzed': days_analyzed,

        # Solar value
        'solar_value': solar_savings,
        'solar_rate': solar_rate,

        # PG&E comparison
        'pge_cost_equivalent': pge_cost,
        'pge_rate': pge_rate,
        'savings_vs_pge': pge_cost,  # Total avoided cost

        # Annual projections
        'projected_annual_kwh': annual_kwh,
        'projected_annual_solar_value': annual_solar_value,
        'projected_annual_pge_cost': annual_pge_cost,
        'projected_annual_savings_vs_pge': annual_savings_vs_pge,

        # Percentage savings
        'percent_saved_vs_pge': (annual_savings_vs_pge / annual_pge_cost * 100) if annual_pge_cost > 0 else 0
    }


def comprehensive_cost_analysis(data, ca_rate=CA_AVG_RATE, pge_rate=PGE_SLO_RATE):

    return {
        'total_savings': total_cost_savings(data, ca_rate),
        'monthly_breakdown': monthly_savings_breakdown(data, ca_rate),
        'yearly_projection': yearly_savings_projection(data, ca_rate),
        'pge_comparison': pge_comparison(data, ca_rate, pge_rate)
    }


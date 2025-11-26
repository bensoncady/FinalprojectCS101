#All Analysis Functions (TASK 2)

"Production Analysis Functions"

def production_analysis(data):
    if not data:
        return None

#Total energy production for each farm
    total_goldtree = sum(energy.goldtree for energy in data)
    total_housing = sum(energy.housing for energy in data)

#Total Combined energy production
    total_production = total_goldtree + total_housing

#Average daily production between both farms
    avg_daily = total_production / len(data)

#Highest and lowest production days
    highest_day = max(data, key=lambda x: x.housing + x.goldtree)
    lowest_day = min(data, key=lambda x: x.housing + x.goldtree)

    return {
        'days_analyzed': len(data),
        'total_production_kwh': total_production,
        'total_goldtree_kwh': total_goldtree,
        'total_housing_kwh': total_housing,
        'average_daily_kwh': avg_daily,
        'highest_day_kwh': highest_day,
        'lowest_day_kwh': lowest_day,
    }

"SEASONAL TREND FUNCTIONS"

#Analyzing production by season, the following
#Following function is a dictionary of seasons

def seasonal_analysis(data):
    seasons = {
        'Winter': [12,1,2],
        'Spring': [3,4,5],
        'Summer': [6,7,8],
        'Autumn': [9,10,11],
    }

    # This groups the data by the seasons
    seasonal_data = {season: [] for season in seasons}

    for energy in data:
        for season, months in seasons.items():
            if energy.month in months:
                seasonal_data[season].append(energy.gold + energy.housing)
                break

    # The following will calculate the average, total, max, min, and days
    #of production per season
    seasonal_stats = {}
    for season, productions in seasonal_data.items():
        if productions:
            seasonal_stats[season] = {
                'avg_production': sum(productions) / len(productions),
                'total_production': sum(productions),
                'max_production': max(productions),
                'min_production': min(productions),
                'days': len(productions)
            }
        else:
            seasonal_stats[season] = None
#returns the above:)
    return seasonal_stats

#The following is the monthly analysis of solar production
def monthly_analysis(data):
    monthly_data = {}
    for energy in data:
        key = (energy.year, energy.month)
        if key not in monthly_data:
            monthly_data[key] = []
        monthly_data[key].append(energy.gold + energy.housing)
#dictionary of each month
    monthly_stats = {}
    monthly_names = ['January', 'February', 'March', 'April', 'May','June',
                     'July', 'August', 'September','October', 'November', 'December'] #
#Calculates the total, avg, max, min, and days recorded for each month's production
    for (year, month), productions in sorted(monthly_data.items()):
        month_label = f"{year}-{monthly_names[month - 1]}"
        monthly_stats[month_label] = {
            'total_production': sum(productions),
            'avg_daily_production': sum(productions) / len(productions),
            'days_recorded': len(productions),
            'max_day': max(productions),
            'min_day': min(productions)
        }

        return monthly_stats


from builddata import *
import unittest
import main
import Analysis


class TestCases(unittest.TestCase):

    def test_production_analysis(self):
        input = get_data()
        expected = {'days_analyzed': 494, 'total_production_kwh': 16228563.75002776, 'total_goldtree_kwh': 13297078.00002776, 'total_housing_kwh': 2931485.75, 'average_daily_kwh': 32851.34362353798, 'highest_day_kwh': Energy(2024, 10, 23, 25761.04274, 420060.25), 'lowest_day_kwh': Energy(2024, 10, 24, 4.923076928, 1272.5)}
        result = Analysis.production_analysis(input)
        self.assertEqual(expected, result)

    def test_seasonal_analysis(self):
        input = get_data()
        expected = {'Winter': {'avg_production': 18386.744252873563, 'total_production': 1599646.75, 'max_production': 31258.25, 'min_production': 3981.25, 'days': 87}, 'Spring': {'avg_production': 33082.43750024783, 'total_production': 3043584.2500228, 'max_production': 256480.75, 'min_production': 1924.1712428, 'days': 92}, 'Summer': {'avg_production': 38627.0114379085, 'total_production': 5909932.75, 'max_production': 47944.75, 'min_production': 20567.0, 'days': 153}, 'Autumn': {'avg_production': 35033.33333336395, 'total_production': 5675400.00000496, 'max_production': 445821.29274, 'min_production': 1277.423076928, 'days': 162}}
        result = Analysis.seasonal_analysis(input)
        self.assertEqual(expected, result)

    def test_monthly_analysis(self):
        input = get_data()
        expected = {'2024-July': {'total_production': 1088755.875, 'avg_daily_production': 35121.157258064515, 'days_recorded': 31, 'max_day': 39114.875, 'min_day': 26000.625}}
        result = Analysis.monthly_analysis(input)
        self.assertEqual(expected, result)




if __name__ == '__main__':
    unittest.main()
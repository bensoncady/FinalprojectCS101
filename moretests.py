import unittest
from builddata import get_data
from CostSavings import (
    total_cost_savings,
    monthly_savings_breakdown,
    yearly_savings_projection,
    pge_comparison,
    comprehensive_cost_analysis
)


class TestCostSavingsRealData(unittest.TestCase):
    """Test cost savings functions with actual Cal Poly data"""

    @classmethod
    def setUpClass(cls):
        """Load real data once for all tests"""
        cls.real_data = get_data()
        print(f"\nLoaded {len(cls.real_data)} days of real Cal Poly solar data")

    def test_total_cost_savings_real_data(self):
        """Test total_cost_savings with real Cal Poly data"""
        print("\n--- TEST: total_cost_savings ---")

        result = total_cost_savings(self.real_data, rate_per_kwh=0.30)

        # Verify result structure
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Check all required keys are present
        self.assertIn('total_kwh_produced', result)
        self.assertIn('total_savings', result)
        self.assertIn('days_analyzed', result)
        self.assertIn('rate_used', result)

        # Verify realistic values for ~500 days
        self.assertGreater(result['total_savings'], 4_000_000,
                           "Total savings should be > $4M")
        self.assertLess(result['total_savings'], 6_000_000,
                        "Total savings should be < $6M")

        # Verify days analyzed matches data length
        self.assertEqual(result['days_analyzed'], len(self.real_data))

        # Verify rate stored correctly
        self.assertEqual(result['rate_used'], 0.30)

        # Verify total kWh is positive and reasonable
        self.assertGreater(result['total_kwh_produced'], 10_000_000)
        self.assertLess(result['total_kwh_produced'], 25_000_000)

        print(f"✓ Total Savings: ${result['total_savings']:,.2f}")
        print(f"✓ Total kWh: {result['total_kwh_produced']:,.0f}")
        print(f"✓ Days Analyzed: {result['days_analyzed']}")
        print(f"✓ Rate Used: ${result['rate_used']:.2f}/kWh")

    def test_monthly_savings_breakdown_real_data(self):
        """Test monthly_savings_breakdown with real Cal Poly data"""
        print("\n--- TEST: monthly_savings_breakdown ---")

        result = monthly_savings_breakdown(self.real_data, rate_per_kwh=0.30)

        # Verify result structure
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Should have at least 15 months of data (July 2024 - Nov 2025)
        self.assertGreaterEqual(len(result), 15,
                                "Should have at least 15 months of data")

        # Verify each month has required keys
        for month, stats in result.items():
            self.assertIn('total_kwh', stats)
            self.assertIn('total_savings', stats)
            self.assertIn('days_recorded', stats)
            self.assertIn('avg_daily_kwh', stats)
            self.assertIn('avg_daily_savings', stats)

            # All values should be positive
            self.assertGreater(stats['total_savings'], 0,
                               f"{month} savings should be positive")
            self.assertGreater(stats['total_kwh'], 0,
                               f"{month} kWh should be positive")
            self.assertGreater(stats['days_recorded'], 0,
                               f"{month} should have days recorded")

            # Verify avg calculations are correct
            expected_avg_kwh = stats['total_kwh'] / stats['days_recorded']
            self.assertAlmostEqual(stats['avg_daily_kwh'], expected_avg_kwh, places=2)

            expected_avg_savings = stats['total_savings'] / stats['days_recorded']
            self.assertAlmostEqual(stats['avg_daily_savings'], expected_avg_savings, places=2)

        # Verify total across all months matches total_cost_savings
        total_from_months = sum(stats['total_savings'] for stats in result.values())
        total_result = total_cost_savings(self.real_data, rate_per_kwh=0.30)
        self.assertAlmostEqual(total_from_months, total_result['total_savings'], places=2,
                               msg="Sum of monthly savings should equal total savings")

        print(f"✓ Months Analyzed: {len(result)}")
        print(f"✓ Sample Month (2024-July): ${result['2024-July']['total_savings']:,.2f}")
        print(f"✓ Total from Months: ${total_from_months:,.2f}")

    def test_yearly_savings_projection_real_data(self):
        """Test yearly_savings_projection with real Cal Poly data"""
        print("\n--- TEST: yearly_savings_projection ---")

        result = yearly_savings_projection(self.real_data, rate_per_kwh=0.30)

        # Verify result structure
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Check all required keys
        required_keys = ['days_analyzed', 'avg_daily_kwh', 'avg_daily_savings',
                         'projected_annual_kwh', 'projected_annual_savings', 'rate_used']
        for key in required_keys:
            self.assertIn(key, result)

        # Verify days analyzed
        self.assertEqual(result['days_analyzed'], len(self.real_data))

        # Verify rate stored correctly
        self.assertEqual(result['rate_used'], 0.30)

        # Verify realistic annual projection ($3-5M per year)
        self.assertGreater(result['projected_annual_savings'], 3_000_000,
                           "Annual projection should be > $3M")
        self.assertLess(result['projected_annual_savings'], 5_000_000,
                        "Annual projection should be < $5M")

        # Verify annual kWh is reasonable (10-15M kWh)
        self.assertGreater(result['projected_annual_kwh'], 10_000_000,
                           "Annual kWh should be > 10M")
        self.assertLess(result['projected_annual_kwh'], 15_000_000,
                        "Annual kWh should be < 15M")

        # Verify average daily calculations
        self.assertGreater(result['avg_daily_kwh'], 25_000)
        self.assertLess(result['avg_daily_kwh'], 45_000)

        # Verify projection math: annual = daily avg * 365
        expected_annual_kwh = result['avg_daily_kwh'] * 365
        self.assertAlmostEqual(result['projected_annual_kwh'], expected_annual_kwh, places=2)

        expected_annual_savings = result['avg_daily_savings'] * 365
        self.assertAlmostEqual(result['projected_annual_savings'], expected_annual_savings, places=2)

        print(f"✓ Days Analyzed: {result['days_analyzed']}")
        print(f"✓ Avg Daily kWh: {result['avg_daily_kwh']:,.0f}")
        print(f"✓ Avg Daily Savings: ${result['avg_daily_savings']:,.2f}")
        print(f"✓ Projected Annual kWh: {result['projected_annual_kwh']:,.0f}")
        print(f"✓ Projected Annual Savings: ${result['projected_annual_savings']:,.2f}")

    def test_pge_comparison_real_data(self):
        """Test pge_comparison with real Cal Poly data"""
        print("\n--- TEST: pge_comparison ---")

        result = pge_comparison(self.real_data, solar_rate=0.30, pge_rate=0.32)

        # Verify result structure
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Check all required keys
        required_keys = ['total_kwh_produced', 'days_analyzed', 'solar_value',
                         'solar_rate', 'pge_cost_equivalent', 'pge_rate',
                         'savings_vs_pge', 'projected_annual_kwh',
                         'projected_annual_solar_value', 'projected_annual_pge_cost',
                         'projected_annual_savings_vs_pge', 'percent_saved_vs_pge']
        for key in required_keys:
            self.assertIn(key, result)

        # Verify days analyzed
        self.assertEqual(result['days_analyzed'], len(self.real_data))

        # Verify rates stored correctly
        self.assertEqual(result['solar_rate'], 0.30)
        self.assertEqual(result['pge_rate'], 0.32)

        # PG&E cost should be higher than solar value (higher rate)
        self.assertGreater(result['pge_cost_equivalent'], result['solar_value'],
                           "PG&E cost should be higher than solar value")

        # Verify realistic values
        self.assertGreater(result['savings_vs_pge'], 4_000_000,
                           "Savings vs PG&E should be > $4M")
        self.assertLess(result['savings_vs_pge'], 7_000_000,
                        "Savings vs PG&E should be < $7M")

        # Verify annual projections are positive
        self.assertGreater(result['projected_annual_savings_vs_pge'], 0)
        self.assertGreater(result['projected_annual_pge_cost'], 0)
        self.assertGreater(result['projected_annual_solar_value'], 0)

        # Verify percent saved calculation
        expected_percent = (result['projected_annual_savings_vs_pge'] /
                            result['projected_annual_pge_cost'] * 100)
        self.assertAlmostEqual(result['percent_saved_vs_pge'], expected_percent, places=2)

        # Percent should be reasonable (not negative, not > 100%)
        self.assertGreater(result['percent_saved_vs_pge'], 0)
        self.assertLess(result['percent_saved_vs_pge'], 100)

        # Verify total kWh matches
        total_result = total_cost_savings(self.real_data, rate_per_kwh=0.30)
        self.assertAlmostEqual(result['total_kwh_produced'],
                               total_result['total_kwh_produced'], places=2)

        print(f"✓ Total kWh: {result['total_kwh_produced']:,.0f}")
        print(f"✓ Solar Value: ${result['solar_value']:,.2f}")
        print(f"✓ PG&E Cost Equivalent: ${result['pge_cost_equivalent']:,.2f}")
        print(f"✓ Savings vs PG&E: ${result['savings_vs_pge']:,.2f}")
        print(f"✓ Annual Savings vs PG&E: ${result['projected_annual_savings_vs_pge']:,.2f}")
        print(f"✓ Percent Saved vs PG&E: {result['percent_saved_vs_pge']:.2f}%")

    def test_comprehensive_cost_analysis_real_data(self):
        """Test comprehensive_cost_analysis with real Cal Poly data"""
        print("\n--- TEST: comprehensive_cost_analysis ---")

        result = comprehensive_cost_analysis(self.real_data, ca_rate=0.30, pge_rate=0.32)

        # Verify result structure - should contain all sub-analyses
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Check that all four sub-analyses are present
        self.assertIn('total_savings', result)
        self.assertIn('monthly_breakdown', result)
        self.assertIn('yearly_projection', result)
        self.assertIn('pge_comparison', result)

        # Verify each sub-analysis exists and has data
        self.assertIsNotNone(result['total_savings'])
        self.assertIsNotNone(result['monthly_breakdown'])
        self.assertIsNotNone(result['yearly_projection'])
        self.assertIsNotNone(result['pge_comparison'])

        # Verify total_savings component
        self.assertIn('total_savings', result['total_savings'])
        self.assertIn('total_kwh_produced', result['total_savings'])
        self.assertGreater(result['total_savings']['total_savings'], 4_000_000)

        # Verify monthly_breakdown component
        self.assertIsInstance(result['monthly_breakdown'], dict)
        self.assertGreaterEqual(len(result['monthly_breakdown']), 15,
                                "Should have at least 15 months")

        # Verify yearly_projection component
        self.assertIn('projected_annual_savings', result['yearly_projection'])
        self.assertIn('projected_annual_kwh', result['yearly_projection'])
        self.assertGreater(result['yearly_projection']['projected_annual_savings'], 3_000_000)

        # Verify pge_comparison component
        self.assertIn('savings_vs_pge', result['pge_comparison'])
        self.assertIn('pge_cost_equivalent', result['pge_comparison'])
        self.assertGreater(result['pge_comparison']['savings_vs_pge'], 4_000_000)

        # Verify consistency across components
        # Total kWh should be the same in all components
        total_kwh = result['total_savings']['total_kwh_produced']
        self.assertAlmostEqual(result['pge_comparison']['total_kwh_produced'],
                               total_kwh, places=2)

        # Days analyzed should be consistent
        days = result['total_savings']['days_analyzed']
        self.assertEqual(result['yearly_projection']['days_analyzed'], days)
        self.assertEqual(result['pge_comparison']['days_analyzed'], days)

        # Monthly breakdown should sum to total
        monthly_total = sum(month['total_savings']
                            for month in result['monthly_breakdown'].values())
        self.assertAlmostEqual(monthly_total,
                               result['total_savings']['total_savings'], places=2)

        print(f"✓ Cost Savings Analysis Completed!")
        print(f"  - Total Savings: ${result['total_savings']['total_savings']:,.2f}")
        print(f"  - Months Analyzed: {len(result['monthly_breakdown'])}")
        print(f"  - Annual Projection: ${result['yearly_projection']['projected_annual_savings']:,.2f}")
        print(f"  - PG&E Savings: ${result['pge_comparison']['savings_vs_pge']:,.2f}")



if __name__ == '__main__':
    unittest.main(verbosity=2)
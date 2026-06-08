import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import AdvertisingEfficiencyGoogleSearchModel


class TestAdvertisingEfficiencyGoogleSearchModelComprehensive(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_metadata_and_getters_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = AdvertisingEfficiencyGoogleSearchModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.LEADS])

        # Verify explicit required variable signature bounds for the upgraded lead funnel
        self.assertEqual(
            model.required_variables,
            [
                variable_names.ADVERTISING_COST,
                variable_names.CPC_GOOGLE_SEARCH,
                variable_names.CONVERSION_RATE_GOOGLE_SEARCH
            ]
        )

        # Verify custom optional array mappings
        self.assertEqual(
            sorted(model.optional_variables),
            sorted([variable_names.USD_TO_RMB, variable_names.ALLOCATION_GOOGLE_SEARCH])
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables uses the new dictionary format."""
        model = AdvertisingEfficiencyGoogleSearchModel()
        self.assertIsInstance(model._optional_variables, dict)

    def test_internal_optional_variables_have_correct_default_values(self):
        """Verify that the cross-border currency rate and search allocation default to 1.0."""
        model = AdvertisingEfficiencyGoogleSearchModel()
        self.assertEqual(model._optional_variables[variable_names.USD_TO_RMB], 1.0)
        self.assertEqual(model._optional_variables[variable_names.ALLOCATION_GOOGLE_SEARCH], 1.0)

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_and_getter_happy_path(self):
        """Verify the property setter completely overwrites and binds the active state."""
        model = AdvertisingEfficiencyGoogleSearchModel()
        fresh_inputs = {
            variable_names.ADVERTISING_COST: 2250.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04
        }

        # Fire property setter
        model.input_variables = fresh_inputs

        # Verify getter returns the exact structural dictionary reference
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify that passing None to the property setter securely defaults to an empty dictionary."""
        initial_inputs = {variable_names.ADVERTISING_COST: 2000.0}
        model = AdvertisingEfficiencyGoogleSearchModel(initial_inputs)

        # Overwrite context explicitly with None via property assign
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify individual metric updates when providing raw string identities and values."""
        model = AdvertisingEfficiencyGoogleSearchModel()
        model.update_input_variable(variable_names.ADVERTISING_COST, 2500.0)
        self.assertEqual(model.input_variables[variable_names.ADVERTISING_COST], 2500.0)

    def test_update_input_variable_with_duck_typed_properties(self):
        """Verify individual metric updates using domain variable Type A objects (.name, .expected_value)."""
        model = AdvertisingEfficiencyGoogleSearchModel()

        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.CONVERSION_RATE_GOOGLE_SEARCH
                self.expected_value = 0.04

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.CONVERSION_RATE_GOOGLE_SEARCH], 0.04)

    def test_update_input_variable_with_duck_typed_getters(self):
        """Verify individual metric updates using domain variable Type B objects (.get_name(), .get_value())."""
        model = AdvertisingEfficiencyGoogleSearchModel()

        class DuckTypeB:
            def get_name(self):
                return variable_names.CPC_GOOGLE_SEARCH

            def get_value(self):
                return 2.50

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.CPC_GOOGLE_SEARCH], 2.50)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.ADVERTISING_COST: 2250.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 0.60,
            variable_names.USD_TO_RMB: 1.0
        }
        model = AdvertisingEfficiencyGoogleSearchModel(inputs)

        # Should clear without raising exceptions or logging errors
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    def test_check_variables_missing_required_logs_error_and_raises(self):
        """Verify check_variables triggers error logs and raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.ADVERTISING_COST: 2250.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.50
            # Missing variable_names.CONVERSION_RATE_GOOGLE_SEARCH!
        }
        model = AdvertisingEfficiencyGoogleSearchModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    def test_check_variables_missing_optional_logs_informational_alert(self):
        """Verify check_variables registers an informational alert but lets processing pass if optionals are absent."""
        valid_inputs_no_optionals = {
            variable_names.ADVERTISING_COST: 2250.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04
            # Missing optional optionsals: ALLOCATION_GOOGLE_SEARCH and USD_TO_RMB!
        }
        model = AdvertisingEfficiencyGoogleSearchModel(valid_inputs_no_optionals)

        # Execution must pass seamlessly
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            self.assertEqual(mock_log.info.call_count, 1)

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS & DIVISION HEALTH GUARDS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify formula execution targets established default parameters and currency adjustments accurately."""
        inputs = {
            variable_names.ADVERTISING_COST: 2250.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 0.60,
            variable_names.USD_TO_RMB: 1.0
        }
        model = AdvertisingEfficiencyGoogleSearchModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check:
        # Clicks = (2250.0 * 0.60) / (2.50 * 1.0) = 1350 / 2.5 = 540 Clicks
        # Leads  = 540 * 0.04 = 21.6 Leads
        expected_leads = (2250.0 * 0.60 * 0.04) / (2.50 * 1.0)
        self.assertAlmostEqual(enriched_output[variable_names.LEADS], expected_leads, places=4)
        self.assertAlmostEqual(enriched_output[variable_names.LEADS], 21.6, places=4)

        # Verify in-place structural validation rule
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_optional_fallbacks(self):
        """Verify formula execution defaults back to 1.0 scalars if optional parameters are completely omitted."""
        inputs = {
            variable_names.ADVERTISING_COST: 2000.0,
            variable_names.CPC_GOOGLE_SEARCH: 2.00,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.05
        }
        model = AdvertisingEfficiencyGoogleSearchModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check with fallbacks:
        # Leads = (2000.0 * 1.0 * 0.05) / (2.00 * 1.0) = 100 / 2 = 50.0 Leads
        self.assertAlmostEqual(enriched_output[variable_names.LEADS], 50.0, places=4)

    def test_evaluate_zero_denominator_handles_division_by_zero_safely(self):
        """Verify that the engine falls back safely to 0.0 Leads when the denominator products evaluate to zero."""
        inputs_zero_cpc = {
            variable_names.ADVERTISING_COST: 2000.0,
            variable_names.CPC_GOOGLE_SEARCH: 0.0,  # Boundary test case denominator anchor
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.05
        }
        model = AdvertisingEfficiencyGoogleSearchModel(inputs_zero_cpc)
        enriched_output = model.evaluate()

        # Assert crash guard catches evaluation loop safely
        self.assertEqual(enriched_output[variable_names.LEADS], 0.0)


if __name__ == "__main__":
    unittest.main()

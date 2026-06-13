import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import CostPerLeadGoogleSearchModel


class TestCostPerLeadGoogleSearchModelComprehensive(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_metadata_and_getters_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = CostPerLeadGoogleSearchModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.CPL_GOOGLE_SEARCH])

        # Verify explicit required variable signature bounds for isolating CPL
        self.assertEqual(
            model.required_variables,
            [
                variable_names.CPC_GOOGLE_SEARCH,
                variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
            ]
        )

        # Verify custom optional array mappings include allocation weights without exchange rates
        self.assertEqual(
            list(model.optional_variables),
            [variable_names.ALLOCATION_GOOGLE_SEARCH]
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables uses the expected dictionary format."""
        model = CostPerLeadGoogleSearchModel()
        self.assertIsInstance(model._optional_variables, dict)

    def test_internal_optional_variables_have_correct_default_values(self):
        """Verify that the search allocation defaults securely to 1.0."""
        model = CostPerLeadGoogleSearchModel()
        self.assertEqual(model._optional_variables[variable_names.ALLOCATION_GOOGLE_SEARCH], 1.0)

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_and_getter_happy_path(self):
        """Verify the property setter completely overwrites and binds the active state."""
        model = CostPerLeadGoogleSearchModel()
        fresh_inputs = {
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
        initial_inputs = {variable_names.CPC_GOOGLE_SEARCH: 2.50}
        model = CostPerLeadGoogleSearchModel(initial_inputs)

        # Overwrite context explicitly with None via property assign
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify individual metric updates when providing raw string identities and values."""
        model = CostPerLeadGoogleSearchModel()
        model.update_input_variable(variable_names.CPC_GOOGLE_SEARCH, 3.10)
        self.assertEqual(model.input_variables[variable_names.CPC_GOOGLE_SEARCH], 3.10)

    def test_update_input_variable_with_duck_typed_properties(self):
        """Verify individual metric updates using domain variable Type A objects (.name, .expected_value)."""
        model = CostPerLeadGoogleSearchModel()

        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.CONVERSION_RATE_GOOGLE_SEARCH
                self.expected_value = 0.05

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.CONVERSION_RATE_GOOGLE_SEARCH], 0.05)

    def test_update_input_variable_with_duck_typed_getters(self):
        """Verify individual metric updates using domain variable Type B objects (.get_name(), .get_value())."""
        model = CostPerLeadGoogleSearchModel()

        class DuckTypeB:
            @property
            def name(self) -> str:
                return variable_names.CPC_GOOGLE_SEARCH

            @property
            def expected_value(self):
                return 1.95

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.CPC_GOOGLE_SEARCH], 1.95)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 0.60
        }
        model = CostPerLeadGoogleSearchModel(inputs)

        # Should clear without raising exceptions or logging errors
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    def test_check_variables_missing_required_logs_error_and_raises(self):
        """Verify check_variables triggers error logs and raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.CPC_GOOGLE_SEARCH: 2.50
            # Missing variable_names.CONVERSION_RATE_GOOGLE_SEARCH!
        }
        model = CostPerLeadGoogleSearchModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    def test_check_variables_missing_optional_logs_informational_alert(self):
        """Verify check_variables registers an informational alert but lets processing pass if optionals are absent."""
        valid_inputs_no_optionals = {
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04
            # Missing optional optionsals: ALLOCATION_GOOGLE_SEARCH
        }
        model = CostPerLeadGoogleSearchModel(valid_inputs_no_optionals)

        # Execution must pass seamlessly
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            self.assertEqual(mock_log.info.call_count, 1)

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS & DIVISION HEALTH GUARDS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify formula execution targets blended multi-channel budget metrics accurately in USD."""
        inputs = {
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 0.60
        }
        model = CostPerLeadGoogleSearchModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check:
        # Blended CPL = 2.50 / (0.04 * 0.60) = 2.50 / 0.024 = 104.16666...
        expected_cpl = 2.50 / (0.04 * 0.60)
        self.assertAlmostEqual(enriched_output[variable_names.CPL_GOOGLE_SEARCH], expected_cpl, places=4)
        self.assertAlmostEqual(enriched_output[variable_names.CPL_GOOGLE_SEARCH], 104.1667, places=4)

        # Verify in-place structural validation rule
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_optional_fallbacks(self):
        """Verify formula execution defaults back to 1.0 allocation scalar if optional parameters are completely omitted."""
        inputs = {
            variable_names.CPC_GOOGLE_SEARCH: 3.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.05
        }
        model = CostPerLeadGoogleSearchModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check with fallback allocation = 1.0:
        # CPL = 3.50 / (0.05 * 1.0) = 3.50 / 0.05 = 70.0 USD
        self.assertAlmostEqual(enriched_output[variable_names.CPL_GOOGLE_SEARCH], 70.0, places=4)

    def test_evaluate_zero_denominator_product_handles_division_by_zero_safely(self):
        """Verify that the engine falls back safely to 0.0 CPL when a denominator metric zeros out."""
        inputs_zero_allocation = {
            variable_names.CPC_GOOGLE_SEARCH: 2.50,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.04,
            variable_names.ALLOCATION_GOOGLE_SEARCH: 0.0  # Zero denominator edge case
        }
        model = CostPerLeadGoogleSearchModel(inputs_zero_allocation)
        enriched_output = model.evaluate()

        # Assert zero crash guard handles processing cleanly
        self.assertEqual(enriched_output[variable_names.CPL_GOOGLE_SEARCH], 0.0)


if __name__ == "__main__":
    unittest.main()

"""Behavior checks for recursive field masking. All values are synthetic."""
import copy
import unittest
from Sensitive_data_making_Engine import mask_sensitive_data


class MaskingTests(unittest.TestCase):
    def test_nested_lists_and_case_insensitive_rules(self):
        value = {"profile": {"PASSWORD": "demo"}, "items": [{"Pin": 1234}]}
        self.assertEqual(mask_sensitive_data(value, ["Password", "PIN"]),
                         {"profile": {"PASSWORD": "********"}, "items": [{"Pin": "********"}]})

    def test_input_and_nested_containers_remain_independent(self):
        value = {"nested": [{"password": "demo", "public": [1, 2]}]}
        original = copy.deepcopy(value)
        result = mask_sensitive_data(value, ["password"])
        result["nested"][0]["public"].append(3)
        self.assertEqual(value, original)

    def test_whole_matching_value_is_replaced(self):
        self.assertEqual(mask_sensitive_data({"secret": {"x": 1}}, ["SECRET"]),
                         {"secret": "********"})

    def test_exact_matching_keeps_other_fields_visible(self):
        self.assertEqual(mask_sensitive_data({"password_hint": "demo", "email": "a@example.com"}, ["password"]),
                         {"password_hint": "demo", "email": "a@example.com"})

    def test_primitives_and_empty_values(self):
        for value in (None, True, 3, 1.5, "plain", [], {}):
            self.assertEqual(mask_sensitive_data(value, []), value)

    def test_generator_rules_are_used_at_all_depths(self):
        self.assertEqual(mask_sensitive_data({"a": [{"PASSWORD": "demo"}]},
                                            (key for key in ["password"])),
                         {"a": [{"PASSWORD": "********"}]})

    def test_invalid_target_rules_fail_clearly(self):
        for keys in ("password", [123], ["password", None]):
            with self.assertRaises(TypeError):
                mask_sensitive_data({}, keys)


if __name__ == "__main__":
    unittest.main()

import unittest
import pandas as pd
from utils import (
    parse_price,
    extract_street_names_from_subtree,
    merge_tree_classification_with_properties
)

class TestUtils(unittest.TestCase):

    # simple testing main function of parsing number from string to float
    def test_parse_price_valid(self):
        self.assertEqual(parse_price("€123,456.78"), 123456.78)
        self.assertEqual(parse_price("€1,000"), 1000.0)
        self.assertEqual(parse_price("€0.99"), 0.99)

    # testing invalid numbers
    def test_parse_price_invalid(self):
        self.assertIsNone(parse_price(None))
        self.assertIsNone(parse_price("Not a price"))
        self.assertIsNone(parse_price("€"))


    # testing on getting the street names of each categories
    def test_extract_street_flattening(self):
        sample_tree_data = {
            "area1": {
                "sub1": {
                    "street A": 5,
                    "street B": 10
                }
            },
            "area2": {
                "street C": 15
            }
        }
        expected = ["street A", "street B", "street C"]
        result = extract_street_names_from_subtree(sample_tree_data)
        self.assertCountEqual(result, expected)

    # testing on combining the identification of short or tall into the data list
    def test_combine_categorised_property_with_price(self):
        properties = pd.DataFrame({
            "Street Name": ["Street A", "Street B", "Street C"],
            "Price": [100000, 200000, 300000]
        })
        categorized_streets = {
            "tall": ["Street A", "Street C"],
            "short": ["Street B"]
        }
        result = merge_tree_classification_with_properties(properties, categorized_streets)

        self.assertIn("hasTallTree", result.columns)
        self.assertIn("hasShortTree", result.columns)
        self.assertEqual(result.loc[result["Street Name"] == "Street A", "hasTallTree"].iloc[0], 1)
        self.assertEqual(result.loc[result["Street Name"] == "Street B", "hasShortTree"].iloc[0], 1)
        self.assertEqual(result.loc[result["Street Name"] == "Street B", "hasTallTree"].iloc[0], 0)
        self.assertEqual(result.loc[result["Street Name"] == "Street C", "hasShortTree"].iloc[0], 0)


if __name__ == "__main__":
    unittest.main()

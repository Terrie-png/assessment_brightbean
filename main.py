from utils import fetch_and_parse_tree_data, load_property_csv, merge_tree_classification_with_properties
import numpy as np
import pandas as pd
import msvcrt

def display_average_prices(properties: pd.DataFrame):
    
    print("Support Evidence: ")
    if (properties["hasTallTree"] == 1).any():
        tall_avg = np.round(properties[properties["hasTallTree"] == 1]["Price"].mean(), 2)
        print(f"Average Price on Streets with Tall Trees: €{tall_avg:,} \n")
    else:
        print("No properties found on streets with tall trees.")

    if (properties["hasShortTree"] == 1).any():
        short_avg = np.round(properties[properties["hasShortTree"] == 1]["Price"].mean(), 2)
        print(f"Average Price on Streets with Short Trees: €{short_avg:,} \n")
    else:
        print("No properties found on streets with short trees.")

    if (short_avg > tall_avg):
        print("Answer:")
        print(f"Properties with short trees have higher average prices.\n")
    
    if(tall_avg > short_avg):
        print("Answer:")
        print(f"Properties with tall trees have higher average prices.\n")

if __name__ == "__main__":
    print("\n==================================================\n")
    print("Question:")
    print("Are houses more expensive on streets with tall trees compared to those with shorter trees?\n")
    # Step 1: Fetch tree data
    url = "https://hiring.brightbeam.engineering/dublin-trees.json"
    categorisedStreetNames = fetch_and_parse_tree_data(url)

    # Step 2: Load property CSV
    properties = load_property_csv("data/dublin-property.csv")

    # Step 3: Combine data
    combined_properties = merge_tree_classification_with_properties(properties, categorisedStreetNames)

    # Step 4: Validate if any street is ambiguously categorized
    masked_ambiguous_properties= combined_properties['hasTallTree'] == combined_properties['hasShortTree']
    if masked_ambiguous_properties.any():
        print("WARNING: Some streets are categorized as both Tall and Short.")
        print(combined_properties[masked_ambiguous_properties][["Street Name", "hasTallTree", "hasShortTree"]])


    # Step 5: Display average prices
    display_average_prices(combined_properties)
    
    print("\n==================================================")
    print("Press any key to quit...")
    msvcrt.getch()

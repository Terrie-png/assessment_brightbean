from utils import fetch_and_parse_tree_data, load_property_csv, combine_cateogrised_property_with_price
import numpy as np
import pandas as pd

def display_average_prices(result: pd.DataFrame):
    overall_avg = np.round(result["Price"].mean(), 2)
    print(f"Overall Average Price: €{overall_avg:,}")

    if (result["IsTreeTall"] == 1).any():
        tall_avg = np.round(result[result["IsTreeTall"] == 1]["Price"].mean(), 2)
        print(f"Average Price on Streets with Tall Trees: €{tall_avg:,}")
    else:
        print("No properties found on streets with tall trees.")

    if (result["IsTreeShort"] == 1).any():
        short_avg = np.round(result[result["IsTreeShort"] == 1]["Price"].mean(), 2)
        print(f"Average Price on Streets with Short Trees: €{short_avg:,}")
    else:
        print("No properties found on streets with short trees.")

    unknown_avg = result[result["IsTreeTall"].isna()]["Price"].mean()
    if not np.isnan(unknown_avg):
        unknown_avg = np.round(unknown_avg, 2)
        print(f"Average Price on Streets with No Tree Data: €{unknown_avg:,}")
        
    if (short_avg > tall_avg):
        print()
        print(f"Based on the statistic analysis, shorter trees' property tend to be more expensive than taller trees' property")
    
    if(tall_avg > short_avg):
        print()
        print(f"Based on the statistic analysis, taller trees' property tend to be more expensive than shorter trees' property")

if __name__ == "__main__":
    # Step 1: Fetch tree data
    categorisedStreetNames = fetch_and_parse_tree_data()

    # Step 2: Load property CSV
    properties = load_property_csv()

    # Step 3: Combine data
    result = combine_cateogrised_property_with_price(properties, categorisedStreetNames)

    # Step 4: Validate if any street is ambiguously categorized
    mask = result['IsTreeTall'] == result['IsTreeShort']
    if mask.any():
        print("WARNING: Some streets are categorized as both Tall and Short.")
        print(result[mask][["Street Name", "IsTreeTall", "IsTreeShort"]])



    # Step 5: Display average prices
    display_average_prices(result)

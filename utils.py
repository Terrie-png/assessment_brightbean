import requests
import pandas as pd
import numpy as np


# This is where I will fetch the tree data and get the street names
def fetch_and_parse_tree_data(url: str) -> dict:
    # fetching the json data
    response = requests.get(url)

    if not response.ok:
        raise RuntimeError(f"Failed to fetch data: {response.status_code}")
    
    # this is where i will be using the function to get the streets name
    return {
        "tall": extract_street_names_from_subtree(response.json()["tall"]),
        "short": extract_street_names_from_subtree(response.json()["short"])
    }


def extract_street_names_from_subtree(subtree: dict | int | float) -> list:
    # checking if the variaable is empty
    if isinstance(subtree, (int,float)):
        return[]
    
    streets = []
    
    # obtaining the tree names of using depth first traversal and is a recursive method.
    for  street_fragment, subtree_node in subtree.items():
        if isinstance(subtree_node, dict):
            streets.extend(extract_street_names_from_subtree(subtree_node)) 
        else:
            streets.append(street_fragment)
    return streets


def parse_price(price_str:str)->float:
    
    # checking the string if is empty or null
    if price_str is None or pd.isna(price_str):
        return None
    
    # price_str= price_str[1:]
    
    # this is a way of doing for replacing the comma and dot into an array and join them afterwards but can have more straight forward method.
    # This is for my personal references.
    
    # parts = [part.strip().replace(',', '') for part in price_str.split('.')]
    # try:
    #     data = float('.'.join(parts))
    #     return data
    # except:
    #     return None  
    
    try:
        # removing the euro sign and comma sing but not dot as it will auto convert in python
        clean_str = price_str.replace("€", "").replace(",","").strip()
        return float(clean_str)
    except (ValueError,TypeError):
        return None
            


def load_property_csv(file_path: str) -> pd.DataFrame:
    try:
        # reading from csv using windows-1252 encoding as tried multiple encoding method and this suit.
        properties = pd.read_csv(file_path,sep=",",encoding="Windows-1252")
        
        if properties.empty:
            raise ValueError("Loaded CSV file contains no data")
    
        # setting the street name to string just in case it auto configured on other data type.
        # altered street name and price column only as these 2 are the only columns will be used for answering the question.
        properties["Street Name"] = properties["Street Name"].astype(str)
        properties["Price"] = properties["Price"].astype(str).apply(parse_price)
        return properties
    
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Failed to decode file. Check encoding format")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Check delimiter and file structure")
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading CSV: {str(e)}")
    
def merge_tree_classification_with_properties(properties: pd.DataFrame, tree_data: dict[str,list[str]])->pd.DataFrame:
    if properties.empty:
        raise ValueError("Something wrong. There are no properties passed in.")
    
    # getting the tall list from the properties data
    tall_list = tree_data.get("tall",[])
    # getting the short tree list from the properties data
    short_list = tree_data.get("short",[])
    
    # setting the condition into an array for identifying
    conditions = [
        properties["Street Name"].isin(tall_list),
        properties["Street Name"].isin(short_list)
    ]
    
    # this will used as [1,0] means that if it matched the tall tree list then it will be 1 in that row.
    properties["hasTallTree"] = np.select(conditions, [1,0], default= np.nan)
    properties["hasShortTree"] = np.select(conditions,[0,1],default=np.nan)
    return properties


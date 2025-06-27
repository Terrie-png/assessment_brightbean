import requests
import pandas as pd
import numpy as np

def fetch_and_parse_tree_data(url: str) -> dict:
    response = requests.get(url)

    if not response.ok:
        raise RuntimeError(f"Failed to fetch data: {response.status_code}")
    
    return {
        "tall": extract_street_name(response.json()["tall"]),
        "short": extract_street_name(response.json()["short"])
    }


def extract_street_name(data: dict | int | float) -> list:
    
    if isinstance(data, (int,float)):
        return[]
    
    streets = []
    for key, value in data.items():
        if isinstance(value, dict):
            streets.extend(extract_street_name(value)) 
        else:
            streets.append(key)
    return streets


def parse_price(price_str:str)->float:
    
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
        clean_str = price_str.replace("€", "").replace(",","").strip()
        return float(clean_str)
    except (ValueError,TypeError):
        return None
            


def load_property_csv(file_path: str) -> pd.DataFrame:
    try:
        properties = pd.read_csv(file_path,sep=",",encoding="Windows-1252")
        
        if properties.empty:
            raise ValueError("Loaded CSV file contains no data")
    
        properties["Street Name"] = properties["Street Name"].astype(str)
        properties["Price"] = properties["Price"].astype(str).apply(parse_price)
        return properties
    
    except UnicodeDecodeError:
        raise UnicodeDecodeError("Failed to decode file. Check encoding format")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Check delimiter and file structure")
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading CSV: {str(e)}")
    
def combine_cateogrised_property_with_price(properties: pd.DataFrame, tree_data: dict[str,list[str]])->pd.DataFrame:
    
    tall_list = tree_data.get("tall",[])
    short_list = tree_data.get("short",[])
    
    conditions = [
        properties["Street Name"].isin(tall_list),
        properties["Street Name"].isin(short_list)
    ]
    
    properties["IsTreeTall"] = np.select(conditions, [1,0], default= np.nan)
    properties["IsTreeShort"] = np.select(conditions,[0,1],default=np.nan)
    return properties


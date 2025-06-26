import requests
import pandas as pd
import numpy as np

def fetch_and_parse_tree_data() -> dict:
    url = "https://hiring.brightbeam.engineering/dublin-trees.json"
    response = requests.get(url)

    if not response.ok:
        raise RuntimeError(f"Failed to fetch data: {response.status_code}")

    fetched_datas = response.json()
    categorisedStreetNames = {}
    
    for category in fetched_datas:
        categorisedStreetNames[category] = extract_street_name(fetched_datas[category])
        
    return categorisedStreetNames


def extract_street_name(obj: dict) -> list:
    streetNames = []
    for key, value in obj.items():
        if isinstance(value, (int, float)): 
            streetNames.append(key)
        elif isinstance(value, dict):
            streetNames.extend(extract_street_name(value)) 
    return streetNames


def parse_price_string(s:str):
    
    if s is None or pd.isna(s):
        return None
    
    s= s[1:]
    if pd.isna(s):
        return None
    
    parts = [part.strip().replace(',', '') for part in s.split('.')]
    
    try:
        data = float('.'.join(parts))
        return data
    except:
        return None  


def load_property_csv() -> pd.DataFrame:
    properties = pd.read_csv("data/dublin-property.csv",sep=",",encoding="Windows-1252")
    
    properties["Street Name"] = properties["Street Name"].astype(str)
    
    properties["Price"] = properties["Price"].astype(str).apply(parse_price_string)
    
    properties["Price"] = pd.to_numeric(properties["Price"], errors="raise")
    
    return properties

def combine_cateogrised_property_with_price(properties: pd.DataFrame, categorizedStreetNames: dict)->pd.DataFrame:
    
    tall_list = categorizedStreetNames.get("tall",[])
    short_list = categorizedStreetNames.get("short",[])
    
    conditions = [
        properties["Street Name"].isin(tall_list),
        properties["Street Name"].isin(short_list)
    ]
    
    properties["IsTreeTall"] = np.select(conditions, [1,0], default= np.nan)
    properties["IsTreeShort"] = np.select(conditions,[0,1],default=np.nan)
    return properties


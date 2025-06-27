# Tree Property Price Analysis

This program analyzes whether properties on streets with tall trees are more expensive than those with short trees in Dublin.

## Question
Are houses more expensive on streets with tall trees compared to those with shorter trees? Let's find out!

## Answer
Properties with tall trees have higher average prices.

Based on the data provided in data folder: 
Average Price on Streets with Tall Trees: €587,800.39 
Average Price on Streets with Short Trees: €488,981.66 


## Requirements

- Python 3.10+
- Pip package manager

## Installation
1. Create and activate a virtual environment (recommended but optional):

(Windows)
```bash
python -m venv venv
venv\Scripts\activate    # Windows
```

(Linux)
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
```

2. Installing the required dependencies package:
```bash
pip install -r requirements.txt
```

## Python Package Requirements
The following packages are required (automatically installed via requirements.txt):
- pandas
- numpy
- requests

## Running the program to view the result
1. After downloading the project open a terminal in the project
2. Execute the main script:
   ```bash
   python main.py
   ```
   or (just incase some installation is different)
   ```bash
   py main.py
   ```

## Output
The program will:
1. Fetch data from the Tree Property Data json provided
2. Load the property price data from a CSV which was inside named "data" folder
3. Merge the tree classification with property data
4. Calculate and display:
    - Average price for properties with tall trees
    - Average prices for properties with short trees
    - Comparison of both prices to proove if it was true that a property with having tall trees required more moneys.
  
## Sample Output
```
==================================================

Question:
Are houses more expensive on streets with tall trees compared to those with shorter trees?

Support Evidence: 
Average Price on Streets with Tall Trees: €587,800.39 

Average Price on Streets with Short Trees: €488,981.66 

Answer:
Properties with tall trees have higher average prices.


==================================================
```
## Testing
To run the unit test:
```bash
python -m unittest discover -s tests
```

## File Structure
<pre>assessment_brightbeam
├── data/
│   |── dublin-property.csv
|   └── dublin-trees.json
├── main.py
├── utils.py
├── tests/
|   └── test_utils.py
├── requirements.txt
└── README.md
</pre>


1. Main.py => the main script
2. utils.py => logic function within for solving the questions
3. tests => unit test script folder
4. test_utils.py => unit testing script
5. data => data folders
6. requirements.txt => dependencies or packages required for installing to run the program

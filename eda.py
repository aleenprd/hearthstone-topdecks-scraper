# %%
"""Perform EDA on HSTD cards."""

from IPython.display import display
import pandas as pd
import numpy as np
from typing import List, Dict
import ast

# Load dataset
INPUT_PATH = 'data/hstd_all_cards_merged.csv'
cards_df = pd.read_csv(INPUT_PATH, encoding='iso-8859-1')

# Trim the columns; exclude NLP
print("DataFrame loaded from: ")
kicked_cols = set([
    'summary',
    'text',
    'comments'
])

cards_df = cards_df.drop(columns=kicked_cols, axis=1)
kept_cols = set(cards_df.columns)

# Establish categorical cols
cat_cols = set([
    'type',
    'rarity',
    'class',
    'set',
    'mechanics',
    'school'
    ])

# This will be our card id
id_col = 'title'

# And numerical cols for later ease of manipulation
num_cols = list(kept_cols.difference(cat_cols))
num_cols.remove(id_col)

# Settle the remaining cols
final_cols = list(cat_cols) + num_cols
cat_cols = list(cat_cols)

# And re-arrange the columns in data type order
final_cols.insert(0, id_col)  # Insert at list top
cards_df = cards_df[final_cols]

# Start inspecting data characteristics
print("\nData shape: ", cards_df.shape)

# Try to display in iPython, else print to console
try:
    display(cards_df.head())
except:
    print(cards_df.head())

print("\nDataFrame data types:")
print(cards_df.dtypes)


# CATEGORICAL COLUMNS INSPECTION
# ---------------------------------- #
print("\nInspecting categorical columns: ", cat_cols)

# How many card cat?
# ---------------------- #
print()
print(
    f"{cards_df.type.nunique()} card types: ",
    np.sort(cards_df.type.unique()))

# How many rarity cat?
# ---------------------- #
print(
    f"{cards_df.rarity.nunique()} card rarities: ",
    np.sort(cards_df.rarity.unique()))


# How many spell school cat?
# ---------------------- #
def nan_to_str(x) -> str:
    """Change from np.nan to a str of choice."""
    if isinstance(x, str):
        return x
    else:
        return 'Not Spell'


cards_df.school = cards_df.school.apply(lambda x: nan_to_str(x))

print(
    f"{cards_df.school.nunique()} spell schools: ",
    np.sort(cards_df.school.unique()))


# How many card classes?
# Account for dual-class cards
# ---------------------- #
def normalize_card_classes(x):
    if len(x) > 1:
        return x[0] + '/' + x[1]
    else:
        return x[0]


# The name class conflicts with Python syntax
cards_df = cards_df.rename({'class': 'card_class'}, axis=1)

cards_df.card_class = cards_df.card_class.apply(lambda x: ast.literal_eval(x))
res = [normalize_card_classes(x) for x in cards_df.card_class]

# Apply the mapping
cards_df.card_class = cards_df.card_class.apply(
    lambda x: normalize_card_classes(x))

print(
    f"{cards_df.card_class.nunique()} card classes: ",
    np.sort(cards_df.card_class.unique()))

# How many card sets?
# ---------------------- #
cards_df.set = cards_df.set.apply(lambda x: x.replace(' ', ''))
cards_df.set = cards_df.set.apply(lambda x: x.replace("'", ''))

print(
    f"{cards_df.set.nunique()} card sets: ",
    np.sort(cards_df.set.unique()))

# How many unique card mechanics combinations?
# ---------------------- #
print(f"{cards_df.mechanics.nunique()} unique card mechanics combinations.")

# How many card mechanics?
# ---------------------- #
cards_df.mechanics = cards_df.mechanics.apply(lambda x: ast.literal_eval(x))
unique_card_mechanics = []

for m in cards_df.mechanics:
    for n in m:
        if n not in set(unique_card_mechanics):
            unique_card_mechanics.append(n)

print(
    f"{len(unique_card_mechanics)} unique card mechanics: ",
    unique_card_mechanics)

# NUMERICAL COLUMNS INSPECTION
# ---------------------------------- #
print("\nInspecting numerical columns: ", num_cols)

try:
    display(cards_df.describe())
except:
    print(cards_df.describe())

# %%

# %%
"""Perform EDA on HSTD cards."""

from IPython.display import display
import pandas as pd
import numpy as np
from typing import List, Dict
import ast
import plotly.express as px

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

# %%
# How many card classes?
# Account for dual-class cards
# ---------------------- #
def normalize_card_classes(x):
    if len(x) > 1:
        return x[0] + '-' + x[1]
    else:
        return x[0]
    
def flag_dual_class(x):
    if len(x) > 1:
        return 1
    else:
        return 0


# %%
# The name class conflicts with Python syntax
cards_df = cards_df.rename({'class': 'card_class'}, axis=1)
cards_df.card_class = cards_df.card_class.apply(lambda x: ast.literal_eval(x))

# Apply the normalization mapping

cards_df['dual_class'] = cards_df.card_class.apply(
    lambda x: flag_dual_class(x))

def get_dual_class_num(x: List, num: int) -> str:
    return x[num]

dual_class_cards_1 = cards_df[cards_df.dual_class == 1]
dual_class_cards_1.card_class = dual_class_cards_1.card_class.apply(
    lambda x: get_dual_class_num(x,0))

dual_class_cards_2 = cards_df[cards_df.dual_class == 1]
dual_class_cards_2.card_class = dual_class_cards_2.card_class.apply(
    lambda x: get_dual_class_num(x,1))

def filter_out_dual_clsss_cards(df: pd.DataFrame):
    return 1


# %%

# %%
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



# %%
# Top and bottom combinations by frequency.
# ---------------------- #
top_mechs = cards_df.mechanics.value_counts()

print("\nTop 10 card combinations: ")
display(top_mechs.head(11))

print("\nBottom 10 card combinations: ")
display(top_mechs.tail(10))

# %%
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
# MANA COST DISTRIBUTION
# ---------------------------------- #

def cost_categorical_bar(
    df: pd.DataFrame,
    category_orders: List,
    )
# %%
# Here we use a column with categorical data
def get_and_sort_int_cats(df: pd.DataFrame, colname: str) -> List:
    unique_sorted = np.sort(df[colname].unique())
    unique_sorted = [str(int(x)) for x in unique_sorted]
    
    return unique_sorted

unique_mana = get_and_sort_int_cats(cards_df, "cost")

def float_col_to_str(df: pd.DataFrame, colname: str) -> pd.DataFrame:
    df[colname] = cards_df[colname].astype(str)

# %%
def mana_by_card_type(
    df: pd.DataFrame, 
    main_colname: str, 
    color_colname: str, 
    unique: List, 
    color_pallette: List
) -> px.histogram:
    """Make plot."""
    fig = px.histogram(
        df,
        x=main_colname,
        color=color_colname,
        category_orders=dict(cost_cat=unique),
        opacity=1,
        color_discrete_sequence=color_pallette
    )

    fig.update_layout(
        title_text='Distribution of Mana Cost by Card Type', # title of plot
        xaxis_title_text='Mana Cost', # xaxis label
        yaxis_title_text='Count', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1, # gap between bars of the same location coordinates,
    )

    fig.show()

card_type_pallette = [
    px.colors.qualitative.Set3[5],
    px.colors.qualitative.Set3[4],
    px.colors.qualitative.Set3[6],
    px.colors.qualitative.Set3[9],
]
    
mana_by_card_type(cards_df, "cost_cat", "type", unique_mana, card_type_pallette)


# %%
color_palette = [
    "#513359",  # warlock
    "#55618d",  # mage
    "#782318",  # warrior
    "#a8adb4",  # priest
    "#725f52",  # neutral
    "#b07124",  # paladin
    "#38393f",  # rogue
    "#2e3561",  # shaman
    "#633e1e",  # druid
    "#3e5c1f",  # hunter
    "#1b3630",  # demon hunter
]
unique_card_class = [
    "Warlock", "Mage", "Warrior", "Priest", "Paladin",
    "Rogue", "Shaman", "Druid", "Demon Hunter",
    
]
mana_by_card_type(cards_df, "cost_cat", "card_class", unique_mana, color_palette)
# %%
# TODO
# Duplicate the dual class cards
# flag them as dual class in extra column

# %%

"""Merges multiple dataframes and saves to CSV."""


import pandas as pd

if __name__ == "__main__":
    df1 = pd.read_csv("data/hstd_all_cards.csv")
    df2 = pd.read_csv("data/hstd_failed_cards.csv")

    frames = [df1, df2]

    for df in frames:
        print(df.shape)

    df = pd.concat(frames)

    print(df.shape)

    df.to_csv("data/hstd_all_cards_merged.csv", index=False)

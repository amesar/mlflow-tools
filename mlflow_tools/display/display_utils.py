"""
Display utilities
"""

def process_df(df, columns=None, sort_attr="name", sort_order="asc", csv_file=None):
    if columns:
        df = df[columns]
    if sort_attr in df.columns:
        df.sort_values(by=[sort_attr], inplace=True, ascending=sort_order == "asc")
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    return df

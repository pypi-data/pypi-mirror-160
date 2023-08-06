import pandas as pd


def df_to_matrix(df, indices):
    """
    Convert a dataframe to a matrix.
    """
    return df.loc[:, indices].values

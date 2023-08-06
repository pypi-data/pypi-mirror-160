def get_cell(df, column, **kwargs):
    """Get a single cell value from a table.

    Parameters
    ----------
    df : data frame
        
    column : column to get a cell from
        
    **kwargs : columns names and values to filter rows
        

    Returns
    -------
    scalar
    """
    if column not in df.columns:
        raise ValueError(f"There is no column {column} in the data frame.")

    for key, val in kwargs.items():
        df = df[df[key] == val]

    # Filtering should return one row from data frame
    if df.shape[0] > 1:
        print(df)
        raise ValueError("get_cell() has returned multiple rows.")

    if df.shape[0] == 0:
        raise ValueError(f"get_cell() has returned 0 rows. \nParameters: {str(kwargs)}")

    return df[column].values[0]

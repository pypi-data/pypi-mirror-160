def dfget(df, column, **kwargs):
    for key, val in kwargs.items():
        df = df[df[key] == val]
    return df[column].values[0]

import random

def train_test_split_func(df_x, df_y, test_size = 0.2):
    rows = df_x.shape[0]
    ids = random.sample(list(df_x.index), int(rows * (1 - test_size)))
    train_index = df_x.index.isin(ids)
    train_x = df_x[train_index]
    train_y = df_y[train_index]
    test_index = ~df_x.index.isin(ids)
    test_x = df_x[test_index]
    test_y = df_y[test_index]
    return train_x, test_x, train_y, test_y
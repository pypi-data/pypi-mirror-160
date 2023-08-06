import numpy as np
import pandas as pd

def check_iv(x, y, n_bins = 10):
    x = np.ravel(x)
    y = np.ravel(y)
    if x.size != y.size:
        print('x size: ', x.size)
        print('y size: ', y.size)
        raise ValueError('x must be same size as y')
    if len(np.unique(y)) != 2:
        print('label unique :', np.unique(y))
        raise ValueError('y label is not binary')
    # get bins
    each_bins = pd.cut(x, bins = n_bins, right=True, labels=None, retbins=False, precision=3, include_lowest=True, duplicates='raise')
    new_x = pd.Series(each_bins)
    new_y = pd.Series(y)
    # get total label count
    sum0 = np.sum(new_y == 0)
    sum1 = np.sum(new_y == 1)
    # get each bin count
    label0 = new_x[new_y == 0]
    label1 = new_x[new_y == 1]
    label0_df = pd.DataFrame(label0.groupby(label0).size())
    label0_df.columns = ['Label0']
    label1_df = pd.DataFrame(label1.groupby(label1).size())
    label1_df.columns = ['Label1']
    # calculate woe and iv
    label_count_df = label1_df.merge(label0_df, left_index = True, right_index = True)
    label_count_df['bin_sum'] = label_count_df['Label0'] + label_count_df['Label1']
    label_count_df['pyi'] = label_count_df['Label1'] / sum1
    label_count_df['pni'] = label_count_df['Label0'] / sum0
    label_count_df['woe'] = np.log(label_count_df['pyi'] / label_count_df['pni'])
    label_count_df['iv'] = (label_count_df['pyi'] - label_count_df['pni']) * label_count_df['woe']
    label_count_df['final_iv'] = label_count_df['iv'].map(lambda x: 0 if x == np.inf else x)
    final_iv = np.sum(label_count_df['final_iv'])
    return label_count_df[['woe', 'iv']], final_iv

def filter_iv_features(df_data, y, iv_value = [4]):
    columns = df_data.columns.values
    c_name = []
    iv_data = []
    level_data = []
    for item in columns:
        if df_data[item].dtypes in ['int64', 'float64']:
            x = df_data[item]
            df_r, iv = check_iv(x, y)
            c_name.append(item)
            iv_data.append(round(iv, 3))
            if iv <= 0.02:
                level = 0
            elif iv <= 0.1:
                level = 1
            elif iv <= 0.3:
                level = 2
            elif iv <= 0.5:
                level = 3
            else:
                level = 4
            level_data.append(level)
    d = pd.DataFrame({'c_name': c_name, 'iv': iv_data, 'level': level_data})
    df_iv_features = d[d['level'].isin(iv_value)]['c_name']
    return df_iv_features

def filter_digital_feature(df_data):
    columns = df_data.columns.values
    columns_after_filter = []
    for item in columns:
        if df_data[item].dtypes in ['int64', 'float64']:
            columns_after_filter.append(item)
    return df_data[columns_after_filter]
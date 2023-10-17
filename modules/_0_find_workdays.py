"""

    """

import pandas as pd
from githubdata import get_data_wo_double_clone
from mirutil.df import save_df_as_prq
from mirutil.jdate import gen_iso_jdate_fr_jdate_in_df
from mirutil.jdate import gen_jdate_fr_date_in_df

from main import c
from main import fp
from main import gdu

def get_adj_prices_data_fr_github() :
    return get_data_wo_double_clone(gdu.adj_price_s)

def get_uniq_dates_mark_tse_open_days(df) :
    # Assuming we have only working days on the adj prices data
    df = df[[c.d]].drop_duplicates()
    df[c.is_tse_open] = True
    return df

def make_whole_date_range_df(df) :
    """ makes whole data range between first and last date """
    date_range = pd.date_range(start = df[c.d].min() , end = df[c.d].max())

    df = pd.DataFrame({
            c.d : date_range
            })

    return df

def add_open_dates_of_tse_and_mark_closed_days(df , dfw) :
    df = df.merge(dfw , on = c.d , how = 'left')
    df[c.is_tse_open] = df[c.is_tse_open].fillna(False)
    return df

def reorder_cols(df) :
    cols = {
            c.d           : 'date' ,
            c.jd          : 'jdate' ,
            c.wd          : 'weekday' ,
            c.is_tse_open : 'IS_TSE_OPEN' ,
            }

    df = df[list(cols.keys())]

    return df

def main() :
    pass

    ##

    dfw = get_adj_prices_data_fr_github()

    ##

    dfw = get_uniq_dates_mark_tse_open_days(dfw)

    ##

    df = make_whole_date_range_df(dfw)

    ##

    df = gen_jdate_fr_date_in_df(df , c.d , c.jd , date_fmt = '%Y-%m-%d')
    df[c.wd] = df[c.jd].apply(lambda x : x.weekday())
    df = gen_iso_jdate_fr_jdate_in_df(df , c.jd , c.jd)

    ##

    df[c.d] = df[c.d].dt.strftime('%Y-%m-%d')

    ##

    df = add_open_dates_of_tse_and_mark_closed_days(df , dfw)

    ##

    df = reorder_cols(df)

    ##

    save_df_as_prq(df , fp.t0)

##
if __name__ == "__main__" :
    main()

"""

    """

from pathlib import Path

from mirutil.ns import update_ns_module , rm_ns_module
from githubdata import GitHubDataRepo
import pandas as pd
from persiantools.jdatetime import JalaliDateTime
from mirutil.df import save_df_as_a_nice_xl

update_ns_module()
import ns

gdu = ns.GDU()
c = ns.Col()

def main() :
    pass

    ##

    # Get All adjusted prices
    gds = GitHubDataRepo(gdu.src)
    dfs = gds.read_data()

    ##
    dfs = dfs[[c.d]].drop_duplicates()

    ##
    dfs[c.is_tse_open] = True

    ##
    date_range = pd.date_range(start = dfs[c.d].min() , end = dfs[c.d].max())

    ##
    df = pd.DataFrame({
            c.d : date_range
            })

    ##
    df[c.jd] = df[c.d].apply(JalaliDateTime.to_jalali)

    ##
    df[c.wd] = df[c.jd].apply(lambda x : x.weekday())

    ##
    df[c.d] = df[c.d].apply(lambda x : x.strftime('%Y-%m-%d'))
    df[c.jd] = df[c.jd].apply(lambda x : x.strftime('%Y-%m-%d'))

    ##
    df = df.merge(dfs , on = c.d , how = 'left')

    ##
    msk = df[c.is_tse_open].isna()
    print(len(msk[msk]))

    df.loc[msk , c.is_tse_open] = False

    ##
    gdt = GitHubDataRepo(gdu.trg)
    gdt.clone_overwrite()

    ##
    fpt = gdt.data_fp

    save_df_as_a_nice_xl(df , fpt)

    ##
    max_jd = df[c.jd].max()

    ##
    msg = f'Got updated until {max_jd} by {gdu.slf}'

    ##
    gdt.commit_and_push(msg , branch = 'main')

    ##
    gds.rmdir()
    gdt.rmdir()

    ##
    rm_ns_module()

##


if __name__ == "__main__" :
    main()
    print(f'{Path(__file__).name} Done!')

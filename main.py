"""

    """

from namespace_mahdimir import tse as tse_ns
from namespace_mahdimir import tse_github_data_url as tgdu
from run_py import DefaultDirs
from run_py import rm_cache_dirs
from run_py import run_modules

class GDU :
    g = tgdu.GitHubDataUrl()

    adj_price_s = g.adj_price
    tse_work_days_t = g.tse_work_days

class Dirs :
    dd = DefaultDirs(make_default_dirs = True)

    gd = dd.gd
    t = dd.t

class FPs :
    dyr = Dirs()

    # temp data files
    t0 = dyr.t / 't0.prq'

# class instances   %%%%%
c = tse_ns.Col()

gdu = GDU()
dyr = Dirs()
fp = FPs()

def main() :
    pass

    ##
    run_modules()

    ##
    rm_cache_dirs()

##
if __name__ == "__main__" :
    main()
    print('\n\n\t\t***** main.py Done! *****\n\n')

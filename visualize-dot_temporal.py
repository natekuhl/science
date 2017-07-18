#!python visualize-dot.py

import argparse
import os
from path import Path
import textwrap
import graphviz as gv
import re

from configobj import ConfigObj
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine


CURRENT_DIR = Path(__file__).parent

def get_db_connection_string():
    local_settings = ConfigObj(os.path.join(CURRENT_DIR,'../blitzcrank/local_settings.conf'))
    return 'postgresql://{user}@{host}/{database}'.format(
        host=local_settings['host'],
        user=local_settings['dbuser'],
        database=local_settings['database'],
    )


def get_args():
    parser = argparse.ArgumentParser(description='Create vizgraph', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        'schema_prefix',
        help="first eight digits of system name prefix"
    )
    parser.add_argument(
        'dot_file_name',
        help="Specify name of dot graph"
    )
    args = parser.parse_args()
    return args


def run():
    args = get_args()
    def get_system_names(engine):
        """ get system names for all published characteristic types
        """
        sql = """
            select
            system_name
            from metadata_characteristictype where substring(system_name from 1 for 8) = '{}'
        """.format(args.schema_prefix)
        with engine.connect() as conn:
            result = conn.execute(sql)
            return [column[0] for column in result.fetchall()]
    engine = create_engine(get_db_connection_string())
    system_names = get_system_names(engine)
    def make_digraph_adv():
        G = gv.Graph(format='svg')
        j = 1
        for name in system_names:
            n = name.split("__")
            i = 0
            while i <= (len(name.split("__"))-1):
                if i == 0:
                    G.node('1','{}'.format(n[i]))
                    i += 1
                    j += 1
                else:
                    if i == 1:
                        G.node('{}'.format(j),'{}'.format(n[i]))
                        G.edge('1','{}'.format(j))
                        i += 1
                        j += 1
                    else:
                        G.node('{}'.format(j),'{}'.format(n[i]))
                        G.edge('{}'.format(j-1),'{}'.format(j))
                        i += 1
                        j += 1
        #filename = G.render(filename="{}".format(args.dot_file_name))
        #print filename
        G.render('img/{}'.format(args.dot_file_name))   
    make_digraph_adv()
    #unflatten -l100 -f args.dot_file_name > args.dot_file_name
    #dot -Gdpi=3000 -Gsize=9,15\! -Tpng args.dot_file_name -o args.png_name 



if __name__ == '__main__':
    run()


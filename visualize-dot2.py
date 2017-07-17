#!python visualize-dot.py

import argparse
import os
from path import Path
import textwrap
import pygraphviz as pgv


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
        G = pgv.AGraph()
        for name in system_names:
            i = 0
            while i < (len(name.split("__"))-1):
                if i+1 == (len(name.split("__"))-1):
                    G.add_node(name)
                    G.add_edge(name.split("__")[i],name)
                    i += 1        
                else:
                    G.add_node(name.split("__")[i])
                    G.add_edge(name.split("__")[i],name.split("__")[i+1])
                    i += 1        
        G.write("{}".format(args.dot_file_name))
    make_digraph_adv()
    #unflatten -l100 -f args.dot_file_name > args.dot_file_name
    #dot -Gdpi=3000 -Gsize=9,15\! -Tpng args.dot_file_name -o args.png_name 



if __name__ == '__main__':
    run()

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


def get_system_names(engine):
    """ get system names for all published characteristic types
    """
    sql = """
        select
        system_name
        from metadata_characteristictype where substring(system_name from 1 for 7) = 'acs2015'
    """
    with engine.connect() as conn:
        result = conn.execute(sql)
        return [column[0] for column in result.fetchall()]

engine = create_engine(get_db_connection_string())

system_names = get_system_names(engine)


def make_digraph():
    f = open('graph1.dot', 'w')
    f.write('strict graph "" {\n')
    for name in system_names:
        trace = " -- ".join('"{0}"'.format(names) for names in name.split("__"))
        f.write('\t {};\n'.format(trace))
    f.write('}\n')

make_digraph()


#if __name__ == '__main__':
#    run()

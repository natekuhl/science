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



def run():
    def get_system_names(engine):
        """ get system names for all published characteristic types
        """
        sql = """
            select
            system_name
            from metadata_characteristictype
        """
        with engine.connect() as conn:
            result = conn.execute(sql)
            return [column[0] for column in result.fetchall()]
    engine = create_engine(get_db_connection_string())
    system_names = get_system_names(engine)
    nodes = []
    for name in system_names:
        nodes = nodes + name.split("__")
    
     
    count = len(nodes)

    j = 1 
    for name in system_names:
        n = name.split("__")
        i = 0
        while i <= (len(n)-1):
            d['key{}'.format(j)]  = '{}'.format(n[i])











if __name__ == '__main__':
    run()



#            while i <= (len(name.split("__"))-1):
#                if i == 0:
#                    G.node('1','{}'.format(n[i]))
#                    i += 1
#                    j += 1
#                else:
#                    if i == 1:
#                        G.node('{}'.format(j),'{}'.format(n[i]))
#                        G.edge('1','{}'.format(j))
#                        i += 1
#                        j += 1
#                    else:
#                        G.node('{}'.format(j),'{}'.format(n[i]))
#                        G.edge('{}'.format(j-1),'{}'.format(j))
#                        i += 1
#                        j += 1

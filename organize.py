#!python visualize-dot.py

import argparse
import os
from path import Path
import textwrap
import collections
import pygraphviz as pgv

from configobj import ConfigObj
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine


"""SET UP CONNECTION TO FLOPPY"""
CURRENT_DIR = Path(__file__).parent

def get_db_connection_string():
    local_settings = ConfigObj(os.path.join(CURRENT_DIR,'../blitzcrank/local_settings.conf'))
    return 'postgresql://{user}@{host}/{database}'.format(
        host=local_settings['host'],
        user=local_settings['dbuser'],
        database=local_settings['database'],
    )


"""DEFINE ARGUMENTS"""

def get_args():
    parser = argparse.ArgumentParser(description='Create vizgraph', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'dot_file_name',
        help="Specify name of dot graph"
    )
    args = parser.parse_args()
    return args

"""RUN FUNCTION"""

def run():
    args = get_args()
    def get_system_names(engine):
        """ get system names for all published characteristic types
        """
        sql = """
            select
            a.system_name as characteristic_type,c.system_name as dataset
            from metadata.characteristictype a 
            join metadata.datasetmembership b on b.characteristic_type_id = a.id
            join metadata.dataset c on c.id = b.dataset_id
        """
        with engine.connect() as conn:
            result = conn.execute(sql)
            return [column for column in result.fetchall()]
    engine = create_engine(get_db_connection_string())
    system_names = get_system_names(engine)

    datasets = []
    for pair in system_names:
        datasets.append(pair[1])

    d = collections.defaultdict(dict)

    for dataset in datasets: 
        d['{}'.format(dataset)] = [] 
        for pair in system_names:
            if pair[1] == dataset:
                d['{}'.format(dataset)].append(pair[0])

    """COLLECT DATASETS TO BE SKIPPED INTO A LIST"""

    with open('skips.txt') as f:
        skips = f.readlines()
    skips = [x.strip() for x in skips]

    """PRINT DICTIONARY TO TXT FILE"""

    f =  open('dataset_groupings.txt', 'w')
    for key, value in d.items():
        if key in skips:
            pass
        else:
            f.write('%s:%s\n' % (key, value))
    f.close()

    """CREATE FUNCTION FOR BUILDING GRAPH/DIAGRAM WITH DOT"""

    def make_digraph():
        g = pgv.AGraph(strict=False,directed=True)
        g.add_node('insert_patch_here')
        for key in d.keys():
            if key in skips:
                pass
            else:
                g.add_node(key) 
                for i in d['{}'.format(key)]:
                    g.add_edge(key,i)
        g.write('generated_dot/{}'.format(args.dot_file_name))
    make_digraph()



if __name__ == '__main__':
    run()

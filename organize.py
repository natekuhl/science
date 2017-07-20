#!python visualize-dot.py

import argparse
import os
from path import Path
import textwrap
import collections

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
    #print(system_names)


    datasets = []
    for pair in system_names:
        datasets.append(pair[1])

    #print(datasets)
    d = collections.defaultdict(dict)

    for pair in system_names:
        


#        n = name.split("__")
#        i = 0
#        d['{}'.format(n[i]) = {}
#        for i in range(len(n)): 
#            d['{}'.format()] 
#









#for row in file_map:
#    # derive row key from something 
#    # when using defaultdict, we can skip the next step creating a dictionary on row_key
#    d[row_key] = {} 
#    for idx, col in enumerate(row):
#        d[row_key][idx] = col
#


if __name__ == '__main__':
    run()



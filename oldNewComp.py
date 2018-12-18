import pandas as pd
import sqlite3
import argparse
import os
from version_utils import rpm

parser = argparse.ArgumentParser()
parser.add_argument("--old_club", help="path for old_club file")
parser.add_argument("--new_club", help="path for new_club file")
parser.add_argument("--output", help="path for output file", default='newones.csv')
args = parser.parse_args()

ssclub_old = pd.read_csv(args.old_club)
# ssclub_old = pd.read_csv('ssclub_old.csv')

ssclub_today = pd.read_csv(args.new_club)
# ssclub_today = pd.read_csv('ssclub_today.csv')


ssclub_old.insert(0, 'simple_rpm_name', 'yet to change')
ssclub_today.insert(0, 'simple_rpm_name', 'yet to change')


def get_rpm_name(rpm_name):
    return rpm.package(rpm_name).name


for index, row in ssclub_old.iterrows():
    row['simple_rpm_name'] = get_rpm_name(row['rpm_name'])

for index, row in ssclub_today.iterrows():
    row['simple_rpm_name'] = get_rpm_name(row['rpm_name'])

if 'work.db' in os.listdir(): os.remove('work.db')
conn = sqlite3.connect('work.db')
c = conn.cursor()
#
ssclub_old.to_sql('ssclub_old', conn, index=False)
ssclub_today.to_sql('ssclub_today', conn, index=False)

c.execute(""" create table newones as select distinct ssclub_today.*
from ssclub_today left join ssclub_old on
(ssclub_old.simple_rpm_name=ssclub_today.simple_rpm_name and
ssclub_old."Component name"=ssclub_today.Componentname and
ssclub_old."Component version name"=ssclub_today.Componentversionname)
where ssclub_old.rpm_name is null;
""")

conn.commit()
ssclub_df = pd.read_sql_query("select * from newones",conn,index_col='rpm_name')
ssclub_df.to_csv(args.output)
# ssclub_df.to_csv('newones.csv')

conn.close()

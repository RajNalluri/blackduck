import pandas as pd
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--source_file", help="path for source.csv file", default='source.csv')
parser.add_argument("--security_file", help="path for security.csv file", default='security.csv')
parser.add_argument("--output", help="path for output file", default='ssclub.csv')
args = parser.parse_args()

sec = pd.read_csv(args.security_file)
sou = pd.read_csv(args.source_file)

conn = sqlite3.connect('work.db')
c = conn.cursor()

sec.to_sql('security', conn, index=False)
sou.to_sql('source', conn, index=False)

c.execute(""" CREATE TABLE ssclub AS SELECT DISTINCT  substr(source."Archive context",
instr(source."Archive context",'!'), -instr(source."Archive context",'!')) as rpm_name,
security."Component name", security."Component version name"
FROM security LEFT JOIN source ON
security."Version id" = source."Version id"
where (security."Remediation status" = "NEW" AND source."Archive context" != "" ) ORDER BY rpm_name;
""")
conn.commit()
ssclub_df = pd.read_sql_query("select * from ssclub",conn,index_col='rpm_name')
ssclub_df.to_csv(args.output)

conn.close()
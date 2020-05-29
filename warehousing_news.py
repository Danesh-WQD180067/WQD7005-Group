import io
# For Data Lake
from hdfs import InsecureClient
# For Data Warehouse
from pyhive import hive

import pandas as pd

df_source = pd.read_csv(r'output/news.csv')

# Define HDFS interface
hdfs_interface = InsecureClient('http://localhost:50070')
hdfs_interface.list('/')

# Create hdfs directories to store data
hdfs_interface.makedirs('/wqd7005')
hdfs_interface.makedirs('/wqd7005/raw_news')
hdfs_interface.list('/wqd7005')

# Write data to raw_news directory

# text buffer
s_buf = io.StringIO()
# saving a data frame to a buffer (same as with a regular file):
df_source.to_csv(s_buf, index=False, header=False)

hdfs_interface.write('/wqd7005/raw_news/000000_0', 
                     data=s_buf.getvalue(), 
                     overwrite=True, 
                     encoding = 'utf-8')

# Check if file has been written correctly
with hdfs_interface.read('/wqd7005/raw_news/000000_0', length=1024) as reader:
  content = reader.read()
content


# Create Hive Cursor
host_name = "localhost"
port = 10000
conn = hive.Connection(host=host_name, port=port, auth='NOSASL')
cur = conn.cursor()

# DATE	

# Create External table for raw_news
cur.execute("DROP TABLE IF EXISTS raw_news")
cur.execute("CREATE EXTERNAL TABLE IF NOT EXISTS \
            raw_news (tdate STRING, \
                    news STRING) \
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' \
            STORED AS TEXTFILE LOCATION '/wqd7005/raw_news'")
            
# Check if warehousing successful:
cur.execute("SELECT * FROM raw_news LIMIT 10")
check=cur.fetchall()
df_check=pd.DataFrame(data=check)
import io
# For Data Lake
from hdfs import InsecureClient
# For Data Warehouse
from pyhive import hive

import pandas as pd

df_source = pd.read_csv(r'output/price.csv')

# Define HDFS interface
hdfs_interface = InsecureClient('http://localhost:50070')
hdfs_interface.list('/')

# Create hdfs directories to store data
hdfs_interface.makedirs('/wqd7005')
hdfs_interface.makedirs('/wqd7005/raw_price')
hdfs_interface.list('/wqd7005')

# Write data to raw_price directory

# text buffer
s_buf = io.StringIO()
# saving a data frame to a buffer (same as with a regular file):
df_source.to_csv(s_buf, index=False, header=False)

hdfs_interface.write('/wqd7005/raw_price/000000_0', 
                     data=s_buf.getvalue(), 
                     overwrite=True, 
                     encoding = 'utf-8')

# Check if file has been written correctly
with hdfs_interface.read('/wqd7005/raw_price/000000_0', length=1024) as reader:
  content = reader.read()
content


# Create Hive Cursor
host_name = "localhost"
port = 10000
conn = hive.Connection(host=host_name, port=port, auth='NOSASL')
cur = conn.cursor()

# DATE	

# Create External table for raw_price
cur.execute("DROP TABLE IF EXISTS raw_price")
cur.execute("CREATE EXTERNAL TABLE IF NOT EXISTS \
            raw_price (tdate STRING, \
                    closing_price DECIMAL(5,2), \
                    open DECIMAL(5,2), \
                    daily_high DECIMAL(5,2), \
                    daily_low DECIMAL(5,2)) \
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' \
            STORED AS TEXTFILE LOCATION '/wqd7005/raw_price'")
            
# Check if warehousing successful:
cur.execute("SELECT * FROM raw_price LIMIT 10")
check=cur.fetchall()
df_check=pd.DataFrame(data=check)
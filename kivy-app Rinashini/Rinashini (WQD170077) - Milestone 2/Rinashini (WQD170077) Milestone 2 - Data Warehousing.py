from io import BytesIO as StringIO
# For Data Lake
from hdfs import InsecureClient
# For Data Warehouse
from pyhive import hive

import pandas as pd

df_source=pd.read_csv(r'dataset1.csv')

# Define HDFS interface
hdfs_interface = InsecureClient('http://localhost:50070')
hdfs_interface.list('/')

# Create hdfs directories to store the data
hdfs_interface.makedirs('/wqd7005')
hdfs_interface.makedirs('/wqd7005/source')
hdfs_interface.list('/wqd7005')

# text buffer
s_buf = StringIO()
# saving the data frame into a buffer (same as with a regular file)
df_source.to_csv(s_buf, index=False, header=False)

hdfs_interface.write('/wqd7005/source/000000_0',
                     data=s_buf.getvalue(),
                     overwrite=True,
                     encoding='utf-8')


# Check file written correctly
with hdfs_interface.read('/wqd7005/source/000000_0', length=1024) as reader:
    content=reader.read()
print(content)


# Create Hive Cursor
host_name="localhost"
port=10000
conn=hive.Connection(host=host_name,port=port, auth='NOSASL')
cur=conn.cursor()


# Create External Table for source
cur.execute("DROP TABLE IF EXISTS source")
cur.execute("CREATE EXTERNAL TABLE IF NOT EXISTS \
            source( tdate STRING, \
                    closing_price DECIMAL(5,2), \
                    open DECIMAL(5,2), \
                    daily_high DECIMAL(5,2), \
                    daily_low DECIMAL(5,2)) \
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' \
            STORED AS TEXTFILE LOCATION '/wqd7005/source'")

# Check if data warehousing successful
cur.execute("SELECT * FROM source LIMIT 10")
check=cur.fetchall()
df_check=pd.DataFrame(data=check)
print(df_check)



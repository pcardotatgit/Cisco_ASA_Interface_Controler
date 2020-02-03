import pandas as pd
from sqlalchemy import create_engine

# the csv file is : devices.csv
#database will be : devices.db
# the table name is  : devices

df = pd.read_csv('devices.csv')
engine = create_engine('sqlite:///devices.db')
df.to_sql('devices', engine) #With this one the table and database must not already exists
#df.to_sql('devices', con=engine, if_exists='append')   #with this one you can append data to an existing database
df.to_sql('devices', con=engine, if_exists='replace')   #with this one you can truncat an existing database
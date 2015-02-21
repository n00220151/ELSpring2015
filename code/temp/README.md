FILE LIST

temp.py
Python script that reads the temperature and writes data to two csv files and an sqlite database.

ftpupload.sh
Bash script that uploads the csv files to cs.newpaltz.edu/~forcel96/WWW/temp.

data/temps.csv
CSV file that contains all recorded temperature data.

data/latest_temp.csv
CSV file that contains only the most recnetly recorded temperature data.

data/temp.db
Sqlite database the contains all recorded temperatue data.
Contains table 'temps' with columns 'datetime', 'tempc', and 'tempf'.

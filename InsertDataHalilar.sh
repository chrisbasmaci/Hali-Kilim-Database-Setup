#/bin/sh
#installs psycopg2 library, in case it is not installed
pip3 install psycopg2-binary #you might need to change it to pip, if pip3 is your default pip.
# Run the shell script with the arguments of IngestData(input files and database configuration parameters).
python3 InsertDataHalilar.py $1 $2 $3 $4 $5 $6 $7 ${8}
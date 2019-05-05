
# Imports
import csv
from os import listdir
import subprocess
import sys
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sqlalchemy
from sqlalchemy import create_engine
import numpy as np
import pandas as pd


# Helper functions
def export_design_matrix(df):
    """
    Pickles design matrix and stores in processed directory to be trained on
    Input: clean design matrix df containing only features and target
    Outpu: pickled design matrix in data directory
    """
    df.to_pickle('../data/processed/data.pkl')
    pass

# Airline cancellation rate
def get_avg_cancellation_rate(by, time):
    pass

def get_past_cancellation_rate(by, time):
    pass



def run_query(query, params, engine):
    '''
    Opens a connection to database to run a query, q
    Input: 
        query (str), a SQL command that requests output
        params (dict), parameters for connecting to psql, including user, host,
            and port
    Output: a pandas dataframe containing the query output
    '''
    return pd.read_sql(query, engine)

    
def show_tables(params):
    # Returns a list of all tables and views in our database
    q = """
    SELECT tablename 
    FROM pg_catalog.pg_tables 
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
    """
    return run_query(q, params)


def run_command(command, params):
    '''
    Opens a connection to database to run a command with no output
    Input: 
        command (str), a SQL query that commits an action
        params (dict), parameters for connecting to psql, including user, host,
            and port
    '''
    with connect(**params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(command)
        pass

        
def create_table(table, params):
    """
    """
    table_query = f"""
        CREATE TABLE {table}(
            year NUMERIC,
            quarter NUMERIC,
            month NUMERIC,
            dayofmonth NUMERIC,
            dayofweek NUMERIC,
            flightdate DATE NOT NULL,
            reporting_airline VARCHAR,
            dot_id_reporting_airline VARCHAR,
            iata_code_reporting_airline VARCHAR,
            tail_number VARCHAR,
            flight_number_reporting_airline VARCHAR NOT NULL,
            originairportid VARCHAR,
            originairportseqid VARCHAR,
            origincitymarketid VARCHAR,
            origin VARCHAR,
            origincityname VARCHAR,
            originstate VARCHAR,
            originstatefips VARCHAR,
            originstatename VARCHAR,
            originwac VARCHAR,
            destairportid VARCHAR,
            destairportseqid VARCHAR,
            destcitymarketid VARCHAR,
            dest VARCHAR,
            destcityname VARCHAR,
            deststate VARCHAR,
            deststatefips VARCHAR,
            deststatename VARCHAR,
            destwac VARCHAR,
            crsdeptime NUMERIC,
            deptime NUMERIC,
            depdelay NUMERIC,
            depdelayminutes NUMERIC,
            depdel15 NUMERIC,
            departuredelaygroups NUMERIC,
            deptimeblk VARCHAR,
            taxiout NUMERIC,
            wheelsoff NUMERIC,
            wheelson NUMERIC,
            taxiin NUMERIC,
            crsarrtime NUMERIC,
            arrtime NUMERIC,
            arrdelay NUMERIC,
            arrdelayminutes NUMERIC,
            arrdel15 NUMERIC,
            arrivaldelaygroups NUMERIC,
            arrtimeblk VARCHAR,
            cancelled NUMERIC,
            cancellationcode NUMERIC,
            diverted NUMERIC,
            crselapsedtime NUMERIC,
            actualelapsedtime NUMERIC,
            airtime NUMERIC,
            flights NUMERIC,
            distance NUMERIC,
            distancegroup NUMERIC,
            carrierdelay NUMERIC,
            weatherdelay NUMERIC,
            nasdelay NUMERIC,
            securitydelay NUMERIC,
            lateaircraftdelay NUMERIC,
            firstdeptime NUMERIC,
            totaladdgtime NUMERIC,
            longestaddgtime NUMERIC,
            divairportlandings VARCHAR,
            divreacheddest VARCHAR,
            divactualelapsedtime VARCHAR,
            divarrdelay VARCHAR,
            divdistance VARCHAR,
            div1airport VARCHAR,
            div1airportid VARCHAR,
            div1airportseqid VARCHAR,
            div1wheelson VARCHAR,
            div1totalgtime VARCHAR,
            div1longestgtime VARCHAR,
            div1wheelsoff VARCHAR,
            div1tailnum VARCHAR,
            div2airport VARCHAR,
            div2airportid VARCHAR,
            div2airportseqid VARCHAR,
            div2wheelson VARCHAR,
            div2totalgtime VARCHAR,
            div2longestgtime VARCHAR,
            div2wheelsoff VARCHAR,
            div2tailnum VARCHAR,
            div3airport VARCHAR,
            div3airportid VARCHAR,
            div3airportseqid VARCHAR,
            div3wheelson VARCHAR,
            div3totalgtime VARCHAR,
            div3longestgtime VARCHAR,
            div3wheelsoff VARCHAR,
            div3tailnum VARCHAR,
            div4airport VARCHAR,
            div4airportid VARCHAR,
            div4airportseqid VARCHAR,
            div4wheelson VARCHAR,
            div4totalgtime VARCHAR,
            div4longestgtime VARCHAR,
            div4wheelsoff VARCHAR,
            div4tailnum VARCHAR,
            div5airport VARCHAR,
            div5airportid VARCHAR,
            div5airportseqid VARCHAR,
            div5wheelson VARCHAR,
            div5totalgtime VARCHAR,
            div5longestgtime VARCHAR,
            div5wheelsoff VARCHAR,
            div5tailnum VARCHAR,
            empty VARCHAR,
            PRIMARY KEY(flightdate, flight_number_reporting_airline)
        );
        """
    run_command(table_query, params)
    pass
    
    
def check_table_exists(table, cursor):
    '''
    Executes a query and checks if item is in returned results
    Input: 
        query (str), a SQL query returning list of items to look within
        item (str), the name of the item to check if exists
        cursor, a psycogp2 cursor object
    Output: boolean, True if item exists
    '''
    query = """
    SELECT tablename 
    FROM pg_catalog.pg_tables 
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
    """
    cursor.execute(query)
    items = [i[0] for i in cursor.fetchall()]
    print(f'Found tables: {items}')
    exists = table in items
    return exists


def check_db_exists(db, cursor):
    '''
    Executes a query and checks if item is in returned results
    Input: 
        query (str), a SQL query returning list of items to look within
        item (str), the name of the item to check if exists
        cursor, a psycogp2 cursor object
    Output: boolean, True if item exists
    '''
    query = 'SELECT datname FROM pg_database;'
    cursor.execute(query)
    items = [i[0] for i in cursor.fetchall()]
    print(f'Found items: {items}')
    exists = db in items
    return exists

    
def load_table(file, path, params, overwrite='ask'):
    ''' 
    Loads a csv into a SQL table
    Input:
        file (str), filename of csv to load
        path (str), relative directory to find file in
        params (dict), parameters for connecting to psql, including user, host,
            and port
        overwrite (str): parameter for whether or not to overwrite existing 
            files, if found. If 'y', any existing file with filename in path 
            will be overwritten. If 'n', function will do nothing. If 'ask', 
            function will prompt user to decide whether or not to replace file.
    '''
    dbname = params['dbname']
#     path = 'Users/scottbutters/src/project-03/data/raw/'
    file_path = path + file
    table_name = f'flights_{file[12:-4]}'.replace('-','_')
    print(table_name)
    
    try:
        with connect(**params) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print(f"Connecting to database {params['dbname']}")
            cur = conn.cursor()
            exists = check_table_exists(table_name, cur)
            if exists:
                if overwrite == 'ask':
                    overwrite = input(f'{table_name} already exists. Update? y/n: ')
                if overwrite.lower() != 'y':
                    return
#             if check_existence(q, table_name, cur):
                # Truncate the table first
                cur.execute(f'TRUNCATE {table_name} CASCADE;')
                print(f'Truncated {table_name}')
            command = f'csvsql --db postgresql:///{dbname}'
            params = f'--tables {table_name} --insert {file_path}'
            args = '--no-constraints --overwrite'
#             subprocess.call(f'{command} {params} {args}')
            subprocess.call(f'{command} {params} {args}', shell=True)

#                 create_table(table_name, params)
                

#                 cur.execute(f'CREATE TABLE {table_name};')
#                 print(f'Created table {table_name}')
#             with open(file_path, 'r') as f:
#                 next(f)  # Skip the header row.
#                 cur.copy_from(f, table_name, sep=',')
                  
                  
#                 c = f"""
#                     COPY {table_name} FROM STDIN WITH CSV HEADER
#                     """
#                 cur.copy_expert(c, f)
            print(f'Loaded data into {table_name}')
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)
    pass
                  

def load_csvs(table, path, params, overwrite='ask'):
    '''
    
    '''
    dbname = params['dbname']
    q = """
        SELECT tablename 
        FROM pg_catalog.pg_tables 
        WHERE schemaname != 'pg_catalog' 
        AND schemaname != 'information_schema';
        """
    try:
        with connect(**params) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print(f'Connecting to database {dbname}')
            cur = conn.cursor()
            exists = check_existence(q, table, cur)
            if exists:
                print(f'Table {table} already exists.')
            if exists:
                if overwrite == 'ask':
                    question = f'''
                    Update? WARNING: This will take a while. y/n: 
                    '''
                    overwrite = input(question)
                if overwrite.lower() != 'y':
                    return
#             if check_existence(q, table_name, cur):
                # Truncate the table first
                cur.execute(f'TRUNCATE {table} CASCADE;')
                print(f'Truncated {table}')
            
            # Write table
            
            
            try:
                print('Running console command:')
                print(f'Collecting csvs from {path}...\n',
                      f'Adding data to table {table}')
                csvstack = f'csvstack {path}*.csv'
                csvsql = f'csvsql --db postgresql:///{dbname}'
                args = f'--tables {table} --insert'
                command = f'{csvstack} | {csvsql}'
                retcode = subprocess.call([command, args])
                print('Success!')
            except:
                print('Write to table failed.')
                print(f'Error: {retcode}')
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)
    pass
                  
                  
def make_table(path, file, engine, table):
    df = pd.read_csv(path + file)

    drop_cols = [
        'DOT_ID_Reporting_Airline',
        'IATA_CODE_Reporting_Airline', 
        'OriginAirportSeqID', 
        'OriginStateFips',
        'OriginWac',
        'DestAirportSeqID', 
        'DestStateFips',
        'DestWac',
        'TaxiOut',
        'WheelsOff', 
        'WheelsOn', 
        'TaxiIn'
    ]

    short_df = df[df.columns[:61]].drop(drop_cols, axis=1)

    shorter_df = short_df[
        short_df['Origin'].str.contains('SEA') |
        short_df['Dest'].str.contains('SEA')
    ]

    index = (shorter_df['FlightDate'].astype(str) 
             + '_' + shorter_df['Flight_Number_Reporting_Airline'].astype(str))

    shorter_df.set_index(
        keys=index,
        inplace=True
    )

    shorter_df.columns = [col.lower() for col in shorter_df.columns]
    
    # Define types
    types = {
        'year': sqlalchemy.types.INTEGER(),
        'quarter': sqlalchemy.types.INTEGER(),
        'month': sqlalchemy.types.INTEGER(),
        'dayofmonth': sqlalchemy.types.INTEGER(),
        'dayofweek': sqlalchemy.types.INTEGER(),
        'flightdate': sqlalchemy.DateTime(),
        'reporting_airline': sqlalchemy.types.VARCHAR(),
        'tail_number': sqlalchemy.types.VARCHAR(),
        'flight_number_reporting_airline': sqlalchemy.types.VARCHAR(),
        'originairportid': sqlalchemy.types.VARCHAR(),
        'origincitymarketid': sqlalchemy.types.VARCHAR(),
        'origin': sqlalchemy.types.VARCHAR(),
        'origincityname': sqlalchemy.types.VARCHAR(),
        'originstate': sqlalchemy.types.VARCHAR(),
        'originstatename': sqlalchemy.types.VARCHAR(),
        'destairportid': sqlalchemy.types.VARCHAR(),
        'destcitymarketid': sqlalchemy.types.VARCHAR(),
        'dest': sqlalchemy.types.VARCHAR(),
        'destcityname': sqlalchemy.types.VARCHAR(),
        'deststate': sqlalchemy.types.VARCHAR(),
        'deststatename': sqlalchemy.types.VARCHAR(),
        'crsdeptime': sqlalchemy.types.INTEGER(),
        'deptime': sqlalchemy.types.INTEGER(),
        'depdelay': sqlalchemy.types.INTEGER(),
        'depdelayminutes': sqlalchemy.types.INTEGER(),
        'depdel15': sqlalchemy.types.BOOLEAN(),
        'departuredelaygroups': sqlalchemy.types.INTEGER(),
        'deptimeblk': sqlalchemy.types.VARCHAR(),
        'crsarrtime': sqlalchemy.types.INTEGER(),
        'arrtime': sqlalchemy.types.INTEGER(),
        'arrdelay': sqlalchemy.types.INTEGER(),
        'arrdelayminutes': sqlalchemy.types.INTEGER(),
        'arrdel15': sqlalchemy.types.BOOLEAN(),
        'arrivaldelaygroups': sqlalchemy.types.INTEGER(),
        'arrtimeblk': sqlalchemy.types.VARCHAR(),
        'cancelled': sqlalchemy.types.INTEGER(),
        'cancellationcode': sqlalchemy.types.VARCHAR(),
        'diverted': sqlalchemy.types.VARCHAR(),
        'crselapsedtime': sqlalchemy.types.VARCHAR(),
        'actualelapsedtime': sqlalchemy.types.INTEGER(),
        'airtime': sqlalchemy.types.INTEGER(),
        'flights': sqlalchemy.types.INTEGER(),
        'distance': sqlalchemy.types.INTEGER(),
        'distancegroup': sqlalchemy.types.INTEGER(),
        'carrierdelay': sqlalchemy.types.VARCHAR(),
        'weatherdelay': sqlalchemy.types.VARCHAR(),
        'nasdelay': sqlalchemy.types.VARCHAR(),
        'securitydelay': sqlalchemy.types.VARCHAR(),
        'lateaircraftdelay': sqlalchemy.types.VARCHAR(),
    }
                  
    # Add to SQL table
    shorter_df.to_sql(
        table, engine, if_exists='append', dtype=types, index=False)
    print(f'Added {file} to table {table}')
                  
    int_path = '../data/interim/'
    shorter_df.to_csv(f'{int_path}reduced_{file}')
    print(f'Wrote {file} to {int_path}')
    pass

                  
def create_db(dbname, params):
    '''
    Connects to psql as default user and creates new database if it doesn't
    already exist
    Input:
        dbname (string), name of new database
        params (dict), parameters for connecting to psql, including user, host,
        and port
    Output: database created in psql
    '''
    
    temp_params = params.copy()
    temp_params['dbname'] = 'postgres'
    with connect(**temp_params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        exists = check_db_exists(dbname, cur)
        if not exists:
            cur.execute(f'CREATE DATABASE {dbname}')
            print(f'Created database {dbname}')
    pass
        

def build_raw_database():
    '''
    Constructs database from raw data CSVs previously downloaded
    '''
    path = '../data/raw/'
    params = {
        'user': 'scottbutters',
        'host': '127.0.0.1',
        'port': 5432,
        'dbname': 'raw_flight_data'
    }
    table_name = 'flights'
    
    connection_string = f"postgresql:///{params['dbname']}"
    engine = create_engine(connection_string)

    # Create db if DNE yet
    create_db(dbname=params['dbname'], params=params)
    
    # Check whether table exists and prompt about dropping
    with connect(**params) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"Connecting to database {params['dbname']}")
        cur = conn.cursor()
        exists = check_table_exists(table_name, cur)
        if exists:
            overwrite = input(f'{table_name} already exists. Update? y/n: ')
            if overwrite.lower() != 'y':
                return
            run_command('DROP TABLE flights;', params)

    # Collect list of csvs
    files = [f for f in listdir(path) if '.csv' in f]
    files = sorted(files)
    
    # Shrink files and load all into SQL table
    for file in files:
        make_table(path, file, engine, table_name)
    pass
        
        
def run():
    """
    Executes a set of helper functions that read files from data/raw, cleans them,
    and converts the data into a design matrix that is ready for modeling.
    """
    build_raw_database()
#     data = clean_data()
#     create_
    
    # clean_dataset_1('data/raw', filename)
    # clean_dataset_2('data/raw', filename)
    # save_cleaned_data_1('data/interim', filename)
    # save_cleaned_data_2('data/interim', filename)
    # build_features()
    # save_features('data/processed')
    pass

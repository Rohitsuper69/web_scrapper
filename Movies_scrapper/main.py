import logging
import os, sys

import time
import requests
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(env_path)

logging.basicConfig(
    filename='error.log',  # Name of the log file
    level=logging.ERROR,   # Log only messages with severity level ERROR or higher
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
)

# Load environment variables from .env file
load_dotenv()

def create_database(dbname, user, password, host='localhost', port='5432'):
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"Database {dbname} created successfully")
    except Exception as e:
        None
    finally:
        cur.close()
        conn.close()


def create_table(dbname, user, password, host='localhost', port='5432'):
    """
    Create a new table named 'movies' in the specified database.

    Parameters:
    dbname (str): The name of the database.
    user (str): The username to connect to the database.
    password (str): The password to connect to the database.
    host (str, optional): The host of the database. Default is 'localhost'.
    port (str, optional): The port of the database. Default is '5432'.

    Returns:
    None
    """
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    
    create_table_query = '''
    CREATE TABLE movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        year INT NOT NULL,
        awards INT,
        nominations INT,
        best_picture BOOLEAN
    );
    '''
    
    try:
        cur.execute(create_table_query)
        conn.commit()
        print("Table movies created successfully")
    except Exception as e:
        None
    cur.close()
    conn.close()

def get_ajax_data(year):
    url = 'https://www.scrapethissite.com/pages/ajax-javascript/'
    params = {
        'ajax': 'true',
        'year': year
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve data for year {year}: HTTP status code {response.status_code}")
        return None
    
    return response.json()

def save_to_db(movies, dbname, user, password, host='localhost', port='5432'):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()
        
        for movie in movies:
            cur.execute("""
                INSERT INTO movies (title, year, awards, nominations, best_picture)
                VALUES (%s, %s, %s, %s, %s)
                """, (
                    movie['title'],
                    movie['year'],
                    movie.get('awards'),
                    movie.get('nominations'),
                    movie.get('best_picture', False)
                )
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"Error saving data to database: {e}", exc_info=True)  # exc_info=True includes traceback information

def main():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')

    # Step 1: Create the database and table
    create_database(dbname, user, password, host, port)
    create_table(dbname, user, password, host, port)
    
    start_year = 2010
    end_year = 2015
    all_movies = []

    for year in range(start_year, end_year + 1):
        movies = get_ajax_data(year)
        if movies is None:
            print(f"No data found for year {year}")
            continue
        
        if isinstance(movies, list):
            all_movies.extend(movies)
        else:
            print(f"Unexpected data structure for year {year}")
            continue
        
        time.sleep(1)
    
    print(f"Scraped {len(all_movies)} movies from {start_year} to {end_year}")
    
    save_to_db(all_movies, dbname, user, password, host, port)

if __name__ == '__main__':
    main()

import logging
import os, sys

import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(env_path)

# Configure logging
logging.basicConfig(
    filename='error.log',  # Name of the log file
    level=logging.ERROR,   # Log only messages with severity level ERROR or higher
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of log messages
)

# Load environment variables from .env file
load_dotenv()

# Function to create a connection to the PostgreSQL database
def create_connection(dbname,user,password,host,port):
    try:
        connection = psycopg2.connect(
            dbname=dbname or os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")

# Function to check if the database exists and create it if it doesn't
def ensure_database_and_table(dbname,user,password,host,port):

    # Connect to the default "postgres" database to create the target database if it doesn't exist
    conn = create_connection(dbname,user,password,host,port)
    if conn is None:
        logging.error("Failed to connect to the default 'postgres' database.")
        return

    conn.autocommit = True
    cur = conn.cursor()

    # Check if the database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (dbname,))
    exists = cur.fetchone()

    if not exists:
        try:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"Database '{dbname}' created successfully")
        except Exception as e:
            logging.error(f"Error creating database: {e}")

    cur.close()
    conn.close()

    # Connect to the newly created or existing database to create the table if it doesn't exist
    conn = create_connection(dbname,user,password,host,port)
    if conn is None:
        logging.error("Failed to connect to the newly created or existing database.")
        return

    cur = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS hockey_teams (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        year INT,
        wins INT,
        losses INT,
        ot_losses INT,
        pct VARCHAR(10),
        gf INT,
        ga INT,
        diff INT
    );
    '''

    try:
        cur.execute(create_table_query)
        conn.commit()
        print("Table hockey_teams created successfully or already exists")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

    cur.close()
    conn.close()

# Function to scrape data from all pages of the webpage and save to the database
def scrape_data_and_save_to_db(dbname,user,password,host,port):
    base_url = 'https://www.scrapethissite.com/pages/forms/'
    ensure_database_and_table(dbname,user,password,host,port)
    page = 1
    while True:
        url = f"{base_url}?page_num={page}&per_page=25"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        team_rows = soup.find_all('tr', class_='team')
        connection = create_connection(dbname,user,password,host,port)

        if connection is None:
            logging.error("Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()

            for row in team_rows:
                # Extract data from each <td> element within the row
                name = row.find('td', class_='name').text.strip()
                year = int(row.find('td', class_='year').text.strip())
                wins = int(row.find('td', class_='wins').text.strip())
                losses = int(row.find('td', class_='losses').text.strip())
                ot_losses_text = row.find('td', class_='ot-losses').text.strip()
                ot_losses = int(ot_losses_text) if ot_losses_text else None  # Convert empty string to None
                pct = row.find('td', class_='pct').text.strip()
                gf = int(row.find('td', class_='gf').text.strip())
                ga = int(row.find('td', class_='ga').text.strip())
                diff = int(row.find('td', class_='diff').text.strip())

                # Execute the SQL INSERT statement
                cursor.execute("""
                    INSERT INTO hockey_teams (name, year, wins, losses, ot_losses, pct, gf, ga, diff)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (name, year, wins, losses, ot_losses, pct, gf, ga, diff))

            # Commit the transaction
            connection.commit()
            print(f"Data from page {page} inserted successfully into the database")

        except (Exception, psycopg2.Error) as error:
            logging.error("Error while inserting data into PostgreSQL:", error)

        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

        # Check if there's a "Next" button
        next_button = soup.find('tr', class_='team')
        if not next_button:
            break  # Exit loop if there's no "Next" button

        # Move to the next page
        page += 1

# Main function to start the scraping process
def main():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    scrape_data_and_save_to_db(dbname,user,password,host,port)

if __name__ == '__main__':
    main()

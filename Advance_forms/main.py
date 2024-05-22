import os, sys
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import logging

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(env_path)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Function to create a connection to the PostgreSQL database
def create_connection(dbname,user,password,host,port):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error while connecting to PostgreSQL: {error}")
        return None

# Function to ensure that the database and table exist
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
    CREATE TABLE IF NOT EXISTS advance_topics (
        id SERIAL PRIMARY KEY,
        heading TEXT,
        content TEXT
    );
    '''

    try:
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'advance_topics' created successfully or already exists")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

    cur.close()
    conn.close()

# Function to scrape data from the webpage and save to the database
def scrape_and_save_data(dbname,user,password,host,port):
    # URL of the webpage you want to scrape
    url = 'https://www.scrapethissite.com/pages/advanced/'

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    headings = soup.find_all('h4')
    contents = soup.find_all('p')

    filtered_contents = [div for div in contents if 'lead' not in div.get('class', [])]

    # Connect to the PostgreSQL database
    conn = create_connection(dbname,user,password,host,port)
    if conn is None:
        logging.error("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        for i in range(len(headings)):
            heading_text = headings[i].text.strip()
            content_text = filtered_contents[i].text.strip()

            # Execute the SQL INSERT statement
            cursor.execute("""
                INSERT INTO advance_topics (heading, content)
                VALUES (%s, %s)
                """, (heading_text, content_text))

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully into the 'advance_topics' table")

    except (Exception, psycopg2.Error) as error:
        logging.error("Error while inserting data into PostgreSQL:", error)

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")

# Main function to start the scraping process
def main():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    # Ensure the database and table exist
    ensure_database_and_table(dbname,user,password,host,port)

    # Scrape data and save to the database
    scrape_and_save_data(dbname,user,password,host,port)

if __name__ == '__main__':
    main()

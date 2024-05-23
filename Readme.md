# Movie Data Scraper

## Description

This project scrapes movie data from a specified website for the years 2010 to 2015 and stores it in a PostgreSQL database. It includes functionality to create the database and table, fetch movie data, and save the data to the database.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RohitSuper69/web_scraper.git
   cd webscraper
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   To use venv (Virtual Environment) in Python, you typically don't need to install it separately because it's part of the Python standard library for versions 3.3 and above. However, if for some reason it's not available or you want to ensure you have the latest version, you can install it via pip:

   ```bash
   pip install virtualenv
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your database credentials:
   ```env
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   ```
   Remember to enclose all your credentials in quotes
   The data is saved along 3 table in the datbase name given which comes under main postgres datbase they can be accessed using pgAdmin 4. If not installed it can be installed from
   https://www.enterprisedb.com/downloads/postgres-postgresql-downloads. This must be done before running the scripts. Now create your credentials and assign port number(default 5432)

## Usage

Run the main script to create the database and table, data, and save it to the database.

```bash
python main.py
```

If you want to run specific for each links then use the following commands

### Link1(Movies Scrapper)

```bash
python Movies_scrapper/main.py
```

### Link2(Hockey Team)

```bash
python Hockey_team/main.py
```

### Link3(Advance Forms)

```bash
python Advance_forms/main.py
```

Data can be accsessed by going to Servers->Postgre SQL(16)->{database_name}->Schemas->public->tables

## Error Handling

In case of any unexpected errors or scenarios the program will terminate with a log file containing the error description which can be used to analyse the problem.

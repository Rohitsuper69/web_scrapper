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

## Usage

Run the main script to create the database and table, scrape movie data, and save it to the database.
You can run all links at once to fetch the data or for the simplicity and useability of the code three different scripts are created for three different links. You can also run the desired script for our purpose seperately

### Overall

```bash
python main.py
```

### Link1

```bash
python Movies_scrapper/main.py
```

### Link2

```bash
python Hockey_team/main.py
```

### Link1

```bash
python Advance_forms/main.py
```

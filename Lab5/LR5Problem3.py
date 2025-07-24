import sqlite3
import os
from datetime import datetime

def create_connection(db_file):
    """Create a database connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"✓ Successfully connected to SQLite database: {db_file}")
        print(f"SQLite version: {sqlite3.version}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(conn, query, description=""):
    """Execute a SELECT query and display results"""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        
        print(f"\n{'='*60}")
        print(f"Query: {description}")
        print(f"{'='*60}")
        print(f"SQL: {query}")
        print(f"{'-'*60}")
        
        if results:
            header = " | ".join(f"{col:<15}" for col in column_names)
            print(header)
            print("-" * len(header))
            
            for row in results:
                row_str = " | ".join(f"{str(val):<15}" for val in row)
                print(row_str)
        else:
            print("No results found.")
            
        print(f"Total records: {len(results)}")
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")

def show_table_info(conn, table_name):
    """Display table structure information"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"\n{'='*60}")
        print(f"Table Structure: {table_name}")
        print(f"{'='*60}")
        
        if columns:
            print(f"{'Column':<20} {'Type':<15} {'Not Null':<10} {'Primary Key':<12}")
            print("-" * 60)
            for col in columns:
                cid, name, data_type, not_null, default_val, pk = col
                print(f"{name:<20} {data_type:<15} {not_null:<10} {pk:<12}")
        else:
            print(f"Table {table_name} does not exist or has no columns.")
            
    except sqlite3.Error as e:
        print(f"Error getting table info: {e}")

def demonstrate_colonial_database(conn):
    """Demonstrate queries on the Colonial Adventure Tours database"""
    
    print("\n" + "="*80)
    print("COLONIAL ADVENTURE TOURS DATABASE DEMONSTRATION")
    print("="*80)
    
    execute_query(conn, 
                 "SELECT name FROM sqlite_master WHERE type='table';", 
                 "List all tables in database")
    
    tables = ['GUIDE', 'TRIP', 'CUSTOMER', 'RESERVATION', 'TRIP_GUIDES']
    for table in tables:
        show_table_info(conn, table)
    
    queries = [
        ("SELECT * FROM GUIDE;", "All Guides Information"),
        ("SELECT * FROM TRIP;", "All Available Trips"),
        ("SELECT * FROM CUSTOMER;", "All Customers"),
        ("SELECT * FROM RESERVATION;", "All Reservations"),
        ("SELECT * FROM TRIP_GUIDES;", "Trip-Guide Assignments"),
        
        ("""SELECT g.FIRST_NAME, g.LAST_NAME, t.TRIP_NAME, t.START_LOCATION 
            FROM GUIDE g 
            JOIN TRIP_GUIDES tg ON g.GUIDE_NUM = tg.GUIDE_NUM 
            JOIN TRIP t ON tg.TRIP_ID = t.TRIP_ID;""", 
         "Guides and their assigned trips"),
        
        ("""SELECT c.FIRST_NAME, c.LAST_NAME, t.TRIP_NAME, r.TRIP_DATE, r.NUM_PERSONS 
            FROM CUSTOMER c 
            JOIN RESERVATION r ON c.CUSTOMER_NUM = r.CUSTOMER_NUM 
            JOIN TRIP t ON r.TRIP_ID = t.TRIP_ID;""", 
         "Customer reservations with trip details"),
        
        ("""SELECT t.TRIP_NAME, t.TYPE, t.SEASON, COUNT(r.RESERVATION_ID) as TOTAL_RESERVATIONS 
            FROM TRIP t 
            LEFT JOIN RESERVATION r ON t.TRIP_ID = r.TRIP_ID 
            GROUP BY t.TRIP_ID, t.TRIP_NAME, t.TYPE, t.SEASON;""", 
         "Trip popularity (reservations count)"),
        
        ("""SELECT STATE, COUNT(*) as TRIP_COUNT 
            FROM TRIP 
            GROUP BY STATE 
            ORDER BY TRIP_COUNT DESC;""", 
         "Trips by state"),
        
        ("""SELECT AVG(TRIP_PRICE) as AVG_PRICE, MAX(TRIP_PRICE) as MAX_PRICE, MIN(TRIP_PRICE) as MIN_PRICE 
            FROM RESERVATION;""", 
         "Trip price statistics")
    ]
    
    for query, description in queries:
        execute_query(conn, query, description)

def create_sample_adventure_trip_demo(conn):
    """Demonstrate the ADVENTURE_TRIP table creation and operations"""
    
    print("\n" + "="*80)
    print("ADVENTURE_TRIP TABLE DEMONSTRATION")
    print("="*80)
    
    try:
        cursor = conn.cursor()
        
        print("\n➤ Creating ADVENTURE_TRIP table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ADVENTURE_TRIP (
                TRIP_ID INTEGER PRIMARY KEY,
                TRIP_NAME VARCHAR(50),
                START_LOCATION VARCHAR(50),
                STATE VARCHAR(2),
                DISTANCE NUMBER,
                MAX_GRP_SIZE NUMBER,
                TYPE VARCHAR(50),
                SEASON VARCHAR(20)
            )
        ''')
        
        show_table_info(conn, 'ADVENTURE_TRIP')
        
        print("\n➤ Inserting Jay Peak trip record...")
        cursor.execute('''
            INSERT INTO ADVENTURE_TRIP 
            (TRIP_ID, TRIP_NAME, START_LOCATION, STATE, DISTANCE, MAX_GRP_SIZE, TYPE, SEASON)
            VALUES (45, 'Jay Peak', 'Jay', 'VT', 8, 8, 'Hiking', 'Summer')
        ''')
        
        execute_query(conn, "SELECT * FROM ADVENTURE_TRIP;", "ADVENTURE_TRIP table contents")
        
        print("\n➤ Dropping ADVENTURE_TRIP table...")
        cursor.execute("DROP TABLE ADVENTURE_TRIP")
        print("✓ ADVENTURE_TRIP table dropped successfully")
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Error in ADVENTURE_TRIP demonstration: {e}")

def create_colonial_tables(conn):
    """Create all Colonial Adventure Tours tables and insert data"""
    
    print("\n" + "="*80)
    print("CREATING COLONIAL ADVENTURE TOURS DATABASE TABLES")
    print("="*80)
    
    try:
        cursor = conn.cursor()
        
        tables_sql = [
            '''CREATE TABLE IF NOT EXISTS GUIDE (
                GUIDE_NUM INTEGER PRIMARY KEY,
                LAST_NAME VARCHAR(15),
                FIRST_NAME VARCHAR(15),
                ADDRESS VARCHAR(15),
                CITY VARCHAR(15),
                STATE VARCHAR(2),
                POSTAL_CODE VARCHAR(5),
                PHONE_NUM VARCHAR(12),
                HIRE_DATE DATE
            )''',
            
            '''CREATE TABLE IF NOT EXISTS TRIP (
                TRIP_ID INTEGER PRIMARY KEY,
                TRIP_NAME VARCHAR(75),
                START_LOCATION VARCHAR(50),
                STATE VARCHAR(2),
                DISTANCE INTEGER,
                MAX_GRP_SIZE INTEGER,
                TYPE VARCHAR(15),
                SEASON VARCHAR(15)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS CUSTOMER (
                CUSTOMER_NUM INTEGER PRIMARY KEY,
                LAST_NAME VARCHAR(15),
                FIRST_NAME VARCHAR(15),
                ADDRESS VARCHAR(15),
                CITY VARCHAR(15),
                STATE VARCHAR(2),
                POSTAL_CODE VARCHAR(5),
                PHONE_NUM VARCHAR(12)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS RESERVATION (
                RESERVATION_ID INTEGER PRIMARY KEY,
                TRIP_ID INTEGER,
                TRIP_DATE DATE,
                NUM_PERSONS INTEGER,
                TRIP_PRICE DECIMAL(6,2),
                OTHER_FEES DECIMAL(6,2),
                CUSTOMER_NUM INTEGER,
                FOREIGN KEY (TRIP_ID) REFERENCES TRIP(TRIP_ID),
                FOREIGN KEY (CUSTOMER_NUM) REFERENCES CUSTOMER(CUSTOMER_NUM)
            )''',
            
            '''CREATE TABLE IF NOT EXISTS TRIP_GUIDES (
                TRIP_ID INTEGER,
                GUIDE_NUM INTEGER,
                PRIMARY KEY (TRIP_ID, GUIDE_NUM),
                FOREIGN KEY (TRIP_ID) REFERENCES TRIP(TRIP_ID),
                FOREIGN KEY (GUIDE_NUM) REFERENCES GUIDE(GUIDE_NUM)
            )'''
        ]
        
        for sql in tables_sql:
            cursor.execute(sql)
            print(f"✓ Table created successfully")
        
        print("\n➤ Inserting sample data...")
        
        guides = [
            (1, 'Boyers', 'Rita', '325 Tawas', 'Boyton', 'MA', '02537', '508-555-7563', '2018-05-10'),
            (2, 'Devon', 'Harley', '35 Shenandoah', 'Harrisonburg', 'VA', '22801', '540-555-4500', '2019-06-15'),
            (3, 'Kiley', 'Susan', '12 Samoset', 'Centerville', 'MA', '02639', '508-555-0079', '2020-03-19'),
            (4, 'Marston', 'Glenn', '845 Belt', 'Owings Mills', 'MD', '21117', '410-555-8590', '2018-08-22')
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO GUIDE VALUES (?,?,?,?,?,?,?,?,?)', guides)
        
        trips = [
            (1, 'Arethusa Falls', 'Jackson', 'NH', 5, 10, 'Hiking', 'Summer'),
            (2, 'Mount Monadnock', 'Jaffrey', 'NH', 9, 15, 'Hiking', 'Early Fall'),
            (3, 'Monponsett Pond', 'Halifax', 'MA', 8, 8, 'Paddling', 'Summer'),
            (4, 'Napatree Point', 'Watch Hill', 'RI', 7, 7, 'Hiking', 'Spring')
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO TRIP VALUES (?,?,?,?,?,?,?,?)', trips)
        
        customers = [
            (101, 'Northfold', 'Melissa', '16 Maple', 'Haver Hill', 'MA', '01830', '781-555-4948'),
            (102, 'Ocean', 'Cynthia', '32 Tristan', 'Springdale', 'CT', '06907', '203-555-7761'),
            (103, 'Kiley', 'Kathleen', '7 Peach Tree', 'Seekonk', 'MA', '02771', '508-555-6057'),
            (104, 'Kelly', 'Brian', '2672 King', 'Westwood', 'MA', '02090', '781-555-2111')
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO CUSTOMER VALUES (?,?,?,?,?,?,?,?)', customers)
        
        reservations = [
            (1, 1, '2021-07-23', 5, 80.00, 0.00, 101),
            (2, 2, '2021-09-14', 2, 110.00, 0.00, 102),
            (3, 1, '2021-07-30', 8, 160.00, 0.00, 103),
            (4, 4, '2021-05-12', 4, 100.00, 15.00, 104)
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO RESERVATION VALUES (?,?,?,?,?,?,?)', reservations)
        
        trip_guides = [
            (1, 1), (1, 3), (2, 2), (3, 1), (4, 4)
        ]
        
        cursor.executemany('INSERT OR REPLACE INTO TRIP_GUIDES VALUES (?,?)', trip_guides)
        
        conn.commit()
        print("✓ All data inserted successfully")
        
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def main():
    """Main function to demonstrate SQLite database operations"""
    
    database = "colonial_adventure.db"
    
    print("="*80)
    print("PYTHON SQLITE DATABASE CONNECTION DEMONSTRATION")
    print("CPE106L - Laboratory Report 5")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    conn = create_connection(database)
    
    if conn is not None:
        try:
            create_colonial_tables(conn)
            
            create_sample_adventure_trip_demo(conn)
            
            demonstrate_colonial_database(conn)
            
            print("\n" + "="*80)
            print("DATABASE DEMONSTRATION COMPLETED SUCCESSFULLY")
            print("="*80)
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
            print(f"\n✓ Database connection closed.")
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    main()

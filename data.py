import sqlite3 as sql

DB_NAME = 'plantas.db'

def init_db():
    """Crea la tabla si no existe al iniciar la app"""
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS plantas(
            name TEXT,
            species TEXT, 
            irri_frequency INTEGER,
            last_watered TEXT
        )'''
    )
    conn.commit()
    conn.close()

def insert_plant(name, species, irri_frequency):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    instruction = 'INSERT INTO plantas (name, species, irri_frequency) VALUES (?, ?, ?)'
    cursor.execute(instruction, (name, species, irri_frequency))
    conn.commit()
    conn.close()

def get_all_plants():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plantas')
    datos = cursor.fetchall()
    conn.close()
    return datos

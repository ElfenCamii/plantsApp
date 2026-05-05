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
            plant_tutor TEXT,
            irri_tutor INTEGER,
            irri_frequency INTEGER,
            last_watered TEXT
        )'''
    )
    conn.commit()
    conn.close()

def insert_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    instruction = '''INSERT INTO plantas 
                     (name, species, plant_tutor, irri_tutor, irri_frequency) 
                     VALUES (?, ?, ?, ?, ?)'''
    
    cursor.execute(instruction, (nombre, especie, tutor, frecuencia_tutor, frecuencia))
    conn.commit()
    conn.close()

def get_all_plants():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plantas')
    datos = cursor.fetchall()
    conn.close()
    return datos

def search_plants(name_to_search):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    term = f'{name_to_search}%'
    instruction = f'SELECT * FROM plantas WHERE name like ?'
    cursor.execute(instruction, (term,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def updatePlantField(plant_name, plant_species, column_name, new_value):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    instruction = f'UPDATE plantas SET {column_name}=? WHERE name=? AND species=?'
    cursor.execute(instruction, (new_value, plant_name, plant_species))
    conn.commit()
    conn.close()

def deletRowPlants(plant_name, plant_species):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    # Corregido: "AND" en lugar de "AMD"
    instruction = 'DELETE FROM plantas WHERE name=? AND species=?'
    cursor.execute(instruction, (plant_name, plant_species))
    filas_borradas = cursor.rowcount
    conn.commit()
    conn.close()
    return filas_borradas 
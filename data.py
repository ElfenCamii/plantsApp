import sqlite3 as sql
from datetime import datetime, date

DB_NAME = 'plantas.db'

def init_db():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS plantas(
            id_planta INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            species TEXT, 
            plant_tutor TEXT,
            irri_tutor INTEGER,
            irri_frequency INTEGER,
            last_watered TEXT,
            last_tutor_watered TEXT,
            image_path TEXT
        )'''
    )
    conn.commit()
    conn.close()

def insert_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia, imagen, last_m, last_t):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    instruction = '''INSERT INTO plantas 
                     (name, species, plant_tutor, irri_tutor, irri_frequency, last_watered, last_tutor_watered, image_path) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(instruction, (nombre, especie, tutor, frecuencia_tutor, frecuencia, last_m, last_t, imagen))
    conn.commit()
    conn.close()

def get_all_plants():
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM plantas')
    datos = cursor.fetchall()
    conn.close()
    return datos

def update_last_watered_m(plant_id, date_str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    solo_fecha = date_str.split(" ")[0] 
    cursor.execute("UPDATE plantas SET last_watered = ? WHERE id_planta = ?", (solo_fecha, plant_id))
    conn.commit()
    conn.close()

def update_last_watered_t(plant_id, date_str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    solo_fecha = date_str.split(" ")[0]
    cursor.execute("UPDATE plantas SET last_tutor_watered = ? WHERE id_planta = ?", (solo_fecha, plant_id))
    conn.commit()
    conn.close()

def delete_plant(plant_id):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plantas WHERE id_planta = ?", (plant_id,))
    conn.commit()
    conn.close()

def calcular_barra_vida(fecha_ultimo_riego, frecuencia):
    if not fecha_ultimo_riego or frecuencia <= 0:
        return 0
    try:
        ultimo_riego = datetime.strptime(fecha_ultimo_riego, '%Y-%m-%d').date()
        hoy = date.today()
        dias_pasados = (hoy - ultimo_riego).days
        porcentaje = 100 - (dias_pasados / frecuencia * 100)
        return max(0, min(100, round(porcentaje)))
    except:
        return 0
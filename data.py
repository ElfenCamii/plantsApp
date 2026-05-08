import sqlite3 as sql
from datetime import datetime, date, timedelta


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


def insert_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia, imagen):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    hoy = date.today().isoformat() 
    instruction = '''INSERT INTO plantas 
                     (name, species, plant_tutor, irri_tutor, irri_frequency, last_watered, last_tutor_watered, image_path) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(instruction, (nombre, especie, tutor, frecuencia_tutor, frecuencia, hoy, hoy, imagen))
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


def deletRowPlants(id_planta):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    # Mucho más limpio y seguro
    instruction = 'DELETE FROM plantas WHERE id_planta=?'
    cursor.execute(instruction, (id_planta,))
    conn.commit()
    conn.close()



def calcular_barra_vida(fecha_ultimo_riego, frecuencia):
    if not fecha_ultimo_riego: # Por si la planta es nueva y no se ha regado
        return 0, "NUNCA REGADA"

    # 1. Convertir el texto de la DB a una fecha real
    ultimo_riego = datetime.strptime(fecha_ultimo_riego, '%Y-%m-%d').date()
    hoy = datetime.now().date()

    # 2. Calcular cuántos días han pasado
    dias_pasados = (hoy - ultimo_riego).days
    
    # 3. Calcular el porcentaje (la "vida")
    # Si han pasado 7 días de una frecuencia de 7, la vida es 0%
    porcentaje = 100 - (dias_pasados / frecuencia * 100)
    
    # Asegurarnos de que no devuelva números negativos
    return max(0, round(porcentaje))


def reset_watering(nombre, especie, es_tutor=False):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    hoy = date.today().isoformat()
    columna = "last_tutor_watered" if es_tutor else "last_watered"
    instruction = f'UPDATE plantas SET {columna}=? WHERE name=? AND species=?'
    cursor.execute(instruction, (hoy, nombre, especie))
    conn.commit()
    conn.close()


# def add_new_column():
#     conn = sql.connect(DB_NAME)
#     cursor = conn.cursor()
#     try:
#         # Agregamos la columna para el último riego del tutor
#         cursor.execute('ALTER TABLE plantas ADD COLUMN last_tutor_watered TEXT')
#         print("Columna agregada con éxito.")
#     except sql.OperationalError:
#         # Si la columna ya existe, esto evita que el programa falle
#         print("La columna ya existe.")
#     conn.commit()
#     conn.close()


def simular_paso_del_tiempo(dias_atras, nombre_planta, especie_planta):
    conn = sql.connect('plantas.db')
    cursor = conn.cursor()
    
    # Calculamos una fecha del pasado
    fecha_falsa = (date.today() - timedelta(days=dias_atras)).isoformat()
    
    # Actualizamos la planta para que parezca que se regó hace X días
    cursor.execute('UPDATE plantas SET last_watered=? WHERE name=? AND species=?', (fecha_falsa, nombre_planta, especie_planta))
    
    conn.commit()
    conn.close()
    print(f"Simulación: {nombre_planta} {especie_planta} ahora aparece como regada hace {dias_atras} días.")
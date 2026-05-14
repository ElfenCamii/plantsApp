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
    # ELIMINAMOS EL SPLIT. Guardamos la cadena completa con hora.
    cursor.execute("UPDATE plantas SET last_watered = ? WHERE id_planta = ?", (date_str, plant_id))
    conn.commit()
    conn.close()

def update_last_watered_t(plant_id, date_str):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    # ELIMINAMOS EL SPLIT.
    cursor.execute("UPDATE plantas SET last_tutor_watered = ? WHERE id_planta = ?", (date_str, plant_id))
    conn.commit()
    conn.close()

def delete_plant(plant_id):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plantas WHERE id_planta = ?", (plant_id,))
    conn.commit()
    conn.close()

def calcular_barra_vida(fecha_ultimo_riego, frecuencia_dias):
    if not fecha_ultimo_riego or frecuencia_dias <= 0:
        return 0
    try:
        frecuencia_horas = frecuencia_dias * 24
        
        # Intentar leer con HORA (nuevo formato)
        try:
            ultimo_riego = datetime.strptime(fecha_ultimo_riego, '%Y-%m-%d %H:%M')
        except ValueError:
            # Si falla, leer solo FECHA (formato viejo) y añadirle hora 00:00
            ultimo_riego = datetime.strptime(fecha_ultimo_riego, '%Y-%m-%d')
        
        ahora = datetime.now()
        diferencia = ahora - ultimo_riego
        horas_pasadas = diferencia.total_seconds() / 3600
        
        if horas_pasadas <= frecuencia_horas:
            porcentaje = 100 - (horas_pasadas / frecuencia_horas * 100)
            return round(porcentaje)
        else:
            horas_retraso = horas_pasadas - frecuencia_horas
            porcentaje_retraso = (horas_retraso / 48) * 100
            return max(-100, round(-porcentaje_retraso))
    except Exception as e:
        print(f"Error en calculo: {e}")
        return 0
    
def get_plant_by_id(plant_id):
    conn = sql.connect(DB_NAME) # Usamos la variable DB_NAME que ya tienes
    cursor = conn.cursor()
    # Cambiado 'id' por 'id_planta'
    cursor.execute("SELECT * FROM plantas WHERE id_planta = ?", (plant_id,))
    planta = cursor.fetchone()
    conn.close()
    return planta

def update_plant_full(p_id, nombre, especie, tutor, freq_t, freq_m, img, u_m, u_t):
    conn = sql.connect(DB_NAME)
    cursor = conn.cursor()
    # Ajustamos los nombres de las columnas para que coincidan con tu tabla:
    # name, species, plant_tutor, irri_tutor, irri_frequency, image_path, last_watered, last_tutor_watered
    cursor.execute("""
        UPDATE plantas SET 
        name=?, species=?, plant_tutor=?, irri_tutor=?, 
        irri_frequency=?, image_path=?, last_watered=?, last_tutor_watered=? 
        WHERE id_planta=?
    """, (nombre, especie, tutor, freq_t, freq_m, img, u_m, u_t, p_id))
    conn.commit()
    conn.close()

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
import data

def add_new_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia):
    
    if tutor == 'si':
        frecuencia_tutor = int(input('Frecuencia de riego del tutor (días): '))
    else:
        frecuencia_tutor = 0

    data.insert_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia)
    print(f'¡{nombre} agregada con éxito!')

def del_plants(nom_eliminar, esp_eliminar):
    filas = data.deletRowPlants(nom_eliminar, esp_eliminar)
    print('\n--- Resultados de la eliminación ---')
    # 3. VERIFICAR si se borró algo
    if filas > 0:
        print(f'¡Éxito! Se eliminaron {filas} registro(s) de "{nom_eliminar} ({esp_eliminar})" ')
    else:
        print(f'No se encontró ninguna planta que se llame "{nom_eliminar}" y sea "{esp_eliminar}"')

def search_plant(criterio):
    resultados = data.search_plants(criterio)
    
    print('\n--- Resultados de búsqueda ---')

    if len(resultados) > 0:
        for p in resultados:
            # p[0] es nombre, p[1] es especie, p[2] es frecuencia
            print(f"-> Encontrada: {p[0]} ({p[1]}) - Tiene tutor {p[2]} - Riego del tutor cada {p[3]} días - Riego maceta cada {p[4]}")
    else:
        print(f'No se encontraron plantas que coincidan con "{criterio}"')

def update_plant_logic():
    print('''
\n¿Qué desea actualizar?
    1. Nombre de una planta
    2. Especie de una planta
    3. Si tiene o no tutor
    4. Frecuencia de riego del tutor
    5. Frecuencia de riego de la maceta
''')
    try:
        user_update = int(input('¿Qué desea hacer?: '))
        
        # Datos necesarios para localizar la planta exacta
        actual_nom = input('Nombre actual de la planta: ')
        actual_esp = input('Especie actual de la planta: ')

        # Diccionario para mapear la opción con el nombre de la columna en la DB
        # Esto hace que el código sea mucho más corto
        columnas = {
            1: ('name', 'Nuevo nombre: '),
            2: ('species', 'Nueva especie: '),
            3: ('plant_tutor', 'Actualización del tutor (si/no): '),
            4: ('irri_tutor', 'Frecuencia de riego del tutor: '),
            5: ('irri_frequency', 'Frecuencia de riego maceta: ')
        }

        if user_update in columnas:
            col_name, prompt_text = columnas[user_update]
            nuevo_valor = input(prompt_text)
            
            data.updatePlantField(actual_nom, actual_esp, col_name, nuevo_valor)
            print(f'\n¡Actualización de {col_name} realizada con éxito!')
        else:
            print("Opción de actualización no válida.")

    except ValueError:
        print('¡Error: Ingresa un número válido!')
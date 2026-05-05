import os
import data

# Inicializamos la base de datos al arrancar
data.init_db()

os.system('cls')

print('-----------------------------------')
print('----------- App Plantas -----------')
print('-----------------------------------')

while True:
    print('''
\nEscribe el número de la opción que desees:
          
    1. Abregar una planta
    2. Actualizar una planta
    3. Mostrar inventario
    4. Eliminar una planta
    5. Buscar una planta
    6. Salir
''')
    try:
        user_action = int(input('¿Qué desea hacer?: '))

        if user_action == 1:
            nombre = input('Nombre de la planta: ')
            especie = input('Especie: ')
            tutor = input('Tiene tutor: ').lower()
            if tutor == 'si':
                frecuencia_tutor = int(input('Frecuencia de riego del tutor (días): '))
            else:
                frecuencia_tutor = 0
            frecuencia = int(input('Frecuencia de riego (días): '))
            
            data.insert_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia)
            print(f'¡{nombre} agregada con éxito!')

        elif user_action == 2:
            print('''
\nQue decea actualizar
                  
    1. Nombre de una planta
    2. Especie de una planta
    3. Si tiene o no tutor
    4. Frecuencia de riego del tutor
    5. Frecuencia de riego de la maceta
''')
            user_update = int(input('¿Qué desea hacer?: '))
            if user_update == 1: # Nombre
                actual_nom = input('Nombre actual: ')
                actual_esp = input('Especie actual: ') # Para diferenciar
                nuevo_nom = input('Nuevo nombre: ')
                
                data.updatePlantField(actual_nom, actual_esp, 'name', nuevo_nom)
                print(f'\n¡Nombre actualizado con éxito!')

            elif user_update == 2: # Especie
                actual_nom = input('Nombre de la planta: ')
                actual_esp = input('Especie actual: ')
                nueva_esp = input('Nueva especie: ')
                
                data.updatePlantField(actual_nom, actual_esp, 'species', nueva_esp)
                print(f'\n¡Especie actualizada con éxito!')
            
            elif user_update == 3: # Tutor
                actual_nom = input('Nombre de la planta: ')
                actual_esp = input('Especie actual: ')
                nueva_tutor = input('Actualización del tutor (si/no): ')
                
                data.updatePlantField(actual_nom, actual_esp, 'plant_tutor', nueva_tutor)
                print(f'\n¡Tutor actualizado con éxito!')

            elif user_update == 4: # Frecuencia de riego del tutor
                actual_nom = input('Nombre de la planta: ')
                actual_esp = input('Especie actual: ')
                frec_tutor = input('Frecuencia de riego del tutor: ')
                
                data.updatePlantField(actual_nom, actual_esp, 'irri_tutor', frec_tutor)
                print(f'\n¡Frecuencia de riego tutor actualizada con éxito!')
            
            elif user_update == 5: # Frecuencia de riego del maceta
                actual_nom = input('Nombre de la planta: ')
                actual_esp = input('Especie actual: ')
                frec_maceta = input('Frecuencia de riego maceta: ')
                
                data.updatePlantField(actual_nom, actual_esp, 'irri_frequency', frec_maceta)
                print(f'\n¡Frecuencia de riego maceta actualizada con éxito!')

        elif user_action == 3:
            plantas = data.get_all_plants()
            print('\n--- Inventario Actual ---')
            for p in plantas:
                print(f"Nombre: {p[0]} | Especie: {p[1]} | Tiene tutor: {p[2]} | Riego del tutor: {p[3]} días | Riego maceta: {p[4]} días")

        elif user_action == 4:
            nom_eliminar = input('Nombre de la planta a eliminar: ')
            esp_eliminar = input('Especie de la planta a eliminar: ')
            filas = data.deletRowPlants(nom_eliminar, esp_eliminar)
            print('\n--- Resultados de la eliminación ---')
            # 3. VERIFICAR si se borró algo
            if filas > 0:
                print(f'¡Éxito! Se eliminaron {filas} registro(s) de "{nom_eliminar} ({esp_eliminar})" ')
            else:
                print(f'No se encontró ninguna planta que se llame "{nom_eliminar}" y sea "{esp_eliminar}"')

        elif user_action == 5:
            criterio = input('Escribe el nombre de la planta a buscar: ')
    
            # Llamamos a la función pasando el criterio y guardamos el resultado
            resultados = data.search_plants(criterio)
    
            print('\n--- Resultados de búsqueda ---')
    
            if len(resultados) > 0:
                for p in resultados:
                    # p[0] es nombre, p[1] es especie, p[2] es frecuencia
                    print(f"-> Encontrada: {p[0]} ({p[1]}) - Tiene tutor {p[2]} - Riego del tutor cada {p[3]} días - Riego maceta cada {p[4]}")
            else:
                print(f'No se encontraron plantas que coincidan con "{criterio}"')

        elif user_action == 6:
            print("Saliendo...")
            break

    except ValueError:
        print('El valor ingresado no es un número!')
        print('Intentelo de nuevo')
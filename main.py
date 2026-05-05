import os
import data
import functions

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
            frecuencia = int(input('Frecuencia de riego maceta (días): '))
            frecuencia_tutor = 0
            functions.add_new_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia)

        elif user_action == 2:
            functions.update_plant_logic()

        elif user_action == 3:
            plantas = data.get_all_plants()
            print('\n--- Inventario Actual ---')
            for p in plantas:
                print(f"Nombre: {p[0]} | Especie: {p[1]} | Tiene tutor: {p[2]} | Riego del tutor: {p[3]} días | Riego maceta: {p[4]} días")

        elif user_action == 4:
            nom_eliminar = input('Nombre de la planta a eliminar: ')
            esp_eliminar = input('Especie de la planta a eliminar: ')
            functions.del_plants(nom_eliminar, esp_eliminar)

        elif user_action == 5:
            criterio = input('Escribe el nombre de la planta a buscar: ')
            functions.search_plant(criterio)

        elif user_action == 6:
            print("Saliendo...")
            break

    except ValueError:
        print('El valor ingresado no es un número!')
        print('Intentelo de nuevo')
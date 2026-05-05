import os
import data # Importamos tu archivo data.py

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
        user_action = int(input('\n¿Qué desea hacer?: '))

        if user_action == 1:
            # Aquí es donde conectamos el input del usuario con la DB
            nombre = input('Nombre de la planta: ')
            especie = input('Especie: ')
            frecuencia = int(input('Frecuencia de riego (días): '))
            
            data.insert_plant(nombre, especie, frecuencia)
            print(f'¡{nombre} agregada con éxito!')

        elif user_action == 3:
            plantas = data.get_all_plants()
            print('\n--- Inventario Actual ---')
            for p in plantas:
                print(f"Nombre: {p[0]} | Especie: {p[1]} | Riego cada: {p[2]} días")

        elif user_action == 6:
            print("Saliendo...")
            break

    except ValueError:
        print('El valor ingresado no es un número!')
        print('Intentelo de nuevo')
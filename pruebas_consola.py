import os
import data
import functions

# Inicializamos la base de datos al arrancar
data.init_db()
# data.add_new_column()

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
    6. Riego de maceta
    7. Riego de tutor
    8. Salir
''')
    try:
        user_action = int(input('¿Qué desea hacer?: '))


        if user_action == 1: # Agregar planta

            nombre = input('Nombre de la planta: ')
            especie = input('Especie: ')
            tutor = input('Tiene tutor: ').lower()
            frecuencia = int(input('Frecuencia de riego maceta (días): '))
            frecuencia_tutor = 0
            functions.add_new_plant(nombre, especie, tutor, frecuencia_tutor, frecuencia)


        elif user_action == 2: # Actualizar planta
            functions.update_plant_logic()


        elif user_action == 3: # Monstrar inventario
            plantas = data.get_all_plants()
            functions.show_inventory_logic(plantas)


        elif user_action == 4: # Eliminar planta 
            nom_eliminar = input('Nombre de la planta a eliminar: ')
            esp_eliminar = input('Especie de la planta a eliminar: ')
            functions.del_plants(nom_eliminar, esp_eliminar)


        elif user_action == 5: # Buscar planta
            criterio = input('Escribe el nombre de la planta a buscar: ')
            functions.search_plant(criterio)


        elif user_action == 6: # Riego maceta
            nom = input('Nombre de la planta que regó: ')
            esp = input('Especie: ')
            data.reset_watering(nom, esp, False)
            print(f"¡Registro de riego de maceta para {nom} actualizado!")


        elif user_action == 7: # Riego tutor
            nom = input('Nombre de la planta que regó: ')
            esp = input('Especie: ')
            data.reset_watering(nom, esp, True)
            print(f"¡Registro de riego de tutor para {nom} actualizado!")


        elif user_action == 8: # Salir
            print("Saliendo...")
            break


        elif user_action == 28:
            nom = input('nombre planta: ')
            esp = input('especie planta: ')
            dias = int(input('dias hacia atras: '))
            data.simular_paso_del_tiempo(dias, nom, esp)

    except ValueError:
        print('El valor ingresado no es un número!')
        print('Intentelo de nuevo')
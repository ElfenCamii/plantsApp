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
            print('\n' + '='*112)
            print(f"{'PLANTA':<15} | {'ESPECIE':<18} | {'ESTADO MACETA':<17} | {'RIEGO MACETA':<14} | {'ESTADO TUTOR':<17} | {'RIEGO TUTOR'}")
            print('-'*112)

            for p in plantas:
                
                porcen_maceta = functions.obtener_estado_riego(p[5], p[4])
                porcen_tutor = functions.obtener_estado_riego(p[6], p[3])
                
                # Crear una barrita visual: [#####     ]
                bloques_m = int(porcen_maceta / 10)
                barra_m = f'[{"#" * bloques_m}{" " * (10 - bloques_m)}]'

                bloques_t = int(porcen_tutor / 10)
                barra_t = f'[{"#" * bloques_t}{" " * (10 - bloques_t)}]'
                
                # Elegir un mensaje según el porcen_maceta
                alerta_maceta = ''
                if porcen_maceta <= 15: alerta_maceta = '🔴🔴🔴🔴'
                elif porcen_maceta <= 20: alerta_maceta = '🟡🔴🔴🔴'
                elif porcen_maceta <= 30: alerta_maceta = '🟡🟡🔴🔴'
                elif porcen_maceta < 50: alerta_maceta = '🟡🟡🟡🔴'
                elif porcen_maceta >= 90: alerta_maceta = '🟢🟢🟢🟢'
                elif porcen_maceta >= 80: alerta_maceta = '🟢🟢🟢🟡'
                elif porcen_maceta >= 70: alerta_maceta = '🟢🟢🟡🟡'
                elif porcen_maceta >= 60: alerta_maceta = '🟢🟡🟡🟡'
                elif porcen_maceta >= 50: alerta_maceta = '🟡🟡🟡🟡'
                
                alerta_tutor = ''
                if porcen_tutor < 15: alerta_tutor = '🔴🔴🔴🔴'
                elif porcen_tutor < 20: alerta_tutor = '🟡🔴🔴🔴'
                elif porcen_tutor < 30: alerta_tutor = '🟡🟡🔴🔴'
                elif porcen_tutor < 50: alerta_tutor = '🟡🟡🟡🔴'
                elif porcen_tutor > 90: alerta_tutor = '🟢🟢🟢🟢'
                elif porcen_tutor > 80: alerta_tutor = '🟢🟢🟢🟡'
                elif porcen_tutor > 70: alerta_tutor = '🟢🟢🟡🟡'
                elif porcen_tutor > 60: alerta_tutor = '🟢🟡🟡🟡'
                elif porcen_tutor > 50: alerta_tutor = '🟡🟡🟡🟡'

                print(f'{p[0]:<15} | {p[1]:<18} | {barra_m} {porcen_maceta:>3}% | {alerta_maceta:<10} | {barra_t} {porcen_tutor:>2}% | {alerta_tutor}')
            print('='*112)


        elif user_action == 4:
            nom_eliminar = input('Nombre de la planta a eliminar: ')
            esp_eliminar = input('Especie de la planta a eliminar: ')
            functions.del_plants(nom_eliminar, esp_eliminar)


        elif user_action == 5:
            criterio = input('Escribe el nombre de la planta a buscar: ')
            functions.search_plant(criterio)


        elif user_action == 6: # Riego maceta
            nom_maceta = input('Escriba el nombree de la planta de rego: ')
            esp_maceta = input('Escriba la especia de la planta que rego: ')

            data.reset_watering(nom_maceta, esp_maceta, False)

        
        elif user_action == 7: # Riego tutor
            nom_tutor = input('Escriba el nombree de la planta de rego: ')
            esp_tutor = input('Escriba la especia de la planta que rego: ')

            data.reset_watering(nom_maceta, esp_maceta, True)


        elif user_action == 7:
            print("Saliendo...")
            break

    except ValueError:
        print('El valor ingresado no es un número!')
        print('Intentelo de nuevo')
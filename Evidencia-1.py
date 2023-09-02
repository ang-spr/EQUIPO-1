#Librerías:
import datetime as dt
import os
from tabulate import tabulate

#Funciones
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def menuActual(numeroMenu, descripcionMenu):
    print(f"Usted se encuentra en:\nOpción {numeroMenu}: {descripcionMenu}")

#Recolección de datos:
fecha_actual = dt.date.today()

lista_menu = [('Número de opción', 'Servicio'),
              (1, 'Registrar nota.'),
              (2, 'Consulta y reportes.'),
              (3, 'Cancelar una nota'),
              (4, 'Recuperar una nota'),
              (5, 'Salir')]

lista_servicios = [('Número de servicio', 'Servicio', 'Precio sugerido'),
                   (1, 'Cambio de nueomatico', 600), 
                   (2, 'Ajuste de vujias', 900),
                   (3, 'Cambio de aceite', 850),
                   (4, 'Reparación de aceite', 4500),
                   (5, 'Trasmisión', 3000)]

#Juntar datos:
nota_final = {}

while True:
    #Menú principal:
    print('----TALLER MECÁNICO DON HAMBLETON----')
    print('Buen día, seleccione la opción que desee realizar:')
    print(tabulate(lista_menu, headers = 'firstrow', tablefmt = 'pretty'))
    
    while True:
        try:
            menu = int(input('Opción: '))
            if menu >= 1 and menu <= 5:
                break
            else:
                print("\nPor favor, ingrese una opción válida del 1 al 5.")
                continue
        except ValueError:
            print("\nPor favor, ingrese un número válido.")
            continue

    #Registrar nota:
    if menu == 1:
        total_costo_servicio = 0
        limpiar_consola()
        menuActual(menu, lista_menu[menu][1])
        
        #Folio:
        nueva_nota = (max(nota_final.keys(), default = 0)) + 1
        print(f'\nNúmero de folio: {nueva_nota}')

        #Fecha:
        while True:
            fecha_registro = input("Ingrese la fecha de la realización de la nota (dd/mm/aaaa): ")
            fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()

            #CAMBIAR LA VALICACIÓN DE FECHA:
            if fecha_procesada > fecha_actual:       
                print("La fecha no debe ser posterior a la fecha Actual. Ingrese una fecha válida.")
                continue
            else: 
                break

        #Nombre del cliente:
        while True:
            nombre_cliente = input('Ingrese el nombre completo del cliente: ')
            #VALIDAR:
            #MAYOR A 2 DÍGITOS Y MENOR QUE 50.
            #NO INGRESAR NÚMERO NI CARÁCTERES ESPECIALES.
            #QUITAR ESPACIOS VACÍOS AL PRINCIPIO Y FINAL DEL TEXTO.

            #CONVERTIRLO A MAYÚSCULAS PARA FACILITAR USO.
            break

        #Servicios realizados:
        while True:
            print('Ingrese el número de servicio que desee: ')
            print(tabulate(lista_servicios, headers = 'firstrow', tablefmt = 'pretty'))
            servicio = int(input('Servicio: '))
            #VALIDAR QUE INGRESE UN NÚMERO VÁLIDO.

            costo_servicio = float(input("Ingrese el costo real del servicio: "))
            #VALIDAR QUE INGRESE UN COSTO VÁLIDO.

            #CAMBIAR LA VALICACIÓN DEL COSTO:
            if costo_servicio <= 0:
                print("El costo debe ser mayor que cero.")
                continue

            print("----------------------------------------\nServicio agregado correctamente.")
            otro_servicio = input('\tDesea ingresar otro servicio (Sí/No): ')

            #CONVERTIR RESPUESTA:
            #CONVERTIRLO A MAYÚSCULAS
            #QUITAR ESPACIOS VACÍOS AL PRINCIPIO Y FINAL DEL TEXTO.
            #QUITAR ACENTOS.

            #VALIDAR QUE INGRESE UNA RESPUESTA CORRECTA.

            total_costo_servicio += costo_servicio

            if otro_servicio == 'SI':
                #GUARDAR SERVICIO Y PRECIO ACTUAL A TUPLA QUE TENGA TODOS LOS SERVICIOS REALIZADOS.
                limpiar_consola()
                print("{Aquí va ir el número de servicio} servicio guardado correctamente.\nIngrese el siguiente servicio:\n\n")
                continue
            
            elif otro_servicio == 'NO':
                #IMPRIMIR FECHA SIN EL TIPO DE DATO QUE ES.
                nota_final[nueva_nota]=(fecha_procesada, nombre_cliente, total_costo_servicio)

                print(f"Nota guardada correctamente.\nEl precio a pagar es: ${total_costo_servicio}\n")
                print(f"{nueva_nota} {nota_final[nueva_nota]}\n")
                input("De clic en Enter para continuar.")
                limpiar_consola()
                break

    #Consulta y reportes:
    elif menu == 2:
        break
    
    #Cancelar una nota:
    elif menu == 3:
        break

    #Recuperar una nota
    elif menu == 4:
        break

    #Salir:
    else:
        break

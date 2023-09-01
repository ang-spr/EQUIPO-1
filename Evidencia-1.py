#Librerías:
import datetime as dt
import os

#Funciones
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

#[CÓDIGO POSIBLE A UTILIZAR]:
'''
tupla_servicio = {1:(600,'Cambio de nueomatico'), 2:(900,'Ajuste de vujias'),
        3:(850,'Cambio de aceite'), 4:(4500,'Reparacion de aceite'), 5:(3000,'Trasmision')}
'''

#Recolección de datos:
fecha_actual = dt.date.today()

#Juntar datos:
nota_final = {}

while True:
    #Menú principal:
    print('----TALLER MECÁNICO DON HAMBLETON----')
    print('Buen día, seleccione la opción que desee realizar:')
    print('\n1. Registrar nota.\n2. Consulta y reportes.\n3. Cancelar una nota.\n4. Recuperar una nota.\n5. Salir.')
    #VALIDAR QUE INGRESE UNA OPCIÓN VÁLIDA.
    menu = int(input('Opción: '))

    #Registrar nota:
    if menu == 1:
        #Folio:
        nueva_nota = (max(nota_final.keys(), default = 0)) + 1
        print(f'\n\nNúmero de folio: {nueva_nota}')

        #Fecha:
        while True:
            fecha_registro = input("Ingrese la fecha de la realización de la nota (dd/mm/aaaa): ")

            #CORREGIR EL PROCESAMIENTO DE LA FECHA:
            fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()

            #CAMBIAR LA VALICACIÓN DE FECHA:
            if fecha_procesada < fecha_actual:       
                print("La fecha es incorrecta. La fecha no debe ser posterior a la actual.")
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

        #Servicio(s) realizado(s):
        total_costo_servicio = 0
        while True:
            print('Los servicios disponibles son los siguientes: ')
            print('1. Cambio de neumáticos: $600\n2. Ajuste de vujias: $900\n3. Cambio de aceite: $850\n4. Reparación de motor: $4500\n5. Transmisión: $3000')
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

            if otro_servicio == 'SI':             
                #GUARDAR SERVICIO Y PRECIO ACTUAL A TUPLA QUE TENGA TODOS LOS SERVICIOS REALIZADOS.
                
                total_costo_servicio += costo_servicio
                limpiar_consola()
                continue
            
            elif otro_servicio == 'NO':
                monto_pagar = print(f'El precio a pagar es: ${total_costo_servicio}')

                #AQUÍ CREO QUE GUARDAREMOS DICCIONARIO.
                #IMPRIMIR FECHA SIN EL TIPO DE DATO QUE ES.
                nota_final[nueva_nota]=(nombre_cliente, fecha_procesada, servicio, monto_pagar)

                #FALTA ENCONTRAR MANERA PARA DAR ENTER Y SALIR.
                print(f"Nota guardada correctamente:\n{nota_final}\nDe clic en Enter para continuar.")
                #limpiar_consola()
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

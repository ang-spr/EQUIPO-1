import datetime as dt

print('----TALLER MECANICO DON HAMBLETON---')

print('Buen dia, seleccione la opcion que desee realizar: \n1-Registrar nota \n2-Consulta y reportes')
print('3-Cancelar una nota \n4-Recuperar una nota \n5-Salir')
menu = int(input('Opcion: '))

folio = {}

fecha_actual=dt.date.today()

while True:
    if menu == 1:
        tupla_servicio = {1:(600,'Cambio de nueomatico'), 2:(900,'Ajuste de vujias'),
            3:(850,'Cambio de aceite'), 4:(4500,'Reparacion de aceite'), 5:(3000,'Trasmision')}
        nombre_cliente = input('Ingrese el nombre del cliente: \n')
       
        print('Los servicios disponibles son los siguientes: ')
        print('1-Cambio de neumaticos: $600 \n2-Ajuste de vujias: $900 \n3-Cambio de aceite: $850')
        print('4-Reparacion de motor: $4500 \n5-Trasmision: $3000')
        servicio = int(input('Servicio: '))
        
        while True:
            fecha_registro=input("Ingresar la fecha del sistema (dd/mm/aaaa): ")
            fecha_procesada = dt.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
            if fecha_procesada < fecha_actual:       
                print("La fecha es incorrecta. La fecha no debe ser posterior a la actual")  
                continue
            else: 
                break

    clave_folio = max(folio.keys(), default = 0) + 1 
    folio[clave_folio] = (nombre_cliente,servicio,fecha_actual)
    print(folio)
    break

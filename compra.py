from search import Search
from match import Match
from stadium import Stadium
from purchase import Purchase
import string
import random

def main_compra(lista_estadios, lista_partidos, lista_purchases, given_purchase_ids): 

    print("...................")
    print("COMPRAR ENTRADAS:")

    while True: 
        opciones = input("""
        1. Buscar Partido: ver los partidos por país, fecha o estadio.

        2. Comprar Entrada: escoger un partido y comprar su entrada. 
        
        Seleccione: 
        """)

        if opciones == "1" or opciones == "2": 
            break
        else: 
            print("Respuesta incorrecta. ")
        
    if opciones == "1": 

        objeto = Search(lista_partidos, lista_estadios)

        while True: 
            filter = input("""
            
            Con base en qué criterio desea buscar: 
            1. Equipo
            2. Estadio
            3. Fecha
            """)

            if int(filter) in range(1, 4):
                break 
            else: 
                print("Opción inválida")

        if filter == "1": Search.search_by_country(objeto)
        elif filter == "2": Search.search_by_stadium(objeto)
        else: 
            Search.search_by_date(objeto)
    
    else: 
        lista_purchases = proceso(lista_partidos, lista_purchases, given_purchase_ids)

        pass

def proceso(lista_partidos, lista_purchases, given_purchase_ids):
    while True: 
        try:
            name = input("\n\nIngrese el nombre del usuario:    ")

            if not "".join(name.split()).isalpha():
                raise Exception 

            id = int(input("Ingrese su número de identificación:    "))
            if int(id) < 0: 
                raise Exception 

            age = int(input("Ingrese su edad:    "))
            if age < 0: 
                raise Exception 

            break

        except: 
            print("\n\tDatos del clientes inválidos. Por favor, ingrese de nuevo sus datos de forma correcta.\n")

    selected_match = select_partido(lista_partidos)
    if selected_match is None:
        print("No se seleccionó un partido valido")
        return lista_purchases

    sector = escoger_tipo_entrada()

    selected_estadio = selected_match.get_stadium()
    if selected_estadio is None:
        print("No se encontró un estadio válido para el partido seleccionado. Abortando proceso de compra.")
        return lista_purchases

    seat = pick_seat(selected_estadio, sector, selected_match)

    if sector == "General": 
        inicial = 35
    else: 
        inicial = 75

    descuento_por_vampiro = vampire(int(id))

    if descuento_por_vampiro:
        print("DESCUENTO ID VAMPIRO (50%)")
        descuento = inicial/2
    else:
        descuento = 0

    impuesto = inicial*0.16

    total = inicial + impuesto - descuento

    partido_str = Match.get_info(selected_match)
    estadio_str = Stadium.get_name(selected_estadio)

    print("""

    --------------------
                Previsualización :
                - Partido: {}
                - Estadio: {}
                - Monto inicial: {}
                - Impuesto: {}
                - Descuento: {}
                - Monto final: {}    
    ----------------------

    """.format(partido_str, estadio_str, inicial, impuesto, descuento,  total))

    while True: 
        validacion = input("""
                    1. Confirmar transacción.
                    2. Anular

        Ingrese elección:  """)
        
        if validacion != "1" and validacion != "2": 
            print("Dato erróneo")

        else: 
            break 

    if validacion == "1": 
        print("\t\t\tCOMPRA REALIZADA CON ÉXITO")

        consumo = []
        codigo = codigo_unico(given_purchase_ids)

        factura = Purchase(codigo, name, id, age, selected_match, sector, seat, total, consumo)

        Match.new_venta(selected_match)
        Match.new_taken_seat(selected_match, seat)

        lista_purchases.append(factura)
        
        given_purchase_ids.append(codigo)

        Purchase.print_receipt(factura)

    else: 

        print("\nCompra anulada.\n")
    
    return lista_purchases
        
def codigo_unico(given_purchase_ids):

    while True:
        n = random.randint(1000, 9999)
        if n not in given_purchase_ids:
            break
    return n

def vampire(id):
 
    id_str = str(id)
    digitos = len(id_str)

    if digitos%2 != 0 or digitos == 2:
        return False
    
    for x in range(1, (int(id)//2 + 1)):
        for y in range(1, (int(id)//2 + 1)):
            if str(x)[-1] == 0 and str(y)[-1] == 0:
                continue

            if len(str(x)) + len(str(y)) != digitos:
                continue

            if x*y == id:
                return True

def pick_seat(estadio, sector, selected_match):

    capacidad = Stadium.get_capacidad(estadio)

    capacidad_total = sum(capacidad)

    matriz_completa = crear_matriz(capacidad_total)

    numero_filas_vip = capacidad[1]//10
    mvip = []
    mgral = []

    for i in range(0, numero_filas_vip):
        mvip.append(matriz_completa[i])

    for i in range(numero_filas_vip, len(matriz_completa)):
        mgral.append(matriz_completa[i])

    print("\n\n\n")

    if sector == "General": 
        print("\t\tMatriz de Asientos General\n")
        print_m(mgral)
        seat = select_seat(selected_match, estadio, mgral)
    else: 
        print("\t\tMatriz de Asientos VIP\n")
        print_m(mvip)
        seat = select_seat(selected_match, estadio, mvip)
    
    return seat

def select_seat(match, estadio, selected_matrix):

    confirmation = False
    print("Asientos Ocupados: ")
    for seat in Match.get_taken_seats(match): 
        print("- " + seat)
    
    while True: 
        try: 

            seat = input("Escriba el código del asiento que desea:   ").upper()

            for line in selected_matrix:
                if seat in line:
                    confirmation = True
                    break 

            if not confirmation: raise Exception

            if seat in Match.get_taken_seats(match):
                raise Exception

            break 
        except:  
            print("El asiento ingresado no es válido o se encuentra ocupado.")

    return seat

def print_m(matrix):
    linea_str = "" 

    for line in matrix: 
        for seat in line: 
            linea_str += seat
            linea_str += "  " 
    
        print(linea_str)
        linea_str = ""

    print("")

def crear_matriz(capacidad):

    abecedario = list(string.ascii_uppercase)
    n_filas = capacidad // 10 #número de filas que se tendran, con este número sacaremos las letras que utilizaremos. 

    filas_letras = []

    for i in range(n_filas): 
       if i < len(abecedario):
           filas_letras.append(abecedario[i])
       else:
           filas_letras.append(abecedario[i % len(abecedario)] + str(i // len(abecedario) + 1))
           

    matrix = []

    for letra in filas_letras: 
        linea = [] 
        for x in range(1,11): 
            linea.append(letra + str(x)) #Letra y número, del 1 al 11 porque será de 1 al 10.  
        matrix.append(linea)

    return matrix

def escoger_tipo_entrada():

    print("\n\nTipos de Entrada: \n1. General: 35$ \n\t- Solo podrá ver el partido desde su asiento. \n\n2. VIP: 75$ \n\t- Podrá disfrutar del restaurante del estadio.    ")

    while True: 
        try:
            boleto_type = input("Ingrese el número de su selección:     ")

            if boleto_type != "1" and boleto_type != "2": 
                raise Exception
            
            break
    
        except:
            print("Por favor, ingrese una opción válida.")

    if boleto_type == "1": boleto_type = "General"
    else: boleto_type = "VIP"

    return boleto_type

def select_partido(lista_partidos):
    print("\nLista de partidos disponibles:")
    headers = ["#", "Partido", "Estadio", "Fecha"]

    table_data = []
    for idx, partido in enumerate(lista_partidos, start=1):
        partido_info = partido.get_info().split(" // ")
        table_data.append([idx, partido_info[0], partido_info[1], partido_info[2]])

    while True:
        try:
            seleccion = int(input("Seleccione el número del partido que desea: "))
            if seleccion < 1 or seleccion > len(lista_partidos):
                raise ValueError("Selección fuera de rango.")

            return lista_partidos[seleccion - 1]
        except ValueError as e:
            print(f"Error: {e}. Por favor, intente nuevamente.")
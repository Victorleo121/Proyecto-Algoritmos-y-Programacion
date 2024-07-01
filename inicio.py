from team import Team
from product import Product
from stadium import Stadium 
from match import Match
import requests

def setting_equipos_all(): 
    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
    json_equipos = descargar(url_equipos)
    equipos_all = [Team(equipo["name"], equipo.get("flag", ""), equipo["code"], equipo["group"], equipo["id"]) for equipo in json_equipos]
    return equipos_all

def setting_stadiums_all(): 
    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
    json_estadios = descargar(url_estadios)
    stadiums_all = []
   
    for estadio in json_estadios:
        id_estadio = estadio.get("id", "")  
        name_estadio = estadio.get("name", "")  
        capacity_estadio = estadio.get("capacity", "")  
        location_estadio = estadio.get("location", "")  

        if "restaurants" in estadio:
            restaurants_estadio = estadio["restaurants"]
        else:
            restaurants_estadio = []

        productos_list_de_obj = []

        for restaurante in restaurants_estadio:
            for product in restaurante.get("products", []):  
                name_producto = product.get("name", "")  
                quantity_producto = product.get("quantity", "")  
                price_producto = product.get("price", "")  
                type_producto = product.get("type", "")  
                adicional_producto = product.get("adicional", "")  

                p = Product(name_producto, quantity_producto, price_producto, type_producto, adicional_producto)
                productos_list_de_obj.append(p)

            restaurante["products"] = productos_list_de_obj
            productos_list_de_obj = []

        s = Stadium(id_estadio, name_estadio, capacity_estadio, location_estadio, restaurants_estadio)
        stadiums_all.append(s)

    return stadiums_all


def descargar(url): 
    import requests
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def setting_matches_all(equipos_all, stadiums_all):
    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
    json_partidos = descargar(url_partidos)

    stadium_dict = {str(stadium.id): stadium for stadium in stadiums_all}

    matches_all = []

    for partido in json_partidos:
        estadio_id = partido["stadium_id"]
        
        if estadio_id not in stadium_dict:
            print(f"Warning: stadium_id '{estadio_id}' not found in stadiums_all. Skipping this match.")
            continue
        
        estadio = stadium_dict[estadio_id]

        home_team_data = partido.get("home")
        away_team_data = partido.get("away")

        if not home_team_data or not away_team_data:
            print(f"Warning: Missing home_team or away_team for match with id '{partido.get('id')}'. Skipping this match.")
            continue

        home_team_name = home_team_data.get("name")
        away_team_name = away_team_data.get("name")

        if not home_team_name or not away_team_name:
            print(f"Warning: Missing home_team_name or away_team_name for match with id '{partido.get('id')}'. Skipping this match.")
            continue

        e_local = None
        e_visitante = None
        
        for equipo in equipos_all: 
            if equipo.get_name() == home_team_name: 
                e_local = equipo
            elif equipo.get_name() == away_team_name:
                e_visitante = equipo

        if e_local is None or e_visitante is None:
            print(f"Warning: Couldn't find home_team or away_team for match with id '{partido['id']}'. Skipping this match.")
            continue  

        taken_seats = []  

        p = Match(e_local, e_visitante, partido["date"], estadio, partido["id"], 0, 0, taken_seats)
        matches_all.append(p)

    return matches_all

def print_all(teams_all, stadiums_all, matches_all):
    print("\n\nEQUIPOS: ")
    for team in teams_all: 
        Team.print_team(team)

    print("\n\nESTADIOS: ")
    for stadium in stadiums_all: 
        Stadium.print_stadium(stadium)
        Stadium.print_restaurants(stadium)

    print("\n\nPARTIDOS: ")
    for match in matches_all: 
        Match.print_match(match)
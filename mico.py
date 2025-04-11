import mysql.connector
from dotenv import load_dotenv
import os
import easygui

from customui import mico_multenterbox

load_dotenv()

mico_image = "Mythic_Mico.png"

mico_db = mysql.connector.connect(
  host=os.getenv("HOST"),
  user=os.getenv("USER"),
  password=os.getenv("PASSWORD")
)

mico_cursor = mico_db.cursor()

# really fast and minimal, use function oriented
mico_procedures = {
    "add_airplane()": {"button": "Add", "choices": [
        "Airline ID", "Tail Num", "Sea Cap", "Speed", "Location ID", "Plane Type",
        "Maintained", "Model", "Neo"]},
    "add_airport()": {"button": "Add", "choices": [
        "Airport ID", "Airport Name", "City", "State", "Country", "Location ID"]},
    "add_person()": {"button": "Add", "choices": [
        "Person ID", "First Name", "Last Name", "Location ID", "Tax ID", "Experience",
        "Miles", "Funds"]},
    "grant_or_revoke_pilot_license()": {"button": "Add/Revoke", "choices": [
        "Person ID", "License"]},
    "offer_flight()": {"button": "Add", "choices": [
        "Flight ID", "Route ID", "Support Airline", "Support Tail", "Progress", "Next Time",
        "Cost"]},
    "flight_landing()": {"button": "Land", "choices": ["flightID"]},
    "flight_takeoff()": {"button": "Takeoff", "choices": ["flightID"]},
    "passengers_board()": {"button": "Board", "choices": ["flightID"]},
    "passengers_disembark()": {"button": "Disembark", "choices": ["flightID"]},
    "assign_pilot()": {"button": "Assign", "choices": ["ip_flightID", "ip_personID"]},
    "recycle_crew()": {"button": "Recycle", "choices": ["flightID"]},
    "retire_flight()": {"button": "Retire", "choices": ["flightID"]},
    "simulation_cycle()": {"button": "Next Step", "choices": []}
}

mico_views = [
    "flights_in_the_air()",
    "flights_on_the_ground()",
    "people_in_the_air()",
    "people_on_the_ground()",
    "route_summary()",
    "alternative_airports()"
]

def main_view():
    choices = []
    choices.extend(mico_procedures.keys())
    choices.extend(mico_views)
    choice = easygui.buttonbox("Choose a thing", image=mico_image, choices=choices)
    if choice in mico_views:
        # display view
        view_text = "Couldn't get this view"
        try:
            mico_cursor.execute(f"SELECT * FROM {choice[:-2]}")
            view_text = str(mico_cursor.fetchall())
        except Exception:
            pass
        easygui.codebox(choice, "View", view_text)
    else:
        # display procedure
        procedure = mico_procedures[choice]
        values = []
        values = mico_multenterbox(choice, "Procedure", procedure["choices"], values, procedure["button"])
        try:
            mico_cursor.callproc(choice[:-2], values)
        except Exception:
            pass
    main_view()

main_view()
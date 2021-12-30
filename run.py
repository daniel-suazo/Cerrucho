import sqlite3
from commands import create_db, charge, add_service, add_person, add_person_service, pay, list_people, list_services

command = input(">")
while command != "quit" or command != "q":
    commands = command.split(" ")
    if commands[0] == "create":
        create_db()
    elif commands[0] == "charge":
        charge()
    elif commands[0] == "add_service":
        add_service(commands[1], commands[2])
    elif commands[0] == "add_person":
        add_person(commands[1], commands[2])
    elif commands[0] == "add_person_service":
        add_person_service(commands[1], commands[2])
    elif commands[0] == "pay":
        pay(commands[1], commands[2])
    elif commands[0] == "list_people":
        list_people()
    elif commands[0] == "list_services":
        list_services()
    elif commands[0] == "list":
        list_people()
        list_services()
    else:
        print("Invalid command")
    command = input(">")

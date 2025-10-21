import json
import os

CATALOGUE_FILE = "catalogues.json"

def load_catalogues():
    if not os.path.exists(CATALOGUE_FILE):
        return {}
    with open(CATALOGUE_FILE, "r") as f:
        return json.load(f)

def save_catalogues(catalogues):
    with open(CATALOGUE_FILE, "w") as f:
        json.dump(catalogues, f, indent=4)

def prompt_name() -> str:
    return input("Enter the name of the catalogue: ")

def list_catalogues():
    catalogues = load_catalogues()
    if not catalogues:
        print("No catalogues found.")
    else:
        print("Catalogues:")
        for name in catalogues:
            print(f"- {name}")

def create_catalogue():
    catalogues = load_catalogues()
    name = prompt_name()
    if name in catalogues:
        print("Catalogue already exists.")
        return
    # Start with empty content or whatever you want the structure to be
    catalogues[name] = {"items": []}
    save_catalogues(catalogues)
    print(f"Catalogue '{name}' created.")

def remove_catalogue():
    catalogues = load_catalogues()
    name = prompt_name()
    if name not in catalogues:
        print("Catalogue does not exist.")
        return
    del catalogues[name]
    save_catalogues(catalogues)
    print(f"Catalogue '{name}' removed.")

def choose_catalogue():
    catalogues = load_catalogues()
    if not catalogues:
        print("\nNo catalogues available.")
        return None, None
    names = list(catalogues.keys())
    print("\nSelect a catalogue:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")
    while True:
        try:
            choice = int(input("\nEnter the number of the catalogue: "))
            if 1 <= choice <= len(names):
                return names[choice - 1], catalogues
            else:
                print("Invalid number, try again.")
        except ValueError:
            print("Please enter a valid number.")

def view_catalogue():
    name, catalogues = choose_catalogue()
    if not name:
        return

    while True:
        print("\nCurrent catalogue items:")
        if catalogues[name]["items"]:
            for i, item in enumerate(catalogues[name]["items"], start=1):
                print(f"\n{i}. {item['name']}: \n{item['description']}")
        else:
            print("No items in this catalogue.")

        action = input("\nReturn to options? (y/n): ").lower()
        if action == "y":
            break
        elif action == "n":
            print("\nReloading...\n")
        else:
            print("\nInvalid input. Please choose 'y' or 'n'.")


def edit_catalogue():
    name, catalogues = choose_catalogue()
    if not name:
        return

    while True:
        print("\nCurrent catalogue items:")
        if catalogues[name]["items"]:
            for i, item in enumerate(catalogues[name]["items"], start=1):
                print(f"{i}. {item['name']}: {item['description']}")
        else:
            print("No items in this catalogue.")

        action = input("\nAdd (a), Remove (r), Rename (e) an item, or Quit (q) editing catalogue: ").lower()
        if action == 'a':
            item_name = input("Enter the item name to add: ")
            item_desc = input("Enter the item description: ")
            catalogues[name]["items"].append({"name": item_name, "description": item_desc})
            print(f"Item '{item_name}' added.")
        elif action == 'r':
            item_name = input("Enter the item name to remove: ")
            found = False
            for item in catalogues[name]["items"]:
                if item["name"] == item_name:
                    catalogues[name]["items"].remove(item)
                    print(f"Item '{item_name}' removed.")
                    found = True
                    break
            if not found:
                print("Item not found in catalogue.")
        elif action == 'e':
            old_name = input("Enter the current item name to rename: ")
            for item in catalogues[name]["items"]:
                if item["name"] == old_name:
                    new_name = input("Enter the new name for the item: ")
                    item["name"] = new_name
                    print(f"Item '{old_name}' renamed to '{new_name}'.")
                    break
            else:
                print("Item not found in catalogue.")
        elif action == 'q':
            print("Finished editing catalogue.")
            break
        else:
            print("Invalid action. Please choose 'a', 'r', 'e', or 'q'.")

    save_catalogues(catalogues)


options = {
    0 : {"desc" : "Exit", "func" : exit},
    1 : {"desc" : "List catalogues", "func" : list_catalogues},
    2 : {"desc" : "Create a new catalog", "func" : create_catalogue},
    3 : {"desc" : "Remove an existing catalog", "func" : remove_catalogue},
    4 : {"desc" : "View an existing catalog", "func" : view_catalogue},
    5 : {"desc" : "Edit an existing catalog", "func" : edit_catalogue}
}

def print_options():
    while True:
        for x in sorted(options):
            print(f'{x} - {options[x]["desc"]}')
        try:
            opt = int(input("Input option: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if opt == 0:
            print("Exiting...")
            break
        elif opt not in options:
            print("Invalid option.")
        else:
            options[opt]["func"]()

if __name__ == "__main__":
    print_options()
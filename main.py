import random
from db import load_pokemon_data, save_pokemon_data
from fetch_pokemon import get_pokemon_list, get_pokemon_details
from show_pokemon import display_pokemon

def main():
    pokemon_collection = load_pokemon_data()

    while True:
        answer = input("Would you like to draw a Pokemon? (yes/no): ").lower()
        if answer == 'yes':
            pokemon_list = get_pokemon_list()
            if pokemon_list:
                chosen = random.choice(pokemon_list)
                if chosen in pokemon_collection:
                    print(f"\n{chosen.capitalize()} is already in your collection!")
                    display_pokemon(chosen, pokemon_collection[chosen])
                else:
                    print(f"Fetching details for {chosen}...")
                    details = get_pokemon_details(chosen)
                    if details:
                        pokemon_collection[chosen] = details
                        save_pokemon_data(pokemon_collection)
                        display_pokemon(chosen, details)
                    else:
                        print("Could not get details.")
            else:
                print("Failed to fetch Pokemon list.")
        elif answer == 'no':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()

def display_pokemon(name, details):
    print(f"\n--- {name.capitalize()} ---")
    if details:
        for key, value in details.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("No details available.")
    print("-" * (len(name) + 7))

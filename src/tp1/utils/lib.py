from scapy.arch import get_if_list, get_working_if


def hello_world() -> str:
    return "hello world"


def choose_interface() -> str:
    try:
        interfaces = get_if_list()
        if not interfaces:
            raise Exception("Aucune interface reseau trouvee")
    except Exception as e:
        print(f"Error: {e}")
        return ""

    print("Available network interfaces:")
    for i, interface in enumerate(interfaces, 1):
        print(f"{i}. {interface}")

    while True:
        try:
            choice = input("\nSelectionnez une interface (numero): ").strip()
            if choice == "":
                selected = interfaces[0]
            else:
                index = int(choice) - 1
                if 0 <= index < len(interfaces):
                    selected = interfaces[index]
                else:
                    print(f"Veuillez entrer un numero entre 1 et {len(interfaces)}")
                    continue
            print(f"Interface selectionnee: {selected}")
            return selected
        except EOFError:
            selected = interfaces[0]
            print(f"Interface selectionnee: {selected}")
            return selected
        except ValueError:
            print("Veuillez entrer un numero valide")
        except Exception as e:
            print(f"Erreur: {e}")
            return get_working_if()
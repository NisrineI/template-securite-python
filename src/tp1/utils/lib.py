def hello_world() -> str:
    """
    Hello world function
    """
    return "hello world"


def choose_interface() -> str:
    """
    Return network interface and input user choice
    """
    from scapy.arch import get_if_list
    from scapy.arch import get_working_if

    try:
        interfaces = get_if_list()
        if not interfaces:
            raise Exception("Aucune interface reseau trouvee")
    except Exception as e:
        print(f"Error: {e}")
        return None

    print("Available network interfaces:")
    for i, interface in enumerate(interfaces, 1):
        print(f"{i}. {interface}")

    while True:
        try:
            choice = input("\nSelectionnez une interface (numero): ").strip()
            if choice == "":
                selected = interfaces[0]
                print(f"Interface selectionnee: {selected}")
                return selected
            index = int(choice) - 1

            if 0 <= index < len(interfaces):
                selected = interfaces[index]
                print(f"Interface selectionnee: {selected}")
                return selected
            else:
                print(f"Veuillez entrer un numero entre 1 et {len(interfaces)}")
        except EOFError:
            selected = interfaces[0]
            print(f"Interface selectionnee: {selected}")
            return selected
        except ValueError:
            print("Veuillez entrer un numero valide")
        except Exception as e:
            print(f"Erreur: {e}")
            return get_working_if()

import subprocess
import platform

# Zmienne:
br = "-------------------------------------------------------"
autor = "I"
n_repo = "name"

# Funkcja do sprawdzania dostępności hosta
def ping_ip(host, attempts):
    system = platform.system()
    if system == "Windows":
        ping_option = '-n'
    else:
        ping_option = '-c'

    success = False
    for _ in range(attempts):
        try:
            result = subprocess.run(['ping', ping_option, '1', host],
                                    capture_output=True,
                                    text=True,
                                    check=True)
            success = True
            break  # Przerwij pętlę, jeśli ping się uda
        except subprocess.CalledProcessError:
            pass  # Kontynuuj, jeśli ping nie powiódł się
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            return False

    return success

print(f"""
 ██████╗ ██████╗ ███████╗███╗   ██╗  ██╗██████╗ 
██╔═══██╗██╔══██╗██╔════╝████╗  ██║  ██║██╔══██╗
██║   ██║██████╔╝█████╗  ██╔██╗ ██║  ██║██████╔╝
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║  ██║██╔═══╝ 
╚██████╔╝██║     ███████╗██║ ╚████║  ██║██║     
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝  ╚═╝╚═╝     

 GitHub : https://github.com/{autor}/{n_repo}
             Create by : {autor}
""")

menu = input("> ")

# Wyświetlanie pomocy
if menu == "help":
    print("                 Podstawowe polecenia")
    print(br)
    print("help - Wyświetla listę poleceń")
    print(" ")
    print(br)
    print("                          IP")
    print("ping - Sprawdzanie IP")
    menu = input("> ")

# Sprawdzanie IP
elif menu == "ping":
    ping = input("IP > ")
    ping_a = int(input("Ile razy sprawdzasz > "))
    
    if not ping:
        print("Nie podałeś adresu IP.")
    elif ping_a <= 0:
        print("Liczba prób musi być większa od 0.")
    else:
        # Wywołuje funkcję ping
            if ping_ip(ping, ping_a):
                print(f"\033[1;33m [Info] \033[0m \033[32m Ping {ping} odpowiada. \033[0m")
            else:
                print(f"\033[1;33m [Info] \033[0m \033[31m Ping {ping} nie działa. \033[0m")


# Błędne polecenie
else:
    print("Jeśli chcesz całą listę poleceń wpisz help")
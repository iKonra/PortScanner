import socket
import threading
from colorama import Fore, Back, Style
import pyfiglet


def scan_ports(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPV4 SOCK_STREAM = TCP
        sock.settimeout(3)  
        result = sock.connect_ex((target, port))
        if result == 0:
            print(Fore.GREEN + f"PORT {port} : OPEN - " + socket.getservbyport(port, "tcp") +  Style.RESET_ALL)
        sock.close()
    except socket.error:
        pass



print("\n\n\n\n\n\n\n\n\n")
print(Fore.CYAN + pyfiglet.figlet_format('PortScanner'))
print(Fore.LIGHTBLACK_EX + pyfiglet.figlet_format('Made by Konra'))

target = input(Fore.RED + 'Whats ip do u want scan: ' + Fore.WHITE)
verify = target.split(".")
verificated = False


while(verificated == False):
    if len(verify) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in verify):
        print("Scanning Ports...")
        verificated = True
    else:
        try:
            target = socket.gethostbyname(target)
            print("Scanning Ports...")
            verificated = True
        except socket.gaierror:
            print("Invalid IP. Try Again.")
            target = input(Fore.RED + 'Whats ip do u want scan: ' + Fore.WHITE) #  Actualizo la ip y sus partes
            verify = target.split(".") # -----------



threads = []
for port in range(1, 10001):
    thread = threading.Thread(target=scan_ports, args=(target, port))
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(Fore.CYAN + "Scan complete!" + Style.RESET_ALL)
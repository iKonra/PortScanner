import socket
import threading
import os
import subprocess
from colorama import Fore, Back, Style
import pyfiglet
import platform
import re



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

def detectar_sistema_operativo(target):
    comando = ["ping", "-n", "1", target] if platform.system().startswith("Win") else ["ping", "-c", "1", target]
    # En windows y en otros Os se usa distinto el ping, se usa los parametros -n/-c para indicar que solo queremos 1 paquete para agilizar el envio

    try:
        salida = subprocess.check_output(comando, universal_newlines=True, stderr=subprocess.DEVNULL)
        # Salida = Capturamos el outpot del comando, convertimos todo a texto, ignoramos errores
        ttl_match = re.search(r"TTL=(\d+)", salida, re.IGNORECASE)
        # Buscamos en la salida del ping un numero despues de "TTL=" (ignorando mayusculas y minusculas)

        if ttl_match:
            ttl = int(ttl_match.group(1))

            if ttl > 64:  
                return Fore.LIGHTGREEN_EX + "Sistema Windows"+ Fore.RESET
            elif ttl <= 64:  
                return Fore.LIGHTGREEN_EX + "Sistema Unix/Linux/MacOs/FreeBSD" + Fore.RESET
            elif ttl >= 200:  
                return Fore.LIGHTGREEN_EX + "Router Cisco/Solaris/AIX" + Fore.RESET
            else:
                return Fore.RED + "Sistema desconocido"+ Fore.RESET

        return Fore.RED + "Sistema Operativo: No se pudo detectar" + Fore.RESET

    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return "Error al hacer ping"


print("\n\n\n\n\n\n\n\n\n")
print(Fore.CYAN + pyfiglet.figlet_format('PortScanner'))
print(Fore.LIGHTBLACK_EX + pyfiglet.figlet_format('Made by Konra'))

target = input(Fore.RED + 'Whats ip/url do u want scan: ' + Fore.WHITE)
verify = target.split(".")
verificated = False


while(verificated == False):
    if len(verify) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in verify):
        print("Scanning Ports...")
        verificated = True
    else:
        try:
            target = socket.gethostbyname(target)
            print("Scanning Ports of " + target)
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


print(detectar_sistema_operativo(target))
print(Fore.CYAN + "Scan complete!" + Style.RESET_ALL)
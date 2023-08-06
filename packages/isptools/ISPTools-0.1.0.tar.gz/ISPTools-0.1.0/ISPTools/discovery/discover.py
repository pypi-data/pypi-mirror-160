import socket

##Obtenemos la Ip de nuestro dispositivo desde python
## Tambien ingresamos manualmente la ip para obtener el pool de las ip
def obtiene_ip(dato):
    if dato == True:
        nombre_equipo = socket.gethostname()
        print ("El nombre de su equipo actual es: ", nombre_equipo)
        direccion_equipo = socket.gethostbyname(nombre_equipo)
        print ("Su IP es: ", direccion_equipo)
        ip_separada = direccion_equipo.split(".")
        return ip_separada
    else:
        ip_ingresada=input("Ingrese la IP con el siguiente formato: 192.168.0.1 \n ")
        ip_separada = ip_ingresada.split(".")
        print (ip_separada)
        return ip_separada
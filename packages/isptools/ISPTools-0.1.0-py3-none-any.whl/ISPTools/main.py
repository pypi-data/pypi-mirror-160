from ISPTools.discovery.discover import obtiene_ip
from ISPTools.Pool.pool import optener_rango_ip
from ISPTools.Ports.port import port
from ISPTools.Ping.hayping import ping, ping_solo

pool_de_ips=[]
pool_de_ip=[]
pool=[]
ip_para_puertos=[]
detecciones=0

salir=False
while not salir:
    print("+-------------------------------------+")
    print ("  Bienvenido al sistema de monitoreo  ")
    print("+-------------------------------------+ \n")
    print("Menu: \n")
    print ("1. Detectar ip e informacion del dispositivo actual:")
    print ("2. Detectar dispositivo en un rango especifico: ")
    print ("3. Hacer ping a una IP: ")
    print ("4. Detectar puertos en una IP: ")
    print ("5. Salir \n")
     
    print ("Elige una opcion \n")
 
    opcion = input(": \n")
 
    if opcion == "1":
        print ("Informacion del dispositivo actual 1 \n")
        ip_separada=obtiene_ip(True)
        print ("\n")
    elif opcion == "2":
        print ("Opcion 2")
        ip_separada=obtiene_ip(False)
        pool=optener_rango_ip(ip_separada)
        while ping(pool):
          print("Hay ping")
          print(pool)
    elif opcion == "3":
        print("Opcion 3")
        ip_ping_sola=input("Ingrese la IP para realizar un monitoreo: ")
        while ping_solo(ip_ping_sola):
            print("Hay ping")
    elif opcion == "4":
       ip=input("Ingrese la IP para realizar un monitoreo de puertos: ")
       port(ip)
    elif opcion == "5":
        print("Gracias por usar mi programa :D ")
        salir = True
    else:
        print ("Introduce un numero entre 1 y 5")
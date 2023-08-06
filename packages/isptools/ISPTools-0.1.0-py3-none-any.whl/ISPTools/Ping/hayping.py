import platform
import subprocess

ip_para_puertos=[]
detecciones=0
def ping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'
    for i in range(1,255):
      command = ['ping', parameter, '1', host[i]]
      response = subprocess.call(command)
      if response == 0:
        print("Se ha detectado un dispositivo")
        print("IP: ", host[i])
        detecciones=detecciones+1
        ip_para_puertos.append(host[i])
      else:
        next
    return detecciones
def ping_solo(host):
    detecciones=0
    a=True
    parameter = '-n' if platform.system().lower()=='windows' else '-c'
    while a:
      command = ['ping', parameter, '1', host]
      response = subprocess.call(command)
      if response == 0:
        print("Hay ping en: ", host)
        detecciones = detecciones+1
        if detecciones >5:
              a=False
      else:
        print("No hay ping en: ", host)
        detecciones = detecciones+1
        if detecciones > 3 or detecciones> 200:
            print("Ha finalizado el programa con", detecciones, " Paquetes")
            a=False
ping_solo("8.8.8.8")
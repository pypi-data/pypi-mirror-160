import socket
def puertos_de_ip(ip):
    
    for port in range(65535): 
        try: 
            serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
            serv.bind((ip,port)) 
        except: 
            print('[Encontrado] Puerto abierto :',port) 
  
    serv.close()
puertos_de_ip("192.168.0.101")
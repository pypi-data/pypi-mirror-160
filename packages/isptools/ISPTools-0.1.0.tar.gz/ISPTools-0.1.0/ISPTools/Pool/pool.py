pool_de_ips=[]
pool_de_ip=[]
pool=[]
def optener_rango_ip(ip_separada):
    for i in range(1,255):
      pool_de_ips=str(ip_separada[0]+"."+ip_separada[1]+"."+ip_separada[2]+"."+str(i))
      pool_de_ip.append(pool_de_ips)
    return pool_de_ip
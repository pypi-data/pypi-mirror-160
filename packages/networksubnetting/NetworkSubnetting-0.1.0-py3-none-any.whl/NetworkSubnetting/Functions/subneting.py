import ipaddress
from ipaddress import *
import re

def ip_directions(ip):
    return list(ip_network(ip).hosts())

def ip_all_directions(ip):
    directions = []
    for addr in IPv4Network(ip):
        directions.append(addr)
    return directions


def contain_direction(ip, ip2):
    return IPv4Address(ip2) in IPv4Network(ip)


def class_ip_direction(ip):
    regex = re.compile(r'([0-9]+).([0-9]+).([0-9]+).([0-9]+)')
    result = re.findall(regex, ip)

    ip = list(result[0])

    if not result:
        return ("Datos incorrectos, por favor intente de nuevo")

    IP_binary_string = '.'.join(bin(int(i))[2:].zfill(8)for i in ip)

    if IP_binary_string.startswith('0'):
        return("Dirección de clase A", IP_binary_string)
    elif IP_binary_string.startswith('10'):
        return("Dirección de clase B", IP_binary_string)
    elif IP_binary_string.startswith('110'):
        return("Dirección de clase C", IP_binary_string)
    elif IP_binary_string.startswith('1110'):
        return("Dirección de clase D", IP_binary_string)
    else:
        return("Dirección de clase E", IP_binary_string)


def data_direction(ip):
    ip = ipaddress.IPv4Network(ip)

    print("\nEs multicast: ", ip.is_multicast)
    print("Es privada: ", ip.is_private)
    print("Es global: ", ip.is_global)
    print("La dirección no esta espicificada: ", ip.is_unspecified)
    print("La dirección es reservada IETF: ", ip.is_reserved)
    print("Es una dirección loopback: ", ip.is_loopback)
    print("La dirección está reservada para uso local de enlace: ", ip.is_link_local, "\n")


def convert_to_bin(decimal):
    regex = re.compile(r'([0-9]+)')
    result = re.findall(regex, decimal)

    ip = list(result)

    if not result:
        return ("Datos incorrectos, por favor intente de nuevo")

    IP_binary_string = '.'.join(bin(int(i))[2:] for i in ip)

    return(IP_binary_string)
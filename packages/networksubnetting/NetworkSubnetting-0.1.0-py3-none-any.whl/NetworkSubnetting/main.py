from Functions import subneting

class NetworkSubnetting():
    def main(self):
        print('--------------------------------------------------')
        print('BIENVENIDO AL PROGRAMA PARA SUBNETEAR REDES')
        print('--------------------------------------------------')
        option = -1
        while option != 0:
            print('[1] Obtener direcciones IP utilizables que pertenecen a la red')
            print('[2] Obtener todas las direcciones IP que pertenecen a la red')
            print('[3] Verificar si una dirección IP pertenece a una red')
            print('[4] Obtener la clase de la dirección IP')
            print('[5] Obtener datos de la dirección IP')
            print('[6] Convertir de decimal a binario')
            print('[7] Convertir de decimal a hexadecimal')
            print('[8] Convertir de binario a decimal')
            print('[9] Convertir de hexadecimal a binario')
            print('[10] Convertir de IPv4 a IPv6')
            print('[0] Salir')

            option = int(input('SELECCIONE UNA OPCIÓN: '))
            if option == 1:
                ip = input('Ingrese la dirección IP: ')
                result = subneting.ip_directions(ip)
                print(result)

            elif option == 2:
                ip = input('Ingrese la dirección IP: ')
                result = subneting.ip_all_directions(ip)
                print(result)

            elif option == 3:
                ip = input('Ingrese la dirección de la red: ')
                ip2 = input('Ingrese la dirección IP que desea verificar: ')
                result = subneting.contain_direction(ip, ip2)
                if result == True:
                    print('La red %s si pertenece a la red %s \n' % (ip2, ip))
                else:
                    print('La red %s no pertenece a la red %s \n' % (ip2, ip))

            elif option == 4:
                ip = input('Ingrese la dirección IP: ')
                result = subneting.class_ip_direction(ip)
                print('\n',result, '\n')

            elif option == 5:
                ip = input('Ingrese la dirección IP: ')
                subneting.data_direction(ip)

            elif option == 6:
                decimal = input('Ingrese el numero decimal que desea convertir a binario: ')
                result = subneting.convert_to_bin(decimal)
                print('\n', result, '\n')

if __name__ == "__main__":
    network_subnetting = NetworkSubnetting()
    network_subnetting.main()

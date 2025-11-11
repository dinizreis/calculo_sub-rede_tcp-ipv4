import ipaddress

def calcular_subrede():
    print("=== Calculadora de Sub-rede ===")

    # Solicita ao usuário o endereço IP e a máscara de sub-rede
    ip_input = input("Digite o endereço IP (ex: 192.168.1.1/24): ")

    try:
        # Cria o objeto de rede IP
        rede = ipaddress.ip_network(ip_input, strict=False)

        print("\n=== Resultados da Sub-rede ===")
        print(f"Rede: {rede.network_address}")
        print(f"Broadcast: {rede.broadcast_address}")
        print(f"Máscara de Sub-rede: {rede.netmask}")
        print(f"Número de Hosts: {rede.num_addresses}")

        # Apenas se for rede com hosts disponíveis
        if rede.num_addresses > 2:
            hosts = list(rede.hosts())
            print(f"Primeiro Host: {hosts[0]}")
            print(f"Último Host: {hosts[-1]}")
        else:
            print("Esta sub-rede não possui hosts disponíveis.")
    except ValueError:
        print("Endereço IP ou máscara de sub-rede inválidos. por favor, tente novamente.")

if __name__ == "__main__":
    calcular_subrede()
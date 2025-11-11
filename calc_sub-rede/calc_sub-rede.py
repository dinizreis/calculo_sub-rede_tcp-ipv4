from ipaddress import ip_network
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

console = Console()

def obter_info_rede(rede_cidr: str):
    ''''
    Recebe uma string no formato CIDR (ex: "192.168.10.0/26")
    e retorna informações detalhadas sobre a sub-rede.
    '''

    net = ip_network(rede_cidr, strict=False)     # aceita IP não-zero de host (ex: 192.168.1.1/24)
    info = {
        "network": str(net.network_address),
        "prefixlen": net.prefixlen,
        "netmask": str(net.netmask),
        "broadcast": str(net.broadcast_address),
        "total_addresses": net.num_addresses,
    }

    # hosts() gera um iterador dos endereços de host válidos (exclui network e broadcast)
    hosts = list(net.hosts())
    if hosts:
        info["first_host"] = str(hosts[0])
        info["last_host"] = str(hosts[-1])
        info["usable_hosts"] = len(hosts)
        # amostra dos primeiros 8 hosts (ou menos, se a rede for pequena)
        info["sample_hosts"] = [str(h) for h in hosts[:8]]
    else:
        info["first_host"] = "-"
        info["last_host"] = "-"
        info["usable_hosts"] = 0
        info["sample_hosts"] = []

        return info
    
def imprimir_tabela(info: dict):
    '''Recebe o dicionário de info e imprime uma tabela formatada com rich.'''

    table = Table(title="Cálculo de Sub-rede IPv4", show_edge=True, header_style="bold magenta")
    table.add_column("Propriedade", style="bold")
    table.add_column("Valor", style="cyan")

    table.add_row("Rede", info["network"])
    table.add_row("Prefixo (CIDR)", f"/{info['prefixlen']}")
    table.add_row("Máscara de Rede", info["netmask"])
    table.add_row("Endereço Broadcast", info["broadcast"])
    table.add_row("Total de Endereços", str(info["total_addresses"]))
    table.add_row("Endereços utilizáveis (hosts)", str(info["usable_hosts"]))
    table.add_row("Primeiro Host", info["first_host"])
    table.add_row("Último Host", info["last_host"])

    console.print(table)

    # painel com amostra de hosts (se houver)
    if info["sample_hosts"]:
        hosts_text = "\n".join(info["sample_hosts"])
        panel = Panel(
            Align.left(hosts_text),
            title="Amostra de Endereços de Host",
            border_style="red",
            subtitle=f"Mostrando até {len(info['sample_hosts'])} hosts"
        )
        console.print(panel)
    else:
        console.print(Panel("Nenhum host utilizável nesta rede.", border_style="blue"))

def calcular_interativo():
    console.rule("[Bold green]Calculadora de Sub-rede IPv4")
    rede_input = console.input("[bold yellow]Digite a rede no formato CIDR (ex: 192.168.10.0/26): [/]")
    try:
        info = obter_info_rede(rede_input.strip())
        imprimir_tabela(info)
    except ValueError as e:
        console.print(f"[red]Endereço inválido:[/] {e}")
        console.print(f"[italic]Formato esperado: 192.168.10.0/24[/]")

if __name__ == "__main__":
    calcular_interativo()
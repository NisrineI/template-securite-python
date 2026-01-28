from collections import defaultdict
from typing import Dict, List, Tuple
from scapy.layers.l2 import ARP, Ether
from scapy.all import sniff, Packet
from scapy.layers.inet import IP, ICMP, TCP, UDP
from tp1.utils.lib import choose_interface
from tp1.utils.config import logger


class Capture:
    def __init__(self) -> None:
        self.interface = choose_interface()
        self.summary = ""
        self.packets: List[Packet] = []
        self.packet_count = 0
        self.protocol_stats: Dict[str, int] = defaultdict(int)

    def packet_callback(self, packet: Packet) -> None:
        self.packets.append(packet)
        self.packet_count += 1
        protocol = self.extract_protocol(packet)
        self.protocol_stats[protocol] += 1
        logger.debug(f"Paquet : {self.packet_count} , Protocole: {protocol}")

    def extract_protocol(self, packet: Packet) -> str:
        if ARP in packet:
            return "ARP"
        if IP in packet:
            ip_proto = packet[IP].proto
            if ip_proto == 6:
                return "TCP"
            elif ip_proto == 17:
                return "UDP"
            elif ip_proto == 1:
                return "ICMP"
        return "Inconnu"

    def capture_traffic(self, packet_count: int = 3) -> None:
        """
        Capture network trafic from an interface
        """
        interface = self.interface
        logger.info(f"Capture traffic from interface {interface}")
        sniff(iface=interface, prn=self.packet_callback, store=False, count=packet_count)

    def sort_network_protocols(self) -> List[Tuple[str, int]]:
        """
        Sort and return all captured network protocols
        """
        return sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True)

    def get_all_protocols(self) -> Dict[str, int]:
        """
        Return all protocols captured with total packets number
        """
        return dict(self.protocol_stats)

    def analyse(self, protocols: str) -> None:
        """
        Analyse all captured data and return statement
        Si un tra c est illégitime (exemple : Injection SQL, ARP
        Spoo ng, etc)
        a Noter la tentative d'attaque.
        b Relever le protocole ainsi que l'adresse réseau/physique
        de l'attaquant.
        c (FACULTATIF) Opérer le blocage de la machine
        attaquante.
        Sinon a cher que tout va bien
        """
        all_protocols = self.get_all_protocols()
        sort = self.sort_network_protocols()
        logger.debug(f"All protocols: {all_protocols}")
        logger.debug(f"Sorted protocols: {sort}")
        self.summary = self.gen_summary()

    def get_summary(self) -> str:
        return self.summary

    def gen_summary(self) -> str:
        """
        Generate summary
        """
        summary = f"\nInterface: {self.interface}\n"
        summary += f"Total paquets: {self.packet_count}\n\n"
        summary += "PROTOCOLES:\n"
        for protocol, count in self.sort_network_protocols():
            summary += f"  {protocol}: {count}\n"
        return summary
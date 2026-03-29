from collections import defaultdict
from typing import Dict, List, Tuple
from scapy.all import sniff, Packet
from scapy.layers.inet import IP
from scapy.layers.l2 import ARP
from src.tp1.utils.lib import choose_interface
from src.tp1.utils.config import logger


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
        logger.debug(f"Paquet {self.packet_count} - Protocole: {protocol}")

    def extract_protocol(self, packet: Packet) -> str:
        if ARP in packet:
            return "ARP"
        if IP in packet:
            protos = {6: "TCP", 17: "UDP", 1: "ICMP"}
            return protos.get(packet[IP].proto, "Inconnu")
        return "Inconnu"

    def capture_traffic(self) -> None:
        logger.info(f"Capture traffic from interface {self.interface}")
        sniff(iface=self.interface, prn=self.packet_callback, store=False, count=100)

    def sort_network_protocols(self) -> List[Tuple[str, int]]:
        return sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True)

    def get_all_protocols(self) -> Dict[str, int]:
        return dict(self.protocol_stats)

    def analyse(self, protocols: str) -> None:
        all_protocols = self.get_all_protocols()
        sort = self.sort_network_protocols()
        logger.debug(f"All protocols: {all_protocols}")
        logger.debug(f"Sorted protocols: {sort}")
        self.summary = self.gen_summary()

    def get_summary(self) -> str:
        return self.summary

    def gen_summary(self) -> str:
        summary = f"\nInterface: {self.interface}\n"
        summary += f"Total paquets: {self.packet_count}\n\n"
        summary += "PROTOCOLES:\n"
        for protocol, count in self.sort_network_protocols():
            summary += f"  {protocol}: {count}\n"
        return summary
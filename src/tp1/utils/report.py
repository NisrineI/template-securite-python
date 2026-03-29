import pygal


class Report:
    def __init__(self, capture, filename, summary):
        self.capture = capture
        self.filename = filename
        self.title = "Capture reseau TP1\n"
        self.summary = summary
        self.array = ""
        self.graph = ""

    def concat_report(self) -> str:
        content = ""
        content += self.title
        content += self.summary
        content += self.array
        content += self.graph
        return content

    def save(self, filename: str) -> None:
        final_content = self.concat_report()
        with open(self.filename, "w") as report:
            report.write(final_content)

    def generate(self, param: str) -> None:
        if param == "graph":
            self._generate_graph()
        elif param == "array":
            self._generate_array()

    def _generate_array(self) -> None:
        array = "\nTABLEAU DES PROTOCOLES\n"
        array += f"{'Protocole':<15} {'Nombre':<10} {'Pourcentage':<10}\n"
        array += "-" * 40 + "\n"
        for protocol, count in self.capture.sort_network_protocols():
            percentage = (count / self.capture.packet_count) * 100
            array += f"{protocol:<15} {count:<10} {percentage:.1f}%\n"
        self.array = array

    def _generate_graph(self) -> None:
        pie_chart = pygal.Pie()
        pie_chart.title = "Repartition des protocoles"
        for protocol, count in self.capture.sort_network_protocols():
            pie_chart.add(protocol, count)
        pie_chart.render_to_file("chart.svg")
        self.graph = "\nGRAPHIQUE (chart.svg)\n"
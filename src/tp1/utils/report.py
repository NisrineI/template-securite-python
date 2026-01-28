from fpdf import FPDF
import pygal


class Report:
    def __init__(self, capture, filename, summary):
        self.capture = capture
        self.filename = filename
        self.title = "Capture reseau TP1\n"
        self.summary = summary
        self.pdf = FPDF()
        self.array = ""
        self.graph = ""

    def concat_report(self) -> str:
        """
        Concat all data in report
        """
        content = ""
        content += self.title
        content += self.summary
        content += self.array
        content += self.graph

        return content

    def save(self, filename: str) -> None:
        """
        Save report in a file
        :param filename:
        :return:
        """
        final_content = self.concat_report()
        with open(self.filename, "w") as report:
            report.write(final_content)

    def generate(self) -> None:
        """
        Generate graph and array
        """
        self._generate_array()
        self._generate_graph()

    def _generate_array(self) -> None:
        """Generer le tableau des protocoles"""
        array_text = "\nTABLEAU DES PROTOCOLES\n"
        array_text += f"{'Protocole':<15} {'Nombre':<10} {'Pourcentage':<10}\n"
        array_text += "-" * 40 + "\n"

        for protocol, count in self.capture.sort_network_protocols():
            percentage = (count / self.capture.packet_count) * 100
            array_text += f"{protocol:<15} {count:<10} {percentage:.1f}%\n"

        self.array = array_text

    def _generate_graph(self) -> None:
        """Generer le graphique"""
        graph_text = "\nGRAPHIQUE\n"

        pie_chart = pygal.Pie()
        pie_chart.title = "Repartition des protocoles"

        for protocol, count in self.capture.sort_network_protocols():
            pie_chart.add(protocol, count)

        pie_chart.render_to_file("chart.svg")

        self.graph = graph_text

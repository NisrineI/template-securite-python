import argparse
from pathlib import Path
from tp2.config import logger
from tp2.utils.analyzer import load_shellcode, analyse

BASE_DIR = Path(__file__).parent / "utils"
SHELLCODE_FACILE = BASE_DIR / "shellcode_easy.txt"
SHELLCODE_MOYEN = BASE_DIR / "shellcode_medium.txt"


def main() -> None:
    logger.info("Starting TP2")

    parser = argparse.ArgumentParser(description="TP2 - Shellcode Analyzer")
    parser.add_argument("-f", "--file", type=str, help="Fichier shellcode a analyser")
    args = parser.parse_args()

    if args.file:
        analyse(args.file, load_shellcode(args.file))
    else:
        analyse("Facile", load_shellcode(SHELLCODE_FACILE))
        analyse("Moyen", load_shellcode(SHELLCODE_MOYEN))


if __name__ == "__main__":
    main()
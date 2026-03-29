import re
from pathlib import Path

from tp2.config import logger

try:
    import pylibemu
except ImportError:
    pylibemu = None

try:
    from capstone import Cs, CS_ARCH_X86, CS_MODE_32
except ImportError:
    Cs = None


def load_shellcode(filepath: str) -> bytes:
    return parse_shellcode(Path(filepath).read_text(encoding="utf-8"))


def parse_shellcode(text: str) -> bytes:
    bytes_list = re.findall(r"\\x([0-9a-fA-F]{2})", text)
    if not bytes_list:
        raise ValueError("No valid \\xNN bytes found")
    return bytes(int(b, 16) for b in bytes_list)


def get_shellcode_strings(shellcode: bytes, min_len: int = 4) -> list[str]:
    out, buf = [], []
    for b in shellcode:
        if 32 <= b <= 126:
            buf.append(b)
        else:
            if len(buf) >= min_len:
                out.append(bytes(buf).decode("ascii", errors="ignore"))
            buf = []
    if len(buf) >= min_len:
        out.append(bytes(buf).decode("ascii", errors="ignore"))
    return out


def get_pylibemu_analysis(shellcode: bytes) -> str | None:
    if pylibemu is None:
        return None
    emulator = pylibemu.Emulator(output_size=4096)
    offset = emulator.shellcode_getpc_test(shellcode)
    if offset < 0:
        return "No shellcode detected."
    emulator.prepare(shellcode, offset)
    emulator.test()
    output = emulator.emu_profile_output
    return output.decode("utf-8", errors="replace") if output else "No profile output."


def get_capstone_analysis(shellcode: bytes) -> str | None:
    if Cs is None:
        return None
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    lines = [f"  0x{i.address:x}: {i.mnemonic} {i.op_str}" for i in md.disasm(shellcode, 0x1000)]
    return "\n".join(lines) if lines else "No instructions decoded."


def analyse(name: str, shellcode: bytes) -> None:
    logger.info(f"Testing shellcode of size {len(shellcode)}B")

    print(f"\n{'=' * 50}")
    print(f"Shellcode : {name} ({len(shellcode)} bytes)")
    print(f"{'=' * 50}")

    print("\n--- Strings ---")
    for s in get_shellcode_strings(shellcode):
        print(f"  {s}")

    print("\n--- Pylibemu ---")
    print(get_pylibemu_analysis(shellcode) or "pylibemu not installed (libemu required).")

    print("\n--- Capstone ---")
    print(get_capstone_analysis(shellcode) or "capstone not installed. Run: pip install capstone")

    logger.info("Shellcode analysed")
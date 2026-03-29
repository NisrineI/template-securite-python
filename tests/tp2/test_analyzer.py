import pytest
from unittest.mock import patch, MagicMock
from tp2.utils.analyzer import load_shellcode, parse_shellcode, get_shellcode_strings, get_pylibemu_analysis, get_capstone_analysis, analyse


def test_parse_shellcode():
    # Given
    text = r"\xEB\x54\x8B\x75"

    # When
    result = parse_shellcode(text)

    # Then
    assert result == bytes([0xEB, 0x54, 0x8B, 0x75])


def test_parse_shellcode_invalid():
    # Given
    text = "ceci nest pas un shellcode"

    # When / Then
    with pytest.raises(ValueError):
        parse_shellcode(text)


def test_load_shellcode(tmp_path):
    # Given
    shellcode_file = tmp_path / "shellcode.txt"
    shellcode_file.write_text(r"\xEB\x54\x8B\x75", encoding="utf-8")

    # When
    result = load_shellcode(str(shellcode_file))

    # Then
    assert result == bytes([0xEB, 0x54, 0x8B, 0x75])


def test_get_shellcode_strings():
    # Given
    shellcode = b"\x00urlmon.dll\x00kernel32\x00\x31"

    # When
    result = get_shellcode_strings(shellcode)

    # Then
    assert "urlmon.dll" in result
    assert "kernel32" in result


def test_get_shellcode_strings_min_len():
    # Given
    shellcode = b"\x00cmd\x00"

    # When
    result = get_shellcode_strings(shellcode, min_len=4)

    # Then
    assert result == []


def test_get_pylibemu_analysis_not_installed():
    # Given
    import tp2.utils.analyzer as analyzer_module
    original = analyzer_module.pylibemu
    analyzer_module.pylibemu = None

    # When
    result = get_pylibemu_analysis(bytes([0xEB, 0x54, 0x8B, 0x75]))

    # Then
    assert result is None
    analyzer_module.pylibemu = original


def test_get_capstone_analysis_not_installed():
    # Given
    import tp2.utils.analyzer as analyzer_module
    original = analyzer_module.Cs
    analyzer_module.Cs = None

    # When
    result = get_capstone_analysis(bytes([0xEB, 0x54, 0x8B, 0x75]))

    # Then
    assert result is None
    analyzer_module.Cs = original


def test_analyse(capsys):
    # Given
    shellcode = bytes([0xEB, 0x54, 0x8B, 0x75, 0x3C, 0x8B, 0x74, 0x35])

    # When
    analyse("Facile", shellcode)

    # Then
    captured = capsys.readouterr()
    assert "Facile" in captured.out
    assert "Strings" in captured.out
    assert "Pylibemu" in captured.out
    assert "Capstone" in captured.out
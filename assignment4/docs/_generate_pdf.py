from pathlib import Path
import re
import textwrap


def pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def main() -> None:
    docs_dir = Path(__file__).resolve().parent
    md_path = docs_dir / "technical_description.md"
    pdf_path = docs_dir / "technical_description.pdf"

    text = md_path.read_text(encoding="utf-8")
    replacements = {
        "—": "-",
        "–": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "…": "...",
        "•": "-",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            lines.append("")
            continue
        line = re.sub(r"^#+\s*", "", line.strip())
        line = line.replace("`", "").replace("**", "")
        wrapped = textwrap.wrap(line, width=92, break_long_words=False, replace_whitespace=False)
        lines.extend(wrapped if wrapped else [""])

    page_height = 842
    page_width = 595
    left_margin = 50
    start_y = 790
    leading = 14
    lines_per_page = 50
    pages = [lines[index:index + lines_per_page] for index in range(0, len(lines), lines_per_page)] or [["Empty document."]]

    objects: list[tuple[int, bytes]] = []
    page_object_numbers: list[int] = []
    next_object_number = 4
    for _ in pages:
        page_object_numbers.append(next_object_number)
        next_object_number += 2

    font_object_number = 3
    for page_index, page_lines in enumerate(pages):
        page_object_number = 4 + page_index * 2
        content_object_number = 5 + page_index * 2
        content_parts = ["BT", "/F1 11 Tf", f"{left_margin} {start_y} Td", f"{leading} TL"]
        first = True
        for line in page_lines:
            safe_line = pdf_escape(line)
            if first:
                content_parts.append(f"({safe_line}) Tj")
                first = False
            else:
                content_parts.append("T*")
                content_parts.append(f"({safe_line}) Tj")
        content_parts.append("ET")
        content_stream = "\n".join(content_parts).encode("latin-1", "replace")
        page_object = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Resources << /Font << /F1 {font_object_number} 0 R >> >> /Contents {content_object_number} 0 R >>"
        ).encode("latin-1")
        content_object = (
            b"<< /Length " + str(len(content_stream)).encode("ascii") + b" >>\nstream\n" + content_stream + b"\nendstream"
        )
        objects.append((page_object_number, page_object))
        objects.append((content_object_number, content_object))

    pages_kids = " ".join(f"{number} 0 R" for number in page_object_numbers)
    base_objects = [
        (1, b"<< /Type /Catalog /Pages 2 0 R >>"),
        (2, f"<< /Type /Pages /Kids [{pages_kids}] /Count {len(page_object_numbers)} >>".encode("latin-1")),
        (3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"),
    ]
    all_objects = sorted(base_objects + objects, key=lambda item: item[0])

    pdf_bytes = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_number, payload in all_objects:
        offsets.append(len(pdf_bytes))
        pdf_bytes.extend(f"{object_number} 0 obj\n".encode("ascii"))
        pdf_bytes.extend(payload)
        pdf_bytes.extend(b"\nendobj\n")

    xref_position = len(pdf_bytes)
    pdf_bytes.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf_bytes.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf_bytes.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_position}\n%%EOF\n".encode("ascii")
    )

    pdf_path.write_bytes(pdf_bytes)
    print(pdf_path)


if __name__ == "__main__":
    main()
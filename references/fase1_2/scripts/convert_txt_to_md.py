import re
import sys
from pathlib import Path


def sanitize_text(text: str) -> str:
    """
    Clean and normalize text content while removing PII/watermarks and promoting
    common section markers.

    Steps:
    - Remove inline watermark segments starting with 'PDF exclusivo para' to end-of-line (case-insensitive)
    - Remove occurrences of 'rm566826' (any case)
    - Remove occurrences of the email 'phellype@gmail.com' (any case)
    - Remove standalone occurrences of the name 'Phellype' (case-insensitive, word-boundary)
    - Promote common section markers (Sumário, Conclusão, Referências) to Markdown headings
    - Collapse 3+ consecutive blank lines to max 2, and trim trailing spaces.
    """
    # Remove watermark substrings but keep the rest of the line
    cleaned = re.sub(r"(?i)PDF\s+exclusivo\s+para[^\n]*", "", text)
    # Remove specific PII tokens
    cleaned = re.sub(r"(?i)rm566826", "", cleaned)
    cleaned = re.sub(r"(?i)phellype@gmail\.com", "", cleaned)
    cleaned = re.sub(r"(?i)\bPhellype\b", "", cleaned)

    # Light normalization only; avoid aggressive insertions that may break words

    # Normalize some common glued tokens from PDF text
    # Add space after 'Fase' when followed by a digit: 'Fase3' -> 'Fase 3'
    cleaned = re.sub(r"(?i)Fase(?=\d)", "Fase ", cleaned)
    # Insert a space before Portuguese articles glued to previous word: 'GitHubO ' -> 'GitHub O '
    cleaned = re.sub(r"(?<=[A-Za-zÁ-ú])(?=(?:O|A|Os|As)\s)", " ", cleaned)
    # Separate page leader + page number glued to section number in TOC lines: '... 3' + '1.1' -> '... 3 1.1'
    cleaned = re.sub(r"(\.{2,}\s*)(\d{1,3})(\d+\.)", r"\1\2 \3", cleaned)

    # If dotted numeric headings (e.g., 1.1, 2.3.4) are glued to previous text, insert a newline before them
    # Require that the token is not preceded by another digit to avoid merging page numbers like "31.1"
    # Only when next non-space char is uppercase to avoid breaking numbers like "4.0 na" or within references
    cleaned = re.sub(r"(?<!\n)(?<!\d)(\d+(?:\.\d+)+)(?=\s*[A-ZÁÉÍÓÚÃÕÇ])", r"\n\1", cleaned)
    # Do not add newlines before single digits to avoid false positives with page numbers

    # If a numeric section marker at start of line is glued to the title word, add a space: "1.4GitHub" -> "1.4 GitHub"
    cleaned = re.sub(r"(^|\n)(\d+(?:\.\d+)*)([A-Za-zÁ-ú])", r"\1\2 \3", cleaned)

    # Remove typical TOC/leader lines entirely (lines containing many dots and page numbers)
    cleaned = re.sub(r"(?mi)^.*\.{5,}.*\d+.*$", "", cleaned)
    # Remove stray page-number lines like "1" or "1." on their own
    cleaned = re.sub(r"(?m)^\s*\d+\.?\s*$", "", cleaned)

    # Trim trailing spaces per line
    cleaned_lines = [ln.rstrip() for ln in cleaned.splitlines()]
    cleaned = "\n".join(cleaned_lines)
    # Normalize excessive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()
    if not cleaned.endswith("\n"):
        cleaned += "\n"
    return cleaned


def promote_numeric_headings(text: str) -> str:
    """Convert lines starting with numeric section markers into Markdown H2 headings.

    Examples:
    - "1 Introdução" -> "## 1 Introdução"
    - "1.2 Título"   -> "## 1.2 Título"
    """
    out_lines: list[str] = []
    body_started = False
    for line in text.splitlines():
        s = line.strip()
        if not s:
            out_lines.append("")
            continue
        # Until the first real heading appears, skip TOC, leaders, and repeated title bits
        if not body_started:
            if s.upper().startswith('SUMÁRIO'):
                continue
            if re.match(r"^\.{5,}\s*\d*\s*$", s):
                continue
            if re.match(r"(?i)^um\s+mapa\s+do\s+tesouro", s):
                continue
            # If a line contains a numeric heading token anywhere, start body from here
            if re.search(r"(^|\s)(\d+(?:\.\d+)*)(\s+)[A-ZÁÉÍÓÚÃÕÇ]", s):
                body_started = True
            else:
                continue
        # Promote Conclusão/Referências outside TOC
        if s.upper() == 'CONCLUSÃO':
            out_lines.append('## Conclusão')
            continue
        if s.upper() == 'REFERÊNCIAS':
            out_lines.append('## Referências')
            continue

        # Numeric headings e.g., "1 Introdução" or "1.2 Título"
        m = re.match(r"^(\d+(?:\.\d+)*)(\s+)(.+)$", s)
        if m:
            num = m.group(1)
            rest = m.group(3)
            # Heuristic: split glued paragraph starters even when glued (no space)
            split_m = re.search(r"(?i)(?<=[a-zá-ú])(?=(Após|Depois|Na|No|Nos|Nas|Em|Além|Por fim)\b)", rest)
            if split_m:
                idx = split_m.start()
                title_part = rest[:idx].strip()
                para_part = rest[idx:].lstrip()
                out_lines.append(f"## {num} {title_part}")
                out_lines.append("")
                out_lines.append(para_part)
            else:
                out_lines.append(f"## {num} {rest}")
            continue
        # Promote Conclusão/Referências markers even when glued
        if re.search(r"(?i)\bCONCLUSÃO\b", s):
            out_lines.append('## Conclusão')
            continue
        if re.search(r"(?i)\bREFERÊNCIAS\b", s):
            out_lines.append('## Referências')
            continue
        out_lines.append(line)
    res = "\n".join(out_lines)
    # Collapse multiple blank lines and ensure trailing newline
    res = re.sub(r"\n{3,}", "\n\n", res).strip()
    return res + "\n"


def convert_folder(folder: Path, *, only_stem: str | None = None, force: bool = False) -> int:
    count = 0
    for txt_path in sorted(folder.glob('*.txt')):
        if only_stem and txt_path.stem.lower() != only_stem.lower():
            continue
        data = b''
        try:
            data = txt_path.read_bytes()
        except Exception:
            data = b''

        raw = ''
        # Preferred strict decodes to avoid mojibake
        for enc in ('utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'latin-1'):
            try:
                raw = data.decode(enc, errors='strict')
                break
            except Exception:
                continue

        body = sanitize_text(raw)
        body = promote_numeric_headings(body)
        title = txt_path.stem
        md_content = f"# {title}\n\n{body}"
        md_path = txt_path.with_suffix('.md')
        # Preserve manual edits unless force=True
        try:
            if not force and md_path.exists() and md_path.stat().st_mtime > txt_path.stat().st_mtime:
                print(f"Ignorado (mais recente): {md_path.name}")
                continue
        except Exception:
            pass
        md_path.write_text(md_content, encoding='utf-8')
        count += 1
    return count


def main():
    # Args (order-agnostic): [fase1|fase2|all]? [--force]? [--file <stem>]? [--dir <path>]?    
    arg = 'all'
    force = False
    only_stem = None
    custom_dir = None

    tokens = sys.argv[1:]
    i = 0
    while i < len(tokens):
        t = tokens[i]
        tl = t.lower()
        if tl in ('fase1', 'fase2', 'all'):
            arg = tl
        elif tl == '--force':
            force = True
        elif tl == '--file' and i + 1 < len(tokens):
            only_stem = tokens[i + 1]
            i += 1
        elif tl == '--dir' and i + 1 < len(tokens):
            custom_dir = Path(tokens[i + 1])
            i += 1
        i += 1
    map_roots = {
        'fase1': Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase1"),
        'fase2': Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase2"),
    }
    if custom_dir is not None:
        roots = [custom_dir]
    elif arg in ('fase1', 'fase2'):
        roots = [map_roots[arg]]
    else:
        roots = [map_roots['fase1'], map_roots['fase2']]

    total = 0
    for root in roots:
        if not root.exists():
            print(f"Pasta não encontrada: {root}")
            continue
        num = convert_folder(root, only_stem=only_stem, force=force)
        total += num
        print(f"Convertidos {num} arquivos em: {root}")
    print(f"Total convertidos: {total}")


if __name__ == "__main__":
    main()

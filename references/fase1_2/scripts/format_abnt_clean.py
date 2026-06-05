#!/usr/bin/env python3
"""
Script melhorado para formatação ABNT dos arquivos Markdown.
Foca em limpeza do conteúdo e estruturação acadêmica adequada.
"""

import re
import sys
from pathlib import Path


def clean_and_structure_content(text: str, chapter_num: int) -> str:
    """Limpa e estrutura o conteúdo seguindo padrões ABNT."""
    
    # 1. Extrair título principal
    title_match = re.search(r'^# (.+)', text, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Capítulo {chapter_num}"
    
    # 2. Remover elementos desnecessários do sumário original
    text = re.sub(r'SUMÁRIO[\s\S]*?(?=\n[A-Z][a-z]|\n\d+\.|\nREFER|$)', '', text, flags=re.IGNORECASE)
    
    # 3. Identificar seções principais baseadas em padrões
    sections = []
    
    # Procurar por seções numeradas ou por palavras-chave
    section_patterns = [
        r'(\d+\.?\d*)\s+([A-Z][^.\n]+)',  # "1.1 Título da seção"
        r'\n([A-Z][A-Z\s]+)\n',          # "CONCLUSÃO"
        r'([Ii]ntrodução|[Cc]onclusão|[Rr]eferências)',  # Seções especiais
    ]
    
    current_section = ""
    content_lines = []
    
    lines = text.split('\n')
    in_references = False
    
    for line in lines:
        line_clean = line.strip()
        
        # Detectar início das referências
        if re.match(r'REFERÊNCIAS|## Referências', line_clean, re.IGNORECASE):
            in_references = True
            content_lines.append("## Referências")
            continue
            
        # Se estamos nas referências, processar diferentemente
        if in_references:
            if line_clean and not line_clean.startswith('#'):
                # Formatar referência individual
                if re.match(r'^[A-Z]', line_clean):
                    content_lines.append(f"\n{line_clean}")
                else:
                    content_lines.append(line_clean)
            continue
        
        # Detectar seções principais no texto
        section_match = re.match(r'^(\d+\.?\d*)\s+(.+)', line_clean)
        if section_match:
            section_num = section_match.group(1)
            section_title = section_match.group(2).strip()
            content_lines.append(f"## {chapter_num}.{section_num} {section_title}")
            continue
            
        # Detectar palavras especiais que indicam seções
        if re.match(r'^(CONCLUSÃO|INTRODUÇÃO)', line_clean, re.IGNORECASE):
            section_title = line_clean.title()
            content_lines.append(f"## {section_title}")
            continue
            
        # Linha normal de conteúdo
        if line_clean:
            content_lines.append(line)
        else:
            content_lines.append("")
    
    # 4. Reconstruir o documento
    result = [f"# {title}", ""]
    
    # 5. Criar sumário baseado nas seções encontradas
    summary_lines = ["## Sumário", ""]
    section_headers = [line for line in content_lines if line.startswith('## ') and 'Sumário' not in line]
    
    for header in section_headers:
        clean_header = header.replace('## ', '').strip()
        summary_lines.append(f"- {clean_header}")
    
    summary_lines.append("")
    result.extend(summary_lines)
    
    # 6. Adicionar conteúdo limpo
    result.extend(content_lines)
    
    # 7. Limpeza final
    final_text = '\n'.join(result)
    final_text = re.sub(r'\n{3,}', '\n\n', final_text)  # Normalizar quebras
    final_text = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', final_text)  # Quebrar parágrafos longos
    
    return final_text.strip() + '\n'


def process_file(file_path: Path) -> bool:
    """Processa um arquivo individual."""
    try:
        # Extrair número do capítulo
        chapter_match = re.search(r'Cap (\d+)', file_path.name)
        chapter_num = int(chapter_match.group(1)) if chapter_match else 1
        
        # Ler conteúdo
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Aplicar formatação
        formatted_content = clean_and_structure_content(content, chapter_num)
        
        # Salvar
        file_path.write_text(formatted_content, encoding='utf-8')
        
        print(f"✅ {file_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ {file_path.name}: {e}")
        return False


def main():
    """Executa formatação para arquivos especificados."""
    
    # Diretórios
    fase1_dir = Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase1")
    fase2_dir = Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase2")
    
    # Determinar escopo
    target = sys.argv[1].lower() if len(sys.argv) > 1 else 'all'
    
    directories = []
    if target in ('fase1', 'all'):
        directories.append(('Fase 1', fase1_dir))
    if target in ('fase2', 'all'):
        directories.append(('Fase 2', fase2_dir))
    
    # Processar
    total, success = 0, 0
    
    for name, directory in directories:
        if not directory.exists():
            print(f"⚠️  {directory} não encontrada")
            continue
            
        print(f"\n📁 {name}:")
        
        for md_file in sorted(directory.glob("*.md")):
            total += 1
            if process_file(md_file):
                success += 1
    
    print(f"\n📊 Processados: {success}/{total} arquivos")


if __name__ == "__main__":
    main()
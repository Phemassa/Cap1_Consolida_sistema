#!/usr/bin/env python3
"""
Script para aplicar formatação ABNT acadêmica aos arquivos Markdown das Fases 1 e 2.
Aplica estrutura hierárquica, sumário, listas formatadas e referências ABNT.
"""

import re
import sys
from pathlib import Path


def create_summary_from_headings(text: str) -> str:
    """Cria um sumário automático baseado nos cabeçalhos do texto."""
    lines = text.split('\n')
    headings = []
    
    for line in lines:
        line = line.strip()
        # Captura cabeçalhos H2 (##) e H3 (###)
        if line.startswith('## ') and not line.lower().startswith('## sumário'):
            heading = line.replace('## ', '').strip()
            headings.append(f"- {heading}")
        elif line.startswith('### '):
            heading = line.replace('### ', '').strip()
            headings.append(f"  - {heading}")
    
    if headings:
        return "## Sumário\n\n" + "\n".join(headings) + "\n- Referências\n\n"
    return ""


def format_lists_and_bullets(text: str) -> str:
    """Formata listas e bullets para padrão acadêmico."""
    # Converter bullets simples em listas numeradas ou com traços
    text = re.sub(r'^•\s*(.+)', r'- \1', text, flags=re.MULTILINE)
    
    # Melhorar formatação de listas numeradas
    text = re.sub(r'^(\d+)\.\s*(.+)', r'\1. **\2**', text, flags=re.MULTILINE)
    
    return text


def format_code_blocks(text: str) -> str:
    """Formata blocos de código com legendas acadêmicas."""
    # Procura por código Python sem formatação e adiciona blocos
    code_pattern = r'(#[^\n]*\n(?:[^\n#]+\n)*[^\n]*)'
    
    def replace_code(match):
        code = match.group(1).strip()
        if 'import' in code or 'def ' in code or 'print(' in code:
            return f"\n```python\n{code}\n```\n"
        return match.group(0)
    
    text = re.sub(code_pattern, replace_code, text)
    return text


def format_references_abnt(text: str) -> str:
    """Formata referências no padrão ABNT."""
    # Encontra seção de referências
    ref_match = re.search(r'(REFERÊNCIAS|Referências)(.+)', text, re.DOTALL | re.IGNORECASE)
    if not ref_match:
        return text
    
    ref_section = ref_match.group(2)
    
    # Separa cada referência (assumindo que cada uma começa com maiúscula após ponto)
    refs = re.split(r'(?<=[.)])([A-Z][A-Z\s,]+)', ref_section)
    
    formatted_refs = []
    for i in range(1, len(refs), 2):
        if i + 1 < len(refs):
            author = refs[i].strip()
            content = refs[i + 1].strip()
            if author and content:
                # Formatar com quebra de linha entre referências
                formatted_refs.append(f"{author}.{content}")
    
    if formatted_refs:
        new_ref_section = "## Referências\n\n" + "\n\n".join(formatted_refs)
        return text.replace(ref_match.group(0), new_ref_section)
    
    return text


def add_section_numbering(text: str, chapter_num: int) -> str:
    """Adiciona numeração hierárquica às seções."""
    lines = text.split('\n')
    result_lines = []
    section_count = 0
    subsection_count = 0
    
    for line in lines:
        if line.startswith('## ') and not line.lower().startswith('## sumário') and not line.lower().startswith('## referências'):
            section_count += 1
            subsection_count = 0
            heading = line.replace('## ', '').strip()
            result_lines.append(f"## {chapter_num}.{section_count} {heading}")
        elif line.startswith('### '):
            subsection_count += 1
            heading = line.replace('### ', '').strip()
            result_lines.append(f"### {chapter_num}.{section_count}.{subsection_count} {heading}")
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)


def format_markdown_abnt(text: str, chapter_num: int) -> str:
    """Aplica formatação ABNT completa ao texto Markdown."""
    
    # 1. Limpar e normalizar o texto
    text = re.sub(r'\n{3,}', '\n\n', text)  # Normalizar quebras de linha
    text = text.strip()
    
    # 2. Aplicar numeração às seções
    text = add_section_numbering(text, chapter_num)
    
    # 3. Formatar listas e bullets
    text = format_lists_and_bullets(text)
    
    # 4. Formatar blocos de código
    text = format_code_blocks(text)
    
    # 5. Formatar referências
    text = format_references_abnt(text)
    
    # 6. Criar e inserir sumário
    summary = create_summary_from_headings(text)
    if summary:
        # Inserir sumário após o título principal
        lines = text.split('\n')
        title_inserted = False
        result_lines = []
        
        for line in lines:
            result_lines.append(line)
            if line.startswith('# ') and not title_inserted:
                result_lines.append('')
                result_lines.extend(summary.split('\n'))
                title_inserted = True
        
        text = '\n'.join(result_lines)
    
    # 7. Limpeza final
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip() + '\n'
    
    return text


def process_markdown_file(file_path: Path) -> bool:
    """Processa um arquivo Markdown aplicando formatação ABNT."""
    try:
        # Extrair número do capítulo do nome do arquivo
        chapter_match = re.search(r'Cap (\d+)', file_path.name)
        chapter_num = int(chapter_match.group(1)) if chapter_match else 1
        
        # Ler arquivo
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Aplicar formatação ABNT
        formatted_content = format_markdown_abnt(content, chapter_num)
        
        # Salvar arquivo formatado
        file_path.write_text(formatted_content, encoding='utf-8')
        
        print(f"✅ Formatado: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path.name}: {e}")
        return False


def main():
    """Função principal para processar todos os arquivos."""
    
    # Definir pastas
    fase1_path = Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase1")
    fase2_path = Path(r"c:\Fiap Projeto\FarmTechSolutions\documentacao\Fase2")
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
    else:
        target = 'all'
    
    folders_to_process = []
    
    if target in ('fase1', 'all'):
        folders_to_process.append(('Fase 1', fase1_path))
    
    if target in ('fase2', 'all'):
        folders_to_process.append(('Fase 2', fase2_path))
    
    # Processar arquivos
    total_processed = 0
    total_success = 0
    
    for folder_name, folder_path in folders_to_process:
        if not folder_path.exists():
            print(f"⚠️  Pasta não encontrada: {folder_path}")
            continue
            
        print(f"\n📁 Processando {folder_name}: {folder_path}")
        
        # Buscar arquivos .md
        md_files = sorted(folder_path.glob("*.md"))
        
        for md_file in md_files:
            total_processed += 1
            if process_markdown_file(md_file):
                total_success += 1
    
    print(f"\n📊 Resumo:")
    print(f"   Arquivos processados: {total_processed}")
    print(f"   Sucessos: {total_success}")
    print(f"   Erros: {total_processed - total_success}")
    
    if total_success > 0:
        print(f"\n🎉 Formatação ABNT aplicada com sucesso!")
    

if __name__ == "__main__":
    main()
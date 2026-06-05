<#
PowerShell helper script with step-by-step commands to create a public GitHub repository and push this project.

Requirements:
- git installed and configured (git config user.name / user.email)
- gh (GitHub CLI) installed and authenticated (run: gh auth login)
- or you can use the GitHub web UI to perform the same steps

USAGE (manual steps shown below):
1) Open PowerShell in the project root (where dashboard.py is).
2) Edit the script and set $GITHUB_ORG_OR_USER and $REPO_NAME.
3) Run commands one by one (they are safe to run interactively).

This script does NOT run network commands automatically; it's a convenience to copy/paste the commands.
#>

# === CONFIGURE these before running ===
$GITHUB_ORG_OR_USER = "<your-github-username-or-org>"   # e.g. "carloscostato-cmyk" or your org
$REPO_NAME = "fiap-farmtech-fase3"
$PUBLIC = $true  # set to $false for private

Write-Host "1) Inicializar repositório local (se ainda não houver):"
Write-Host "   git init"
Write-Host "   git add ."
Write-Host "   git commit -m \"Initial commit: project upload\""
Write-Host ""

Write-Host "2) Criar repositório no GitHub (usando gh CLI):"
Write-Host "   gh repo create $GITHUB_ORG_OR_USER/$REPO_NAME --public --source=. --remote=origin --push"
Write-Host "   # Se preferir privado, substitua --public por --private"
Write-Host ""

Write-Host "3) Adicionar colaboradores (exemplo com gh api):"
Write-Host "   # adicionar 'carloscostato-cmyk' com permissão push (write):"
Write-Host "   gh api --method PUT /repos/$GITHUB_ORG_OR_USER/$REPO_NAME/collaborators/carloscostato-cmyk -f permission=push"
Write-Host "   # adicionar 'Cesar-Azeredo':"
Write-Host "   gh api --method PUT /repos/$GITHUB_ORG_OR_USER/$REPO_NAME/collaborators/Cesar-Azeredo -f permission=push"
Write-Host ""

Write-Host "4) Alternativa (web):" 
Write-Host "   - Vá para https://github.com/$GITHUB_ORG_OR_USER/$REPO_NAME/settings/access -> Collaborators and teams -> Add people"
Write-Host ""

Write-Host "NOTAS IMPORTANTES:" 
Write-Host " - Removi senhas embutidas antes de commitar (substitua por variáveis de ambiente)."
Write-Host " - Confirme que NÃO há arquivos com segredos antes de dar git push."
Write-Host " - Caso não tenha gh CLI, autentique-se no GitHub e crie o repo via https://github.com/new . Depois adicione o remote e faça push:"
Write-Host "     git remote add origin https://github.com/$GITHUB_ORG_OR_USER/$REPO_NAME.git"
Write-Host "     git branch -M main"
Write-Host "     git push -u origin main"
Write-Host ""
Write-Host "FIM. Copie/cole os comandos sugeridos para executar."

# Cap 9 - O fantástico mundo do Github

## Sumário

# Cap 9 - O fantástico mundo do Github

O fantástico mundo do GithubFigura 43–Comparando as branches no GitHubFonte: Elaborado pela autora(2022)6.

Verifique as mudanças e adicione um comentário explicando o que foi feito.7.

Clique no botão "Create pull request".

O fantástico mundo do GithubFigura 44–Criando um pull request no GitHubFonte: Elaborado pela autora(2022)Após um pull request ser aberto, a equipe responsável pelo projeto geralmente revisará  as  mudanças  propostas  e  pode  comentar  ou  pedir  correções.

Se  as mudanças  são  aprovadas,  o  administrador  do  projeto  irá  mesclar  a  branch  com  as alterações para a branch principal (geralmente a "master").

Se houver conflitos, eles precisam ser resolvidos antes da mesclagem.

O fantástico mundo do Github3.16Aprovação do Pull RequestA aprovação de um pull request pode ser feita por meio da interface do GitHub.

Ao abrir a página do pull request, você pode ver uma lista de revisões e comentários feitos por outros colaboradores.

Se tudo estiver deacordo com as expectativas e os padrões de qualidade, você pode clicar no botão "Merge Pull Request" para mesclar a branch com a branch base.

Figura 45–Aprovaçãode um pull request no GitHubFonte: Elaborado pela autora(2022)
O fantástico mundo do GithubAntes de clicar no botão, é possível escolher a forma como a mesclagem será realizada (por exemplo, se será feito um merge ou um rebase).

Depois que o merge é feito,  a  branch  original  é  excluída  e  o  histórico  de  alterações  é  adicionado  ao repositório principal.

Figura 46–Exclusão da branch no GitHubFonte: Elaborado pela autora(2022)
O fantástico mundo do GithubEm  alguns  casos,  pode  ser  necessário  fazer  mais  algumas  correções  ou ajustes antes da aprovação do pull request.

Nesses casos, é importante comentar as alterações feitas ou incluir novos commits na branch para que outros colaboradores possam ver as mudanças.

Quando tudo estiver resolvido, é só repetir o processo de aprovação.

O fantástico mundo do Github4 HANDS ON: HORA DA PRÁTICAAgora que aprendemos o funcionamento do Git e GitHub e já temos o nosso ambiente   configurado   e   funcionando,   que   tal   fazermos   alguns   exercícios   e aprendermosa lidar com algumas situações bastante comuns de versionamento?4.1 O que será que eu fiz?

Meu querido Jedi,você está trabalhando em um timee pediram para você e seu colega Obi Wan alterarem o mesmo arquivo poesia.py, mas esqueceram de avisá-los  e  você já  fez  commit  no  seu  repositório  local...  agora  é  bom  comparar  as alterações feitas por Obi Wan com as suas.

Como fazer isso?

Você pode usar o comando git fetchpara baixar as alterações feitas pelo Obi Wan ao repositório remoto, sem fazer mergecom sua branchlocal.

Em seguida, você pode usar o comando git diffpara comparar as suas alterações com as feitas por Obi Wan.git fetch origingit diff origin/master..

HEADFigura 47–Examinando as diferenças entre o repositório local e oremotoFonte: Elaborado pela autora(2022)
O fantástico mundo do GithubO comando git fetchbusca as alterações feitas na branchmaster no repositório remoto e compara-as com sua branchlocal atual (HEAD).

Você pode usar o diffpara ver as diferenças e decidir como resolvê-las(se énecessário fazer merge ou corrigir suas alterações antes de fazer o merge).4.2 Um passinho para trásC-3PO acabou de checar o seu código e recomendou você voltar a versão do seu  código  no  arquivo  poesia.py,pois  o  seu  colega  Obi  Wan  também alterou  esse arquivo e já subiu as alterações para o GitHub.

E apesar de você já ter feito o commit local, C-3PO pediu para voltar a versão que estava no repositório remoto para então fazer as alterações necessárias.

Primeiro  vamos  dar  uma  olhadinha  o  que  o  C-3PO  está  falandovendo  os arquivos local e remoto.

Figura 48–Olhando o arquivo poesia.py local e remotoFonte: Elaborado pela autora(2022)Um Jedi experiente como você vai garantir estar na branchcorreta(git checkout master)e irá “puxar” as alterações remotas (git pull origin master).

O fantástico mundo do GithubFigura 49–Puxando as alterações do repositório remotoFonte: Elaborado pela autora(2022)Note que há uma marcação de conflito.

C-3PO já estava prevendo isso!

Agora temos que abrir o arquivo e resolver o conflito manualmente.

Figura 50–Arquivo com conflito Fonte: Elaborado pela autora(2023)
O fantástico mundo do GithubSomente depois fazer o trio de comandos: git add/git commit/git push.

Observe que o arquivo media.py ainda está sendo desenvolvido na working área, e por isso é apontado como “untracked”.

Figura 51–Versão final do arquivo poesia.pyFonte: Elaborado pela autora(2023)
O fantástico mundo do Github## Referências

TORVALDS,   L.inus;  HAMANO,   Junio   C; et   al.

Documentação   do   Git.  2023.

Disponível em: <https://git-scm.com/docs/git>.

Acesso em: 12abr.2024

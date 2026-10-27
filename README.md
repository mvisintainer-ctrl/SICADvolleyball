# SICAD Volleyball para Windows

[**BAIXAR O PROGRAMA — EDIÇÃO WINDOWS 10 10240**](https://github.com/mvisintainer-ctrl/SICADvolleyball/raw/refs/heads/main/downloads/SICADvolleyball-Win10-10240.zip)

1. Baixe o ZIP e extraia em uma **pasta nova**.
2. Abra **SICADvolleyball.exe** com duplo clique.

Não precisa instalar Python nem Excel. Esta edição usa Python 3.10 e Qt 5 para atender Windows 10 de 64 bits, incluindo a compilação 10240. Substitui a edição Qt 6 anterior, cuja exigência de APIs mais recentes causava falha ao importar QtCore nesse Windows.

O pacote público começa sem dados pessoais. Use Novo atleta para criar cadastros de teste. Os dados inseridos ficam no seu computador.

Os seis testes passaram com o novo runtime, e o executável abriu sob Wine 8, com zero cadastros, e encerrou sem erro. Foram verificadas as 79 DLLs/extensões empacotadas quanto às importações diretas das APIs mais recentes listadas no relatório. O teste final em Windows 10 10240 real e a impressora física continuam pendentes, assim como os ajustes visuais e dos desenhos no PDF.

Se houver falha na inicialização, o programa mostra a localização do relatório `erro-inicializacao.txt`.

[Instruções e código-fonte](programa/README.md).

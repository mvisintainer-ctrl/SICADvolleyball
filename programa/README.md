# SICAD Volleyball — versão pública de teste

Programa Windows 10 de 64 bits, incluindo a compilação 10240, independente de Excel e Python no computador que executa o aplicativo.

## Baixar e abrir

Baixe `downloads/SICADvolleyball-Win10-10240.zip`, extraia o ZIP e abra **SICADvolleyball.exe** com duplo clique. Este pacote começa **sem cadastros pessoais**. Use Novo atleta para criar dados de teste.

As telas incluem Cadastro, Ficha, Dados e Pagamentos. Cadastro tem seções Pessoais, Adicionais e Formação; Pagamentos tem Mirim, Infantil e Infanto-juvenil. A pesquisa aceita nome, código, categoria ou posição. Há seleção de foto, geração de PDF e backup local.

Os dados de teste ficam na pasta AppLocalDataLocation do Qt, em `SICAD/SICADvolleyballTeste/sicad.sqlite3`, normalmente em `%LOCALAPPDATA%`. A edição não altera o modelo Excel. Novas fotos são guardadas no banco local.

Esta é uma versão para avaliação. A aparência e os desenhos do PDF ainda precisam de ajustes. A impressora física e o funcionamento em um computador Windows real ainda precisam ser conferidos. O `.exe` foi compilado com Python Windows sob Wine; o relatório do pacote descreve a validação realizada. Não há suporte geral a novas fórmulas Excel.

## Recompilar

Instale Python 3.10 de 64 bits no Windows e abra `build-windows.bat`. O executável será gerado em `dist/SICADvolleyball.exe`.

## Desenvolver e testar

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
QT_QPA_PLATFORM=offscreen .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m app.main
```

No Windows, use `.venv\Scripts\python.exe` no lugar de `.venv/bin/python`.

O modelo `assets/template.xlsx` foi reconstruído sem os cadastros, preenchimentos pessoais, pagamentos preenchidos, VBA, ActiveX, comentários ou vínculos externos. Foram preservados rótulos genéricos, estilos, geometria das telas e imagens de interface revisadas. A planilha original não faz parte deste pacote.

Python: PSF; openpyxl: MIT; PySide2, Qt 5 e Shiboken2: LGPL v3. Fontes Qt: https://code.qt.io/qt/qtbase.git/tag/?h=v5.15.2 e PySide6: https://code.qt.io/pyside/pyside-setup.git/tag/?h=v5.15.2.

## Compatibilidade com Windows 10 10240

Esta edição usa Python 3.10.11 e Qt 5.15.2/PySide2 5.15.2.1. A edição anterior com Qt 6.8 exigia APIs ausentes nessa compilação, incluindo a importação direta de `SetThreadDescription`. A nova edição usa Qt 5 e inclui as DLLs do runtime C++ ao lado do próprio runtime Python.

Se a abertura falhar, o iniciador salva um relatório `erro-inicializacao.txt` em `SICAD/SICADvolleyballTeste` na pasta de dados local do usuário e mostra sua localização. A validação sob Wine não substitui o teste em um Windows físico com compilação 10240.

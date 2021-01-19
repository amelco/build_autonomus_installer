# Script de construção do instalador do autonomus

Com a finalidade de agilizar o processo de *deploy* do Autonomus, um script para a construção
do instalador para Windows foi criado.

Este documento possui as informações necessárias à sua execução e apresenta uma visão geral de seu funcionamento.

Enviar dúvidas para: amelco.herman@gmail.com

## Conteúdo

O Script consiste em 2 arquivos e um diretório, organizados na seguinte estrutura:

```
. 
|--/needed_files/
|--build-win.py
|--make-installer.nsi
```

`needed_files/` é o diretório em que se encontra os arquivos necessários ao instalador que são
externos aos repositórios. Por exemplo, o pacote `VC_Redist`, ícone do programa, o socket e
o script de inicialização do autonomus.

`build-win.py` é o script que automatiza todo o processo, desde a atualização dos repositórios até
a execução do script do instalador (`make-installer.nsi`)

`make-installer.nsi` é o script do programa NSIS que gera um instalador para o Windows.


## Utilização

Execute na linha de comando do windows, dentro do diretório onde está o script: `python build-win.py`

OBS.: Não é necessário criar um ambiente virtual.


## Requisitos

- python
- node
- npm
- NSIS [https://nsis.sourceforge.io/Download]


## Funcionamento

O script irá verificar a existência dos repositórios necessários à construção do instalador no
diretório corrente. Caso não exista (primeira execução), irá ser criado e atualizado. Caso os
repositórios existam, serão atualizados.

A atualização dos repositórios são feitas na `branch dev`.

Os ambientes virtuais necessários (nos casos dos códigos em python) serão automaticamente criados
e todas as dependências serão baixadas. De forma análoga, todas as dependências dos códigos em 
javascript que utilizam o node, também serão baixadas.

Em seguida são executadas as builds de cada repositório, front-end e back-end. Todas as modificações
necessárias (manipulação/modificação de arquivos) também são realizadas.

Com as builds prontas, o script do instalador NSIS é executado. Ele irá gerar um arquivo único
executável de instalação (`autonomus-installer.exe`) já comprimido. É esse arquivo que deverá ser
distribuído ao público.

## Executando o instalador

O instalador deve ser executado aceitando todas as opções padrão. O autonomus e os componentes necessários
à sua execução (`VC_Redist`) serão instalados.

Após a instalação, oitem `LAIS` irá aparecer no menu iniciar contendo o script de execução do autonomus.
Para iniciar o autonomus, o socket e o back-end, basta clicar nesse ícone.

## TODO

[ ] Econtrar uma forma de unificar a incialização do autonomus, socket e back-end, em uma única janela.
[ ] Implementar a desinstalação completa do autonomus.

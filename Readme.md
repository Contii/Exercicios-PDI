# Projeto de Processamento de Imagens e Reconhecimento de Padrões

Este repositório contém os projetos e atividades desenvolvidos na disciplina de Processamento de Imagens e Reconhecimento de Padrões do curso de Ciência da Computação da UTFPR campus Medianeira.

## Funcionamento.
O script da pasta raiz contém um menu para navegar entre os scripts das pastas.

Todas as imagens e vídeos manipulados estão na pasta Media.

Cada pasta possui uma breve descrição sobre o que seus scripts fazem.


## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes requisitos instalados:

- Python 3.x: [Download Python](https://www.python.org/downloads/)

- OpenCV: [OpenCV](https://opencv.org/)
<sub>Voce pode optar por baixar o opencv diretamente com o arquivo requirements.txt</sub>

## Instalação

#### Crie um ambiente virtual
Usando a ferramenta `virtualenv` ou `venv`. (a sintaxe pode variar dependendo do sistema operacional):

`python -m venv myenv`

#### Ative o ambiente virtual:
A ativação depende do sistema operacional. No Windows, o comando é:

`myenv\Scripts\activate`

<sub>No Linux ou macOS:</sub>
 `source myenv/bin/activate`
 
 #### Instalar as bibliotecas:
 
execute o seguinte comando no terminal bash:

`pip install  -r  requirements.txt`

Se necessário  executar  o  Activate.ps1  na  pasta  Scripts,  talvez  seja  preciso  desativar  a  seguranca  do  PoweShell.

`Get-ExecutionPolicy`
`Set-ExecutionPolicy RemoteSigned`

<sub>isso afeta  a  seguranca  do  SO,  então  lembre-se  de  reativa-lo  depois  de  terminar.</sub>

`Set-ExecutionPolicy Restricted`


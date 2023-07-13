# PowerDNS Reverse Zone Generator

Esse script Python foi criado para auxiliar na geração de registros de DNS reverso para blocos CIDR no PowerDNS. É especialmente útil para administradores de sistemas que precisam automatizar essa tarefa.

## Requisitos

- Python 3.6+
- PowerDNS com um banco de dados MySQL

## Dependências

Este projeto depende dos seguintes pacotes Python:

- mysql-connector-python
- python-dotenv
- netaddr

Essas dependências podem ser instaladas com o comando pip abaixo:

```bash
pip install -r requirements.txt
```

## Como usar

Primeiramente, você deve clonar este repositório em seu computador local. Use o comando a seguir para fazer isso:

```bash

git clone https://github.com/seu_usuario/powerdns_reverse_generate.git
```
Entre no diretório do projeto:
```
bash

cd powerdns_reverse_generate
```
Crie um ambiente virtual Python (isso isola as dependências do projeto):

```bash

python -m venv venv
```
Ative o ambiente virtual:

```bash

# Para Windows Power Shell
.\venv\Scripts\Activate.ps1

# Para Windows Command Shell
.\venv\Scripts\Activate.bat

# Para Mac ou Linux
source venv/bin/activate
```
Instale as dependências:

```bash

pip install -r requirements.txt

```
## Executar

Agora você pode executar o script. Substitua "XXX.XXX.XXX.XXX/CDR" pelo bloco CIDR para o qual você deseja criar registros de DNS reverso:

```bash

python main.py XXX.XXX.XXX.XXX/CDR

```

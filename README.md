# Projeto Interdisciplinar III - Sistemas de Informação ESPM

<p align="center">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

# Sistema de Controle de Dispensa

### 2025-01

## Integrantes
- [Arthur Borba](https://github.com/Borba70)
- [Enrico Comassetto Di Gioia](https://github.com/EnricoDiGioia)
- [Ana Carolina Albi Pereira](https://github.com/anacarolinaalbi)

## Descrição do Projeto

A solução gira em torno de utilizar sensores de presença para verificar a disponibilidade de leitos em hospitais e fazer um mapa de calor por especialidade, transmitindo as informações para ambulâncias com o objetivo de diminuir o tempo em que os pacientes serão atendidos.

É exibido como um mapa de calor para o motorista, facilitando a localização do hospital com a especialidade necessária de forma mais ágil, eficiente e com menor tempo de espera.

## Configuração do Projeto

Para executar, deve criar o arquivo `config.py` da seguinte forma:

```python
host = '0.0.0.0'
port = 3000
conexao_banco = 'mysql+mysqlconnector://usuario:senha@host/banco'
url_api = 'https://site.com'
```

Todos os comandos abaixo assumem que o terminal esteja com o diretório atual na raiz do projeto.

## Criação e Ativação do venv

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```
.venv\Scripts\activate
python app.py
```

## Mais Informações

https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/

# Licença

Este projeto é licenciado sob a [MIT License](https://github.com/tech-espm/inter-3sem-healthgrid/blob/main/LICENSE).

<p align="right">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo-si-512.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

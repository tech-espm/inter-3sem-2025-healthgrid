# Vamos utilizar o pacote SQLAlchemy para acesso a banco de dados:
# https://docs.sqlalchemy.org
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install SQLAlchemy
#
# Além disso, o SQLAlchemy precisa de um driver do conexão ao banco. Isso depende do servidor
# (MySQL, Postgres, SQL Server, Oracle...) e do driver real. Vamos utilizar o driver MySQL-Connector,
# que também precisa ser instalado (de preferência com o VS Code fechado):
# python -m pip install mysql-connector-python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco

# Como criar uma comunicação com o banco de dados:
# https://docs.sqlalchemy.org/en/14/core/engines.html
#
# Detalhes específicos ao MySQL
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
#
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine(conexao_banco)

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

def listarPessoas():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, nome, email) in pessoas:
			print(f'\nid: {id} / nome: {nome} / email: {email}')

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def obterPessoa(id):
	with Session(engine) as sessao:
		parametros = {
			'id': id
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		pessoa = sessao.execute(text("SELECT id, nome, email FROM pessoa WHERE id = :id"), parametros).first()

		if pessoa == None:
			print('Pessoa não encontrada!')
		else:
			print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def criarPessoa(nome, email):
	# É importante utilizar o método begin() para que a sessão seja comitada
	# automaticamente ao final, caso não ocorra uma exceção!
	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
	# e nenhuma alteração será persistida. Para mais informações de como explicitar
	# esse processo de commit() e rollback():
	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
	with Session(engine) as sessao, sessao.begin():
		pessoa = {
			'nome': nome,
			'email': email
		}

		sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), pessoa)

		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
		# é passar uma lista como segundo parâmetro:
		# lista = [ ... ]
		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)

def obterDadosHeatmap():
    with Session(engine) as sessao:
        # Agrupa pessoas por primeira letra do nome para simular setores
        dados = sessao.execute(text("""
            SELECT 
                LEFT(nome, 1) as setor,
                COUNT(*) as ocupacao
            FROM pessoa
            GROUP BY LEFT(nome, 1)
            ORDER BY LEFT(nome, 1)
        """))
        
        resultado = []
        for row in dados:
            resultado.append({
                'setor': row.setor,
                'ocupacao': row.ocupacao,
                'capacidade': 10,  # capacidade fixa para exemplo
                'taxa_ocupacao': float(row.ocupacao * 10)  # multiplica por 10 para ter percentual
            })
        return resultado

def obterEstatisticasGerais():
    with Session(engine) as sessao:
        # Obtém estatísticas da tabela pessoa
        dados = sessao.execute(text("""
            SELECT 
                COUNT(*) as total_pessoas,
                COUNT(DISTINCT email) as emails_unicos
            FROM pessoa
        """))
        
        row = dados.first()
        return {
            'total_internados': row.total_pessoas,
            'atendimentos_hoje': row.emails_unicos,
            'tempo_medio_atendimento': 30.5  # valor fixo para exemplo
        }

def obterOcupacaoUltimos7Dias():
    with Session(engine) as sessao:
        # Simula dados de ocupação usando o ID das pessoas
        dados = sessao.execute(text("""
            SELECT 
                id % 7 as dia_id,
                COUNT(*) as total
            FROM pessoa
            GROUP BY id % 7
            ORDER BY dia_id
        """))
        
        # Dias da semana para exemplo
        dias = ['19/04', '20/04', '21/04', '22/04', '23/04', '24/04', '25/04']
        
        resultado = []
        for row in dados:
            resultado.append({
                'dia': dias[row.dia_id],
                'ocupacao': row.total
            })
        return resultado

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html

from flask import g, session, request, redirect, url_for, render_template
import psycopg2, psycopg2.extras

from random import randint,shuffle
import datetime

from perguntados import app

global partidas
partidas = []


@app.before_request
def before_request():
   g.db = psycopg2.connect(host='localhost', database='perguntados',user='postgres', password='klinsman')

# Disconnect database
@app.teardown_request
def teardown_request(exception):
    g.db.close()


def write_submit_data(data1, data2, data3):
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "insert into %s (username, email, senha) values ('%s', '%s', '%s');" % ("jogador", data1, data2, data3)
	cur.execute(sql)
	g.db.commit()
	cur.close()

def read_database(term, table):
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "select %s from %s;" % (term, table)
	cur.execute(sql)
	data = cur.fetchall()
	cur.close()
	return data
def user_id(name):
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "select player from jogador where username = '%s';" % (name)
	cur.execute(sql)
	data = cur.fetchall()
	cur.close()
	for x in data:
		for y in x:
			return y
def read_player2():
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "SELECT player2 from partidas where player1 = " + str(session['id']) + ";"
	cur.execute(sql)
	data = cur.fetchall()
	for x in data:
		for y in x:
			return y
	cur.close()

def read_data_partida():
	dados = []
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "SELECT * from partidas where id = " + str(session['idPartida']) + ";"
	cur.execute(sql)
	data = cur.fetchall()
	for x in data:
		for y in x:
			dados.append(y)
	return dados

def read_data_pergunta(idd):
	dados = []
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "SELECT * from perguntas where id = " + str(idd) + ";"
	cur.execute(sql)
	data = cur.fetchall()
	for x in data:
		for y in x:
			dados.append(y)
	
	return dados

def read_player_name(idd):
	cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	sql = "SELECT username from jogador where player = " + str(idd) + ";"
	cur.execute(sql)
	data = cur.fetchall()
	for x in data:
		for y in x:
			return y



@app.route('/', methods=['POST','GET'])
def index():		
		#verifica se o usuario está logado no sistema se sim ele redireciona para o painel
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		return redirect(url_for('painel'))


	
@app.route('/login', methods=['POST','GET'])
def login():

	if request.method == 'POST':
		#faz login no sistema
		if (request.form['submit'] == "b1"):
			login = False
			senha = False
			for x in read_database("username", "jogador"):
				for y in x:
					if(request.form['UserName'] == y):
						login = True

			for x in read_database("senha", "jogador"):
				for y in x:
					if(request.form['senha'] == y):
						senha = True

			if(login == True and senha == True):
				session['username'] = request.form['UserName']
				session['logged_in'] = True
				session['id'] = user_id(request.form['UserName'])
				session['inPartida'] = False
				session['idPartida'] = None
				session['respondidas'] = ["index", "index","index","index","index"]
				session['count'] = 0
				session['pontos'] = 0
				session['correta'] = None
				return redirect(url_for('painel'))

			elif(login == False and senha == False):
				return render_template('index.html', error=True, error2=True)

			elif(senha == False):
				return render_template('index.html', error2=True, name=request.form['UserName'])

			elif(login == False):
				return render_template('index.html', error=True)
		
		if (request.form['submit'] == "b2"):
			return redirect(url_for('cadastro'))

	else:
		return render_template('index.html', senha = True, login = True)

@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
	if(request.method == "POST"):
		if (request.form['submit'] == 'b2'):

			write_submit_data(request.form['nome'], request.form['email'],request.form['senha'])
			
			return render_template('listagem/painel.html', text=request.form['nome'])
	else:
		return render_template('cadastro/cadastro.html')

@app.route('/painel', methods=['POST','GET'])
def painel():

	if not session.get('logged_in'):
		return redirect(url_for('index'))
	else:
		vencedor = ""
		if(len(partidas) > 0):
			print(session['idPartida'])
			if(session['idPartida']):
				dados = read_data_partida()
				print(dados)
				if(len(dados) >= 6):
					if(dados[4] == None and dados[5] != None and dados[6] != None):

						if(dados[5] > dados[6]):
							vencedor = read_player_name(dados[2])
						elif(dados[5] < dados[6]):
							vencedor = read_player_name(dados[3])
						else:
							vencedor = 'Empate'

			return render_template('listagem/painel.html', vencedor=vencedor, text=session['username'], partida= partidas, id=session['id'])

		else:
			return render_template('listagem/painel.html', text=session['username'])



@app.route('/criar_pergunta', methods=['POST','GET'])
def criar_pergunta():
	if not session.get('logged_in'):
		return redirect(url_for('index'))

	else:
		#cadastra perguntas novas
		if(request.method == "POST"):
			pergunta = request.form['pergunta']
			categoria = int(request.form['categoria'])
			resp1 = request.form['resp1']
			resp2 = request.form['resp2']
			resp3 = request.form['resp3']
			respC = request.form['respC']

			cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
			sql = "insert into perguntas (pergunta,  resposta1,  resposta2,  resposta3, correta, categoria) values ('%s', '%s', '%s','%s', '%s', %i);" % (pergunta, resp1, resp2, resp3, respC, categoria)
			cur.execute(sql)
			g.db.commit()
			cur.close()

			return redirect(url_for('painel'))	

		else:
			return render_template('partida/criar_pergunta.html')

@app.route('/criar_partida', methods=['POST','GET'])
def criar_partida():
	if not session.get('logged_in'):
		return redirect(url_for('index'))

	else:
		if(request.method == 'POST'):
			if (request.form['apagar'] == "d"):
				if(len(partidas) > 0):
					count = 0
					for x in partidas:
						if(x[0] == session['username']):
							partidas.pop(count)
						count+=1
				cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
				sql = "delete from partidas where player1 = '%i';" % (session['id'])
				cur.execute(sql)
				g.db.commit()
				cur.close()
	

				return redirect(url_for('painel'))
	
		else:
			if(session['username'] in partidas):
				return redirect(url_for('painel'))
			else:
				jogo = [session['username'], session['id']]
				partidas.append(jogo)
				cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
				sql = "insert into partidas (player1) values ('%i');" % (session['id'])
				cur.execute(sql)
				g.db.commit()
				cur.close()
				return redirect(url_for('painel'))


@app.route('/logout', methods=['POST','GET'])
def logout():
   session['logged_in'] = False
   session ['inPartida'] = False
   session['id'] = None
   session['respondidas'] = ["index", "index","index","index","index"]
   session['correta'] = None
   session['count'] = 0
   session['pontos'] = 0
   return redirect(url_for('index'))


@app.route('/partidaoff', methods=['POST','GET'])
def partidaoff():
	if(request.method == 'POST'):
		session['inPartida'] = False
		session['idPartida'] = None
		session['respondidas'] = ["index", "index","index","index","index"]
		session['count'] = 0
		session['pontos'] = 0
		session['correta'] = None
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		sql = "UPDATE partidas SET player2 = NULL"  + " WHERE player2 = " + str(session['id']) + ";"
		cur.execute(sql)
		g.db.commit()
		cur.close()

	return redirect(url_for('painel'))


@app.route('/partida', methods=['POST','GET'])
def partida():
	if not session.get('logged_in'):
		return render_template('index.html')
	else:

		for x in read_database('player1', 'partidas'):
			for y in x:
				if(session['id'] == y):
					if (read_player2() != None):
						cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
						sql = "SELECT id from partidas where player1 = " + str(session['id']) + ";"
						cur.execute(sql)
						data = cur.fetchall()
						cur.close()
						for x in data:
							for y in x:
								session['idPartida'] = y
						session['inPartida'] = True
						return redirect(url_for('jogar'))

					return redirect(url_for('painel'))

		

		if(session['inPartida']):
			cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
			sql = "SELECT * from partidas where player2 = " + str(session['id']) + ";"
			cur.execute(sql)
			data = cur.fetchall()
			#print(data)
			cur.close()
			return redirect(url_for('jogar'))


		else:	
			for x in read_database('player1', 'partidas'):
				for y in x:
					if(session['id'] != y):
						cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
						sql = "UPDATE partidas SET player2 = " + str(session['id']) + " WHERE player1 = " + str(request.form['submit']) + ";"
						cur.execute(sql)
						g.db.commit()

						sql = "SELECT id from partidas where player2 = " + str(session['id']) + ";"
						cur.execute(sql)
						data = cur.fetchall()
						cur.close()
						for x in data:
							for y in x:
								session['idPartida'] = y

						session['inPartida'] = True
						return redirect(url_for('jogar'))
						
		
		return redirect(url_for('painel'))



@app.route('/jogar', methods=['POST','GET'])
def jogar():
	if(request.method == 'POST'):
		if(session['correta'].startswith(request.form['submit'])):
			if(read_player2() == None):
				print('ponto2')
				session['pontos']+=1
				cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
				sql = "UPDATE partidas SET pontos2 = " + str(session['pontos']) + " WHERE id = " + str(session['idPartida']) + ";"
				cur.execute(sql)
				g.db.commit()
				cur.close()
			elif(read_player2() != session['id']):
				print('ponto1')
				session['pontos']+=1
				cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
				sql = "UPDATE partidas SET pontos1 = " + str(session['pontos']) + " WHERE id = " + str(session['idPartida']) + ";"
				cur.execute(sql)
				g.db.commit()
				cur.close()
		
		return redirect(url_for('jogar'))

	if(session['inPartida']):
		perguntas = []
		atual = None
		for x in read_database('id', 'perguntas'):
			for y in x:
				perguntas.append(y)


		shuffle(perguntas)

		
		for x in perguntas:
			if(x in session['respondidas']):
				pass
			elif(session['count'] <= 4):
				atual = x 
				session['respondidas'][session['count']] = x
				session['count']+=1
				break
			else:
				session['respondidas'] = ["index", "index","index","index","index"]
				session['inPartida'] = False
				return redirect(url_for('partidaoff'))
		print(session['respondidas'])	


###########################################################################################
		dados = read_data_partida()

		if(dados[5] == None):
			dados[5] = 0

		if(dados[6] == None):
			dados[6] = 0

		
		cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
		sql = "SELECT UserName from jogador where player= " + str(dados[2]) + ";"
		cur.execute(sql)
		data = cur.fetchall()
		for x in data:
			for y in x:
				name2 = y
		
		sql = "SELECT UserName from jogador where player= " + str(dados[3]) + ";"
		cur.execute(sql)
		data = cur.fetchall()
		for x in data:
			for y in x:
				name1 = y
		cur.close()
		#############################################################################3
		#ler pergunta
		perguntaData = read_data_pergunta(atual)
		session['correta'] = perguntaData[5]
		alternativas = []
		alternativas.append(perguntaData[2])
		alternativas.append(perguntaData[3])
		alternativas.append(perguntaData[4])
		alternativas.append(perguntaData[5])
		shuffle(alternativas)

		return render_template('partida/jogadas.html', pergunta=perguntaData[1], player1=name2 ,player2=name1,pontos1=dados[5],pontos2=dados[6], opcoes=alternativas)
	
	return redirect(url_for('painel'))
				
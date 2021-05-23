from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory
from flask_socketio import SocketIO, emit
import json
from dbmanager import dbexec, dbset
import time

dbset = "chat" #Définition du nom de la db, voir le fichier dbmanager.py

def logChatData(args):
	dbexec(f"INSERT INTO chat VALUES(?, ?, ?)", args, fetch=False)
#Création de la db initiale
try:
	dbexec("""CREATE TABLE chat(
		time INT,
		user TEXT,
		message TEXT
		)""")
except:
	print('err')

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/assets/<path:path>')
def send_static(path):
	return send_from_directory('assets', path)

@app.route('/', methods=["GET"])
def mainpge():
	#Test pour voir si le nom à été défini
	if not request.cookies.get('userID'):
		return render_template('setnom.html') #Si non, on renvoie le client sur la page de création
	else:
		data = dbexec("SELECT * FROM chat", mult=True) #On tire tous les messages de la db
		return render_template('main.html', data=data) #Render avec la data sous forme de liste avec tes tuples>> [(),(),()]

#Envoi d'un message
@app.route('/chatpost', methods=["POST"])
def chatpost():
	if(request.form['message']==""): #On ignore is le message est vide
		return
	else: #Sinon on l'injecte dans la db et on recharge la page pour l'afficher
		logChatData([time.time(), request.cookies.get('userID'), request.form['message']])
		return redirect(url_for('mainpge'))

@app.route('/setcookiepost', methods=['POST'])
def setcookie(): #Définition du nom d'utilisateur
	user = request.form['value']
	resp = make_response(redirect(url_for('mainpge'))) #Redirection sur la page main
	resp.set_cookie('userID', user) #Définition du cookie
	return resp

@socketio.on('connect')
def connecthandl():
	print(f'a client connected: {request.cookies.get("userID")}')
	emit('connectserv', {"data": request.cookies.get('userID')}, broadcast=True)

@socketio.on('disconnect')
def disconnecthandl():
	print(f'a client disconnected: {request.cookies.get("userID")}')
	emit('disconnectserv', {"data": request.cookies.get('userID')}, broadcast=True)

@socketio.on('chat message')
def handle_chat(data):
	print(f'rcv msg, data : {data}')
	data['time'] = time.time()
	logChatData([data['time'], data['user'], data['data']])

	emit('response', data, broadcast=True)
	print('Response emited')

socketio.run(app, host='0.0.0.0', port=8080, debug=True, use_reloader=True)
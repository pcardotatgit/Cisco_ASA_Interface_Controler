# -*- coding: UTF-8 -*-
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
import sqlite3
from netmiko import ConnectHandler
import sys
engine = create_engine('sqlite:///users.db', echo=True)

def select_device(name):
	device=[]
	with sqlite3.connect("devices.db") as conn:
		cursor=conn.cursor()
		sql_request = "SELECT * from devices where name = '" + name +"'"
		cursor.execute(sql_request)		
		for resultat in cursor:
			#print(resultat)		
			device = {
				'device_type': resultat[1],
				'ip': resultat[3],
				'username': resultat[4],
				'password': resultat[5]
			} 				
	return(device)
	
def connect(device,command):
	#connection a l ASA
	#print (device)
	net_connect = ConnectHandler(**device)
	net_connect.find_prompt()
	output = net_connect.send_command(command)
	#print (output)
	return(output)	
	

def creer_csv_loop_on(texte,a,mots1:list,mots2:list,start,end,parse_first_line,colomn:list):
	#	a =	separator
	# 	colomn  =	colomns to keep  if =[0]  keep all colomns
	#	mots1 = 	list of words to find in the line we want to keep
	# 	mots2 =	list of words to not find in the line we want to keep. if one wor is found then the line is not kept
	#	start 	=	if the line begins with with this word then start to keep lines  until the end word is found
	#	parse_first_line = 1 if we want to parse the first kept line  and = 0 if we don't want
	lignes = texte.split('\n')
	commencer=0
	output=""
	for ligne in lignes:
		if ligne.find(start) >= 0:
			commencer=1
			if parse_first_line ==1:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 0:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')		
						# REMPLACEMENT de CARACTERES FIN		
						x = x + ';'
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")	
				x = x + "\r\n"
				output=output + x
				#fa.write('\n')				
		if ligne.find(end) >= 0:
			commencer=0
			x = x + "\r\n"
			output=output + x
			#fa.write('\n')
		if commencer:
			if mots1[0] != 'ALLWORDS':
				OK=0
				for x in mots1:
					if x in ligne:
						OK=1
			else:
				OK=1					
			for x in mots2:
				if x in ligne:
					OK=0	
			if OK:
				i1=1
				while i1 != 0:		
					ligne=ligne.replace('  ',' ')
					if ligne.find("  ") >= 0:
						ligne=ligne.replace("  "," ")
						i1=1
					else :
						i1=0				
				tableau=ligne.split(a)
				#i2=i2
				i2=1
				for x in tableau:
					x=x.strip()
					if i2 in colomn:
						OK2=1
					else:
						OK2=0
					if colomn[0] == 0:
						OK2=1
					if x !='' and OK2:
						# REMPLACEMENT de CARACTERES DEBUT
						x=x.replace('"','')
						x=x.replace(',','')
						# REMPLACEMENT de CARACTERES FIN
						x = x + ';'
						output=output + x
						#fa.write(x)
						#fa.write(';')
					i2=i2+1
				#print ("=====")
				#fa.write('\n')
		
	return(output)	
 
app = Flask(__name__)
 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('welcome.html',USERNAME=session['user'])
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		session['logged_in'] = True
		session['user'] = POST_USERNAME
	else:
		flash('wrong password!')
	return home()
	
	
@app.route("/logout")
def logout():
	session['logged_in'] = False
	return home()	
	
@app.route('/test', methods=['GET'])
def test():
	if session['user']== "patrick":
		return render_template('test.html')	
	else:
		return render_template('deny.html',USERNAME=session['user'])
		
@app.route('/devices')
def devices_list():
	if session['logged_in'] == True and session['user']== "patrick":
		device=[]
		with sqlite3.connect("devices.db") as conn:
			cursor=conn.cursor()
			sql_request = "SELECT * from devices"
			cursor.execute(sql_request)	
			devices=[]
			for resultat in cursor:
				#print(resultat)	
				device = {
					'index': resultat[0],
					'device_type': resultat[1],
					'name': resultat[2],
					'ip': resultat[3],
					'username': resultat[4],
					'password': resultat[5],
					'status': resultat[6]
				}
				devices.append(device)	
			ligne_out=""
			for equipement in devices:
				ligne_out=ligne_out+"<h3>"+equipement['ip']+"</h3>"
		return render_template('devices.html',equipts=devices)
	else:
		return render_template('deny.html',USERNAME=session['user'])		
 
@app.route('/interfaces/<name>')
def interfaces_list(name): 
	device = select_device(name)
	net_connect = ConnectHandler(**device)
	net_connect.find_prompt()
	output = net_connect.send_command("show interface")
		
	# creer une liste de chaine de caractères qui correspondent à des lignes qu'on va conserver si la chaine existe dedans
	mots_ok=['Interface','MAC address','IP address','1 minute input rate','5 minute input rate']
	#  creer une liste de chaine de caractères qui correspondent à des lignes QU'ON NE VA PAS conserver si la chaine existe dedans. Et ce contrôle arrivera avant le contrôle précédent
	mots_nok=['*****','*****']
	colonnes=[0]
	#colonnes=[0,1,2]
	# Puis on définit le mot qui nous permet d'identifier un début de groupe ( dans notre exemple tous les groupes seront les interfaces )
	mot_debut_de_groupe = "Interface"  # le mot contenu dans la ligne qui nous permet d'identifier la premiere ligne du groupe. toutes les lignes qui la suivent seront conservées selon les listes mots_ok et mots_nok
	# Puis on définit le mot qui nous permet d'identifier la fin du groupe 
	mot_fin_de_groupe = "5 minute drop rate"
	result = creer_csv_loop_on(output,',',mots_ok,mots_nok,mot_debut_de_groupe,mot_fin_de_groupe,0,colonnes)
	result=result.replace("Interface","<br>&Interface")
	result=result.replace("\r\n\r\n","<br>")
	result=result.replace("MAC address ","")
	result=result.replace("IP address ","")
	result=result.replace("line protocol is ","")
	result=result.replace("is ","")
	result=result.replace("subnet mask ","")
	result=result.replace("1 minute","<br>1 minute")
	
	lignes = result.split('<br>')
	interfaces=[]
	for ligne in lignes:
		if len(ligne) > 5:
			if(ligne.find('input')<0):
				mots = ligne.split(";")
				motsB = mots[0].split(" ")
				interface ={
					'interface': motsB[1],
					'name':motsB[2],
					'state':mots[1],
					'line_protocol':mots[2],
					'mac':mots[3],
					'ip':mots[5],
					'mask':mots[6]
				}
				interfaces.append(interface)
	return render_template('interfaces.html',interfaces=interfaces,device_name=name)
	
@app.route('/interface_up/<device_name>/<name>/<number>')
def interface_up(name,number,device_name): 	
	device = select_device(device_name)
	net_connect = ConnectHandler(**device)
	net_connect.find_prompt()
	command1="interface "+ name +'/'+number
	command2="no shutdown"
	config_commands = [command1,command2] 
	output = net_connect.send_config_set(config_commands)
	return redirect(url_for('interfaces_list',name=device_name))
	
@app.route('/interface_down/<device_name>/<name>/<number>')
def interface_down(name,number,device_name): 	
	device = select_device(device_name)
	net_connect = ConnectHandler(**device)
	net_connect.find_prompt()
	command1="interface "+ name +'/'+number
	command2="shutdown"
	config_commands = [command1,command2] 
	output = net_connect.send_config_set(config_commands)
	new_url='/interfaces/'+device_name
	return redirect(url_for('interfaces_list',name=device_name))
	
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)
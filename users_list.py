# -*- coding: UTF-8 -*-
import sys
import sqlite3
users=[]
with sqlite3.connect("users.db") as conn:
	cursor=conn.cursor()
	sql_request = "SELECT * from users"
	cursor.execute(sql_request)	
	user=[]
	for resultat in cursor:
		#print(resultat)	
		user = {
			'name': resultat[1],
			'password': resultat[2]
		}
		users.append(user)
	for administrator in users:
		print(administrator)	

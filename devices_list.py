# -*- coding: UTF-8 -*-
import sys
import sqlite3
device=[]
with sqlite3.connect("devices.db") as conn:
	cursor=conn.cursor()
	sql_request = "SELECT * from devices"
	cursor.execute(sql_request)	
	devices=[]
	for resultat in cursor:
		#print(resultat)	
		device = {
			'device_type': resultat[1],
			'name': resultat[2],
			'ip': resultat[3],
			'username': resultat[4],
			'password': resultat[5],
			'status': resultat[6]
		}
		devices.append(device)
	for equipement in devices:
		print(equipement)	

import sqlite3

def ouvrir_connexion():
	cnx = None
	try:
		cnx = sqlite3.connect('projet/db/base.db')
	except BaseException as e:
		print(e)
	return cnx
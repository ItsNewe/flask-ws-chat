import sqlite3
from sqlite3 import Error
dbset=None
# query=la requête,
# arg=arguments évnetuels, défaut: aucun
# fetch=si la requête doit retourner une valeur ou non, défaut: oui
# db= Nom du fichier de la base de données
def dbexec(query, arg=None, fetch=True, db=dbset, mult=False):
	try:
		conn = sqlite3.connect('{}.db'.format(db))
		c = conn.cursor()

		if arg:
			c.execute(query, arg)
		else:
			c.execute(query)

		if fetch:
			if mult:
				az=c.fetchall()
			else:
				az = c.fetchone()

			conn.commit()
			conn.close()
			if az!=None and az[0]:
				return(az)
			else:
				return False
		conn.commit()

	except Exception as e:
		print("\033[91mUne erreur est survenue pendant la gestion de la requête SQL: {}\033[0m".format(e))

	finally:
		conn.close()
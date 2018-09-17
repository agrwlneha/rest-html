import flask 
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True

DB_NAME = "users.db"

# @app.before_first_request
# def DBInitialiser():
# 	createDatabase()

@app.route('/')
def home(): 
	return render_template('index.html')

@app.route('/getAll', methods = ['GET'])
def getAll():
	try:
		connection = sqlite3.connect(DB_NAME)
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()
		cursor.execute('SELECT * FROM users')
		listOfUsers = cursor.fetchall()
		# listOfUsers = flask.jsonify(listOfUsers)
		return render_template('getUser.html', value=listOfUsers)
	except:
		connection.rollback()
	finally:
		connection.close()

def createDatabase():
	db = sqlite3.connect(DB_NAME)
	print "database opened successfully"
	db.execute('CREATE TABLE users (id NUMBER, first_name TEXT, last_name TEXT, company_name TEXT, city TEXT, state TEXT, zip NUMBER, email TEXT, web TEXT, age NUMBER)')
	print "table created"
	db.close()

@app.route('/createUser') 
def createUser():
	return render_template('createUser.html')

@app.route('/addRecord',  methods = ['POST', 'GET'])
def addRecord():
	if request.method == 'POST':
		try:
			id = request.form['id']
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			company_name = request.form['company_name']
			city = request.form['city']
			state = request.form['state']
			zip = request.form['zip']
			email = request.form['email']
			web = request.form['web']
			age = request.form['age']
			with sqlite3.connect(DB_NAME) as connection:
				cursor = connection.cursor()
				cursor.execute("INSERT INTO users (id,first_name,last_name,company_name,city,state,zip,email,web,age) VALUES (?,?,?,?,?,?,?,?,?,?)", (id,first_name,last_name,company_name,city,state,zip,email,web,age))
				connection.commit()
				msg = "Added user successfully"
				# send html code 201 on success
		except:
			connection.rollback()
			msg = "error in adding user"
		finally:
			return render_template('result.html', value=msg)
			connection.close()

@app.route('/deleteUser')
def deleteUser():
	return render_template('deleteUser.html')

@app.route('/deleteRecord', methods=['POST'])
def deleteRecord():
	try:
		id = request.form['id']
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()
		cursor.execute("DELETE FROM users WHERE id=(?)",(id))
		connection.commit()
		msg = "Deleted user successfully"
	except:
		connection.rollback()
		msg = "Error in deleting user"
	finally:
		connection.close()
		return render_template('result.html', value=msg)

@app.route('/updateUser')
def updateUser():
	return render_template('updateUser.html')

@app.route('/updateRecord' , methods=['POST'])
def updateRecord():
	try:
		id = request.form['id']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		connection = sqlite3.connect(DB_NAME)
		cursor = connection.cursor()
		cursor.execute("UPDATE users SET first_name = (?) , last_name = (?) WHERE id = (?)", (first_name,last_name,id))
		connection.commit()
		msg = "user updated"
	except:
		connection.rollback()
		msg = "update failed"
	finally:
		return render_template('result.html', value = msg)
		connection.close()
		
@app.route('/modifiedGet')
def modifiedGet():
	return render_template('getByParameter.html')

@app.route('/getByParameter' , methods=['POST'])
def getByParameter():
	input_page = request.form['page']
	input_limit = request.form['limit']
	name = request.form['name']
	input_sort = request.form['sort']	
	# if 'page' in request.args:
	# 	input_page = int(request.args['page']) 
	# if 'limit' in request.args:
	# 	input_limit = int(request.args['limit']) 
	# if 'name' in request.args:
	# 	name = request.args['name']
	# if 'sort' in request.args:
	# 	input_sort = request.args['sort']

	try:
		connection = sqlite3.connect(DB_NAME)
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()
		# cursor.execute("SELECT * FROM users WHERE first_name LIKE ('%' || (?) || '%') ", (name)) WHERE first_name LIKE (?) OR last_name LIKE (?) '%'+name+'%', '%'+name+'%',
		# cursor.execute("SELECT * FROM users  ORDER BY (?)", (input_sort,))
		# cursor.execute("SELECT * FROM users WHERE first_name LIKE (?) OR last_name LIKE (?) LIMIT (?) ORDER BY last_name ASC", ('%'+name+'%', '%'+name+'%', input_limit,))

		# cursor.execute("SELECT * FROM users WHERE first_name LIKE '%am%' OR last_name LIKE '%am%' LIMIT (?),(?) ORDER BY last_name", (input_page, input_limit))
		cursor.execute("SELECT * FROM users LIMIT (?),(?)", (input_page, input_limit))
		listOfUsers = cursor.fetchall()
	except:
		listOfUsers = []
		connection.rollback()
	finally:
		return render_template('getUser.html', value=listOfUsers)
		connection.close()

app.run()


from flask import Flask, request, session, redirect, render_template, g, url_for, jsonify
from functools import wraps

from commandrunner import CommandRunner

import requests, sqlite3, os, bcrypt

application = Flask(__name__)
application.config['DEBUG'] = True
application.secret_key = 'as3r14saf3tGWEF'

salt = "$2b$12$t8q0bzSdcveQ4A.GE/7TLu"

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):

		try:

			if session['logged_in'] != True:

				return redirect("/login", code=302)

			return f(*args, **kwargs)

		except KeyError, e:

			return redirect("/login", code=302)

	return decorated_function


@application.route('/logout', methods=['GET', 'POST'])
def logout():

	session['username'] = None
	session['logged_in'] = None

	return render_template('login.html')


@application.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		password = bcrypt.hashpw(password.encode('utf8'), salt)

		session['username'] = request.form['username']

		try:

			conn = sqlite3.connect('confgrdb.db')
			c = conn.cursor()

			selectuser = """SELECT username, password FROM users WHERE username = '""" + username + """'"""
			c.execute(selectuser)

			result = c.fetchone()

		except Exception:

			return "Error"

		if result == None:

			return "False"

		dbuser = result[0]
		dbpassword = result[1]

		c.close()

		if username == dbuser and password == dbpassword:

			session['logged_in'] = True

			return "True"

		else:

			return "False"

	else:

		return render_template('login.html')



@application.route("/")
@login_required
def home(title=None, devices=None):

	title = "Home"


	try:

		conn = sqlite3.connect('confgrdb.db')
		c = conn.cursor()

		selectdevicenames = """SELECT devicename from inventory"""

		devices = []

		c.execute(selectdevicenames)
		data = c.fetchall()

		for x in data:

			devicename = str(x[0])
			devices.append(devicename)

		conn.close()

	except Exception:

		devices = "Error"


	return render_template('home.html', title=title, devices=devices, username=session['username'])


@application.route("/inventory")
@application.route("/inventory/")
@application.route('/inventory/<name>')
@login_required
def inventory(name=None, title=None):

	title = "Inventory"

	return render_template('inventory.html', name=name, title=title, username=session['username'])


@application.route("/admin")
@application.route("/admin/")
@login_required
def admin(title=None):

	title = "Admin"

	try:

		conn = sqlite3.connect('confgrdb.db')
		c = conn.cursor()

		selectuser = """SELECT firstname, lastname, username FROM users"""
		c.execute(selectuser)

		results = c.fetchall()

	except Exception:

		return "Error"

	userlist = results


	return render_template('admin.html', title=title, username=session['username'], userlist=userlist)

@application.route("/profile/<username>")
@login_required
def profile(username, title=None):

	title = "Profile"

	try:

		conn = sqlite3.connect('confgrdb.db')
		c = conn.cursor()

		selectuser = """SELECT firstname, lastname, email, username FROM users WHERE username = '""" + username + """'"""
		c.execute(selectuser)

		result = c.fetchone()

	except Exception:

		return "Error"

	firstname = result[0]
	lastname = result[1]
	email = result[2]
	searchedusername = result[3]


	return render_template('profile.html', title=title, username=session['username'], firstname=firstname, lastname=lastname, email=email, searchedusername=searchedusername)


@application.route("/profile/<username>/edit", methods=['GET'])
@login_required
def profileedit(username, title=None):

	title = "Profile"
	username = session['username']

	try:

		conn = sqlite3.connect('confgrdb.db')
		c = conn.cursor()

		selectuser = """SELECT firstname, lastname, email FROM users WHERE username = '""" + username + """'"""
		c.execute(selectuser)

		result = c.fetchone()

	except Exception:

		return "Error"

	firstname = result[0]
	lastname = result[1]
	email = result[2]


	return render_template('profileedit.html', title=title, username=session['username'], firstname=firstname, lastname=lastname, email=email)


@application.route("/createuser", methods=['GET'])
@login_required
def createuser(title=None):

	title = "Profile"
	username = session['username']

	try:

		conn = sqlite3.connect('confgrdb.db')
		c = conn.cursor()

		selectuser = """SELECT firstname, lastname, email FROM users WHERE username = '""" + username + """'"""
		c.execute(selectuser)

		result = c.fetchone()

	except Exception:

		return "Error"


	return render_template('createuser.html', title=title, username=session['username'])

@application.route("/createuser", methods=['POST'])
@login_required
def createuser_post(title=None):


	username = request.form['username']
	password = request.form['password']
	first = request.form['first']
	last = request.form['last']
	email = request.form['email']


	password = bcrypt.hashpw(password.encode('utf8'), salt)

	try:

		conn = sqlite3.connect('confgrdb.db')
		
		c = conn.cursor()
		insertuser = """INSERT INTO users 
								(username, password, firstname, lastname, email)
								VALUES
								('""" + username + """', '""" + password + """', '""" + first + """', '""" + last + """', '""" + email + """')"""


		c.execute(insertuser)

		conn.commit()
		conn.close()

	except Exception:

		return "Error", 500


	return "Created", 201

@application.route("/deleteuser", methods=['POST'])
@login_required
def deleteuser_post(title=None):


	username = request.form['username']

	try:

		conn = sqlite3.connect('confgrdb.db')
		
		c = conn.cursor()
		deleteuser = """DELETE FROM users WHERE username = '""" + username + """'"""

		c.execute(deleteuser)

		conn.commit()
		conn.close()

	except Exception:

		return "Error", 500


	return "Deleted", 200

@application.route("/profileedit", methods=['POST'])
@login_required
def profileedit_post():

	username = request.form['username']
	first = request.form['first']
	last = request.form['last']
	email = request.form['email']

	try:

		conn = sqlite3.connect('confgrdb.db')
		
		c = conn.cursor()
		update = """UPDATE users SET firstname='""" + first + """' WHERE username='""" + username + """'"""
		c.execute(update)

		conn.commit()
		conn.close()

	except Exception:

		return "Error"

	return first



@application.route('/admin', methods=['POST'])
def admin_post():

	netboxurl = "http://" + str(request.form['netboxurl']) + "/api/dcim/devices/?limit=10000"
	netboxapikey = request.form['netboxapikey']

	headers = {'Authorization': 'Token ' + str(netboxapikey)}

	response = requests.get(netboxurl, headers=headers)

	data = response.json()
	responsecode = str(response)

	conn = sqlite3.connect('confgrdb.db')
	c = conn.cursor()


	for x in data['results']:

		devicename = str(x['name'])
		devicesite = str(x['site']['name'])
		devicemodel = str(x['device_type']['model'])


		insertdevice = """INSERT INTO inventory 
						(devicename, devicesite, devicemodel)
						VALUES
						('""" + devicename + """', '""" + devicesite + """', '""" + devicemodel + """')"""

		c.execute(insertdevice)

	conn.commit()
	conn.close()

	if responsecode == "<Response [200]>":

		return "Connected"

	else:

		return "Failed"

@application.route('/runcommands', methods=['POST'])
def runcommands():

	devicelist = request.form['devicelist'].split("|")
	deviceusername = request.form['deviceusername']
	devicepassword = request.form['devicepassword']
	commandstorun = request.form['commandstorun']

	commandlist = commandstorun.split()

	# last item is empty
	for device in devicelist[:-1]:

		runner = CommandRunner(device, deviceusername, devicepassword)

		output = runner.command(commandstorun)

		runner.disconnect()

	return output

@application.errorhandler(404)
@login_required
def page_not_found(e, title=None):

	title = "404"

	return render_template('404.html', title=title, username=session['username']), 404


@application.errorhandler(500)
@login_required
def server_error(e, title=None):

	title = "500"

	return render_template('500.html', title=title, username=session['username']), 500



if __name__ == "__main__":
	application.run(host='0.0.0.0')
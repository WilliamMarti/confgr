from flask import Flask, request, session, redirect, render_template

from commandrunner import CommandRunner

import requests, sqlite3, os, flask_login

application = Flask(__name__)
application.config['DEBUG'] = True
application.secret_key = 'as3r14saf3tGWEF'

login_manager = flask_login.LoginManager()
login_manager.init_app(application)

# Our mock database.
users = {'testuser': {'password': 'secret'}}



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

		session['username'] = request.form['username']

		if username == 'test' and password == 'test':

			session['logged_in'] = True

			return "True"

		else:

			return "False"

	else:

		return render_template('login.html')



@application.route("/")
def home(title=None, devices=None):


	if not session.get('logged_in'):

		title = "Admin"

		return redirect("/login", code=302)

	else:

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


	return render_template('home.html', title=title, devices=devices)


@application.route("/inventory")
@application.route("/inventory/")
@application.route('/inventory/<name>')
def inventory(name=None, title=None):

	title = "Inventory"

	return render_template('inventory.html', name=name, title=title)


@application.route("/admin")
def admin(title=None):


	if not session.get('logged_in'):

		title = "Admin"

		return redirect("/login", code=302)

	else:

		title = "Admin"

		return render_template('admin.html', title=title)


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

		#c.execute("""INSERT INTO inventory (devicename, devicesite, devicemodel) VALUES ('""" + devicename + """','""" + devicesite + """','""" + devicemodel + """')""")
		c.execute(insertdevice)

	conn.commit()
	conn.close()




	if responsecode == "<Response [200]>":

		return "Connected"

	else:

		return "Failed"

@application.errorhandler(404)
def page_not_found(e, title=None):

	title = "404"

	return render_template('404.html', title=title), 404


@application.errorhandler(500)
def server_error(e, title=None):

	title = "500"

	return render_template('500.html', title=title), 500



if __name__ == "__main__":
    application.run(host='0.0.0.0')
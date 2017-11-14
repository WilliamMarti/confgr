from flask import Flask
from flask import render_template
from flask import request

from commandrunner import CommandRunner

import requests, sqlite3

app = Flask(__name__)


@app.route("/")
def hello(title=None):

	title = "Home"

	conn = sqlite3.connect('confgrdb.db')
	c = conn.cursor()

	selectdevicenames = """SELECT devicename from inventory"""

	devices = []

	c.execute(selectdevicenames)
	data = c.fetchall()

	for x in data:

		devicename = str(x[0])
		devices.append(devicename)

	print devices

	conn.close()


	return render_template('home.html', title=title, devices=devices)


@app.route("/inventory")
@app.route("/inventory/")
@app.route('/inventory/<name>')
def inventory(name=None, title=None):

	title = "Inventory"

	return render_template('inventory.html', name=name, title=title)


@app.route("/admin")
def admin(title=None):

	title = "Admin"

	return render_template('admin.html', title=title)

@app.route('/admin', methods=['POST'])
def admin_post():

	netboxurl = "https://" + str(request.form['netboxurl']) + "/api/dcim/devices/?limit=10000"
	netboxapikey = request.form['netboxapikey']

	headers = {'Authorization': 'Token ' + str(netboxapikey), 
				'Accept': 'application/json; indent=4'}

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

		print insertdevice

		#c.execute("""INSERT INTO inventory (devicename, devicesite, devicemodel) VALUES ('""" + devicename + """','""" + devicesite + """','""" + devicemodel + """')""")
		c.execute(insertdevice)

	conn.commit()
	conn.close()




	if responsecode == "<Response [200]>":

		return "Connected"

	else:

		return "Failed"

@app.errorhandler(404)
def page_not_found(e, title=None):

	title = "404"

	return render_template('404.html', title=title), 404


@app.errorhandler(500)
def server_error(e, title=None):

	title = "500"

	return render_template('500.html', title=title), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0')
from netmiko import ConnectHandler

class CommandRunner:

	net_connect = None

	def __init__(self, ip, username, password):

		device = {
			'device_type': 'cisco_ios_telnet',
			'ip': ip,
			'username': username,
			'password': password
		}

		NetController.net_connect = ConnectHandler(**device)

		NetController.net_connect.enable()


	def command(self, commandlist):

		print commandlist

		for i in range(len(commandlist)):
			output = NetController.net_connect.send_command(commandlist[i])
			print output

	def test():

		print "test"
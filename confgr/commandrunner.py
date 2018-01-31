from netmiko import ConnectHandler

class CommandRunner:

	net_connect = None

	def __init__(self, ip, username, password):

		device = {
			'device_type': 'cisco_ios',
			'ip': ip,
			'username': username,
			'password': password
		}

		self.net_connect = ConnectHandler(**device)

		self.net_connect.enable()


	def command(self, commandlist):

		commandlist = commandlist.splitlines()

		output = self.net_connect.send_config_set(commandlist)

		return output


	def disconnect(self):

		self.net_connect.disconnect()
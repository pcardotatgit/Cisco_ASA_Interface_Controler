# Cisco_ASA_Interface_Controler

This python flask application is an example of a tiny controler for Cisco ASA devices ( or anyother Cisco devices ).

This challenge gather almost all knowledge people acquired during the Python Training for Network and Security Engineers.

This challenge is called : Create a Web Controler to manage our device's interfaces

- Create a sqli table named user.db with the following fields :
	- username
	- password

	Add into it at least one users and it's password
	
- Create a sqli table named devices with the following fields :
	- device_type
	- name
	- IP
	- username
	- password
	- state

- Create a second table named interfaces with the following fields :

	- device_name
	- interface
	- index
	- name
	- ip_address
	- Mac_address
	- state

- Add your ASA into the devices table 
- Start the Python Embeded Web Server and listen on the port : 4000
- You should be able to connect to http://localhost:4000 with your browser
- You should have to authenticate with a correct username / password to be able to have access to the application
- You should be able to display a device list and choose one of them
- When you select a device you should display a table with all it's interfaces characteristics. If the Interface is UP display a Green Button, and it the interface is down/administratively down display a Red Button.
- You should be able to change interface status just by clicking on it's Button

# ABOUT THIS SUGGESTED SOLUTION

- Everything is stored into sqlite database.  You must use username = patrick and password = cisco 
- Login, and then select [ GO TO DEVICE LIST AND SELECT ONE ]. Select your device and display it's interface's statuses
- The users_list.py script allows you to display the user list contained into users.db
- The add_devices_to_sqllite_db.py script allows you to add devices into the devices.db from the CSV file named devices.csv
- The devices_list.py script allows you to display the device list contained into the devices.db
- The add_users.py script allows you to add users into the users.db

In addition, this application generate a JSON output file name ** interfaces.csv ** in the ** out **  folder

This file can be accessed directly without any authentication thru the following path ** http://{server_ip_address}/out**

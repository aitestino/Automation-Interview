import paramiko
import sys

#set the hostname, user, and pass args for ssh
hostname = '10.10.20.48'
username = 'developer'
password = sys.argv[1]

#create ssh connect
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#initiate ssh connection to router
client.connect(hostname=hostname, username=username, password=password)

#open a channel for remote server
channel = client.invoke_shell()

#run the command
channel.send('\n')
channel.sendall("show ip int brief\n")

#attempt to wait for command to run
while not channel.recv_ready():
    pass

#read the command
output = channel.recv(1024).decode('utf-8')
print(output)
interfaces = {}

for line in output.split('\n')[2:]:
    if line:
        fields = line.split()
        interface_name = fields[0]
        status = fields[4]
        if status == 'up':
            interfaces[interface_name] = 'up'
        elif status == 'administratively down':
            interfaces[interface_name] = 'admin down'
        else:
            interfaces[interface_name] = 'not connected'
#assign dot1q tag of '999' to subinterfaces  for ports that are down

for interface_name, status in interface.items():
    if status == 'admin down':
        sub_interface_name = f'{interface_name}.999'
        interfaces[sub_interface_name] = 'admin down'

#print the list of interface and their statuses
for interface_name, status in interfaces.items():
    print(f'{interface_name}: {status}')

#end connection
client.close()

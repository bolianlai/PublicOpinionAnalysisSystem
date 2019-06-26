import telnetlib
import getpass
import sys



HOST = "localhost"
user = 'bolian'
tn = telnetlib.Telnet('127.0.0.1', port=6023, timeout=10)
print('@1')
tn.read_until(b"Username: ")
print('@2')

tn.write(b"bolian\n")
print('@3')
tn.read_until(b"Password: ")
tn.write(b"yourpassword\n")
print('@4')
tn.write(b"engine\n")
print('@5')

print(tn.read_very_eager())

print('@6')
tn.write(b"exit\n")

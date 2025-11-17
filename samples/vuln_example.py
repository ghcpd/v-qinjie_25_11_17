import os

username = input('user: ')
query = "SELECT * FROM users WHERE name = '" + username + "'"
print(query)

cmd = 'cat ' + filename
os.system(cmd)

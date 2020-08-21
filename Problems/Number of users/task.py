# write your code here
with open('users.json') as json_file:
    dicti = json.load(json_file)

print(len(dicti['users']))

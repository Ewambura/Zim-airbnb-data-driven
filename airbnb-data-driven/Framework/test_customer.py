import yaml
from pathlib import Path
import pymysql
import datetime
from user import user


'''
TODO:
x- truncate() for testing
x- test insert()
x- test deleteById()
x- test update()
- test verify new/update:
    - email in use
    - password len
    - passwords match
    - user role
- test tryLogin()




'''

u = user()
u.truncate()


d = {'first_name_': 'Tariro', 'last_name_': 'Moyo', 'email': 'tariro@zimbnb.co.zw',
     'role': 'guest', 'password': 'pass123', 'password2': 'pass123'}
u.set(d)
if u.verify_new():
    u.insert()
    print(f"ID {u.data[0][u.pk]} inserted")
else:
    print(u.errors)


u.deleteById(u.data[0][u.pk])

u = user()
u.getAll()
print(f"len of u.data is {len(u.data)} after delete.")



u = user()
u.truncate()


d = {'first_name_': 'Tariro', 'last_name_': 'Moyo', 'email': 'tariro@zimbnb.co.zw',
     'role': 'guest', 'password': 'pass123', 'password2': 'pass123'}
u.set(d)
if u.verify_new():
    u.insert()
    print(f"ID {u.data[0][u.pk]} inserted")
else:
    print(u.errors)


u = user()
u.getByField('email', 'tariro@zimbnb.co.zw')
u.data[0]['first_name_'] = 'Rudo'
if u.verify_update():
    u.update(u.data[0][u.pk])
    print(f"ID {u.data[0][u.pk]} updated")
    u = user()
    u.getAll()
    print(f"new first_name_ is {u.data[0]['first_name_']}")
else:
    print(u.errors)




u = user()
u.getByField('email', 'tariro@zimbnb.co.zw')
u.data[0]['password'] = 'abc'
u.data[0]['password2'] = 'xyz'
if u.verify_update():
    u.update(u.data[0][u.pk])
else:
    print(u.errors)

u = user()
u.getByField('email', 'tariro@zimbnb.co.zw')
u.data[0]['role'] = 'superuser'
if u.verify_update():
    u.update(u.data[0][u.pk])
else:
    print(u.errors)


d = {'first_name_': 'Tariro', 'last_name_': 'Moyo', 'email': 'tariro@zimbnb.co.zw',
     'role': 'guest', 'password': 'pass123', 'password2': 'pass123'}
u = user()
u.set(d)
if u.verify_new():
    u.insert()
    print(f"ID {u.data[0][u.pk]} inserted")
else:
    print(u.errors)


u = user()
if u.tryLogin('tariro@zimbnb.co.zw', 'pass123'):
    print(f"user with email {u.data[0]['email']} logged in")
else:
    print('login failed')

u = user()
if u.tryLogin('tariro@zimbnb.co.zw', 'wrongpassword'):
    print(f"user with email {u.data[0]['email']} logged in")
else:
    print('login failed')


u = user()
u.getByField('email', 'tariro@zimbnb.co.zw')
print(u.data[0]['password'])
u.data[0]['password'] = 'newpass1'
u.data[0]['password2'] = 'newpass1'
if u.verify_update():
    u.update(u.data[0][u.pk])
    print(u.data[0]['password'])
else:
    print(u.errors)

u = user()
if u.tryLogin('tariro@zimbnb.co.zw', 'newpass1'):
    print(f"user with email {u.data[0]['email']} logged in")
else:
    print('login failed')

u = user()
if u.tryLogin('tariro@zimbnb.co.zw', 'pass123'):
    print(f"user with email {u.data[0]['email']} logged in")
else:
    print('login failed')

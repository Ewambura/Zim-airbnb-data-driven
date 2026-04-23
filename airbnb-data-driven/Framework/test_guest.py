from user import user

from user import user

'''
TODO:
x- test insert()         (CREATE block)
x- test deleteById()     (DELETE block)
x- test update()         (UPDATE name block)
- test getById()         (READ block)
'''

# ── After first run, hardcode this and comment out CREATE ──
user_id = 16


# ── TRUNCATE (run once to reset, then comment out) ────────────────────
# u = user()
# u.truncate()


# ── CREATE ────────────────────────────────────────────────────────────
# u = user()
# d = {'first_name_': 'Tariro', 'last_name_': 'Moyo', 'email': 'tariro@zimbnb.co.zw',
#      'role': 'guest', 'password': 'pass123', 'password2': 'pass123'}
# u.set(d)
# if u.verify_new():
#     u.insert()
#     user_id = u.data[0][u.pk]
#     print(f"CREATE: ID {user_id} inserted")
# else:
#     print(f"CREATE failed: {u.errors}")


# ── READ ──────────────────────────────────────────────────────────────
# u = user()
# u.getById(user_id)
# print(f"READ: {u.data[0]['first_name_']} {u.data[0]['last_name_']} ({u.data[0]['email']})")


# ── DELETE ────────────────────────────────────────────────────────────
# u = user()
# u.deleteById(user_id)
# u.getAll()
# print(f"DELETE: {len(u.data)} users remaining after delete")


# ── UPDATE name ───────────────────────────────────────────────────────
# u = user()
# u.getById(user_id)
# u.data[0]['first_name_'] = 'Rudo'
# if u.verify_update():
#     u.update(user_id)
#     u.getById(user_id)
#     print(f"UPDATE name: new first_name_ is {u.data[0]['first_name_']}")
# else:
#     print(f"UPDATE name failed: {u.errors}")





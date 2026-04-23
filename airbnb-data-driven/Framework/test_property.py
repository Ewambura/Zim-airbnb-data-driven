import yaml
from pathlib import Path
import pymysql
import datetime
from property import Property
from user import user

property_id = 16
owner_id = 32


# ── SETUP: create or reuse test owner ─────────────────────────────────────────
# u = user()
# d = {'first_name_': 'Test1', 'last_name_': 'ZimBnB', 'email': 'testowneroi@zimbnb.co.zw',
#      'role': 'owner', 'password': 'owner123', 'password2': 'owner123'}
# u.set(d)
# if u.verify_new():
#     u.insert()
#     owner_id = u.data[0][u.pk]
#     print(f"Test owner created with ID {owner_id}")
# else:
#     u.getByField('email', 'testowneroi@zimbnb.co.zw')
#     owner_id = u.data[0][u.pk]
#     print(f"Using existing owner ID {owner_id}")



# ── CREATE ─────────────────────────────────────────────────────────────────────
# p = Property()
# result = p.createProperty(
#     owner_id=owner_id,
#     title='Green City Cottage',
#     description='The destination to relax and unwind.',
#     address='12 Samora Machel Ave',
#     city='Harare',
#     province='Harare',
#     property_type='cottage',
#     price_per_night=120,
#     num_bedrooms=2,
#     num_bathrooms=1,
#     num_guests=4
# )
# if result['success']:
#     property_id = result['property_id']
#     print(f"CREATE: ID {property_id} inserted")
# else:
#     print(f"CREATE failed: {result['error']}")


# # ── READ ───────────────────────────────────────────────────────────────────────
# p = Property()
# p.getById(property_id)
# print(f"READ: {p.data[0]['title']} in {p.data[0]['city']}")


# # ── UPDATE ─────────────────────────────────────────────────────────────────────
# p = Property()
# result = p.updateProperty(property_id, owner_id, city='Bulawayo')
# if result['success']:
#     p.getById(property_id)
#     print(f"UPDATE: new city is {p.data[0]['city']}")
# else:
#     print(f"UPDATE failed: {result['error']}")


# # ── DELETE ─────────────────────────────────────────────────────────────────────
# p = Property()
# result = p.deleteProperty(property_id, owner_id)
# if result['success']:
#     print(f"DELETE: ID {property_id} deleted")
# else:
#     print(f"DELETE failed: {result['error']}")






# # ── FILTERS ────────────────────────────────────────────────────────────────────
p = Property()
results = p.getByCity('Harare')
print(f"FILTER by city (Harare): {len(results)} properties")

# p = Property()
# results = p.getByPriceRange(min_price=50, max_price=200)
# print(f"FILTER by price $50-$200: {len(results)} properties")

# p = Property()
# results = p.getByMinBedrooms(2)
# print(f"FILTER >= 2 bedrooms: {len(results)} properties")

# p = Property()
# results = p.filterProperties(city='Harare', min_price=50, property_type='cottage')
# print(f"FILTER Harare cottages from $50: {len(results)} properties")



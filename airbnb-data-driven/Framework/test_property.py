import yaml
from pathlib import Path
import pymysql
import datetime
from property import Property
from user import user


'''
TODO:
x- test createProperty()
x- test deleteProperty()
x- test updateProperty()
- test ownership verification:
    - wrong owner on update
    - wrong owner on delete
- test validation:
    - missing required fields
    - invalid price (zero)
- test filter methods:
    - getByCity()
    - getByPriceRange()
    - getByMinBedrooms()
    - filterProperties()




'''

# create a test owner account to use throughout
u = user()
d = {'first_name_': 'TestOwner', 'last_name_': 'ZimBnB', 'email': 'testowner@zimbnb.co.zw',
     'role': 'owner', 'password': 'owner123', 'password2': 'owner123'}
u.set(d)
if u.verify_new():
    u.insert()
    owner_id = u.data[0][u.pk]
    print(f"Test owner created with ID {owner_id}")
else:
    u.getByField('email', 'testowner@zimbnb.co.zw')
    owner_id = u.data[0][u.pk]
    print(f"Using existing owner ID {owner_id}")


p = Property()
result = p.createProperty(
    owner_id=owner_id,
    title='Harare City Cottage',
    description='A cozy cottage in the heart of Harare.',
    address='12 Samora Machel Ave',
    city='Harare',
    province='Harare',
    property_type='cottage',
    price_per_night=120,
    num_bedrooms=2,
    num_bathrooms=1,
    num_guests=4
)
if result['success']:
    print(f"ID {result['property_id']} inserted")
    property_id = result['property_id']
else:
    print(result['error'])


p = Property()
result = p.deleteProperty(property_id, owner_id)
if result['success']:
    print(f"ID {property_id} deleted")
else:
    print(result['error'])

p = Property()
p.getAll()
print(f"len of p.data is {len(p.data)} after delete.")



p = Property()
result = p.createProperty(
    owner_id=owner_id,
    title='Harare City Cottage',
    description='A cozy cottage in the heart of Harare.',
    address='12 Samora Machel Ave',
    city='Harare',
    province='Harare',
    property_type='cottage',
    price_per_night=120,
    num_bedrooms=2,
    num_bathrooms=1,
    num_guests=4
)
if result['success']:
    print(f"ID {result['property_id']} inserted")
    property_id = result['property_id']
else:
    print(result['error'])


p = Property()
p.getById(property_id)
p.data[0]['city'] = 'Bulawayo'
result = p.updateProperty(property_id, owner_id, city='Bulawayo')
if result['success']:
    print(f"ID {property_id} updated")
    p = Property()
    p.getById(property_id)
    print(f"new city is {p.data[0]['city']}")
else:
    print(result['error'])


p = Property()
result = p.updateProperty(property_id, owner_id=99999, title='Hacked Title')
if result['success']:
    print(f"ID {property_id} updated")
else:
    print(result['error'])

p = Property()
result = p.deleteProperty(property_id, owner_id=99999)
if result['success']:
    print(f"ID {property_id} deleted")
else:
    print(result['error'])


p = Property()
result = p.createProperty(
    owner_id=owner_id,
    title=None,
    description='Missing title test.',
    address='99 Test Rd',
    city='Mutare',
    province='Manicaland',
    property_type='apartment',
    price_per_night=80,
    num_bedrooms=1,
    num_bathrooms=1,
    num_guests=2
)
if result['success']:
    print(f"ID {result['property_id']} inserted")
else:
    print(result['error'])

p = Property()
result = p.createProperty(
    owner_id=owner_id,
    title='Zero Price Flat',
    description='Should not be allowed.',
    address='5 Test St',
    city='Gweru',
    province='Midlands',
    property_type='apartment',
    price_per_night=0,
    num_bedrooms=1,
    num_bathrooms=1,
    num_guests=2
)
if result['success']:
    print(f"ID {result['property_id']} inserted")
else:
    print(result['error'])


p = Property()
results = p.getByCity('Harare')
print(f"Properties in Harare: {len(results)}")

p = Property()
results = p.getByPriceRange(min_price=50, max_price=200)
print(f"Properties $50-$200/night: {len(results)}")

p = Property()
results = p.getByMinBedrooms(2)
print(f"Properties with >= 2 bedrooms: {len(results)}")

p = Property()
results = p.filterProperties(city='Harare', min_price=50, property_type='cottage')
print(f"Harare cottages from $50: {len(results)}")


p = Property()
result = p.deleteProperty(property_id, owner_id)
if result['success']:
    print(f"cleanup: property {property_id} deleted")

u = user()
u.getByField('email', 'testowner@zimbnb.co.zw')
if u.data:
    u.deleteById(u.data[0][u.pk])
    print("cleanup: test owner deleted")

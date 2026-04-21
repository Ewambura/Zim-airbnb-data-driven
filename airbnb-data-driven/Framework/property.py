from baseObject import baseObject


class Property(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByOwnerId(self, owner_id):
		self.getByField('owner_id', owner_id)
		return self.data

	def getByCity(self, city):
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}` WHERE LOWER(`city`) = LOWER(%s);'''
		self.cur.execute(sql, [city])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getByPriceRange(self, min_price=None, max_price=None):
		self.data = []
		conditions = []
		tokens = []

		if min_price is not None:
			conditions.append('`price_per_night` >= %s')
			tokens.append(min_price)
		if max_price is not None:
			conditions.append('`price_per_night` <= %s')
			tokens.append(max_price)

		if not conditions:
			self.getAll()
			return self.data

		sql = f'''SELECT * FROM `{self.tn}` WHERE {' AND '.join(conditions)};'''
		self.cur.execute(sql, tokens)
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getByMinBedrooms(self, min_bedrooms):
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}` WHERE `num_bedrooms` >= %s;'''
		self.cur.execute(sql, [min_bedrooms])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getByPropertyType(self, property_type):
		self.getByField('property_type', property_type)
		return self.data

	def getByMinGuests(self, min_guests):
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}` WHERE `max_guests` >= %s;'''
		self.cur.execute(sql, [min_guests])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def filterProperties(self, city=None, province=None, min_price=None, max_price=None,
						 min_bedrooms=None, property_type=None, min_guests=None,
						 order_by=None):
		self.data = []
		conditions = []
		tokens = []

		if city is not None:
			conditions.append('LOWER(`city`) = LOWER(%s)')
			tokens.append(city)

		if province is not None:
			conditions.append('LOWER(`province`) = LOWER(%s)')
			tokens.append(province)

		if min_price is not None:
			conditions.append('`price_per_night` >= %s')
			tokens.append(min_price)

		if max_price is not None:
			conditions.append('`price_per_night` <= %s')
			tokens.append(max_price)

		if min_bedrooms is not None:
			conditions.append('`num_bedrooms` >= %s')
			tokens.append(min_bedrooms)

		if property_type is not None:
			conditions.append('`property_type` = %s')
			tokens.append(property_type)

		if min_guests is not None:
			conditions.append('`max_guests` >= %s')
			tokens.append(min_guests)

		sql = f'''SELECT * FROM `{self.tn}`'''

		if conditions:
			sql += ' WHERE ' + ' AND '.join(conditions)

		allowed_order_columns = ['price_per_night', 'num_bedrooms', 'max_guests', 'city', 'title', 'province']
		if order_by and order_by in allowed_order_columns:
			sql += f' ORDER BY `{order_by}`'

		sql += ';'

		self.cur.execute(sql, tokens)
		for row in self.cur:
			self.data.append(row)

		return self.data

	def getDistinctProvinces(self):
		"""Get list of distinct provinces for filter dropdown"""
		self.data = []
		sql = '''SELECT DISTINCT `province` FROM `PROPERTY` WHERE `province` IS NOT NULL ORDER BY `province`;'''
		self.cur.execute(sql)
		provinces = []
		for row in self.cur:
			provinces.append(row['province'])
		return provinces

	def getByIds(self, ids):
		"""Get properties by a list of IDs."""
		if not ids:
			return []
		self.data = []
		placeholders = ','.join(['%s'] * len(ids))
		sql = f'''SELECT * FROM `{self.tn}` WHERE `{self.pk}` IN ({placeholders});'''
		self.cur.execute(sql, ids)
		for row in self.cur:
			self.data.append(row)
		return self.data

	def verifyOwnership(self, property_id, owner_id):
		sql = '''SELECT 1 FROM `PROPERTY` WHERE `property_id` = %s AND `owner_id` = %s;'''
		self.cur.execute(sql, [property_id, owner_id])
		result = self.cur.fetchone()
		return result is not None

	def createProperty(self, owner_id, title, description, address, city,
					   province, property_type, price_per_night, num_bedrooms,
					   num_bathrooms, num_guests, check_in_time='3PM', check_out_time='11AM'):
		if not all([owner_id, title, city, property_type, price_per_night is not None]):
			return {'success': False, 'error': 'Missing required fields'}

		if price_per_night <= 0:
			return {'success': False, 'error': 'Price must be greater than 0'}

		# Ensure PROPERTYOWNER record exists (auto-create if missing)
		self.cur.execute('SELECT owner_id FROM `PROPERTYOWNER` WHERE `owner_id` = %s;', [owner_id])
		if not self.cur.fetchone():
			self.cur.execute(
				'INSERT INTO `PROPERTYOWNER` (owner_id, business_name_, payout_method) VALUES (%s, %s, %s);',
				[owner_id, '', '']
			)

		property_data = {
			'owner_id': owner_id,
			'title': title,
			'description': description,
			'address': address,
			'city': city,
			'province': province,
			'property_type': property_type,
			'price_per_night': price_per_night,
			'num_bedrooms': num_bedrooms,
			'num_bathrooms': num_bathrooms,
			'max_guests': num_guests,
			'check_in_time': check_in_time,
			'check_out_time': check_out_time,
			'property_name_': title[:20] if title else 'Property',
			'is_available': 'YES'
		}
		self.set(property_data)
		self.insert()
		return {'success': True, 'property_id': self.data[0].get(self.pk)}

	def updateProperty(self, property_id, owner_id, title=None, description=None,
					   address=None, city=None, province=None, property_type=None,
					   price_per_night=None, num_bedrooms=None,
					   num_bathrooms=None, num_guests=None):
		if not self.verifyOwnership(property_id, owner_id):
			return {'success': False, 'error': 'You do not own this property'}

		allowed_fields = {
			'title': title,
			'description': description,
			'address': address,
			'city': city,
			'province': province,
			'property_type': property_type,
			'price_per_night': price_per_night,
			'num_bedrooms': num_bedrooms,
			'num_bathrooms': num_bathrooms,
			'max_guests': num_guests
		}

		updates = []
		tokens = []
		for field, value in allowed_fields.items():
			if value is not None:
				updates.append(f'`{field}` = %s')
				tokens.append(value)

		if not updates:
			return {'success': False, 'error': 'No fields to update'}

		tokens.append(property_id)
		sql = f'''UPDATE `{self.tn}` SET {', '.join(updates)} WHERE `{self.pk}` = %s;'''
		self.cur.execute(sql, tokens)
		return {'success': True}

	def attachFirstImages(self, properties):
		"""One query: attach first_image URL to each property dict in the list."""
		if not properties:
			return properties
		ids = [p['property_id'] for p in properties]
		placeholders = ','.join(['%s'] * len(ids))
		sql = f'''
			SELECT pi.property_Id, pi.image_url
			FROM `PROPERTY_IMAGE` pi
			INNER JOIN (
				SELECT MIN(image_id) AS min_id
				FROM `PROPERTY_IMAGE`
				WHERE `property_Id` IN ({placeholders})
				GROUP BY `property_Id`
			) first_img ON pi.image_id = first_img.min_id;
		'''
		self.cur.execute(sql, ids)
		image_map = {row['property_Id']: row['image_url'] for row in self.cur}
		for p in properties:
			p['first_image'] = image_map.get(p['property_id'])
		return properties

	def deleteProperty(self, property_id, owner_id):
		if not self.verifyOwnership(property_id, owner_id):
			return {'success': False, 'error': 'You do not own this property'}

		# Check for active bookings
		sql = '''SELECT COUNT(*) as active FROM `BOOKING`
				 WHERE `property_id` = %s AND `check_out_date` >= CURDATE();'''
		self.cur.execute(sql, [property_id])
		result = self.cur.fetchone()
		if result['active'] > 0:
			return {'success': False, 'error': 'Cannot delete property with active bookings'}

		self.deleteById(property_id)
		return {'success': True}

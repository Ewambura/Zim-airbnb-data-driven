from baseObject import baseObject


class Availability(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByPropertyId(self, property_id):
		self.getByField('property_id', property_id)
		return self.data

	def getAvailableRanges(self, property_id):
		"""Get all available date ranges for a property."""
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}`
				  WHERE `property_id` = %s AND `is_available` = 'true'
				  ORDER BY `start_date` ASC;'''
		self.cur.execute(sql, [property_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getUnavailableRanges(self, property_id):
		"""Get all unavailable/blocked date ranges for a property."""
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}`
				  WHERE `property_id` = %s AND `is_available` = 'false'
				  ORDER BY `start_date` ASC;'''
		self.cur.execute(sql, [property_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def checkDateRange(self, property_id, start_date, end_date):
		"""Check if a date range is available (no blocking entries overlap)."""
		sql = '''SELECT COUNT(*) as conflicts FROM `AVAILABILITY`
				 WHERE `property_id` = %s
				 AND `is_available` = 'false'
				 AND NOT (`end_date` < %s OR `start_date` > %s);'''
		self.cur.execute(sql, [property_id, start_date, end_date])
		result = self.cur.fetchone()
		return result['conflicts'] == 0

	def setAvailability(self, property_id, start_date, end_date, is_available, owner_id):
		"""Set availability for a date range."""
		sql = '''SELECT `owner_id` FROM `PROPERTY` WHERE `property_id` = %s;'''
		self.cur.execute(sql, [property_id])
		result = self.cur.fetchone()
		if not result or result['owner_id'] != owner_id:
			return {'success': False, 'error': 'You do not own this property'}

		avail_data = {
			'property_id': property_id,
			'start_date': start_date,
			'end_date': end_date,
			'is_available': 'true' if is_available else 'false'
		}
		self.set(avail_data)
		self.insert()
		return {'success': True, 'aval_id': self.data[0].get(self.pk)}

	def blockDates(self, property_id, start_date, end_date, owner_id):
		"""Block a date range (mark as unavailable)."""
		return self.setAvailability(property_id, start_date, end_date, False, owner_id)

	def unblockDates(self, property_id, start_date, end_date, owner_id):
		"""Unblock a date range (mark as available)."""
		return self.setAvailability(property_id, start_date, end_date, True, owner_id)

	def deleteAvailability(self, aval_id, owner_id):
		"""Delete an availability record."""
		self.getById(aval_id)
		if len(self.data) == 0:
			return {'success': False, 'error': 'Availability record not found'}

		property_id = self.data[0]['property_id']

		sql = '''SELECT `owner_id` FROM `PROPERTY` WHERE `property_id` = %s;'''
		self.cur.execute(sql, [property_id])
		result = self.cur.fetchone()
		if not result or result['owner_id'] != owner_id:
			return {'success': False, 'error': 'You do not own this property'}

		self.deleteById(aval_id)
		return {'success': True}

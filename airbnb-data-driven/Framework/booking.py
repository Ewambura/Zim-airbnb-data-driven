from baseObject import baseObject


class Booking(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByGuestId(self, guest_id):
		self.getByField('guest_id', guest_id)
		return self.data

	def getByPropertyId(self, property_id):
		self.getByField('property_id', property_id)
		return self.data

	def getByDateRange(self, start_date, end_date):
		"""Get bookings within a date range. Dates are stored as integers."""
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}`
				  WHERE `check_in_date` >= %s AND `check_out_date` <= %s;'''
		self.cur.execute(sql, [start_date, end_date])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def checkAvailability(self, property_id, check_in, check_out):
		"""Check if dates are available. Dates should be integers matching DB format."""
		sql = '''SELECT COUNT(*) as conflicts FROM `BOOKING`
				 WHERE `property_id` = %s
				 AND NOT (`check_out_date` <= %s OR `check_in_date` >= %s);'''
		self.cur.execute(sql, [property_id, check_in, check_out])
		result = self.cur.fetchone()
		return result['conflicts'] == 0

	def createBooking(self, property_id, guest_id, check_in, check_out, num_guests):
		"""Create a booking. check_in and check_out should be integers."""
		# Verify user exists and has role='guest'
		sql = '''SELECT role FROM `USER` WHERE `user_id` = %s;'''
		self.cur.execute(sql, [guest_id])
		user_row = self.cur.fetchone()
		if not user_row:
			return {'success': False, 'error': 'User not found'}
		if user_row['role'] != 'guest':
			return {'success': False, 'error': 'Only guests can make bookings'}

		# Ensure GUEST record exists (auto-create if missing)
		sql = '''SELECT guest_id FROM `GUEST` WHERE `guest_id` = %s;'''
		self.cur.execute(sql, [guest_id])
		if not self.cur.fetchone():
			sql = '''INSERT INTO `GUEST` (guest_id, emergency_contact_name, emergency_contact_phone) VALUES (%s, '', '');'''
			self.cur.execute(sql, [guest_id])

		if not self.checkAvailability(property_id, check_in, check_out):
			return {'success': False, 'error': 'Property not available for selected dates'}

		# Validate check_out is after check_in
		if check_out <= check_in:
			return {'success': False, 'error': 'Check-out must be after check-in'}

		booking_data = {
			'property_id': property_id,
			'guest_id': guest_id,
			'check_in_date': check_in,
			'check_out_date': check_out,
			'num_guests': num_guests
		}
		self.set(booking_data)
		self.insert()
		return {'success': True, 'booking_id': self.data[0].get(self.pk)}

	def cancelBooking(self, booking_id, guest_id):
		"""Cancel a booking. Only the guest who made it can cancel."""
		self.getById(booking_id)
		if len(self.data) == 0:
			return {'success': False, 'error': 'Booking not found'}

		if self.data[0]['guest_id'] != guest_id:
			return {'success': False, 'error': 'You can only cancel your own bookings'}

		self.deleteById(booking_id)
		return {'success': True}

	def getUpcoming(self, guest_id):
		"""Get upcoming bookings for a guest."""
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}`
				  WHERE `guest_id` = %s
				  ORDER BY `check_in_date` ASC;'''
		self.cur.execute(sql, [guest_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getPast(self, guest_id):
		"""Get past bookings for a guest."""
		self.data = []
		sql = f'''SELECT * FROM `{self.tn}`
				  WHERE `guest_id` = %s
				  ORDER BY `check_out_date` DESC;'''
		self.cur.execute(sql, [guest_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

from baseObject import baseObject


class Guest(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByGuestId(self, guest_id):
		self.getByField('guest_id', guest_id)
		return self.data

	def getProfile(self, guest_id):
		self.data = []
		# Note: GUEST table doesn't have user_id foreign key in current schema
		# Returns guest record directly
		self.getById(guest_id)
		return self.data

	def getBookingHistory(self, guest_id):
		"""Get past bookings with nights count and total cost."""
		from datetime import date
		today_int = int(date.today().strftime('%Y%m%d'))
		self.data = []
		sql = '''SELECT b.*, p.title, p.city, p.price_per_night, p.property_type,
					DATEDIFF(
						STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
						STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
					) AS nights
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 AND b.guest_id = %s
				 AND b.check_out_date < %s
				 ORDER BY b.check_in_date DESC;'''
		self.cur.execute(sql, [guest_id, today_int])
		for row in self.cur:
			row['total_cost'] = (row['nights'] or 0) * float(row['price_per_night'] or 0)
			self.data.append(row)
		return self.data

	def getTotalSpent(self, guest_id):
		"""Calculate real totals: bookings, nights, and amount spent."""
		sql = '''SELECT
					COUNT(*) AS total_bookings,
					COALESCE(SUM(
						DATEDIFF(
							STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
							STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
						) * p.price_per_night
					), 0) AS total_spent,
					COALESCE(SUM(
						DATEDIFF(
							STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
							STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
						)
					), 0) AS total_nights
				 FROM `BOOKING` b
				 JOIN `PROPERTY` p ON b.property_id = p.property_id
				 WHERE b.guest_id = %s;'''
		self.cur.execute(sql, [guest_id])
		result = self.cur.fetchone()
		return {
			'total_spent':   int(result['total_spent']   or 0),
			'total_bookings': int(result['total_bookings'] or 0),
			'total_nights':  int(result['total_nights']  or 0)
		}

	def getReviewsWritten(self, guest_id):
		self.data = []
		# REVIEW links to BOOKING, not directly to PROPERTY
		sql = '''SELECT r.*, b.property_id
				 FROM `REVIEW` r, `BOOKING` b
				 WHERE r.booking_id = b.Booking_id
				 AND r.guest_id = %s
				 ORDER BY r.dated_posted_ DESC;'''
		self.cur.execute(sql, [guest_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getFavoriteProperties(self, guest_id):
		self.data = []
		sql = '''SELECT p.*, COUNT(*) as times_booked
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 AND b.guest_id = %s
				 GROUP BY b.property_id
				 HAVING times_booked > 1
				 ORDER BY times_booked DESC;'''
		self.cur.execute(sql, [guest_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getUpcomingBookings(self, guest_id):
		"""Get upcoming bookings with nights count and total cost."""
		from datetime import date
		today_int = int(date.today().strftime('%Y%m%d'))
		self.data = []
		sql = '''SELECT b.*, p.title, p.city, p.address, p.price_per_night, p.property_type,
					DATEDIFF(
						STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
						STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
					) AS nights
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 AND b.guest_id = %s
				 AND b.check_out_date >= %s
				 ORDER BY b.check_in_date ASC;'''
		self.cur.execute(sql, [guest_id, today_int])
		for row in self.cur:
			row['total_cost'] = (row['nights'] or 0) * float(row['price_per_night'] or 0)
			self.data.append(row)
		return self.data

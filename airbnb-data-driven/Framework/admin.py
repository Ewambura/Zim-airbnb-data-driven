from baseObject import baseObject


class Admin(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByAdminId(self, admin_id):
		self.getByField('admin_id', admin_id)
		return self.data

	def getAllUsers(self):
		self.data = []
		sql = '''SELECT * FROM `USER` ORDER BY `user_id` DESC;'''
		self.cur.execute(sql)
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getUsersByRole(self, role):
		self.data = []
		sql = '''SELECT * FROM `USER` WHERE `role` = %s ORDER BY `user_id` DESC;'''
		self.cur.execute(sql, [role])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getFilteredUsers(self, role=None, search=None):
		self.data = []
		conditions = []
		params = []

		if role:
			conditions.append('`role` = %s')
			params.append(role)

		if search:
			search_term = f'%{search}%'
			conditions.append('(`first_name_` LIKE %s OR `last_name_` LIKE %s OR `email` LIKE %s)')
			params.extend([search_term, search_term, search_term])

		where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''
		sql = f'SELECT * FROM `USER` {where} ORDER BY `user_id` DESC;'
		self.cur.execute(sql, params)
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getAllBookings(self, limit=100):
		self.data = []
		sql = '''SELECT b.*, p.title as property_title
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 ORDER BY b.check_in_date DESC
				 LIMIT %s;'''
		self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getAllProperties(self):
		self.data = []
		sql = '''SELECT p.*, po.business_name_ as owner_business,
		                u.email as owner_email,
		                u.first_name_ as owner_first_name,
		                u.last_name_ as owner_last_name
				 FROM `PROPERTY` p
				 LEFT JOIN `PROPERTYOWNER` po ON p.owner_id = po.owner_id
				 LEFT JOIN `USER` u ON p.owner_id = u.user_id
				 ORDER BY p.property_id DESC;'''
		self.cur.execute(sql)
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getPlatformStats(self):
		stats = {}

		sql = '''SELECT COUNT(*) as count FROM `USER`;'''
		self.cur.execute(sql)
		stats['total_users'] = self.cur.fetchone()['count']

		sql = '''SELECT COUNT(*) as count FROM `GUEST`;'''
		self.cur.execute(sql)
		stats['total_guests'] = self.cur.fetchone()['count']

		sql = '''SELECT COUNT(*) as count FROM `PROPERTYOWNER`;'''
		self.cur.execute(sql)
		stats['total_owners'] = self.cur.fetchone()['count']

		sql = '''SELECT COUNT(*) as count FROM `PROPERTY`;'''
		self.cur.execute(sql)
		stats['total_properties'] = self.cur.fetchone()['count']

		sql = '''SELECT COUNT(*) as count FROM `BOOKING`;'''
		self.cur.execute(sql)
		stats['total_bookings'] = self.cur.fetchone()['count']

		sql = '''SELECT COUNT(*) as count FROM `REVIEW`;'''
		self.cur.execute(sql)
		stats['total_reviews'] = self.cur.fetchone()['count']

		stats['total_revenue'] = 0  # Would need calculation based on booking dates

		sql = '''SELECT AVG(rating) as avg FROM `REVIEW`;'''
		self.cur.execute(sql)
		result = self.cur.fetchone()
		stats['platform_avg_rating'] = round(float(result['avg']), 2) if result['avg'] else 0

		return stats

	def getRecentActivity(self, limit=20):
		self.data = []
		sql = '''SELECT 'booking' as type, b.Booking_id as id,
				        b.check_in_date as date, p.title as details
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 ORDER BY b.Booking_id DESC
				 LIMIT %s;'''
		self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getRecentReviews(self, limit=20):
		self.data = []
		sql = '''SELECT r.*
				 FROM `REVIEW` r
				 ORDER BY r.dated_posted_ DESC
				 LIMIT %s;'''
		self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getTopProperties(self, limit=10):
		self.data = []
		sql = '''SELECT p.*, COUNT(b.Booking_id) as booking_count,
				        COALESCE(AVG(r.rating), 0) as avg_rating
				 FROM `PROPERTY` p
				 LEFT JOIN `BOOKING` b ON p.property_id = b.property_id
				 LEFT JOIN `REVIEW` r ON b.Booking_id = r.booking_id
				 GROUP BY p.property_id
				 ORDER BY booking_count DESC
				 LIMIT %s;'''
		self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getTopOwners(self, limit=10):
		self.data = []
		sql = '''SELECT po.*,
				        COUNT(DISTINCT p.property_id) as property_count,
				        COUNT(DISTINCT b.Booking_id) as total_bookings
				 FROM `PROPERTYOWNER` po
				 LEFT JOIN `PROPERTY` p ON po.owner_id = p.owner_id
				 LEFT JOIN `BOOKING` b ON p.property_id = b.property_id
				 GROUP BY po.owner_id
				 ORDER BY total_bookings DESC
				 LIMIT %s;'''
		self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getBookingsByMonth(self, months=12):
		self.data = []
		sql = '''SELECT FLOOR(check_in_date / 100) AS month_key,
		                COUNT(*) AS booking_count
		         FROM `BOOKING`
		         WHERE check_in_date > 0
		         GROUP BY month_key
		         ORDER BY month_key ASC
		         LIMIT %s;'''
		self.cur.execute(sql, [months])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def searchUsers(self, query):
		self.data = []
		search_term = f'%{query}%'
		sql = '''SELECT * FROM `USER`
				 WHERE `first_name_` LIKE %s
				 OR `last_name_` LIKE %s
				 OR `email` LIKE %s;'''
		self.cur.execute(sql, [search_term, search_term, search_term])
		for row in self.cur:
			self.data.append(row)
		return self.data

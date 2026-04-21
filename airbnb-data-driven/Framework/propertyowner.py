from baseObject import baseObject


class PropertyOwner(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByOwnerId(self, owner_id):
		self.getByField('owner_id', owner_id)
		return self.data

	def getProfile(self, owner_id):
		self.data = []
		# PROPERTYOWNER table - return owner record directly
		self.getById(owner_id)
		return self.data

	def getProperties(self, owner_id):
		self.data = []
		sql = '''SELECT * FROM `PROPERTY` WHERE `owner_id` = %s;'''
		self.cur.execute(sql, [owner_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getPropertiesWithStats(self, owner_id):
		self.data = []
		# Join REVIEW through BOOKING since REVIEW has booking_id, not property_id
		sql = '''SELECT p.*,
				        COUNT(DISTINCT b.Booking_id) as total_bookings,
				        COALESCE(AVG(r.rating), 0) as avg_rating,
				        COUNT(DISTINCT r.review_id) as total_reviews
				 FROM `PROPERTY` p
				 LEFT JOIN `BOOKING` b ON p.property_id = b.property_id
				 LEFT JOIN `REVIEW` r ON b.Booking_id = r.booking_id
				 WHERE p.owner_id = %s
				 GROUP BY p.property_id;'''
		self.cur.execute(sql, [owner_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getTotalEarnings(self, owner_id):
		sql = '''SELECT
					COUNT(DISTINCT b.Booking_id) AS total_bookings,
					COUNT(DISTINCT p.property_id) AS total_properties,
					COALESCE(SUM(
						DATEDIFF(
							STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
							STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
						) * p.price_per_night
					), 0) AS total_earnings
				 FROM `PROPERTY` p
				 LEFT JOIN `BOOKING` b ON p.property_id = b.property_id
				 WHERE p.owner_id = %s;'''
		self.cur.execute(sql, [owner_id])
		result = self.cur.fetchone()
		return {
			'total_earnings':   int(result['total_earnings']   or 0),
			'total_bookings':   int(result['total_bookings']   or 0),
			'total_properties': int(result['total_properties'] or 0)
		}

	def getBookingsForOwner(self, owner_id):
		self.data = []
		sql = '''SELECT b.*, p.title as property_title
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 AND p.owner_id = %s
				 ORDER BY b.check_in_date DESC;'''
		self.cur.execute(sql, [owner_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getUpcomingBookings(self, owner_id):
		self.data = []
		from datetime import date
		today_int = int(date.today().strftime('%Y%m%d'))
		sql = '''SELECT b.*, p.title as property_title
				 FROM `BOOKING` b, `PROPERTY` p
				 WHERE b.property_id = p.property_id
				 AND p.owner_id = %s
				 AND b.check_out_date >= %s
				 ORDER BY b.check_in_date ASC;'''
		self.cur.execute(sql, [owner_id, today_int])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getReviewsReceived(self, owner_id):
		self.data = []
		# REVIEW has owner_id directly
		sql = '''SELECT r.*
				 FROM `REVIEW` r
				 WHERE r.owner_id = %s
				 ORDER BY r.dated_posted_ DESC;'''
		self.cur.execute(sql, [owner_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getAverageRating(self, owner_id):
		sql = '''SELECT AVG(r.rating) as avg_rating, COUNT(*) as total_reviews
				 FROM `REVIEW` r
				 WHERE r.owner_id = %s;'''
		self.cur.execute(sql, [owner_id])
		result = self.cur.fetchone()
		return {
			'average_rating': round(float(result['avg_rating']), 2) if result['avg_rating'] else 0,
			'total_reviews': result['total_reviews']
		}

	def getEarningsByProperty(self, owner_id):
		self.data = []
		sql = '''SELECT p.property_id, p.title, p.price_per_night,
					COUNT(b.Booking_id) AS bookings,
					COALESCE(SUM(
						DATEDIFF(
							STR_TO_DATE(CAST(b.check_out_date AS CHAR), '%%Y%%m%%d'),
							STR_TO_DATE(CAST(b.check_in_date  AS CHAR), '%%Y%%m%%d')
						) * p.price_per_night
					), 0) AS revenue
				 FROM `PROPERTY` p
				 LEFT JOIN `BOOKING` b ON p.property_id = b.property_id
				 WHERE p.owner_id = %s
				 GROUP BY p.property_id
				 ORDER BY revenue DESC;'''
		self.cur.execute(sql, [owner_id])
		for row in self.cur:
			self.data.append(row)
		return self.data

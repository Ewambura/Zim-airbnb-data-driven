from baseObject import baseObject
import datetime


class Review(baseObject):
	def __init__(self, config_path='config.yml'):
		self.setup(config_path)

	def getByGuestId(self, guest_id):
		self.getByField('guest_id', guest_id)
		return self.data

	def getByOwnerId(self, owner_id):
		self.getByField('owner_id', owner_id)
		return self.data

	def getByBookingId(self, booking_id):
		self.getByField('booking_id', booking_id)
		return self.data

	def getAverageRatingForOwner(self, owner_id):
		sql = '''SELECT AVG(`rating`) as avg_rating, COUNT(*) as total_reviews
				 FROM `REVIEW` WHERE `owner_id` = %s;'''
		self.cur.execute(sql, [owner_id])
		result = self.cur.fetchone()
		return {
			'average_rating': float(result['avg_rating']) if result['avg_rating'] else 0,
			'total_reviews': result['total_reviews']
		}

	def verifyGuestHasBooking(self, guest_id, booking_id):
		sql = '''SELECT 1 FROM `BOOKING`
				 WHERE `guest_id` = %s AND `Booking_id` = %s;'''
		self.cur.execute(sql, [guest_id, booking_id])
		result = self.cur.fetchone()
		return result is not None

	def hasReviewedBooking(self, guest_id, booking_id):
		sql = '''SELECT 1 FROM `REVIEW`
				 WHERE `guest_id` = %s AND `booking_id` = %s;'''
		self.cur.execute(sql, [guest_id, booking_id])
		result = self.cur.fetchone()
		return result is not None

	def createReview(self, guest_id, booking_id, owner_id, rating, comment, review_type='property'):
		if not self.verifyGuestHasBooking(guest_id, booking_id):
			return {'success': False, 'error': 'You can only review bookings you have made'}

		if self.hasReviewedBooking(guest_id, booking_id):
			return {'success': False, 'error': 'You have already reviewed this booking'}

		if rating < 1 or rating > 5:
			return {'success': False, 'error': 'Rating must be between 1 and 5'}

		review_data = {
			'guest_id': guest_id,
			'booking_id': booking_id,
			'owner_id': owner_id,
			'rating': rating,
			'comment': comment,
			'review_type': review_type,
			'dated_posted_': datetime.datetime.now().strftime('%Y-%m-%d')
		}
		self.set(review_data)
		self.insert()
		return {'success': True, 'review_id': self.data[0].get(self.pk)}

	def filterByRating(self, min_rating, owner_id=None):
		self.data = []
		if owner_id:
			sql = f'''SELECT * FROM `{self.tn}`
					  WHERE `rating` >= %s AND `owner_id` = %s
					  ORDER BY `rating` DESC;'''
			self.cur.execute(sql, [min_rating, owner_id])
		else:
			sql = f'''SELECT * FROM `{self.tn}`
					  WHERE `rating` >= %s
					  ORDER BY `rating` DESC;'''
			self.cur.execute(sql, [min_rating])
		for row in self.cur:
			self.data.append(row)
		return self.data

	def getRecentReviews(self, limit=10, owner_id=None):
		self.data = []
		if owner_id:
			sql = f'''SELECT * FROM `{self.tn}`
					  WHERE `owner_id` = %s
					  ORDER BY `dated_posted_` DESC LIMIT %s;'''
			self.cur.execute(sql, [owner_id, limit])
		else:
			sql = f'''SELECT * FROM `{self.tn}`
					  ORDER BY `dated_posted_` DESC LIMIT %s;'''
			self.cur.execute(sql, [limit])
		for row in self.cur:
			self.data.append(row)
		return self.data

"""
ZimBnB Test Suite
=================
Comprehensive unit tests for all model classes.
Run with: python test.py
"""

import unittest
import os

# Import all model classes
from property import Property
from booking import Booking
from review import Review
# Availability table was folded into PROPERTY (available_from, available_to, is_available)
from propertyimage import Property_Image
from guest import Guest
from propertyowner import PropertyOwner
from admin import Admin
from user import user

# Config path relative to Framework directory
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yml')


class TestProperty(unittest.TestCase):
	"""Test Property class methods."""

	@classmethod
	def setUpClass(cls):
		cls.prop = Property(CONFIG_PATH)

	def test_getAll_returns_list(self):
		"""getAll should return a list."""
		self.prop.getAll()
		self.assertIsInstance(self.prop.data, list)

	def test_getByCity_returns_list(self):
		"""getByCity should return a list."""
		result = self.prop.getByCity('Harare')
		self.assertIsInstance(result, list)

	def test_getByPriceRange_returns_list(self):
		"""getByPriceRange should return a list."""
		result = self.prop.getByPriceRange(min_price=50, max_price=500)
		self.assertIsInstance(result, list)

	def test_getByMinBedrooms_returns_list(self):
		"""getByMinBedrooms should return a list."""
		result = self.prop.getByMinBedrooms(1)
		self.assertIsInstance(result, list)

	def test_getByMinGuests_returns_list(self):
		"""getByMinGuests should return a list (uses max_guests column)."""
		result = self.prop.getByMinGuests(2)
		self.assertIsInstance(result, list)

	def test_filterProperties_returns_list(self):
		"""filterProperties should return a list."""
		result = self.prop.filterProperties()
		self.assertIsInstance(result, list)

	def test_verifyOwnership_returns_bool(self):
		"""verifyOwnership should return boolean."""
		result = self.prop.verifyOwnership(1, 1)
		self.assertIsInstance(result, bool)

	def test_createProperty_missing_fields(self):
		"""createProperty without required fields should fail."""
		result = self.prop.createProperty(
			owner_id=1, title=None, description='Test', address='123 Test',
			city='Test', province='Harare', property_type='apartment', price_per_night=100,
			num_bedrooms=2, num_bathrooms=1, num_guests=4
		)
		self.assertFalse(result['success'])

	def test_createProperty_invalid_price(self):
		"""createProperty with zero price should fail."""
		result = self.prop.createProperty(
			owner_id=1, title='Test', description='Test', address='123 Test',
			city='Test', province='Harare', property_type='apartment', price_per_night=0,
			num_bedrooms=2, num_bathrooms=1, num_guests=4
		)
		self.assertFalse(result['success'])

	def test_updateProperty_wrong_owner(self):
		"""updateProperty should require ownership."""
		result = self.prop.updateProperty(property_id=1, owner_id=99999, title='New')
		self.assertFalse(result['success'])
		self.assertIn('do not own', result['error'])

	def test_deleteProperty_wrong_owner(self):
		"""deleteProperty should require ownership."""
		result = self.prop.deleteProperty(property_id=1, owner_id=99999)
		self.assertFalse(result['success'])
		self.assertIn('do not own', result['error'])


class TestBooking(unittest.TestCase):
	"""Test Booking class methods."""

	@classmethod
	def setUpClass(cls):
		cls.booking = Booking(CONFIG_PATH)

	def test_getByGuestId_returns_list(self):
		"""getByGuestId should return a list."""
		result = self.booking.getByGuestId(1)
		self.assertIsInstance(result, list)

	def test_getByPropertyId_returns_list(self):
		"""getByPropertyId should return a list."""
		result = self.booking.getByPropertyId(1)
		self.assertIsInstance(result, list)

	def test_checkAvailability_returns_bool(self):
		"""checkAvailability should return boolean."""
		result = self.booking.checkAvailability(1, 20300101, 20300105)
		self.assertIsInstance(result, bool)

	def test_getUpcoming_returns_list(self):
		"""getUpcoming should return a list."""
		result = self.booking.getUpcoming(1)
		self.assertIsInstance(result, list)

	def test_getPast_returns_list(self):
		"""getPast should return a list."""
		result = self.booking.getPast(1)
		self.assertIsInstance(result, list)

	def test_createBooking_checkout_before_checkin(self):
		"""createBooking should reject checkout before checkin."""
		result = self.booking.createBooking(
			property_id=1, guest_id=1, check_in=20300110, check_out=20300105, num_guests=2
		)
		self.assertFalse(result['success'])

	def test_cancelBooking_wrong_guest(self):
		"""cancelBooking should only allow booking owner to cancel."""
		result = self.booking.cancelBooking(booking_id=1, guest_id=99999)
		self.assertFalse(result['success'])


class TestReview(unittest.TestCase):
	"""Test Review class methods."""

	@classmethod
	def setUpClass(cls):
		cls.review = Review(CONFIG_PATH)

	def test_getByGuestId_returns_list(self):
		"""getByGuestId should return a list."""
		result = self.review.getByGuestId(1)
		self.assertIsInstance(result, list)

	def test_getByOwnerId_returns_list(self):
		"""getByOwnerId should return a list."""
		result = self.review.getByOwnerId(1)
		self.assertIsInstance(result, list)

	def test_getByBookingId_returns_list(self):
		"""getByBookingId should return a list."""
		result = self.review.getByBookingId(1)
		self.assertIsInstance(result, list)

	def test_getAverageRatingForOwner_returns_dict(self):
		"""getAverageRatingForOwner should return dict."""
		result = self.review.getAverageRatingForOwner(1)
		self.assertIn('average_rating', result)
		self.assertIn('total_reviews', result)

	def test_filterByRating_returns_list(self):
		"""filterByRating should return a list."""
		result = self.review.filterByRating(3)
		self.assertIsInstance(result, list)

	def test_getRecentReviews_returns_list(self):
		"""getRecentReviews should return a list."""
		result = self.review.getRecentReviews(10)
		self.assertIsInstance(result, list)


class TestPropertyImage(unittest.TestCase):
	"""Test Property_Image class methods."""

	@classmethod
	def setUpClass(cls):
		cls.img = Property_Image(CONFIG_PATH)

	def test_getByPropertyId_returns_list(self):
		"""getByPropertyId should return a list."""
		result = self.img.getByPropertyId(1)
		self.assertIsInstance(result, list)

	def test_getImageById_returns_list(self):
		"""getImageById should return a list."""
		result = self.img.getImageById(1)
		self.assertIsInstance(result, list)

	def test_verifyOwnership_returns_bool(self):
		"""verifyOwnership should return boolean."""
		result = self.img.verifyOwnership(1, 1)
		self.assertIsInstance(result, bool)

	def test_createImage_wrong_owner(self):
		"""createImage should verify ownership."""
		result = self.img.createImage(
			property_id=1, owner_id=99999, caption='Test', image_url='http://test.com/img.jpg'
		)
		self.assertFalse(result['success'])
		self.assertIn('do not own', result['error'])

	def test_updateImage_not_found(self):
		"""updateImage should return error if image not found."""
		result = self.img.updateImage(image_id=99999, owner_id=1, caption='New')
		self.assertFalse(result['success'])
		self.assertIn('not found', result['error'])

	def test_deleteImage_not_found(self):
		"""deleteImage should return error if image not found."""
		result = self.img.deleteImage(image_id=99999, owner_id=1)
		self.assertFalse(result['success'])
		self.assertIn('not found', result['error'])


class TestGuest(unittest.TestCase):
	"""Test Guest class methods."""

	@classmethod
	def setUpClass(cls):
		cls.guest = Guest(CONFIG_PATH)

	def test_getByGuestId_returns_list(self):
		"""getByGuestId should return a list."""
		result = self.guest.getByGuestId(1)
		self.assertIsInstance(result, list)

	def test_getProfile_returns_list(self):
		"""getProfile should return a list."""
		result = self.guest.getProfile(1)
		self.assertIsInstance(result, list)

	def test_getBookingHistory_returns_list(self):
		"""getBookingHistory should return a list."""
		result = self.guest.getBookingHistory(1)
		self.assertIsInstance(result, list)

	def test_getTotalSpent_returns_dict(self):
		"""getTotalSpent should return dict."""
		result = self.guest.getTotalSpent(1)
		self.assertIn('total_spent', result)
		self.assertIn('total_bookings', result)

	def test_getReviewsWritten_returns_list(self):
		"""getReviewsWritten should return a list."""
		result = self.guest.getReviewsWritten(1)
		self.assertIsInstance(result, list)

	def test_getFavoriteProperties_returns_list(self):
		"""getFavoriteProperties should return a list."""
		result = self.guest.getFavoriteProperties(1)
		self.assertIsInstance(result, list)

	def test_getUpcomingBookings_returns_list(self):
		"""getUpcomingBookings should return a list."""
		result = self.guest.getUpcomingBookings(1)
		self.assertIsInstance(result, list)


class TestPropertyOwner(unittest.TestCase):
	"""Test PropertyOwner class methods."""

	@classmethod
	def setUpClass(cls):
		cls.owner = PropertyOwner(CONFIG_PATH)

	def test_getByOwnerId_returns_list(self):
		"""getByOwnerId should return a list."""
		result = self.owner.getByOwnerId(1)
		self.assertIsInstance(result, list)

	def test_getProfile_returns_list(self):
		"""getProfile should return a list."""
		result = self.owner.getProfile(1)
		self.assertIsInstance(result, list)

	def test_getProperties_returns_list(self):
		"""getProperties should return a list."""
		result = self.owner.getProperties(1)
		self.assertIsInstance(result, list)

	def test_getPropertiesWithStats_returns_list(self):
		"""getPropertiesWithStats should return a list."""
		result = self.owner.getPropertiesWithStats(1)
		self.assertIsInstance(result, list)

	def test_getTotalEarnings_returns_dict(self):
		"""getTotalEarnings should return dict."""
		result = self.owner.getTotalEarnings(1)
		self.assertIn('total_earnings', result)
		self.assertIn('total_bookings', result)

	def test_getBookingsForOwner_returns_list(self):
		"""getBookingsForOwner should return a list."""
		result = self.owner.getBookingsForOwner(1)
		self.assertIsInstance(result, list)

	def test_getReviewsReceived_returns_list(self):
		"""getReviewsReceived should return a list."""
		result = self.owner.getReviewsReceived(1)
		self.assertIsInstance(result, list)

	def test_getAverageRating_returns_dict(self):
		"""getAverageRating should return dict."""
		result = self.owner.getAverageRating(1)
		self.assertIn('average_rating', result)
		self.assertIn('total_reviews', result)

	def test_getEarningsByProperty_returns_list(self):
		"""getEarningsByProperty should return a list."""
		result = self.owner.getEarningsByProperty(1)
		self.assertIsInstance(result, list)


class TestAdmin(unittest.TestCase):
	"""Test Admin class methods."""

	@classmethod
	def setUpClass(cls):
		cls.admin = Admin(CONFIG_PATH)

	def test_getByAdminId_returns_list(self):
		"""getByAdminId should return a list."""
		result = self.admin.getByAdminId(1)
		self.assertIsInstance(result, list)

	def test_getAllUsers_returns_list(self):
		"""getAllUsers should return a list."""
		result = self.admin.getAllUsers()
		self.assertIsInstance(result, list)

	def test_getUsersByRole_returns_list(self):
		"""getUsersByRole should return a list."""
		result = self.admin.getUsersByRole('admin')
		self.assertIsInstance(result, list)

	def test_getAllBookings_returns_list(self):
		"""getAllBookings should return a list."""
		result = self.admin.getAllBookings(10)
		self.assertIsInstance(result, list)

	def test_getAllProperties_returns_list(self):
		"""getAllProperties should return a list."""
		result = self.admin.getAllProperties()
		self.assertIsInstance(result, list)

	def test_getPlatformStats_returns_dict(self):
		"""getPlatformStats should return dict with all stats."""
		result = self.admin.getPlatformStats()
		self.assertIn('total_users', result)
		self.assertIn('total_properties', result)
		self.assertIn('total_bookings', result)

	def test_getRecentActivity_returns_list(self):
		"""getRecentActivity should return a list."""
		result = self.admin.getRecentActivity(10)
		self.assertIsInstance(result, list)

	def test_getRecentReviews_returns_list(self):
		"""getRecentReviews should return a list."""
		result = self.admin.getRecentReviews(10)
		self.assertIsInstance(result, list)

	def test_getTopProperties_returns_list(self):
		"""getTopProperties should return a list."""
		result = self.admin.getTopProperties(5)
		self.assertIsInstance(result, list)

	def test_getTopOwners_returns_list(self):
		"""getTopOwners should return a list."""
		result = self.admin.getTopOwners(5)
		self.assertIsInstance(result, list)

	def test_searchUsers_returns_list(self):
		"""searchUsers should return a list."""
		result = self.admin.searchUsers('test')
		self.assertIsInstance(result, list)


class TestUser(unittest.TestCase):
	"""Test user class methods."""

	@classmethod
	def setUpClass(cls):
		cls.usr = user(CONFIG_PATH)

	def test_rolelist_returns_list(self):
		"""rolelist should return list of roles."""
		result = self.usr.rolelist()
		self.assertIsInstance(result, list)
		self.assertIn('admin', result)
		self.assertIn('guest', result)

	def test_hashpassword_returns_string(self):
		"""hashpassword should return MD5 hash string."""
		result = self.usr.hashpassword('test123')
		self.assertIsInstance(result, str)
		self.assertEqual(len(result), 32)

	def test_hashpassword_consistent(self):
		"""hashpassword should return same hash for same input."""
		hash1 = self.usr.hashpassword('password')
		hash2 = self.usr.hashpassword('password')
		self.assertEqual(hash1, hash2)

	def test_tryLogin_returns_bool(self):
		"""tryLogin should return boolean."""
		result = self.usr.tryLogin('nonexistent@email.com', 'wrongpass')
		self.assertIsInstance(result, bool)


if __name__ == '__main__':
	unittest.main(verbosity=2)

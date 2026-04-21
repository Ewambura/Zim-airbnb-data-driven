# ZimBnB API Documentation

## Overview
This document describes all methods available in the ZimBnB application layer classes.

---

## 1. baseObject ([Framework/baseObject.py](Framework/baseObject.py))

Base class providing core CRUD operations for all models.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `setup(config_path)` | config_path: str | None | Initializes DB connection, loads config |
| `set(d)` | d: dict | None | Sets data to a list containing the dict |
| `getFields()` | None | None | Retrieves table fields from DB |
| `insert(n=0)` | n: int | None | Inserts record using self.data[n] |
| `getAll(order='')` | order: str | None | Gets all records, optional ORDER BY |
| `getById(id)` | id: int | None | Gets record by primary key |
| `getByField(fieldname, value)` | fieldname: str, value: any | None | Gets records where field = value |
| `deleteById(id)` | id: int | None | Deletes record by primary key |
| `update(id, n=0)` | id: int, n: int | None | **NEW** - Updates record by primary key |

---

## 2. Property ([Framework/property.py](Framework/property.py))

Manages property listings.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByOwnerId(owner_id)` | owner_id: int | list | Gets all properties for an owner |
| `getByCity(city)` | city: str | list | Filter by city (case-insensitive) |
| `getByPriceRange(min_price, max_price)` | min_price: float, max_price: float | list | Filter by price range |
| `getByMinBedrooms(min_bedrooms)` | min_bedrooms: int | list | Filter by min bedrooms |
| `getByPropertyType(property_type)` | property_type: str | list | Filter by type |
| `getByMinGuests(min_guests)` | min_guests: int | list | Filter by guest capacity |
| `filterProperties(...)` | city, min_price, max_price, min_bedrooms, property_type, min_guests, order_by | list | Combined filter (all optional) |
| `verifyOwnership(property_id, owner_id)` | property_id: int, owner_id: int | bool | **NEW** - Check if owner owns property |
| `createProperty(owner_id, title, ...)` | owner_id, title, description, address, city, property_type, price_per_night, num_bedrooms, num_bathrooms, num_guests | dict | **NEW** - Create property with validation |
| `updateProperty(property_id, owner_id, ...)` | property_id: int, owner_id: int, **kwargs | dict | **NEW** - Update property (ownership verified) |
| `deleteProperty(property_id, owner_id)` | property_id: int, owner_id: int | dict | **NEW** - Delete property (checks active bookings) |

---

## 3. Property_Image ([Framework/propertyimage.py](Framework/propertyimage.py))

Manages property images with ownership verification.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByPropertyId(property_id)` | property_id: int | list | Gets all images for a property |
| `getImageById(image_id)` | image_id: int | list | **NEW** - Get single image |
| `verifyOwnership(property_id, owner_id)` | property_id: int, owner_id: int | bool | **NEW** - Check if owner owns property |
| `createImage(property_id, owner_id, caption, url_attached, date_uploaded)` | ... | dict | **NEW** - Create image with ownership check |
| `updateImage(image_id, owner_id, caption, url_attached)` | ... | dict | **NEW** - Update image with ownership check |
| `deleteImage(image_id, owner_id)` | image_id: int, owner_id: int | dict | **NEW** - Delete image with ownership check |

---

## 4. Booking ([Framework/booking.py](Framework/booking.py))

Manages property bookings.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByGuestId(guest_id)` | guest_id: int | list | Gets bookings for a guest |
| `getByPropertyId(property_id)` | property_id: int | list | **NEW** - Gets bookings for a property |
| `getByDateRange(start_date, end_date)` | start_date: str, end_date: str | list | **NEW** - Filter by date range |
| `checkAvailability(property_id, check_in, check_out)` | ... | bool | **NEW** - Check if dates available |
| `createBooking(property_id, guest_id, check_in, check_out, num_guests)` | ... | dict | **NEW** - Create booking with validation |
| `cancelBooking(booking_id, guest_id)` | booking_id: int, guest_id: int | dict | **NEW** - Cancel booking (guest verified) |
| `getUpcoming(guest_id)` | guest_id: int | list | **NEW** - Get future bookings |
| `getPast(guest_id)` | guest_id: int | list | **NEW** - Get past bookings |

---

## 5. Review ([Framework/review.py](Framework/review.py))

Manages property reviews.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByGuestId(guest_id)` | guest_id: int | list | Gets reviews by a guest |
| `getByOwnerId(owner_id)` | owner_id: int | list | Gets reviews for an owner |
| `getByPropertyId(property_id)` | property_id: int | list | **NEW** - Gets reviews for a property |
| `getAverageRating(property_id)` | property_id: int | dict | **NEW** - Returns {average_rating, total_reviews} |
| `verifyGuestStayed(guest_id, property_id)` | ... | bool | **NEW** - Check if guest completed stay |
| `hasReviewed(guest_id, property_id)` | ... | bool | **NEW** - Check if already reviewed |
| `createReview(guest_id, property_id, owner_id, rating, comments)` | ... | dict | **NEW** - Create review with validation |
| `filterByRating(min_rating, property_id)` | min_rating: int, property_id: int | list | **NEW** - Filter by min rating |
| `getRecentReviews(limit, property_id)` | limit: int, property_id: int | list | **NEW** - Get recent reviews |

---

## 6. Availability ([Framework/availability.py](Framework/availability.py))

Manages property availability dates.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByPropertyId(property_id)` | property_id: int | list | Gets all availability for property |
| `getAvailableDates(property_id, start_date, end_date)` | ... | list | **NEW** - Get available dates |
| `getUnavailableDates(property_id)` | property_id: int | list | **NEW** - Get blocked dates |
| `checkDateRange(property_id, start_date, end_date)` | ... | bool | **NEW** - Check if range available |
| `setDateAvailability(property_id, avail_date, is_available, owner_id)` | ... | dict | **NEW** - Set single date |
| `blockDates(property_id, start_date, end_date, owner_id)` | ... | dict | **NEW** - Block date range |
| `unblockDates(property_id, start_date, end_date, owner_id)` | ... | dict | **NEW** - Unblock date range |

---

## 7. Guest ([Framework/guest.py](Framework/guest.py))

Manages guest profiles and history.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByUserId(user_id)` | user_id: int | list | Gets guest by user ID |
| `getProfile(guest_id)` | guest_id: int | list | **NEW** - Full profile with user details (JOIN) |
| `getBookingHistory(guest_id)` | guest_id: int | list | **NEW** - All bookings with property info |
| `getTotalSpent(guest_id)` | guest_id: int | dict | **NEW** - Returns {total_spent, total_bookings} |
| `getReviewsWritten(guest_id)` | guest_id: int | list | **NEW** - All reviews by guest |
| `getFavoriteProperties(guest_id)` | guest_id: int | list | **NEW** - Properties booked > 1 time |
| `getUpcomingBookings(guest_id)` | guest_id: int | list | **NEW** - Future bookings |

---

## 8. PropertyOwner ([Framework/propertyowner.py](Framework/propertyowner.py))

Manages property owner profiles and business metrics.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByUserId(user_id)` | user_id: int | list | Gets owner by user ID |
| `getProfile(owner_id)` | owner_id: int | list | **NEW** - Full profile with user details |
| `getProperties(owner_id)` | owner_id: int | list | **NEW** - All properties owned |
| `getPropertiesWithStats(owner_id)` | owner_id: int | list | **NEW** - Properties with booking/rating stats |
| `getTotalEarnings(owner_id)` | owner_id: int | dict | **NEW** - Returns {total_earnings, total_bookings, total_properties} |
| `getBookingsForOwner(owner_id)` | owner_id: int | list | **NEW** - All bookings across properties |
| `getUpcomingBookings(owner_id)` | owner_id: int | list | **NEW** - Future bookings |
| `getReviewsReceived(owner_id)` | owner_id: int | list | **NEW** - All reviews for owner's properties |
| `getAverageRating(owner_id)` | owner_id: int | dict | **NEW** - Returns {average_rating, total_reviews} |
| `getEarningsByProperty(owner_id)` | owner_id: int | list | **NEW** - Earnings breakdown per property |

---

## 9. Admin ([Framework/admin.py](Framework/admin.py))

Platform administration and statistics.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getByUserId(user_id)` | user_id: int | list | Gets admin by user ID |
| `getAllUsers()` | None | list | **NEW** - All users in system |
| `getUsersByRole(role)` | role: str | list | **NEW** - Filter users by role |
| `getAllBookings(limit)` | limit: int | list | **NEW** - Recent bookings platform-wide |
| `getAllProperties()` | None | list | **NEW** - All properties with owner info |
| `getPlatformStats()` | None | dict | **NEW** - Dashboard stats (users, revenue, etc.) |
| `getRecentActivity(limit)` | limit: int | list | **NEW** - Recent booking activity |
| `getRecentReviews(limit)` | limit: int | list | **NEW** - Recent reviews |
| `getTopProperties(limit)` | limit: int | list | **NEW** - Most booked properties |
| `getTopOwners(limit)` | limit: int | list | **NEW** - Highest earning owners |
| `searchUsers(query)` | query: str | list | **NEW** - Search users by name/email |

---

## Summary Statistics

| Class | Original Methods | New Methods | Total |
|-------|------------------|-------------|-------|
| baseObject | 8 | 1 | 9 |
| Property | 1 | 10 | 11 |
| Property_Image | 1 | 5 | 6 |
| Booking | 1 | 7 | 8 |
| Review | 2 | 7 | 9 |
| Availability | 1 | 6 | 7 |
| Guest | 1 | 6 | 7 |
| PropertyOwner | 1 | 9 | 10 |
| Admin | 1 | 10 | 11 |
| **TOTAL** | **17** | **61** | **78** |

---

## Return Value Conventions

### Success/Error Dict Pattern
Methods that modify data return:
```python
{'success': True, 'record_id': 123}  # On success
{'success': False, 'error': 'Error message'}  # On failure
```

### Aggregate Dict Pattern
Methods that return statistics:
```python
{'average_rating': 4.5, 'total_reviews': 25}
{'total_spent': 1500.00, 'total_bookings': 5}
```

### List Pattern
Most query methods populate and return `self.data`:
```python
[{'id': 1, 'name': '...'}, {'id': 2, 'name': '...'}]
```

---

## Security Features

1. **SQL Injection Prevention**: All methods use parameterized queries with `%s` placeholders
2. **Ownership Verification**: Image/Availability modifications check property ownership
3. **Guest Verification**: Booking cancellation verifies guest ownership
4. **Review Validation**: Reviews require completed stay + no duplicates
5. **ORDER BY Whitelist**: filterProperties() only allows safe column names

---

*Generated for ZimBnB Data-Driven Project*

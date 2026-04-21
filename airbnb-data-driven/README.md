# ZimBnB - Property Rental Platform

A data-driven property rental application for Zimbabwe, built with Python/Flask and MySQL. ZimBnB connects property owners with guests seeking short-term accommodation across all ten provinces of Zimbabwe.

---

## Business Rules

### Users & Accounts
- Anyone can register with a **unique email** and a password of at least 3 characters
- Passwords are stored securely (hashed — never plain text)
- Two roles exist: **Guest/Owner** (customers) and **Admin** (platform staff)

### Properties
- Any owner can create a listing — price per night must be greater than $0
- Only the **property owner** can edit, update, or delete their own listings
- A property **cannot be deleted** if it has current or upcoming bookings
- Owners can add and remove photos from their own properties
- Properties are listed across Zimbabwe's 10 provinces

### Availability
- Only the property owner can set availability dates on their listing
- Properties have an availability range (start date, end date) and status flag

### Bookings
- Guests can book any available property
- Check-out date must be **after** check-in (minimum 1 night)
- The system checks for conflicts — **no double-bookings** allowed
- Only the guest who made a booking can cancel it

### Reviews
- A guest can only review a property **after completing a stay** there
- Each guest can leave **one review per property**
- Ratings must be between **1 and 5**

### Admins
- Admins have full access to manage users, properties, bookings, and reviews across the platform

---

## Quick Start

```bash
cd Framework
python3 app.py
```

The app runs on `http://localhost:5001`

## Running Tests

```bash
cd Framework
python3 test.py -v
```

61 unit tests covering all model classes.

---

## Database Schema

### Tables (8 total)
- `USER` - All user accounts with authentication credentials
- `ADMIN` - Administrator profiles (subtype of USER)
- `GUEST` - Guest profiles (subtype of USER)
- `PROPERTYOWNER` - Property owner profiles (subtype of USER)
- `PROPERTY` - Property listings with details, pricing, and availability
- `PROPERTY_IMAGE` - Property photos
- `BOOKING` - Reservations
- `REVIEW` - Guest reviews and ratings

### Key Relationships
- Each property belongs to one property owner
- Each booking links one guest to one property
- Each review links one guest to one property they stayed at
- ADMIN, GUEST, and PROPERTYOWNER are subtypes of USER

---

## Project Structure

```
airbnb-data-driven/
├── Framework/
│   ├── app.py              # Flask application
│   ├── baseObject.py       # Base ORM class
│   ├── property.py         # Property management
│   ├── booking.py          # Booking logic
│   ├── review.py           # Review system
│   ├── propertyimage.py    # Image handling
│   ├── guest.py            # Guest functions
│   ├── propertyowner.py    # Owner functions
│   ├── admin.py            # Admin functions
│   ├── user.py             # Authentication
│   └── test.py             # Unit tests
├── templates/              # HTML templates
├── static/                 # CSS and uploads
├── config.yml              # Database config
└── API_DOCUMENTATION.md    # API reference
```

---

## Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.

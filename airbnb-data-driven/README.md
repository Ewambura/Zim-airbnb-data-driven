# ZimBnB — Property Rental Platform

A data-driven property rental web application for Zimbabwe, built with Python (Flask) and MySQL. ZimBnB connects property owners with guests seeking short-term accommodation across all ten provinces of Zimbabwe.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [User Types](#user-types)
3. [Demo Credentials](#demo-credentials)
4. [Use Cases](#use-cases)
5. [Relational Diagram](#relational-diagram)
6. [Database Schema](#database-schema)
7. [SQL Views](#sql-views)
8. [Business Rules](#business-rules)

---

## Project Overview

Group Members
1.Chris Zvikomborero 
2.Emmanuel Wambura

ZimBnB is a full-stack rental platform that allows property owners to list their properties and guests to search, book, and review them. An admin panel provides platform-wide oversight and management.

- **Backend:** Python / Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Architecture:** Data-driven ORM layer with parameterized queries

---

## User Types

The system has three distinct user types, each with their own dashboard and permissions.

| User Type | Description |
|-----------|-------------|
| **Guest** | Registered users who can search properties, make bookings, cancel bookings, and leave reviews after completed stays. |
| **Property Owner** | Registered users who can list properties, manage availability, upload images, and track bookings and earnings. |
| **Admin** | Platform staff with full access to manage all users, properties, bookings, and reviews across the system. |

---

## Demo Credentials

Use the following credentials to log in and explore each user role.

| Name | Role | Email | Password |
|------|------|-------|----------|
| Anderson Kuda | Admin | `kudademo@gmail.com` | `123xyz` |
| Boris Bsmith | Property Owner | `datademo@gmail.com` | `123xyz` |
| Pavi GA | Guest | `enddemo@gmail.com` | `123xyz` |

---

## Use Cases

### Guest
- Register and log in to the platform
- Browse and search available properties by location, price, bedrooms, and type
- View full property details and photos
- Book a property for a selected date range
- Cancel an existing booking
- Leave a review and rating after a completed stay
- View upcoming and past bookings from the dashboard

### Property Owner
- Register and log in to the platform
- Create, edit, and delete property listings
- Upload and manage property photos
- Set and manage availability dates for each property
- View all incoming bookings across their properties
- Track total earnings and per-property revenue breakdowns
- View reviews received from guests

### Admin
- View a platform-wide dashboard with key statistics (total users, bookings, revenue, average rating)
- Manage all registered users (view, search, reset passwords)
- View and manage all properties across the platform
- View and manage all bookings
- View and delete reviews
- Monitor recent platform activity

---

## Relational Diagram

![Relational Schema](static/Relational_schema.png)

---

## Database Schema

The database consists of **8 tables** using a supertype/subtype pattern for user roles.

| Table | Description |
|-------|-------------|
| `USER` | Core user accounts — stores credentials, role, and registration date for all users |
| `ADMIN` | Admin profile — subtype of USER, for platform staff |
| `GUEST` | Guest profile — subtype of USER, for guests making bookings |
| `PROPERTYOWNER` | Owner profile — subtype of USER, for property owners |
| `PROPERTY` | Property listings — title, description, location, pricing, and capacity |
| `PROPERTY_IMAGE` | Photos attached to property listings |
| `BOOKING` | Reservations linking a guest to a property with check-in/check-out dates |
| `REVIEW` | Ratings and comments left by guests after a completed stay |

### Key Relationships

- `ADMIN`, `GUEST`, and `PROPERTYOWNER` are all subtypes of `USER` (linked by `user_id`)
- Each `PROPERTY` belongs to one `PROPERTYOWNER`
- Each `BOOKING` links one `GUEST` to one `PROPERTY`
- Each `REVIEW` is tied to a `BOOKING`, linking a `GUEST` to a `PROPERTY` they have stayed at
- `PROPERTY_IMAGE` records are associated with a specific `PROPERTY`

---

## SQL Views

### View 1 — Property Performance Summary

**Purpose:** Returns each property alongside its total number of bookings and average guest rating. Useful for identifying top-performing listings and for owner dashboard reporting.

**Tables used:** `PROPERTY`, `BOOKING`, `REVIEW`

**Implemented as:** `getPropertiesWithStats(owner_id)` in `propertyowner.py`

---

### View 2 — Owner Earnings Overview

**Purpose:** Returns each property owner with their total number of properties, total bookings received, and total earnings across all their listings. Useful for admin-level financial reporting and owner dashboards.

**Tables used:** `PROPERTYOWNER`, `PROPERTY`, `BOOKING`

**Implemented as:** `getEarningsByProperty(owner_id)` in `propertyowner.py`

---

### View 3 — Guest Booking History with Property Details

**Purpose:** Returns a full history of bookings for each guest, including the property name, location, check-in/check-out dates, and total cost. Useful for guest dashboards and booking management.

**Tables used:** `GUEST`, `BOOKING`, `PROPERTY`

**Implemented as:** `getBookingHistory(guest_id)` in `guest.py`

---

## Business Rules

| Area | Rule |
|------|------|
| **Registration** | All users must register with a unique email and a password of at least 3 characters |
| **Passwords** | Passwords are stored securely as hashed values — never plain text |
| **Properties** | Price per night must be greater than $0 |
| **Ownership** | Only the property owner can edit, update, or delete their own listings |
| **Deletion** | A property cannot be deleted if it has current or upcoming bookings |
| **Availability** | Only the property owner can set availability dates for their listing |
| **Bookings** | Check-out date must be after check-in date (minimum 1 night) |
| **Double-booking** | The system checks for conflicts — no two bookings can overlap for the same property |
| **Cancellation** | Only the guest who made a booking can cancel it |
| **Reviews** | A guest can only leave a review after completing a stay at that property |
| **One review** | Each guest may leave only one review per property |
| **Ratings** | Ratings must be between 1 and 5 |
| **Admin access** | Admins have full access to manage all users, properties, bookings, and reviews |
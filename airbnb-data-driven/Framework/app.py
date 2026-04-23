from flask import Flask, render_template, request, session, redirect, jsonify
from flask_session import Session
from datetime import timedelta
from functools import wraps
from werkzeug.utils import secure_filename
import os
import time

# Import models
from user import user
from guest import Guest
from propertyowner import PropertyOwner
from property import Property
from propertyimage import Property_Image
from booking import Booking
from review import Review
from admin import Admin

# Config path for models
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yml')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__, static_url_path='/static', static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

# ── Jinja2 filters ────────────────────────────────────────
@app.template_filter('fmt_date')
def fmt_date(date_int):
    """Convert YYYYMMDD integer → 'Apr 16, 2026'"""
    from datetime import datetime
    try:
        return datetime.strptime(str(int(date_int)), '%Y%m%d').strftime('%b %d, %Y')
    except Exception:
        return str(date_int)

@app.template_global()
def update_query(**kwargs):
    """Return a query string with current params updated by kwargs. Pass None to remove a key."""
    from urllib.parse import urlencode
    params = dict(request.args)
    for k, v in kwargs.items():
        if v is None:
            params.pop(k, None)
        else:
            params[k] = v
    return urlencode(params)

@app.template_filter('days_until')
def days_until(date_int):
    """Days from today until a YYYYMMDD integer date. Negative = past."""
    from datetime import date, datetime
    try:
        target = datetime.strptime(str(int(date_int)), '%Y%m%d').date()
        return (target - date.today()).days
    except Exception:
        return 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# Owner required decorator
def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'owner':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        if session.get('role') != 'admin':
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'user_id' in session:
        role = session.get('role', '')
        if role == 'guest':
            return redirect('/guest/dashboard')
        elif role == 'owner':
            return redirect('/owner/dashboard')
        elif role == 'admin':
            return redirect('/admin/dashboard')
    return redirect('/properties')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        u = user(CONFIG_PATH)
        if u.tryLogin(email, password):
            # Login successful - store user info in session
            session['user_id'] = u.data[0]['user_id']
            session['email'] = u.data[0]['email']
            session['first_name'] = u.data[0]['first_name_']
            session['last_name'] = u.data[0]['last_name_']
            session['role'] = u.data[0]['role']

            # Redirect based on role
            role = u.data[0]['role']
            if role == 'guest':
                return redirect('/guest/dashboard')
            elif role == 'owner':
                return redirect('/owner/dashboard')
            elif role == 'admin':
                return redirect('/admin/dashboard')
            else:
                return redirect('/properties')
        else:
            msg = 'Invalid email or password'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    success = False

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        role = request.form.get('role', 'guest')
        print(f"[DEBUG REGISTER] role={role!r} pw_len={len(password)} pw2_len={len(password2)} match={password==password2}")

        # Create user object and set data
        u = user(CONFIG_PATH)
        u.data = [{
            'first_name_': first_name,
            'last_name_': last_name,
            'email': email,
            'password': password,
            'password2': password2,
            'role': role
        }]

        # Validate using verify_new
        if u.verify_new():
            # Insert into USER table
            u.insert()
            new_user_id = u.data[0].get('user_id')

            # Insert into subtype table based on role
            if role == 'guest':
                g = Guest(CONFIG_PATH)
                g.data = [{
                    'guest_id': new_user_id,
                    'emergency_contact_name': '',
                    'emergency_contact_phone': ''
                }]
                g.insert()
            elif role == 'owner':
                o = PropertyOwner(CONFIG_PATH)
                o.data = [{
                    'owner_id': new_user_id,
                    'business_name_': f"{first_name} {last_name}",
                    'payout_method': 'pending'
                }]
                o.insert()

            success = True
        else:
            errors = u.errors

    return render_template('register.html', errors=errors, success=success)

@app.route('/showcase')
def showcase():
    return render_template('showcase.html')

# ==================== GUEST ROUTES ====================

@app.route('/guest/dashboard')
@login_required
def guest_dashboard():
    guest = Guest(CONFIG_PATH)

    upcoming = guest.getUpcomingBookings(session['user_id'])
    history = guest.getBookingHistory(session['user_id'])
    stats = guest.getTotalSpent(session['user_id'])

    return render_template('guest/dashboard.html',
                           upcoming=upcoming,
                           history=history,
                           stats=stats)

# ==================== PROPERTY ROUTES ====================

@app.route('/properties')
def properties_list():
    # Get filter parameters
    city = request.args.get('city', '')
    province = request.args.get('province', '')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    min_bedrooms = request.args.get('min_bedrooms', type=int)
    property_type = request.args.get('property_type', '')

    prop = Property(CONFIG_PATH)

    # Get provinces for dropdown
    provinces = prop.getDistinctProvinces()

    # Apply filters if any provided
    if any([city, province, min_price, max_price, min_bedrooms, property_type]):
        properties = prop.filterProperties(
            city=city if city else None,
            province=province if province else None,
            min_price=min_price,
            max_price=max_price,
            min_bedrooms=min_bedrooms,
            property_type=property_type if property_type else None
        )
    else:
        prop.getAll()
        properties = prop.data

    properties = prop.attachFirstImages(properties)
    return render_template('properties/list.html', properties=properties, provinces=provinces)

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    prop = Property(CONFIG_PATH)
    prop.getById(property_id)

    if not prop.data:
        return redirect('/properties')

    property_data = prop.data[0]

    # Get images
    img = Property_Image(CONFIG_PATH)
    images = img.getByPropertyId(property_id)

    # Get reviews for this property's owner
    rev = Review(CONFIG_PATH)
    reviews = rev.getByOwnerId(property_data['owner_id'])

    return render_template('properties/detail.html',
                           property=property_data,
                           images=images,
                           reviews=reviews)

# ==================== BOOKING ROUTES ====================

@app.route('/booking/create/<int:property_id>', methods=['GET', 'POST'])
@login_required
def booking_create(property_id):
    # Only guests can make bookings
    if session.get('role') != 'guest':
        return redirect('/properties')

    prop = Property(CONFIG_PATH)
    prop.getById(property_id)

    if not prop.data:
        return redirect('/properties')

    property_data = prop.data[0]
    msg = None
    success = False

    # Pre-fill values passed from the detail page via query params
    prefill_check_in   = request.args.get('check_in', '')
    prefill_check_out  = request.args.get('check_out', '')
    prefill_num_guests = request.args.get('num_guests', 1, type=int)

    if request.method == 'POST':
        check_in = request.form.get('check_in', '')
        check_out = request.form.get('check_out', '')
        num_guests = request.form.get('num_guests', type=int)

        # Convert dates to integer format YYYYMMDD
        try:
            check_in_int = int(check_in.replace('-', ''))
            check_out_int = int(check_out.replace('-', ''))
        except:
            msg = 'Invalid date format'
            return render_template('booking/create.html', property=property_data, msg=msg)

        book = Booking(CONFIG_PATH)
        result = book.createBooking(
            property_id=property_id,
            guest_id=session['user_id'],
            check_in=check_in_int,
            check_out=check_out_int,
            num_guests=num_guests
        )

        if result.get('success'):
            success = True
            msg = 'Booking created successfully!'
        else:
            msg = result.get('error', 'Booking failed')

    return render_template('booking/create.html',
                           property=property_data,
                           msg=msg,
                           success=success,
                           prefill_check_in=prefill_check_in,
                           prefill_check_out=prefill_check_out,
                           prefill_num_guests=prefill_num_guests)

@app.route('/booking/cancel/<int:booking_id>', methods=['POST'])
@login_required
def booking_cancel(booking_id):
    book = Booking(CONFIG_PATH)
    result = book.cancelBooking(booking_id, session['user_id'])

    # Redirect back to dashboard with appropriate message
    return redirect('/guest/dashboard')

# ==================== REVIEW ROUTES ====================

@app.route('/review/create/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def review_create(booking_id):
    if session.get('role') in ('admin', 'owner'):
        return redirect('/admin/dashboard' if session.get('role') == 'admin' else '/owner/dashboard')

    book = Booking(CONFIG_PATH)
    book.getById(booking_id)

    if not book.data:
        return redirect('/guest/dashboard')

    booking_data = book.data[0]

    # Verify this booking belongs to the logged-in user
    if booking_data['guest_id'] != session['user_id']:
        return redirect('/guest/dashboard')

    # Block review if checkout date has not yet passed
    from datetime import date
    today_int = int(date.today().strftime('%Y%m%d'))
    checkout_int = booking_data.get('check_out_date', 0)
    if int(checkout_int) >= today_int:
        return render_template('review/create.html',
                               booking=booking_data,
                               property={},
                               msg=None,
                               success=False,
                               too_early=True)

    # Get property info
    prop = Property(CONFIG_PATH)
    prop.getById(booking_data['property_id'])
    property_data = prop.data[0] if prop.data else {}

    msg = None
    success = False

    if request.method == 'POST':
        rating = request.form.get('rating', type=int)
        comment = request.form.get('comment', '')

        rev = Review(CONFIG_PATH)
        result = rev.createReview(
            guest_id=session['user_id'],
            booking_id=booking_id,
            owner_id=property_data.get('owner_id'),
            rating=rating,
            comment=comment
        )

        if result.get('success'):
            success = True
            msg = 'Review submitted successfully!'
        else:
            msg = result.get('error', 'Review submission failed')

    return render_template('review/create.html',
                           booking=booking_data,
                           property=property_data,
                           msg=msg,
                           success=success)

# ==================== OWNER ROUTES ====================

@app.route('/owner/dashboard')
@owner_required
def owner_dashboard():
    owner = PropertyOwner(CONFIG_PATH)

    stats       = owner.getTotalEarnings(session['user_id'])
    rating      = owner.getAverageRating(session['user_id'])
    upcoming    = owner.getUpcomingBookings(session['user_id'])
    reviews     = owner.getReviewsReceived(session['user_id'])[:5]
    by_property = owner.getEarningsByProperty(session['user_id'])
    max_revenue = max((p['revenue'] for p in by_property), default=1) or 1

    return render_template('owner/dashboard.html',
                           stats=stats,
                           rating=rating,
                           upcoming=upcoming,
                           reviews=reviews,
                           by_property=by_property,
                           max_revenue=max_revenue)

@app.route('/owner/properties')
@owner_required
def owner_properties():
    owner = PropertyOwner(CONFIG_PATH)
    properties = owner.getPropertiesWithStats(session['user_id'])

    return render_template('owner/properties.html', properties=properties)

@app.route('/owner/property/create', methods=['GET', 'POST'])
@owner_required
def owner_property_create():
    msg = None
    success = False

    if request.method == 'POST':
        price_raw = request.form.get('price_per_night', '')
        try:
            price_val = float(price_raw)
            if price_val != int(price_val) or int(price_val) < 1:
                raise ValueError
            price_per_night = int(price_val)
        except (ValueError, TypeError):
            msg = 'Price per night must be a whole number (e.g. 100), no decimals allowed.'
            return render_template('owner/property_form.html', property=None, msg=msg)

        prop = Property(CONFIG_PATH)
        result = prop.createProperty(
            owner_id=session['user_id'],
            title=request.form.get('title', ''),
            description=request.form.get('description', ''),
            address=request.form.get('address', ''),
            city=request.form.get('city', ''),
            province=request.form.get('province', ''),
            property_type=request.form.get('property_type', ''),
            price_per_night=price_per_night,
            num_bedrooms=request.form.get('num_bedrooms', type=int),
            num_bathrooms=request.form.get('num_bathrooms', type=int),
            num_guests=request.form.get('max_guests', type=int)
        )

        if result.get('success'):
            return redirect('/owner/properties')
        else:
            msg = result.get('error', 'Failed to create property')

    return render_template('owner/property_form.html', property=None, msg=msg)

@app.route('/owner/property/<int:property_id>/edit', methods=['GET', 'POST'])
@owner_required
def owner_property_edit(property_id):
    prop = Property(CONFIG_PATH)

    # Verify ownership
    if not prop.verifyOwnership(property_id, session['user_id']):
        return redirect('/owner/properties')

    prop.getById(property_id)
    if not prop.data:
        return redirect('/owner/properties')

    property_data = prop.data[0]
    msg = None

    if request.method == 'POST':
        price_raw = request.form.get('price_per_night', '')
        try:
            price_val = float(price_raw)
            if price_val != int(price_val) or int(price_val) < 1:
                raise ValueError
            price_per_night = int(price_val)
        except (ValueError, TypeError):
            msg = 'Price per night must be a whole number (e.g. 100), no decimals allowed.'
            return render_template('owner/property_form.html', property=property_data, msg=msg)

        result = prop.updateProperty(
            property_id=property_id,
            owner_id=session['user_id'],
            title=request.form.get('title'),
            description=request.form.get('description'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            province=request.form.get('province'),
            property_type=request.form.get('property_type'),
            price_per_night=price_per_night,
            num_bedrooms=request.form.get('num_bedrooms', type=int),
            num_bathrooms=request.form.get('num_bathrooms', type=int),
            num_guests=request.form.get('max_guests', type=int)
        )

        if result.get('success'):
            return redirect('/owner/properties')
        else:
            msg = result.get('error', 'Failed to update property')

    return render_template('owner/property_form.html', property=property_data, msg=msg)

@app.route('/owner/property/<int:property_id>/delete', methods=['POST'])
@owner_required
def owner_property_delete(property_id):
    prop = Property(CONFIG_PATH)
    prop.deleteProperty(property_id, session['user_id'])
    return redirect('/owner/properties')

@app.route('/owner/property/<int:property_id>/images', methods=['GET', 'POST'])
@owner_required
def owner_property_images(property_id):
    prop = Property(CONFIG_PATH)

    # Verify ownership
    if not prop.verifyOwnership(property_id, session['user_id']):
        return redirect('/owner/properties')

    prop.getById(property_id)
    property_data = prop.data[0] if prop.data else {}

    img = Property_Image(CONFIG_PATH)
    images = img.getByPropertyId(property_id)

    msg = None

    if request.method == 'POST':
        image_url = request.form.get('image_url', '')
        caption = request.form.get('caption', '')

        if image_url:
            result = img.createImage(
                property_id=property_id,
                owner_id=session['user_id'],
                caption=caption,
                image_url=image_url
            )
            if result.get('success'):
                return redirect(f'/owner/property/{property_id}/images')
            else:
                msg = result.get('error', 'Failed to add image')

    return render_template('owner/property_images.html',
                           property=property_data,
                           images=images,
                           msg=msg)

@app.route('/owner/property/<int:property_id>/images/upload', methods=['POST'])
@owner_required
def owner_property_image_upload(property_id):
    prop = Property(CONFIG_PATH)

    # Verify ownership
    if not prop.verifyOwnership(property_id, session['user_id']):
        return redirect('/owner/properties')

    if 'image_file' not in request.files:
        return redirect(f'/owner/property/{property_id}/images')

    file = request.files['image_file']
    caption = request.form.get('caption', '')

    if file.filename == '':
        return redirect(f'/owner/property/{property_id}/images')

    if file and allowed_file(file.filename):
        # Create unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{property_id}_{int(time.time())}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the file
        file.save(filepath)

        # Store in database with URL path
        image_url = f"/static/uploads/{unique_filename}"
        img = Property_Image(CONFIG_PATH)
        img.createImage(
            property_id=property_id,
            owner_id=session['user_id'],
            caption=caption,
            image_url=image_url
        )

    return redirect(f'/owner/property/{property_id}/images')

@app.route('/owner/image/<int:image_id>/delete', methods=['POST'])
@owner_required
def owner_image_delete(image_id):
    img = Property_Image(CONFIG_PATH)
    img.getById(image_id)

    if img.data:
        property_id = img.data[0].get('property_Id')
        img.deleteImage(image_id, session['user_id'])
        return redirect(f'/owner/property/{property_id}/images')

    return redirect('/owner/properties')

@app.route('/owner/bookings')
@owner_required
def owner_bookings():
    owner = PropertyOwner(CONFIG_PATH)
    bookings = owner.getBookingsForOwner(session['user_id'])

    return render_template('owner/bookings.html', bookings=bookings)

@app.route('/owner/reviews')
@owner_required
def owner_reviews():
    owner = PropertyOwner(CONFIG_PATH)
    reviews = owner.getReviewsReceived(session['user_id'])
    rating = owner.getAverageRating(session['user_id'])

    return render_template('owner/reviews.html', reviews=reviews, rating=rating)

@app.route('/owner/earnings')
@owner_required
def owner_earnings():
    owner = PropertyOwner(CONFIG_PATH)
    stats = owner.getTotalEarnings(session['user_id'])
    by_property = owner.getEarningsByProperty(session['user_id'])

    return render_template('owner/earnings.html', stats=stats, by_property=by_property)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    admin = Admin(CONFIG_PATH)

    stats = admin.getPlatformStats()
    top_properties = admin.getTopProperties(5)
    top_owners = admin.getTopOwners(5)
    recent_activity = admin.getRecentActivity(10)
    bookings_by_month_raw = admin.getBookingsByMonth(12)

    # Format for Chart.js: labels like "Jan 2025", counts as integers
    import calendar
    chart_labels = []
    chart_counts = []
    for row in bookings_by_month_raw:
        month_key = int(row['month_key'])
        year  = month_key // 100
        month = month_key % 100
        if 1 <= month <= 12:
            chart_labels.append(f"{calendar.month_abbr[month]} {year}")
            chart_counts.append(int(row['booking_count']))

    return render_template('admin/dashboard.html',
                           stats=stats,
                           top_properties=top_properties,
                           top_owners=top_owners,
                           recent_activity=recent_activity,
                           chart_labels=chart_labels,
                           chart_counts=chart_counts)

@app.route('/admin/users')
@admin_required
def admin_users():
    admin = Admin(CONFIG_PATH)

    role_filter = request.args.get('role', '')
    search_query = request.args.get('q', '')

    users = admin.getFilteredUsers(role=role_filter or None, search=search_query or None)

    return render_template('admin/users.html', users=users, role_filter=role_filter, search_query=search_query)

@app.route('/admin/properties')
@admin_required
def admin_properties():
    admin = Admin(CONFIG_PATH)
    properties = admin.getAllProperties()

    return render_template('admin/properties.html', properties=properties)

@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    admin = Admin(CONFIG_PATH)
    bookings = admin.getAllBookings(100)

    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/reviews')
@admin_required
def admin_reviews():
    admin = Admin(CONFIG_PATH)
    reviews = admin.getRecentReviews(50)

    return render_template('admin/reviews.html', reviews=reviews)

@app.route('/admin/review/<int:review_id>/delete', methods=['POST'])
@admin_required
def admin_delete_review(review_id):
    review = Review(CONFIG_PATH)
    review.deleteById(review_id)
    return redirect('/admin/reviews')

@app.route('/admin/user/<int:user_id>/reset-password', methods=['GET', 'POST'])
@admin_required
def admin_reset_password(user_id):
    u = user(CONFIG_PATH)
    u.getById(user_id)

    if not u.data:
        return redirect('/admin/users')

    target_user = u.data[0]
    msg = None
    success = False

    if request.method == 'POST':
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if len(new_password) < 3:
            msg = 'Password must be at least 3 characters'
        elif new_password != confirm_password:
            msg = 'Passwords do not match'
        else:
            # Hash and update password
            import hashlib
            hashed = hashlib.md5(new_password.encode()).hexdigest()
            u.cur.execute(
                '''UPDATE `USER` SET `password` = %s WHERE `user_id` = %s;''',
                [hashed, user_id]
            )
            success = True
            msg = f"Password reset successfully for {target_user['first_name_']} {target_user['last_name_']}"

    return render_template('admin/reset_password.html',
                           target_user=target_user,
                           msg=msg,
                           success=success)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
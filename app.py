from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# =========================================
# SECRET KEY
# =========================================

app.secret_key = 'deepfake_secret_key'

# =========================================
# UPLOAD FOLDER
# =========================================

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# =========================================
# MYSQL CONFIGURATION
# =========================================

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'nadnan226'

app.config['MYSQL_DB'] = 'deepfake_db'

# =========================================
# MYSQL OBJECT
# =========================================

mysql = MySQL(app)

# =========================================
# HOME PAGE
# =========================================

@app.route('/')

def home():

    return render_template('index.html')

# =========================================
# REGISTER PAGE
# =========================================

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = request.form['password']

        cursor = mysql.connection.cursor()

        query = """
        INSERT INTO users
        (username, email, password)
        VALUES (%s, %s, %s)
        """

        values = (username, email, password)

        cursor.execute(query, values)

        mysql.connection.commit()

        cursor.close()

        return redirect('/login')

    return render_template('register.html')

# =========================================
# LOGIN PAGE
# =========================================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        cursor = mysql.connection.cursor()

        query = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        values = (email, password)

        cursor.execute(query, values)

        user = cursor.fetchone()

        cursor.close()

        if user:

            return redirect('/dashboard')

        else:

            flash('Invalid Email or Password')

            return redirect('/login')

    return render_template('login.html')

# =========================================
# DASHBOARD
# =========================================

@app.route('/dashboard')

def dashboard():

    return render_template('dashboard.html')

# =========================================
# UPLOAD PAGE + FILE UPLOAD
# =========================================

@app.route('/upload', methods=['GET', 'POST'])

def upload():

    if request.method == 'POST':

        title = request.form['title']

        description = request.form['description']

        media_type = request.form['media_type']

        media_file = request.files['media_file']

        # TEMP USER ID

        user_id = 1

        # SAVE FILE

        filename = secure_filename(media_file.filename)

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        media_file.save(filepath)

        # INSERT REPORT

        cursor = mysql.connection.cursor()

        report_query = """
        INSERT INTO reports
        (user_id, title, description)
        VALUES (%s, %s, %s)
        """

        report_values = (
            user_id,
            title,
            description
        )

        cursor.execute(
            report_query,
            report_values
        )

        mysql.connection.commit()

        # GET REPORT ID

        report_id = cursor.lastrowid

        # INSERT MEDIA FILE

        media_query = """
        INSERT INTO mediafiles
        (report_id, file_path, media_type)
        VALUES (%s, %s, %s)
        """

        media_values = (
            report_id,
            filepath,
            media_type
        )

        cursor.execute(
            media_query,
            media_values
        )

        mysql.connection.commit()

        cursor.close()

        flash('Media Report Uploaded Successfully')

        return redirect('/upload')

    return render_template('upload.html')

# =========================================
# ADMIN PAGE
# =========================================

@app.route('/admin', methods=['GET', 'POST'])

def admin():

    cursor = mysql.connection.cursor()

    # UPDATE REPORT STATUS

    if request.method == 'POST':

        report_id = request.form['report_id']

        status = request.form['status']

        remarks = request.form['remarks']

        # UPDATE REPORT TABLE

        update_query = """
        UPDATE reports
        SET status=%s
        WHERE report_id=%s
        """

        update_values = (
            status,
            report_id
        )

        cursor.execute(
            update_query,
            update_values
        )

        mysql.connection.commit()

        # INSERT VERIFICATION RECORD

        verification_query = """
        INSERT INTO verification
        (report_id, admin_id, result, remarks)
        VALUES (%s, %s, %s, %s)
        """

        verification_values = (
            report_id,
            1,
            status,
            remarks
        )

        cursor.execute(
            verification_query,
            verification_values
        )

        mysql.connection.commit()

        flash('Verification Updated Successfully')

    # FETCH REPORTS

    fetch_query = """
    SELECT *
    FROM reports
    ORDER BY upload_date DESC
    """

    cursor.execute(fetch_query)

    reports = cursor.fetchall()

    cursor.close()

    return render_template(
        'admin.html',
        reports=reports
    )

@app.route('/analytics')

def analytics():

    cursor = mysql.connection.cursor()

    # TOTAL REPORTS

    cursor.execute(
        "SELECT COUNT(*) FROM reports"
    )

    total_reports = cursor.fetchone()[0]

    # FAKE REPORTS

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE status='Fake'"
    )

    fake_reports = cursor.fetchone()[0]

    # REAL REPORTS

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE status='Real'"
    )

    real_reports = cursor.fetchone()[0]

    # UNDER INVESTIGATION

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM reports
        WHERE status='Under Investigation'
        """
    )

    investigation_reports = cursor.fetchone()[0]

    # TOTAL USERS

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    total_users = cursor.fetchone()[0]

    cursor.close()

    return render_template(

        'analytics.html',

        total_reports=total_reports,

        fake_reports=fake_reports,

        real_reports=real_reports,

        investigation_reports=investigation_reports,

        total_users=total_users
    )

@app.route('/history')

def history():

    search = request.args.get('search')

    cursor = mysql.connection.cursor()

    # SEARCH QUERY

    if search:

        query = """
        SELECT
            reports.report_id,
            reports.title,
            reports.description,
            reports.status,
            reports.upload_date,
            mediafiles.media_type

        FROM reports

        JOIN mediafiles
        ON reports.report_id = mediafiles.report_id

        WHERE reports.title LIKE %s
        OR reports.status LIKE %s
        OR mediafiles.media_type LIKE %s

        ORDER BY reports.upload_date DESC
        """

        search_term = "%" + search + "%"

        cursor.execute(
            query,
            (
                search_term,
                search_term,
                search_term
            )
        )

    else:

        query = """
        SELECT
            reports.report_id,
            reports.title,
            reports.description,
            reports.status,
            reports.upload_date,
            mediafiles.media_type

        FROM reports

        JOIN mediafiles
        ON reports.report_id = mediafiles.report_id

        ORDER BY reports.upload_date DESC
        """

        cursor.execute(query)

    reports = cursor.fetchall()

    cursor.close()

    return render_template(
        'history.html',
        reports=reports
    )
if __name__ == '__main__':

    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.secret_key = "secretkey"

# MYSQL CONNECTION
import os
# if os.getenv("MYSQLHOST"):

#     db = mysql.connector.connect(
#         host=os.getenv("MYSQLHOST"),
#         user=os.getenv("MYSQLUSER"),
#         password=os.getenv("MYSQLPASSWORD"),
#         database=os.getenv("MYSQLDATABASE"),
#         port=int(os.getenv("MYSQLPORT"))
#     )

# else:

#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="YOUR_LOCAL_MYSQL_PASSWORD",
#         database="voting_system"
#     )
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

cursor = db.cursor(dictionary=True)

# EMAIL VALIDATION

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def valid_email(email):
    return re.match(email_pattern, email)


# HOME PAGE

@app.route('/')
def home():

    cursor.execute(
        "SELECT * FROM election_settings LIMIT 1"
    )

    election = cursor.fetchone()

    # NO ELECTION CONFIGURED

    if not election:

        return render_template(
            'home.html',
            election=None,
            status_message="No Election Configured",
            countdown_time=""
        )

    status_message = ""

    countdown_time = ""

    current_time = datetime.now()

    # INACTIVE ELECTION

    if election['status'] == 'inactive':

        status_message = (
            "No Active Election"
        )

    else:

        start_time = election['start_time']

        end_time = election['end_time']

        result_time = election['result_time']

        if current_time < start_time:

            status_message = (
                "Election Has Not Started"
            )

            countdown_time = start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        elif current_time < end_time:

            status_message = (
                "Election Is Live"
            )

            countdown_time = end_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        elif current_time < result_time:

            status_message = (
                "Voting Closed"
            )

            countdown_time = result_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        else:

            status_message = (
                "Results Published"
            )

    return render_template(
        'home.html',
        election=election,
        status_message=status_message,
        countdown_time=countdown_time
    )


# REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name'].strip()

        email = request.form['email'].lower().strip()

        password = request.form['password']

        # EMAIL VALIDATION

        if not valid_email(email):

            flash(
                "Invalid Email Format",
                "error"
            )

            return render_template(
                'register.html'
            )

        # PASSWORD VALIDATION

        if len(password) < 6:

            flash(
                "Password must be at least 6 characters",
                "error"
            )

            return render_template(
                'register.html'
            )

        # EXISTING USER CHECK

        query = """
        SELECT * FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        existing_user = cursor.fetchone()

        if existing_user:

            flash(
                "Email already registered. Please login.",
                "error"
            )

            return redirect('/login')

        # HASH PASSWORD

        hashed_password = generate_password_hash(
            password
        )

        # INSERT USER

        insert_query = """
        INSERT INTO users(
            name,
            email,
            password,
            voted
        )
        VALUES(%s, %s, %s, %s)
        """

        values = (
            name,
            email,
            hashed_password,
            0
        )

        cursor.execute(
            insert_query,
            values
        )

        db.commit()

        flash(
            "Registration Successful",
            "success"
        )

        return redirect('/login')

    return render_template(
        'register.html'
    )


# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email'].lower()

        password = request.form['password']

        query = """
        SELECT * FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        if not user:

            flash(
                "User Not Found",
                "error"
            )

            return render_template(
                'login.html'
            )

        if not check_password_hash(
            user['password'],
            password
        ):

            flash(
                "Incorrect Password",
                "error"
            )

            return render_template(
                'login.html'
            )

        session['user_email'] = email

        flash(
            "Login Successful",
            "success"
        )

        return redirect('/vote')

    return render_template(
        'login.html'
    )


# VOTE

@app.route('/vote', methods=['GET', 'POST'])
def vote():

    if 'user_email' not in session:

        return redirect('/login')

    cursor.execute(
        "SELECT * FROM election_settings LIMIT 1"
    )

    election = cursor.fetchone()
    if not election:

        return render_template(
            'public_results.html',
            election=None,
            results_published=False,
            hours=0,
            minutes=0,
            no_election=True
        )

    # if not election:

    #     flash(
    #         "Election not configured",
    #         "error"
    #     )

    #     return redirect('/')

    current_time = datetime.now()

    start_time = election['start_time']

    end_time = election['end_time']

    # ELECTION NOT STARTED

    if current_time < start_time:

        flash(
            f"Election has not started yet. Starts at {start_time}",
            "error"
        )

        return render_template(
            'vote.html',
            candidates=[],
            election=election
        )

    # ELECTION ENDED

    if current_time > end_time:

        flash(
            "Voting has ended.",
            "error"
        )

        return render_template(
            'vote.html',
            candidates=[],
            election=election
        )

    # FETCH USER

    email = session['user_email']

    query = """
    SELECT * FROM users
    WHERE email = %s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    # ALREADY VOTED

    if user['voted'] == 1:

        flash(
            "You have already voted",
            "error"
        )

        return redirect('/success')

    # SUBMIT VOTE

    if request.method == 'POST':

        candidate_id = request.form.get('candidate')

        if not candidate_id:

            flash(
                "Please select a candidate",
                "error"
            )

            return redirect('/vote')

        update_query = """
        UPDATE candidates
        SET votes = votes + 1
        WHERE id = %s
        """

        cursor.execute(
            update_query,
            (candidate_id,)
        )

        voted_query = """
        UPDATE users
        SET voted = 1
        WHERE email = %s
        """

        cursor.execute(
            voted_query,
            (email,)
        )

        db.commit()

        flash(
            "Vote submitted successfully",
            "success"
        )

        return redirect('/success')

    # FETCH CANDIDATES

    cursor.execute(
        "SELECT * FROM candidates"
    )

    candidates = cursor.fetchall()

    return render_template(
        'vote.html',
        candidates=candidates,
        election=election
    )


# SUCCESS PAGE

@app.route('/success')
def success():

    return render_template(
        'success.html'
    )


# ADMIN LOGIN

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        if (
            email == 'admin@gmail.com'
            and password == 'admin123'
        ):

            session['admin'] = True

            flash(
                "Admin Login Successful",
                "success"
            )

            return redirect('/admin-dashboard')

        flash(
            "Invalid Admin Credentials",
            "error"
        )

        return render_template(
            'admin_login.html'
        )

    return render_template(
        'admin_login.html'
    )


# ADMIN DASHBOARD

@app.route('/admin-dashboard')
def admin_dashboard():

    if 'admin' not in session:

        return redirect('/admin-login')

    cursor.execute(
        "SELECT * FROM candidates"
    )

    candidates = cursor.fetchall()

    return render_template(
        'admin_dashboard.html',
        candidates=candidates
    )


# ADD CANDIDATE

@app.route('/add-candidate', methods=['POST'])
def add_candidate():

    if 'admin' not in session:

        return redirect('/admin-login')

    name = request.form['name'].strip()

    party = request.form['party'].strip()

    slogan = request.form['slogan'].strip()

    # DUPLICATE CHECK

    check_query = """
    SELECT * FROM candidates
    WHERE LOWER(name) = %s
    """

    cursor.execute(
        check_query,
        (name.lower(),)
    )

    existing_candidate = cursor.fetchone()

    if existing_candidate:

        flash(
            "Candidate already exists",
            "error"
        )

        return redirect('/admin-dashboard')

    query = """
    INSERT INTO candidates(
        name,
        party,
        slogan
    )
    VALUES(%s, %s, %s)
    """

    values = (
        name,
        party,
        slogan
    )

    cursor.execute(query, values)

    db.commit()

    flash(
        "Candidate Added Successfully",
        "success"
    )

    return redirect('/admin-dashboard')


# UPDATE ELECTION

@app.route('/update-election', methods=['POST'])
def update_election():

    if 'admin' not in session:

        return redirect('/admin-login')

    election_name = request.form['election_name']

    start_time = datetime.strptime(
        request.form['start_time'],
        "%Y-%m-%dT%H:%M"
    )

    end_time = datetime.strptime(
        request.form['end_time'],
        "%Y-%m-%dT%H:%M"
    )

    result_time = datetime.strptime(
        request.form['result_time'],
        "%Y-%m-%dT%H:%M"
    )

    # VALIDATIONS

    if start_time >= end_time:

        flash(
            "End time must be after start time",
            "error"
        )

        return redirect('/admin-dashboard')

    if end_time >= result_time:

        flash(
            "Result time must be after election end time",
            "error"
        )

        return redirect('/admin-dashboard')

    query = """
    UPDATE election_settings
    SET
    election_name = %s,
    start_time = %s,
    end_time = %s,
    result_time = %s,
    status = 'upcoming'
    WHERE id = 1
    """

    values = (
        election_name,
        start_time,
        end_time,
        result_time
    )

    cursor.execute(query, values)

    # RESET USERS

    cursor.execute(
        "UPDATE users SET voted = FALSE"
    )

    # RESET VOTES

    cursor.execute(
        "UPDATE candidates SET votes = 0"
    )

    db.commit()

    flash(
        "Election Updated Successfully",
        "success"
    )

    return redirect('/admin-dashboard')


# DELETE CANDIDATE

@app.route('/delete-candidate/<int:id>')
def delete_candidate(id):

    if 'admin' not in session:

        return redirect('/admin-login')

    # PREVENT DELETION AFTER VOTING

    cursor.execute(
        "SELECT SUM(votes) AS total FROM candidates"
    )

    vote_data = cursor.fetchone()

    total_votes = vote_data['total']

    if total_votes and total_votes > 0:

        flash(
            "Cannot delete candidate after voting started",
            "error"
        )

        return redirect('/admin-dashboard')

    query = """
    DELETE FROM candidates
    WHERE id = %s
    """

    cursor.execute(query, (id,))

    db.commit()

    flash(
        "Candidate Deleted Successfully",
        "success"
    )

    return redirect('/admin-dashboard')


# ADMIN RESULTS

@app.route('/results')
def results():

    if 'admin' not in session:

        return redirect('/admin-login')

    cursor.execute(
        "SELECT * FROM candidates ORDER BY votes DESC"
    )

    candidates = cursor.fetchall()

    return render_template(
        'results.html',
        candidates=candidates
    )


# PUBLIC RESULTS

@app.route('/public-results')
def public_results():

    cursor.execute(
        "SELECT * FROM election_settings LIMIT 1"
    )

    election = cursor.fetchone()

    if not election:

        return render_template(
            'public_results.html',
            no_election=True
        )

    current_time = datetime.now()

    result_time = election['result_time']
    
    if current_time < result_time:

        remaining_time = result_time - current_time

        hours = remaining_time.seconds // 3600

        minutes = (remaining_time.seconds % 3600) // 60

        return render_template(
            'public_results.html',
            election=election,
            results_published=False,
            hours=hours,
            minutes=minutes
        )
    # FETCH RESULTS

    cursor.execute(
        "SELECT * FROM candidates ORDER BY votes DESC"
    )

    candidates = cursor.fetchall()

    total_votes = sum(
        candidate['votes']
        for candidate in candidates
    )

    # CALCULATE PERCENTAGES

    for candidate in candidates:

        if total_votes > 0:

            percentage = (
                candidate['votes']
                / total_votes
            ) * 100

            candidate['percentage'] = round(
                percentage,
                1
            )

        else:

            candidate['percentage'] = 0

    winners = []

    highest_votes = 0

    if candidates:

        highest_votes = max(
            candidate['votes']
            for candidate in candidates
        )

    # HANDLE TIE

    if highest_votes > 0:

        winners = [

            candidate

            for candidate in candidates

            if candidate['votes'] == highest_votes
        ]

    return render_template(
        'public_results.html',
        election=election,
        candidates=candidates,
        total_votes=total_votes,
        winners=winners,
        highest_votes=highest_votes,
        results_published=True
    )


# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect('/')


# RUN APP

if __name__ == '__main__':

    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, RadioField, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import bcrypt
from flask_mysqldb import MySQL

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rohit@5021'
app.config['MYSQL_DB'] = 'registationdb'

mysql = MySQL(app)

# Forms

class RegisterForm(FlaskForm):
    # Form fields for user registration
    FirstName = StringField('First Name', validators=[DataRequired()])
    LastName = StringField('Last Name', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    ConfirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    Mobile_No = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    Age = IntegerField('Age', validators=[DataRequired()])
    Gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    CurrentAddress = TextAreaField('Current Address', validators=[DataRequired()])
    PermanentAdd = TextAreaField('Permanent Address', validators=[DataRequired()])
    City = SelectField('City', choices=[('city1', 'City 1'), ('city2', 'City 2')], validators=[DataRequired()])
    Pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6)])
    State = SelectField('State', choices=[('state1', 'State 1'), ('state2', 'State 2')], validators=[DataRequired()])
    Country = SelectField('Country', choices=[('country1', 'Country 1'), ('country2', 'Country 2')], validators=[DataRequired()])

    # Custom validator for email uniqueness
    def validate_Email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')


class LoginForm(FlaskForm):
    # Form fields for user login
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    # Form fields for editing user profile
    FirstName = StringField('First Name')
    LastName = StringField('Last Name')
    Email = StringField('Email')
    Mobile_No = StringField('Mobile Number')
    Age = IntegerField('Age')
    Gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    CurrentAddress = TextAreaField('Current Address')
    PermanentAdd = TextAreaField('Permanent Address')
    City = SelectField('City', choices=[('city1', 'City 1'), ('city2', 'City 2')])
    Pincode = StringField('Pincode')
    State = SelectField('State', choices=[('state1', 'State 1'), ('state2', 'State 2')])
    Country = SelectField('Country', choices=[('country1', 'Country 1'), ('country2', 'Country 2')])


# Routes

@app.route('/')
def home():
    # Render the home page and display a registration success message if available
    message = session.pop('registration_successful', None)
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Handle form submission for user registration
        FirstName = form.FirstName.data
        LastName = form.LastName.data
        Email = form.Email.data
        Password = form.Password.data
        hashed_password = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt())

        # Insert user data into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user (FirstName, LastName, Email, Password, Mobile_No, Age, Gender, CurrentAddress, PermanentAdd, City, Pincode, State, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (FirstName, LastName, Email, hashed_password, form.Mobile_No.data, form.Age.data, form.Gender.data, form.CurrentAddress.data, form.PermanentAdd.data, form.City.data, form.Pincode.data, form.State.data, form.Country.data))
        mysql.connection.commit()
        cursor.close()

        session['registration_successful'] = True
        return redirect(url_for('thank_YOU'))

    return render_template('register.html', form=form)

@app.route('/thank_you')
def thank_YOU():
    # Render the thank you page after successful registration
    message = "Thank you for registering!"
    return render_template('thankyou.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle user login
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email=%s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Render the user dashboard if logged in
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html', user=user)
    
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Allow users to edit their profile if logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    form = EditProfileForm(obj={
        'FirstName': user[1],
        'LastName': user[2],
        'Email': user[3],
        'Mobile_No': user[5],
        'Age': user[6],
        'Gender': user[7],
        'CurrentAddress': user[8],
        'PermanentAdd': user[9],
        'City': user[10],
        'Pincode': user[11],
        'State': user[12],
        'Country': user[13]
    })

    if form.validate_on_submit():
        # Handle profile updates
        first_name = form.FirstName.data
        last_name = form.LastName.data
        email = form.Email.data
        mobile_no = form.Mobile_No.data
        age = form.Age.data
        gender = form.Gender.data
        current_address = form.CurrentAddress.data
        permanent_add = form.PermanentAdd.data
        city = form.City.data
        pincode = form.Pincode.data
        state = form.State.data
        country = form.Country.data

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE user
            SET FirstName = %s, LastName = %s, Email = %s, Mobile_No = %s, Age = %s, Gender = %s, 
                CurrentAddress = %s, PermanentAdd = %s, City = %s, Pincode = %s, State = %s, Country = %s
            WHERE id = %s
        """, (first_name, last_name, email, mobile_no, age, gender, current_address, permanent_add, city, pincode, state, country, user_id))
        mysql.connection.commit()
        cursor.close()

        flash('Profile updated successfully')
        return redirect(url_for('dashboard'))

    return render_template('edit_profile.html', form=form)

@app.route('/logout')
def logout():
    # Handle user logout
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

@app.route('/register_t')
def register_t():
    # Render registration page
    return render_template('register.html')

@app.route('/search_ferry', methods=['POST'])
def search_ferry():
    # Handle ferry search based on user input
    if request.method == 'POST':
        from_location = request.form.get('from')
        to_location = request.form.get('to')
        onward_date = request.form.get('onward_date')
        cursor = mysql.connection.cursor()
        query = """
        SELECT * FROM ferry_schedule
        WHERE from_location = %s AND to_location = %s AND onward_date = %s
        """
        cursor.execute(query, (from_location, to_location, onward_date))
        results = cursor.fetchall()
        cursor.close()
        return render_template('search_results.html', results=results)
    return redirect(url_for('home'))

@app.route('/services')
def services():
    # Render services page
    return render_template('services.html')

@app.route('/about')
def about():
    # Render about page
    return render_template('about.html')

@app.route('/contact')
def contact():
    # Render contact page
    return render_template('contact.html')

@app.route('/our_Team')
def our_Team():
    # Render team page
    return render_template('our_Team.html')

@app.route('/help')
def help_support():
    # Render help and support page
    return render_template('help_support.html')

@app.route('/ticket', methods=['POST', 'GET'])
def ticket():
    # Handle ticket booking
    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        date = request.form['date']
        tickets = request.form['tickets']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO new_table (name, destination, date, tickets) VALUES (%s, %s, %s, %s)",
                       (name, destination, date, tickets))
        mysql.connection.commit()
        cursor.close()

        flash('Ticket booking successful')
        return redirect(url_for('home'))
    return render_template('ticket.html')

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode

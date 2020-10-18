from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db_name = "auth.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'

db = SQLAlchemy(app)

class User(db.Model):                                   #creating a user model using flask sqlalchemy
    uid = db.Column(db.Integer, primary_key=True)       #the id created when adding a session to the user
    firstname = db.Column(db.String(100), nullable=False) #the information that will be stored in each corresponding column in the db
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username


def create_db():       #run this function if there is no current db created
    db.create_all()
    
def api_signup(db):
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not (firstname and lastname and email and username and password):
            flash("Fields cannot be empty")
            return redirect(url_for('signup'))
        else:
            firstname = firstname.strip()       #strip() removing all whitespaces
            lastname = lastname.strip()
            email = email.strip()
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(firstname = firstname, lastname = lastname, email = email, username=username, pass_hash=hashed_pwd)  #creating new_user object
        db.session.add(new_user)  #storing the object 'new_user' into the session, this allows for users to be authenticated to certain pages when requiring                         session[]=true
                                  #for exampe, if session[amrit, singh, ...] = true, it will allow that user to login and access the homepage from there
        try:
            db.session.commit()   #transaction is committed and user is given an id, new_user.id
        except sqlalchemy.exc.IntegrityError:
            flash("Email {e} is already in use.".format(e=email))
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")

def api_login(User):
    if request.method == "POST":
        username = request.form['username']  #session variable username and password are found and user can login
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):   #the check_password_hash function will check plaintext password with hashed value stored in database to see if they match
            session[username] = True        #will store session cookie with true if username and password is valid
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")

def api_user_home(username):
    if not session.get(username):   #if session cookie value is not true, it will not allow access to this page and return error 401
        abort(401)
  
    return render_template("user_home.html", username=username)

def api_logout(username):
    """ Logout user and redirect to login page with success message."""
    session.pop(username, None)     #removes the current users session cookie when logging out, this pops out 'username' session variable
    flash("successfully logged out.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)

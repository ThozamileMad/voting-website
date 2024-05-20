from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from databases import sqlalchemy_app, web_databases
from country_data import COUNTRIES, PROVINCES, LANGUAGES, POLITICAL_PARTIES
from error_handler import ErrorHandler


app = Flask(__name__)
app.config["SECRET_KEY"] = "ABC"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_BINDS"] = {"registrations": "sqlite:///registrations.db"}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = sqlalchemy_app(app)
wdb = web_databases(app, UserMixin, db)

Registrations = wdb[0]
Users = wdb[1]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def restrict_signup_login(function):
    @wraps(function)
    def inner_function(*args, **kwargs):
        if current_user.is_authenticated:
            return abort(403, "Unauthorised, access denied until user is logged out.")
        else:
            return function(*args, **kwargs)
    return inner_function


def restrict_page_if_not_logged_in(function):
    @wraps(function)
    def inner_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403, "Unauthorised, access denied until user is logged in.")
        else:
            return function(*args, **kwargs)
    return inner_function


@app.route("/")
def home():
    return render_template("home.html")


def db_add(item):
    db.session.add(item)
    db.session.commit()


@app.route("/register/<err>", methods=["GET", "POST"])
@restrict_page_if_not_logged_in
def register(err):
    err_han = ErrorHandler()
    numbers_symbols = err_han.num_sym_lst
    symbols = err_han.sym_lst
    letters_symbols = err_han.let_sym_lst

    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        address = request.form.get("address")
        id_number = request.form.get("id_number")
        contact_numbers = request.form.get("contact_numbers")
        proof_of_address = request.form.get("proof_of_address")
        province = request.form.get("province")
        citizenship = request.form.get("citizenship")
        language = request.form.get("language")
        political_party_affiliation = request.form.get("political_party_affiliation")
        date = request.form.get("date")
        gender = request.form.get("gender")
        disabled = request.form.get("disabled")
        married = request.form.get("marital-status")
        id_numbers = [data.id_number for data in db.session.query(Registrations).all()]

        # detects invalid char such as symbols and numbers in first name and last name input fields
        if err_han.detect_invalid_char(numbers_symbols, name):
            return redirect(url_for("register", err="Invalid*First*Name!!!"))
        if err_han.detect_invalid_char(numbers_symbols, surname):
            return redirect(url_for("register", err="Invalid*Last*Name!!!"))

        # detects invalid ID Number entries.
        # this code ensures valid South African ID Number format is used.
        if err_han.detect_invalid_char(letters_symbols, id_numbers):
            return redirect(url_for("register", err="Invalid*ID*Number!!!"))
        if err_han.detect_invalid_id_number(id_number):
            return redirect(url_for("register", err="Invalid*ID*Number!!!"))

        # checks if ID number exists in database
        if err_han.detect_if_id_number_exists(id_numbers, id_number):
            return redirect(url_for("register", err="ID*Number*is*already*in*database!!!"))

        # checks if user meets the minimum age requirements - 16 yrs
        if err_han.detect_invalid_date(date):
            return redirect(url_for("register", err="You*Are*Too*Young!!!"))

        # detects invalid char such as symbols in the address field
        if err_han.detect_invalid_char(symbols, address):
            return redirect(url_for("register", err="Invalid*Address!!!"))

        # detects invalid char such as symbols and numbers in contact field
        if err_han.detect_invalid_char(letters_symbols, contact_numbers):
            return redirect(url_for("register", err="Invalid*Contact*Number!!!"))

        # checks if address matches with proof of address
        if address.lower() != proof_of_address.lower():
            return redirect(url_for("register", err="Invalid*Proof*of*Address!!!"))

        # checks if citizenship, province and language fields are empty
        dropdown_inputs = [(citizenship, "Invalid*Citizenship!!!"), (province, "Invalid*Province!!!"), (language, "Invalid*Language!!!"), (political_party_affiliation, "Invalid*Political*Party*Affiliation!!!")]
        for tup in dropdown_inputs:
            if tup[0] == "none":
                return redirect(url_for("register", err=tup[1]))

        db_add(Registrations(name=name,
                             surname=surname,
                             id_number=id_number,
                             address=address,
                             date_of_birth=date,
                             contact_numbers=contact_numbers,
                             proof_of_address=proof_of_address,
                             citizenship=citizenship,
                             province=province,
                             language=language,
                             political_party_affiliation=political_party_affiliation,
                             disabled=disabled,
                             gender=gender,
                             married=married))

        return redirect(url_for("home"))

    return render_template("register.html",
                           err=err,
                           country_dict=COUNTRIES,
                           provinces=PROVINCES,
                           languages=LANGUAGES,
                           political_parties=POLITICAL_PARTIES)


@app.route("/sign_up/<err>", methods=["POST", "GET"])
@restrict_signup_login
def sign_up(err):
    err_han = ErrorHandler()
    numbers_symbols = err_han.num_sym_lst
    letters_symbols = err_han.let_sym_lst

    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        id_number = request.form.get("id_number")
        email = request.form.get("email")
        password = request.form.get("password")

        print(id_number)

        # checks if id or email or password already in database
        id_numbers = [data.id_number for data in db.session.query(Users).all()]
        emails = [data.email for data in db.session.query(Users).all()]
        passwords = [check_password_hash(data.password, password) for data in db.session.query(Users).all()]

        # detects invalid char such as symbols and numbers in first name and last name input fields
        if err_han.detect_invalid_char(numbers_symbols, name):
            return redirect(url_for("sign_up", err="Invalid*First*Name!!!"))
        if err_han.detect_invalid_char(numbers_symbols, surname):
            return redirect(url_for("sign_up", err="Invalid*Last*Name!!!"))

        # checks if id number is in database
        if id_number in id_numbers:
            return redirect(url_for("sign_up", err="ID*Numbers*is*already*in*database!!!"))

        # detects invalid ID Number entries.
        # this code ensures valid South African ID Number format is used.
        if err_han.detect_invalid_char(letters_symbols, id_numbers):
            return redirect(url_for("sign_up", err="Invalid*ID*Number!!!"))
        if err_han.detect_invalid_id_number(id_number):
            return redirect(url_for("sign_up", err="Invalid*ID*Number!!!"))

        # checks email is in database
        if email in emails:
            return redirect(url_for("sign_up", err="Email*is*already*in*database!!!"))

        # checks password is in database
        if True in passwords:
            return redirect(url_for("sign_up", err="Password*is*already*in*database!!!"))

        hashed_password = generate_password_hash(password)

        db_add(Users(name=name,
                     surname=surname,
                     id_number=id_number,
                     email=email,
                     password=hashed_password,
                     tsandcs=True))

        login_user(Users.query.filter_by(email=email).first())
        return redirect(url_for("home"))

    return render_template("sign_up.html", err=err)


@app.route("/sign_in/<err>", methods=["GET", "POST"])
@restrict_signup_login
def sign_in(err):
    if request.method == "POST":
        id_number = request.form.get("id_number")
        password = request.form.get("password")

        # Checks if id number and password match.
        # if they do the else statement logs user in and redirects to home page
        id_numbers = [data.id_number for data in db.session.query(Users).all()]
        passwords = [check_password_hash(data.password, password) for data in db.session.query(Users).all()]
        if id_number not in id_numbers:
            return redirect(url_for("sign_in", err="ID*Numbers*does*not*match*with*any*other*ID*Number*in*the*database!!!"))
        if True not in passwords:
            return redirect(url_for("sign_in",
                                    err="Password*does*not*match*with*any*other*passwords*in*the*database!!!"))
        else:
            login_user(Users.query.filter_by(id_number=id_number).first())
            return redirect(url_for("home"))

    return render_template("sign_in.html", err=err)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
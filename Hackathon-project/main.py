from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from databases import sqlalchemy_app, web_databases
from country_data import COUNTRIES, PROVINCES, LANGUAGES, POLITICAL_PARTIES, POLITICAL_PARTY_IMAGE_PATH, PARTY_DESCRIPTIONS, PARTY_COLORS, STATS_DESCRIPTIONS
from error_handler import ErrorHandler
from blockchain import *
from graphs import ResultsChart


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
    return render_template("home.html", is_logged_in=current_user.is_authenticated)


def db_add(item):
    db.session.add(item)
    db.session.commit()


@app.route("/register/<err>", methods=["GET", "POST"])
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

       if err_han.detect_id_date_match(id_number, date):
            return redirect(url_for("register", err="ID*Date*Of*Birth*Does*Not*Match*Date*Of*Birth*Provided!!!"))


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

        return redirect(url_for("vote"))

    return render_template("register.html",
                           err=err,
                           country_dict=COUNTRIES,
                           provinces=PROVINCES,
                           languages=LANGUAGES,
                           political_parties=POLITICAL_PARTIES,
                           is_logged_in=current_user.is_authenticated)


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
                     tsandcs=True,
                     party_vote=""))

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
    return render_template("contact.html", is_logged_in=current_user.is_authenticated)


@app.route("/vote", methods=["GET", "POST"])
def vote():
    modified_political_party = [party_name.lower() for party_name in POLITICAL_PARTIES]
    if request.method == "POST":
        user_input = "".join([request.form.get(party) for party in modified_political_party if request.form.get(party) != None])
        user_id = current_user.get_id()
        user_db_data = Users.query.filter_by(id=user_id).first()
        user_name = user_db_data.name
        user_surname = user_db_data.surname
        user_id_number = user_db_data.id_number
        
        blc_user_class = User(user_name, user_surname, user_id_number)
        blc_user_vote_information_class = User_vote_information(blc_user_class, user_input)
        blc_user_voteblock_class = VoteBlock("Initialiser", user_vote_information=blc_user_vote_information_class)

        # add party name to database
        user_db_data.party_vote = user_input
        db.session.commit()

        return redirect(url_for("home"))
    
    return render_template("vote.html",
                           party_names=modified_political_party,
                           party_img_path=POLITICAL_PARTY_IMAGE_PATH,
                           party_descriptions=PARTY_DESCRIPTIONS,
                           party_colors=PARTY_COLORS,
                           is_logged_in=current_user.is_authenticated)


@app.route("/results")
def results():
    vote_data = [data.party_vote for data in db.session.query(Users).all()]
    vote_stats = {party.lower(): 1 for party in POLITICAL_PARTIES}

    for (k, v) in vote_stats.items():
        if k in vote_data:
            vote_stats[k] = vote_data.count(k)

    modified_vote_stats = [vote_stats[key] for key in vote_stats][::-1]

    chart_cls = ResultsChart(POLITICAL_PARTIES[::-1], modified_vote_stats, PARTY_COLORS[::-1])
    chart_cls.make_bar_chart()
    chart_cls.make_pie_charts()

    pie_charts = [img_path.split()[-1].lower() for img_path in POLITICAL_PARTIES]
    stats_des = [STATS_DESCRIPTIONS[num].replace("[insert percentage]", str(round(chart_cls.percentages[num], 2))) for num in range(len(STATS_DESCRIPTIONS))]

    return render_template("results.html",
                           parties=POLITICAL_PARTIES,
                           pie_charts=pie_charts,
                           stats_des=stats_des,
                           colors=PARTY_COLORS,
                           is_logged_in=current_user.is_authenticated)


@app.route("/faq")
def faq():
    return render_template("faq.html", is_logged_in=current_user.is_authenticated)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

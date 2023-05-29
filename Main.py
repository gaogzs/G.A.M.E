# Import Modules
from RandomModule import funcPicker
from flask import *
from tinydb import *
from Security import *
from random import random, choice, choices
from datetime import *
from RaschModel import *
from os import remove

script = Flask(__name__)
script.secret_key = b'rbaehryjg078t g8 4720fpwe0788998T708&*t^(*t o)vhjvui^UI*t76R'


def take_column(table, key):
    column = []
    for row in table:
        column.append(row[key])
    return column

# Function to sort a list of dictionary by a certain key


def sort_dict_list(undecorated, sort_on):
    decorated = [(dict_[sort_on], dict_) for dict_ in undecorated]
    decorated.sort(key=lambda tup: tup[0])
    result = [dict_ for (key, dict_) in decorated]
    return result

# While accessing the website, dierect to the login page
@script.route("/")
def index():
    return redirect(url_for("login"))

# Login page
@script.route("/login", methods=["POST", "GET"])
def login():
    error_message = ""  # Initalise error message
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]  # Tske returned values
        user_list = TinyDB("databases/userlist.json")
        stored_user = user_list.get(where("username") == username)
        if not stored_user:  # If username not in database, return error
            error_message = "User not found"
        elif not check_encrypted_password(password, stored_user["password"]):  # If password failed comparison, return error
            error_message = "Password incorrect"
        else:  # If nothing aboved happen, initialise the user's information and redirect to menu
            session["username"] = stored_user["username"]
            session["authority"] = stored_user["authority"]
            return redirect(url_for("login_redirect"))
        flash(error_message, "login_error")  # Flash the error to the html document
    return render_template("login.html")

# A redirect page to tell user they have logged in
@script.route("/login_redirect")
def login_redirect():
    return render_template("redirect.html", process="Log in", target="main menu", redirect_url=url_for("home"))

# Register page
@script.route("/register", methods=["POST", "GET"])
def register():
    error_message = ""  # Initalise error message
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        rpassword = form["rpassword"]
        user_list = TinyDB("databases/userlist.json")
        stored_user = user_list.get(where("username") == username)
        if stored_user:  # If username already in database, return error
            error_message = "User already exist"
        elif password != rpassword:  # If two passwords are different, return error
            error_message = "Repeated passwords don't match"
        elif len(password) < 6:  # If password too short, return error
            error_message = "Password has to be at least 6 characters"
        else:  # If nothing aboved happen, store the user to database and redirect to login page
            user_list.insert({"username": username, "password": encrypt_password(password), "authority": "normal", "ability": 1, "done_sets": []})  # All registered accounts are normal accounts, testers and admins can only be set manually
            return redirect(url_for("register_redirect"))
        flash(error_message, "register_error")
    return render_template("register.html")

# A redirect page to tell user they have registered
@script.route("/register_redirect")
def register_redirect():
    return render_template("redirect.html", process="Register", target="log in page", redirect_url=url_for("login"))

# The home page
@script.route("/home", methods=["POST", "GET"])
def home():
    exam_record = TinyDB("databases/examrecord.json")
    set_list = TinyDB("databases/setlist.json")
    user_list = TinyDB("databases/userlist.json")  # Initalise databases
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        actype = form["actype"]
        if actype == "normal":
            user_list.insert({"username": username, "password": encrypt_password(password), "authority": actype, "ability": 1, "done_sets": []})
        else:
            user_list.insert({"username": username, "password": encrypt_password(password), "authority": actype, "ability": 1})
    ability = user_list.get(where("username") == session["username"])["ability"]
    if session["authority"] == "admin":  # If user is an admin, fetch all exam record, otherwise the user's records only
        visible_record = exam_record.all()
    else:
        visible_record = exam_record.search(where("username") == session["username"])
    topic_count = {}
    if exam_record.search((where("type") == "regular practice") & (where("username") == session["username"])):  # Fetch the number of different topics the user has done
        for row in exam_record.search((where("type") == "regular practice") & (where("username") == session["username"])):
            get_topic = set_list.get(where("setname") == row["setname"])["topic"]
            if get_topic not in topic_count:
                topic_count[get_topic] = 1
            else:
                topic_count[get_topic] += 1
    return render_template("menu.html", username=session["username"], authority=session["authority"], record=visible_record, topic_key=list(topic_count.keys()), topic_value=list(topic_count.values()), ability=ability)

# View the answering detail of the record
@script.route("/view-record/<string:username>/<path:datetime>")
def view_record(username, datetime):
    exam_record = TinyDB("databases/examrecord.json")
    target_record = exam_record.get((where("username") == username) & (where("datetime") == datetime))
    marks = target_record["marks"]
    set_name = target_record["setname"]
    set_viewing = TinyDB("questionset/{}.json".format(set_name))  # Get the mark and set content of that record
    number_serie = [i for i in range(len(marks))]

    return render_template("view_record.html", set=set_viewing.all(), authority=session["authority"], marks=marks, serie=number_serie)

# Starting page of practice section
@script.route("/exam")
def exam():
    set_list = TinyDB("databases/setlist.json")
    user_list = TinyDB("databases/userlist.json")  # Initalise databases
    if session["authority"] == "normal":  # A normal user can only do one question set once
        done_sets = user_list.get(where("username") == session["username"])["done_sets"]
    else:
        done_sets = []
    return render_template("exam.html", set_list=set_list, authority=session["authority"], page="exam", done_sets=done_sets)


# Actual practice section
mark_list = []
@script.route("/exam/<path:set_name>", methods=["POST", "GET"])
def examing(set_name):
    global mark_list
    set_list = TinyDB("databases/setlist.json")
    if "/" in set_name:  # Once answered
        set_name, question_index = set_name.split("/", 1)
        set_topic = set_list.get(where("setname") == set_name)["topic"]
        question_count = set_list.get(where("setname") == set_name)["question_count"]
        set_examing = TinyDB("questionset/{}.json".format(set_name))
        n = len(set_examing)
        number_serie = [i for i in range(n)]
        if question_index == "end":  # If the exam has ended
            correct_count = 0
            wrong_count = 0
            for mark in mark_list:
                if mark > 0:
                    correct_count += 1
                elif mark < 0:
                    wrong_count += 1
            exam_record = TinyDB("databases/examrecord.json")
            user_list = TinyDB("databases/userlist.json")
            set_difficulty = set_list.get(where("setname") == set_name)["difficulty"]
            user_ability = user_list.get(where("username") == session["username"])["ability"]
            if session["authority"] == "normal":  # If normal user, add the current question set to already answered
                current_done_sets = user_list.get(where("username") == session["username"])["done_sets"]
                current_done_sets.append(set_name)
                user_list.update({"done_sets": current_done_sets}, where("username") == session["username"])
            now = datetime.now()  # Record the current time
            current_time = now.strftime("%m/%d/%Y|%H:%M:%S")
            exam_record.insert({"type": "regular practice", "username": session["username"], "ability": user_ability, "setname": set_name, "difficulty": set_difficulty, "datetime": current_time, "marks": mark_list})  # Add to the exam record
            if session["authority"] == "normal":  # If normal user, its new ability is calculated
                rasch_matrix = exam_record.search(where("username") == session["username"])
                rasch_abil = estimate_abil(rasch_matrix)
                user_list.update({"ability": rasch_abil}, where("username") == session["username"])
                new_ability = rasch_abil
            else:
                new_ability = user_ability
            return render_template("exam_result.html", total=n, correct=correct_count, wrong=wrong_count, page="exam", topic=set_topic, authority=session["authority"], old_ability=user_ability, new_ability=new_ability)  # Display the final result
        else:
            question_index = int(question_index)
            set_examing_list = set_examing.all()
            if request.method == "POST":  # If an answer is returned
                form = request.form
                mark_list[question_index] = 1  # Preset the mark to be correct
                for key, value in set_examing_list[question_index]["answer"].items():
                    if str(value) != form[key]:
                        mark_list[question_index] = -1  # If any element of the answer is wrong, set it as wrong
    else:
        set_topic = set_list.get(where("setname") == set_name)["topic"]
        question_count = set_list.get(where("setname") == set_name)["question_count"]
        set_examing = TinyDB("questionset/{}.json".format(set_name))  # Open the question set
        n = len(set_examing)
        question_index = -1
        number_serie = [i for i in range(n)]
        mark_list = [0 for i in range(n)]  # Initialise marks

    flash(mark_list, "mark")
    return render_template("exam_set.html", set=set_examing, name=set_name, authority=session["authority"], index=question_index, serie=number_serie, page="exam", topic=set_topic, question_count=question_count)

# Algorithm to decide the following question set
@script.route("/exam_next")
def next():
    user_list = TinyDB("databases/userlist.json")
    set_list = TinyDB("databases/setlist.json")  # Initalise databases
    ability = user_list.get(where("username") == session["username"])["ability"]
    done_sets = user_list.get(where("username") == session["username"])["done_sets"]  # Filtering sets not answered yet
    available_sets = set_list.search(~ (where("setname").one_of(done_sets)))
    available_sets = sort_dict_list(available_sets, "difficulty")  # Sort the list of sets from lower difficulty to higher
    last_dif = 11
    for row in available_sets:  # Finding the available set with least difference in difficulty and ability
        if row["difficulty"] >= ability:
            if row["difficulty"] - ability < last_dif:
                next_set_name = row["setname"]
            break
        else:
            last_dif = ability - row["difficulty"]
            next_set_name = row["setname"]
    return redirect("/exam/{}".format(next_set_name))

# Starting page of rasch testing
@script.route("/rasch", methods=["POST", "GET"])
def rasch():
    set_list = TinyDB("databases/setlist.json")
    user_list = TinyDB("databases/userlist.json")  # Initalise databases
    ability = user_list.get(where("username") == session["username"])["ability"]
    if request.method == "POST":  # Change recorded ability if requested
        form = request.form
        user_list.update({"ability": float(form["ability"])}, where("username") == session["username"])
        ability = float(form["ability"])
    return render_template("exam.html", set_list=set_list, authority=session["authority"], page="rasch", current_ability=ability, done_sets=[])


# Actual rasch test
mark_list = []
@script.route("/rasch/<path:set_name>", methods=["POST", "GET"])
def estimation(set_name):  # Almost everything is the same as regular practice
    global mark_list
    set_list = TinyDB("databases/setlist.json")
    if "/" in set_name:
        set_name, question_index = set_name.split("/", 1)
        set_topic = set_list.get(where("setname") == set_name)["topic"]
        question_count = set_list.get(where("setname") == set_name)["question_count"]
        set_examing = TinyDB("questionset/{}.json".format(set_name))
        n = len(set_examing)
        number_serie = [i for i in range(n)]
        if question_index == "end":  # Difference is at this ending section
            correct_count = 0
            wrong_count = 0
            for mark in mark_list:
                if mark > 0:
                    correct_count += 1
                elif mark < 0:
                    wrong_count += 1
            exam_record = TinyDB("databases/examrecord.json")
            user_list = TinyDB("databases/userlist.json")  # Initalise databases
            set_difficulty = set_list.get(where("setname") == set_name)["difficulty"]
            user_ability = user_list.get(where("username") == session["username"])["ability"]
            now = datetime.now()
            current_time = now.strftime("%m/%d/%Y|%H:%M:%S")
            exam_record.insert({"type": "difficulty estimation", "username": session["username"], "ability": user_ability, "setname": set_name, "difficulty": set_difficulty, "datetime": current_time, "marks": mark_list})
            rasch_matrix = exam_record.search((where("setname") == set_name) & (where("type") == "difficulty estimation"))  # Find all related records to this set
            rasch_dif = estimate_dif(rasch_matrix)  # Go through the Rasch algorithm
            set_list.update({"rasch_dif": rasch_dif}, where("setname") == set_name)  # Update new estimated difficulty

            return render_template("exam_result.html", total=n, correct=correct_count, wrong=wrong_count, page="rasch", authority=session["authority"])
        else:
            question_index = int(question_index)
            set_examing_list = set_examing.all()
            if request.method == "POST":
                form = request.form
                mark_list[question_index] = 1
                for key, value in set_examing_list[question_index]["answer"].items():
                    if str(value) != form[key]:
                        mark_list[question_index] = -1
    else:
        set_topic = set_list.get(where("setname") == set_name)["topic"]
        question_count = set_list.get(where("setname") == set_name)["question_count"]
        set_examing = TinyDB("questionset/{}.json".format(set_name))
        n = len(set_examing)
        question_index = -1
        number_serie = [i for i in range(n)]
        mark_list = [0 for i in range(n)]

    flash(mark_list, "mark")
    return render_template("exam_set.html", set=set_examing, name=set_name, authority=session["authority"], index=question_index, serie=number_serie, page="rasch", topic=set_topic, question_count=question_count)

# Generation page
@script.route("/generation", methods=["POST", "GET"])
def generator():
    set_list = TinyDB("databases/setlist.json")
    if request.method == "POST":
        question_table = TinyDB("databases/questdb.json")
        form = request.form
        topic = form["topic"]  # Return topic, difficulty and amount of questions
        difficulty = float(form["difficulty"])
        n = int(form["amount"])
        available = question_table.search((where("type") == topic) & (where("base_dif") <= difficulty))  # Fetch all templates with same topic and lower base difficulty
        base_dif_list = take_column(available, "base_dif")  # Take the column of base difficulty
        set_name = str(int(10000000 * random()))  # Randomly generate a set name which is a string of number
        while set_list.search(where("name") == set_name):  # The name must not exist before
            set_name = str(int(10000000 * random()))
        new_path = "questionset/{}.json".format(set_name)  # Set the path to store the set
        new_set = TinyDB(new_path)
        for i in range(n):
            new_quest = choices(available, [(difficulty - k) for k in base_dif_list])[0]  # Choose template with weight, harder templates are less likely to be chosen
            new_set.insert(funcPicker[new_quest["index"]](difficulty - new_quest["base_dif"]))
        set_list.insert({"setname": set_name, "difficulty": -1, "question_count": n, "rasch_dif": -1, "topic": topic})  # Register the new set
    question_table = TinyDB("databases/questdb.json")
    topic_list = []
    for row in question_table:  # Fetch all different topics for the user to choose
        if not row["type"] in topic_list:
            topic_list.append(row["type"])

    return render_template("generator.html", topic_list=topic_list, set_list=set_list, authority=session["authority"])

# Page for viewing generated question sets and change difficulty
@script.route("/view-set/<set_name>", methods=["POST", "GET"])
def view(set_name):
    set_list = TinyDB("databases/setlist.json")
    current_difficulty = set_list.get(where("setname") == set_name)["difficulty"]
    set_viewing = TinyDB("questionset/{}.json".format(set_name))
    if request.method == "POST":  # Change the set's difficulty if requested
        form = request.form
        new_difficulty = float(form["new_difficulty"])
        set_list.update({"difficulty": new_difficulty}, where("setname") == set_name)
    return render_template("view_set.html", set=set_viewing, name=set_name, authority=session["authority"], current_difficulty=current_difficulty)

# Function to delete existing set
@script.route("/delete-set/<set_name>")
def delete(set_name):
    set_list = TinyDB("databases/setlist.json")  # Delete from register list
    set_list.remove(where("setname") == set_name)
    remove("questionset/{}.json".format(set_name))  # Delete the file

    return redirect("/generation")


if __name__ == "__main__":
    script.run(host="127.0.0.1", port="5000", debug=True)

from flask import Flask, render_template, request, session
# from flask_session import Session
# uuid can identify each user separetly by saving their ip,mac etc addresses
import uuid
# to change file name so that each users profile picture file name will become unique
import os
import schedule

app = Flask(__name__)

# app.config["SESSION_PARMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

app.secret_key = "SecretKey"

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/design")
def design():
    return render_template("design.html")

@app.route("/form/<string:design>", methods=["POST"])
def form(design):
    session["design_session"] = design
    return render_template("form.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    design_upload = session.get("design_session")
    if design_upload == "design1":
        design_name = "design1.html"
    elif design_upload == "design2":
        design_name = "design2.html"
    elif design_upload == "design3":
        design_name = "design3.html"
    elif design_upload == "design4":
        design_name = "design4.html"
    if request.method == "POST":
        user_data = {
            'firstname': request.form.get('firstname'),
            'lastname': request.form.get('lastname'),
            'facebook': request.form.get('facebook'),
            'github': request.form.get('github'),
            'schoolName': request.form.get('schoolName'),
            'collegename': request.form.get('collegename'),
            'phoneNumber': request.form.get('phoneNumber'),
            'email': request.form.get('email'),
            'about': request.form.get('about'),
            'skill1': request.form.get('skill1'),
            'skill2': request.form.get('skill2'),
            'skill3': request.form.get('skill3')
        }
        # Image Saving
        key = uuid.uuid1() # Will Generate new key every time
        img = request.files["profile_pic"]
        img.save(f"static/user_images/{img.filename}") # image save folder
        img_new_name = f"{key}{img.filename}"
        os.rename(f"static/user_images/{img.filename}", f"static/user_images/{img_new_name}") # rename so that every file name won't same 

    return render_template(design_name, user=user_data, img = img_new_name)

def delete():
    files = os.listdir("static/user_images")
    for i in files:
        # print(i)
        os.remove(f"static/user_images/{i}")

if __name__ == "__main__":
    schedule.every().day.at("23:59").do(delete)
    app.run(debug=True)

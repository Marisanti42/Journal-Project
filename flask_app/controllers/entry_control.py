from flask import redirect, render_template, request, session
from flask_app.models import entry_model
from flask_app import app

#Add a entry route
@app.route("/entry/new")
def new_entry():
    if "user_id" not in session:
        return redirect ("/")
    first_name = session["first_name"]
    id = session["user_id"]
    return render_template("new_entry.html", first_name=first_name, id=id)

#New entry added to database
@app.route("/entry/create", methods=["POST"])
def add_entry():
    if "user_id" not in session:
        return redirect("/")
    is_valid = entry_model.Entry.validate_entry(request.form)
    if not is_valid:
        return redirect("/entry/new")
    else:
        data = {
            'title':request.form["title"],
            'content':request.form["content"],
            'user_id':session["user_id"]
        }
        id = entry_model.Entry.new_entry(data)
        entry_model.Entry.new_entry(data)
        return redirect(f"/show/{id}")

#View a specific entry route 
@app.route("/show/<int:id>")
def show_entry(id):
    if "user_id" not in session:
        return redirect("/")
    first_name = session["first_name"]
    this_entry = entry_model.Entry.view_entry(id)
    id = session["user_id"]
    return render_template("show_entry.html", first_name=first_name, entry=this_entry, id=id)

#Edit a entry route
@app.route("/edit/<int:id>")
def edit_entry(id):
    if 'user_id' not in session:
        return redirect("/")
    first_name = session["first_name"]
    entry = entry_model.Entry.view_entry(id)
    id = session["user_id"]
    return render_template("edit_entry.html", entry=entry, first_name=first_name, id=id)

#Entry is updated in the database
@app.route("/edit/<int:id>/update", methods=["POST"])
def update_entry(id):
    if 'user_id' not in session:
        return redirect("/")
    is_valid = entry_model.Entry.validate_entry(request.form)
    if not is_valid:
        return redirect(f"/edit/{id}")
    else:
        data = {
            'title':request.form["title"],
            'content':request.form["content"],
            'updated_at':request.form["updated_at"],
            'user_id':session["user_id"],
            'id':id
        }
        entry_model.Entry.update_entry(data)
        return redirect(f"/show/{id}")

#Delete a entry route
@app.route("/edit/<int:id>/destroy")
def delete_entry(id):
    if 'user_id' not in session:
        return redirect("/")
    entry_model.Entry.delete_entry(id)
    return redirect(f"/user/account/{id}")

from quart import flash
from quart import Quart
from quart import redirect
from quart import render_template
from quart import request

from db import db

app = Quart(__name__)
app.config.update(SECRET_KEY="5ecret")


@app.route("/")
async def home():
    return await render_template("index.html", todos=db.list())  # noqa


@app.route("/create/", methods=["GET", "POST"])
async def create():
    if request.method == "GET":
        return await render_template("form.html")  # noqa
    form = await request.form
    db.create(name=form["name"])
    await flash(message="Created!")
    return redirect("/")


@app.route("/edit/<pk>/", methods=["GET", "POST"], defaults={"pk": None})
@app.route("/edit/<pk>/", methods=["GET", "POST"])
async def edit(pk):
    if request.method == "GET":
        return await render_template("form.html", todo=db.get(pk))  # noqa
    form = await request.form
    db.update(pk, name=form["name"])
    await flash(message="Updated!")
    return redirect("/")


@app.route("/toggle/<pk>/", methods=["GET"])
async def toggle(pk):
    completed = not db.get(pk)["is_completed"]
    db.toggle(pk, completed)
    await flash(message="Toggled!")
    return redirect("/")


@app.route("/delete/<pk>/", methods=["GET", "POST"])
async def delete(pk):
    if request.method == "GET":
        return await render_template("delete.html", todo=db.get(pk))  # noqa
    db.delete(pk)
    await flash(message="Deleted!")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

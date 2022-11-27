from datetime import datetime
from flask import (
    Flask, 
    redirect,
    render_template, 
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    finished = db.Column(db.Boolean)

    def __repr__(self):
        return f'*Project {self.title}*'


@app.route("/")
def home():
    projects = Project.query.all()

    return render_template(
        "index.html",
        projects_list=projects,
    )

# żądanie wyświetl mi stronę główną - request HTTP GET /
# żądanie wyświetl mi szczegóły zadania - request HTTP GET /task/{id}
# żądanie wyświetl mi stronę z wszystkimi zadaniami - request HTTP GET /tasks
# żądanie utwórz nowe zadanie - request HTTP POST /task + dane

@app.route("/projects", methods=["POST"])
def add_project():
    title = request.form.get("title")
    category = request.form.get("category")
    link = request.form.get("link")

    new_project = Project(
        title=title,
        category=category,
        link=link,
    )

    db.session.add(new_project)
    db.session.commit()
    db.session.close()
    
    return redirect(url_for('home'))
    

@app.route("/projects/<int:id>/delete")
def delete_project(id):
    project_to_delete = Project.query.get_or_404(id)
    
    db.session.delete(project_to_delete)
    db.session.commit()
    db.session.close()
    return redirect(url_for('home'))


@app.route("/projects/<int:id>/change_status")
def change_status(id):
    project = Project.query.get_or_404(id)
    project.finished = not project.finished

    db.session.commit()
    return redirect(url_for('home'))
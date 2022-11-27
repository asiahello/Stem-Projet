import requests

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
    weather_mood = get_weater_mood()

    return render_template(
        "index.html",
        projects_list=projects,
        weather_mood=weather_mood,
    )

def get_weater_mood():
    temperature, pressure, rainfall = get_weather_data()
    rain_info = get_rain_info(rainfall)

    if pressure < 1010 or pressure > 1025:
        work_mood = 'nie sprzyja'
        comment = 'czekam na lepsze ciśnienie'
    else:  # cisnienie jest ok
        if rainfall < 10:  # nie pada
            if temperature > 20: # nie pada i jest ciepło
                work_mood = 'nie sprzyja'
                comment = 'nie pada więc możliwe że jeste offline'
            else: # nie pada i jest zimno
                work_mood = 'sprzyja'
                comment = 'ale przyja również spacerom'
        else:  # pada
            work_mood = 'sprzyja'
            comment = 'więc prawdopodobnie pracuję nad którymś z projektów'

    return f'Pogoda {work_mood} programowaniu, {comment}. PS. {rain_info}'

def get_weather_data():
    url = 'https://danepubliczne.imgw.pl/api/data/synop/station/warszawa'
    response = requests.get(url)
    weather_data = response.json()
    temperature = float(weather_data['temperatura'])
    pressure = float(weather_data['cisnienie'])
    rainfall = float(weather_data['suma_opadu'])
    return temperature, pressure, rainfall

def get_rain_info(rainfall):
    if rainfall < 1:
        return 'Dziś nie pada :)'
    elif rainfall < 10:
        return 'Może lekko popadać'
    else:
        return 'Weź parasol!'


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
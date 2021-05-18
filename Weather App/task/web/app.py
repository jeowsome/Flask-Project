import sys

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_sqlalchemy import SQLAlchemy

from weather_service import get_current_weather, check_city

app = Flask(__name__)
app.config['SECRET_KEY'] = "69c56eeb6775b9eebe832cf96cf7e4f7"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class City(db.Model):
    """Data model for the city."""
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return self.name


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        cities = City.query.all()
        cities_weather = [get_current_weather(city=city.name, city_id=city.id) for city in cities]
        return render_template('index.html', weather=cities_weather)
    elif request.method == 'POST':
        city_name = request.form.get("city_name")
        if city_name:
            city_name = city_name.rstrip()
            if check_city(city_name):
                query = City.query.filter_by(name=city_name).first()
                if not query:
                    new_city = City(name=city_name)
                    db.session.add(new_city)
                    db.session.commit()
                else:
                    flash('The city has already been added to the list!')
                return redirect(url_for('index'))
            else:
                flash("The city doesn't exist!")
                return redirect('/')
        else:
            flash('Enter city name!')
            return redirect(url_for('index'))


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    if city is not None:
        db.session.delete(city)
        db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

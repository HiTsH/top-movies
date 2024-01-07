from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
# Create database movies-collection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
db = SQLAlchemy()
db.init_app(app)

TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/original/'
TMDB_ACCESS_TOKEN = 'Your API Read Access Token'
TMDB_API_KEY = 'Your API Key'
headers = {
    'authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
    'accept': 'application/json',
}


# Create db tables
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


class EditForm(FlaskForm):
    new_rating = StringField(label='Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    new_review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label='Done')


class AddForm(FlaskForm):
    add = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')


@app.route("/")
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.id)).scalars()
    return render_template("index.html", movies=all_movies)


@app.route('/edit', methods=['GET', 'POST'])
def edit_movie():
    form = EditForm()
    movie_id = request.args.get('id', type=int)
    movie_selected = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():
        movie_selected.rating = form.new_rating.data
        movie_selected.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', id=movie_id, form=form, movie=movie_selected)


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    form = AddForm()
    movie_title = form.add.data
    if form.validate_on_submit():
        params = {
            'query': movie_title,
        }
        url = 'https://api.themoviedb.org/3/search/movie'

        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()['results']

            return render_template('select.html', movies=data)

        except requests.exceptions.RequestException as e:
            print(f'Error during API request: {e}')
    return render_template('add.html', title=movie_title, form=form)


@app.route('/delete')
def delete_movie():
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/find')
def find_movie():
    movie_api_id = request.args.get('id')
    if movie_api_id:
        url = f'https://api.themoviedb.org/3/movie/{movie_api_id}'

        response = requests.get(url=url, headers=headers)
        data = response.json()
        new_movie = Movie(
            title=data['title'],
            year=data['release_date'].split('-')[0],
            description=data['overview'],
            img_url=f'{TMDB_IMAGE_URL}{data["poster_path"]}',
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit_movie', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)

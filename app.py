from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db = SQLAlchemy(app)

# Define the Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

# WTForm for adding a new song
class SongForm(FlaskForm):
    id = IntegerField('ID')
    genre = StringField('Žánr', validators=[DataRequired()])
    artist = StringField('Interpret', validators=[DataRequired()])
    title = StringField('Píseň', validators=[DataRequired()])
    year = IntegerField('Rok Vydání', validators=[DataRequired()])
    submit = SubmitField('Přidat Píseň')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()
    if not Song.query.first():
        db.session.add_all([
            Song(genre='Pop', artist='Michael Jackson', title='Thriller', year=1982),
            Song(genre='Rock', artist='Queen', title='Bohemian Rhapsody', year=1975),
            Song(genre='Jazz', artist='Miles Davis', title='So What', year=1959)
        ])
        db.session.commit()

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(id=form.id.data, genre=form.genre.data, artist=form.artist.data, title=form.title.data, year=form.year.data)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    song = Song.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

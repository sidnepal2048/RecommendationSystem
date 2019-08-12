from flask import Flask, render_template, url_for, request, redirect, flash, session
from forms import RegistrationForm, LoginForm, SearchMovies
from flaskext.mysql import MySQL
import movierecommend
import startmovieslist


mysql = MySQL()

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'recommend'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['SECRET_KEY'] = '11184a54434874b276bb840f788d5cc1'
conn = mysql.connect()
cursor = conn.cursor()
posts = [

	{
		'author': 'Siddhartha Nepal',
		'title': 'Movie Recommendation System',
		'content': 'List of Movies',
		'date_posted': 'August 12, 2019'
	}
]


@app.route("/")
@app.route("/home")
def home():
	print('I am in home')
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	form1 = SearchMovies()
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		print('email: ' + email)
		password = request.form['password']
		print('password: ' + password)
		cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
		account = cursor.fetchone()
		print('User_id: ')
		print((account[0:1][0]))
		if account:
			print('I passed login form')
			session['loggedin'] = True
			session['user_id'] = account[0]
			print('user_id from session')
			print(session['user_id'])
			print('I am above search.html')
			movie1 = startmovieslist.movielist
			print(movie1)
			return render_template('search.html', form=form1, movie1=movie1)
		else:
			msg = 'Incorrect username/password!'
	return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	#if form.validate_on_submit():
	if request.method == "POST":
		details = request.form
		username = details['username']
		email = details['email']
		password = details['password']
		confirmPassword = details['confirm_password']
		cursor.execute("INSERT INTO user(username, email, password, confirmPassword) VALUES (%s, %s, %s, %s )", (username, email, password, confirmPassword))
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			flash('Your account has been created! You are now able to log in', 'success')
			return redirect(url_for('home'))
		else:
			flash('Not success', 'unsuccessful')
	return render_template('register.html', title='Register', form=form)


@app.route("/search", methods=['POST', 'GET'])
def search():
	form = SearchMovies()
	if request.method == 'POST':
		user_id = session['user_id']
		print('I am in search route')
		print(user_id)
		movies = request.form['movies'].strip()
		print('here is entered movies name')
		#print(movierecommend.recommend_movie(movies))
		movi = movierecommend.recommend_movie(movies, user_id)
		print(movi)
		return render_template('movies.html', movi=movi)
	return render_template('search.html', title='Search Movies', form=form)


@app.route("/logout")
def logout():
	#form = SearchMovies()
	if 'loggedin' in session:
		return redirect(url_for('login'))
		#return render_template('search.html', user_id=session['user_id'], form=form)
	#return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)



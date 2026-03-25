from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from password_manager import init_db, add_account, get_accounts, get_fernet

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

fernet = get_fernet()
init_db()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template('contact.html', success=True)
    return render_template('contact.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        add_account(website, username, password, fernet)
        return redirect(url_for('list_accounts'))
    return render_template('add.html')

@app.route('/list')
def list_accounts():
    accounts = get_accounts(fernet)
    return render_template('list.html', accounts=accounts)

@app.route('/users')
def user_list():
    users = User.query.all() 
    return render_template('user_list.html', users=users)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
      
        if User.query.count() == 0:
            admin_user = User(username='admin', email='admin@example.com', is_admin=True)
            normal_user = User(username='user1', email='user1@example.com', is_admin=False)
            db.session.add_all([admin_user, normal_user])
            db.session.commit()

    app.run(port=8000, debug=True)

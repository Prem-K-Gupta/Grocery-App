from flask import Flask, render_template, request, session,redirect,url_for, flash
# from application.my_decorator import check_role_and_username
from application.database import *

secret_key = 'atoinlanioj48re7at90wliovaorv'

def check_role_and_username(f,role=None):
    if session.get('current_user'):
        if session['current_user']['role']=='admin':
            return f
        else:
            return 'Unknown role.'
    else:
        return "Something went wrong"

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.app_context().push()
db.create_all()

# Now controllers come here

@app.route('/login/user',methods=['GET', 'POST'])
def login_user():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user:
            if user.password==password:
                if user.role=='user':
                    current_user={}
                    current_user['role']="user"
                    current_user['username']=username
                    session['current_user']=current_user
                    if 'session_cart' not in session:
                        session['session_cart'] = []
                    flash("User login successful.")
                    return redirect(url_for('user_page'))
                else:
                    return render_template('login_user.html', message_type='warning', message_body="You are not authorized to access this page!")
            else:
                return render_template('login_user.html', message_type='danger', message_body="Either username or password wrong!")
        else:
            return render_template('login_user.html', message_type='warning', message_body="User not found")
    return render_template('login_user.html')

@app.route('/login/manager',methods=['GET', 'POST'])
def login_manager():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user=User.query.filter_by(username=username).first()
        if user:
            if user.password==password:
                if user.role=='admin':
                    current_user={}
                    current_user['role']="admin"
                    current_user['username']=username
                    session['current_user']=current_user
                    flash("You have login successfully.")
                    return redirect(url_for('manager_page'))
                else:
                    return render_template('login_manager.html', message_type='warning', message_body="You are not authorized to access this page!")
            else:
                return render_template('login_manager.html', message_type='danger', message_body="Either username or password wrong!")
        else:
            return render_template('login_manager.html', message_type='warning', message_body="User not found!")
    return render_template('login_manager.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user:
            user=User(username=username, password=password, role="user")
            db.session.add(user)
            db.session.commit()
            current_user={}
            current_user['role']="user"
            current_user['username']=username
            session['current_user']=current_user
            if 'session_cart' not in session:
                session['session_cart'] = []
            flash("Registeration successful")
            return redirect(url_for('user_page'))
        else:
            return render_template('register.html', message_type='info', message_body="User already exits!")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout successful!")
    return redirect(url_for('index'))

from application.manager import *
from application.user import *
from application.welcome import *


# code to run the app
if __name__=='__main__':
    app.run(debug=True)

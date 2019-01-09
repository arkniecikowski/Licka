import os, sqlite3
from flask import Flask, request, render_template, redirect, url_for,g, flash, session, logging
from werkzeug import secure_filename
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

UPLOAD_FOLDER_TXT = '/root/zapis/txt'
UPLOAD_FOLDER_PHOTOS = '/root/zapis/photos'
ALLOWED_EXTENSIONS_TXT = set(['txt'])
ALLOWED_EXTENSIONS_PHOTOS = set(['jpg','png','jpeg','gif'])
DATABASE = '/path/to/ex1.db'

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_TXT

def allowed_file_photos(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_PHOTOS

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db
	
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
 
 
app.config['UPLOAD_FOLDER_TXT'] = UPLOAD_FOLDER_TXT
app.config['UPLOAD_FOLDER_PHOTOS'] = UPLOAD_FOLDER_PHOTOS

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_TXT'], filename))
            return redirect(url_for('index',filename=filename))
        elif file and allowed_file_photos(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_PHOTOS'], filename))
            return redirect(url_for('index',filename=filename))
    return render_template('upload.html')

class RegisterForm(Form):
	name = StringField('name', [validators.Length(min=1,max=50)])
	password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Password do not match')])
	confirm = PasswordField('Confirm Password')
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		return render_template('home.html')	
	return render_template('register.html',form=form)	
	
if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0',port=5005)

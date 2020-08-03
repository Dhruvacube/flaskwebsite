from flask import Flask, render_template, request, session, redirect,flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os
import pymysql
from random import sample
import secrets 
import pyqrcode
from PIL import Image
import shutil
pymysql.install_as_MySQLdb()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'config.json')

with open(my_file, 'r') as c:
    params = json.load(c)["params"]

local_server = True
"""
pip install wheel
pip install pymysql
"""

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','pdf','txt', 'html', 'php', 'css', 'css', 'js', 'ppt', 'ppsx', 'pptx', 'py', 'docx', 'doc', 'exe', 'mp4', 'wav', 'mpe4', 'mp3'}
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(50)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)
mail.init_app(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(250), unique=False, nullable=True)
    msg = db.Column(db.String(250), unique=False, nullable=False)
    dt_time = db.Column(db.String(120), unique=True, nullable=True)

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80), unique=False, nullable=False)
    body = db.Column(db.String(120), unique=False, nullable=False)

class Passwordtracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    dt_time = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def home():
    """For The Cover Page"""
    name1 = "Dhruva Shaw"
    cover = Cover.query.all()
    return render_template('cover.html', title = name1,params=params,cover=cover)

@app.route("/main")
def main():
    """Enters the main site"""
    name1 = "Dhruva Shaw"
    return render_template('index.html', title = name1,params=params)

@app.route("/about")
def about():
    """About Us Section"""
    name1 = "Dhruva Shaw | About Us|"
    return render_template('about.html', title = name1,params=params)

@app.route("/sitetester", methods = ['GET','POST'])
def sitetester():
    """SiteTester Section"""
    name1 = "Dhruva Shaw | SiteTester|"
    return render_template('sitetester.html', title = name1,params=params)

@app.route("/contact", methods = ['GET','POST'])
def contact():
    """Contact Us Section"""
    if request.method=='POST':
        """ADD ENTRY TO DATABASE"""
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        msg = request.form.get('message')
        date = datetime.now()
        entry = Contacts(name=name, email=email, subject=subject, msg=msg, dt_time=date)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name +' given at Dhruva Shaw',
                          sender=email,
                          recipients=[params['gmail-user']],
                          body="Name: "+name+"\n"+"Subject: "+ subject+ "\n"+"Message of the user: "+msg + "\n"+"Email-ID: "+email
                          )

    name1 = "Dhruva Shaw | Contact Us |"
    return render_template('contact.html', title = name1,params=params)

@app.errorhandler(404)
def page_not_found(e):
    name1= "| Url not Found |"
    # note that we set the 404 status explicitly
    return render_template('404.html', params=params, title=name1), 404



#######################################################
#The Admin Page Functions

#Dashboard and Login
@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    """For login page and dashboard page"""
    name1 = "| Welcome to Dashboard |"
    if ('user' in session and session['user']==params['admin_email']):
        return render_template('dashboard-admin.html', title=name1, params=params)
    if (request.method=='POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if(username== params['admin_email'] and password==params['admin_password']):
            session['user'] = username
            return render_template('dashboard-admin.html', title=name1, params=params)
        else:
            flash('Please enter the password or email correctly!')
    return render_template('login-admin.html', title = name1,params=params)


#######################################################
#Admin Contact Us

#Contact Us Admin
@app.route("/contactus-admin")
def contactusadmin():
    """Admin Contact Us """
    name1 = "Dhruva Shaw ||Admin|| |Contact Us|"
    if ('user' in session and session['user']==params['admin_email']):
        contact = Contacts.query.all()
        return render_template("contactus-admin.html",params=params, title=name1, contact=contact)
    return redirect("/dashboard")


#Delete Contact Us User
@app.route("/delete-contactus-admin/<string:id>")
def deletecontactusadmin(id):
    """For deleting the contact us responses"""
    if ('user' in session and session['user']==params['admin_email']):
        contact =Contacts.query.filter_by(id=id).first()
        db.session.delete(contact)
        db.session.commit()
        flash("The Contact user has been successfully deleted!")
    return redirect('/contactus-admin')


#View Contact Us User
@app.route("/view-contactus-admin/<string:id>")
def viewcontactusadmin(id):
    """For deleting the contact us responses"""
    name1 = "Dhruva Shaw || Admin ||  | View Contact Us |"
    if ('user' in session and session['user']==params['admin_email']):
        contact =Contacts.query.filter_by(id=id).all()
        return render_template('view-contactus-admin.html', params=params, title=name1, contact=contact)
    return redirect("/contactus-admin")


#Mail Contact Us User
@app.route("/mail-contactus-admin/<string:id>", methods=['GET','POST'])
def mailcontactusadmin(id):
    """For deleting the contact us responses"""
    name1 = "Dhruva Shaw || Admin ||  | Mail Contact Us |"
    if ('user' in session and session['user']==params['admin_email']):
        contact =Contacts.query.filter_by(id=id).first()
        if request.method=='POST':
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            msg = request.form.get('message')
            date = datetime.now()
            mail.send_message(subject,
                        sender=params['gmail-user'],
                        recipients=[str(email)],
                        body="Dear, "+"\n"+name+"\n"+"\n"+"Thanks for contacting us."+ "\n"+ str(msg) + "\n"+"\n"+"Regards, "+"\n"+"Dhruva Shaw" +"\n"+"\n"+"Youtube: " + str(params['youtube_url']) + "\n"+"Instagram: " + str(params['insta_url']) + "\n" + "Github: " + str(params['github_url']) + "\n" + "Velosofy: "+str(params['velosofy_url'])
                        )
            flash("The mail has been sent!")
        return render_template('mail-contactus-admin.html', params=params, title=name1, contact=contact)
    return redirect("/contactus-admin")


#Ends
#######################################################



#######################################################
#Forgot Password

@app.route("/forgot")
def forgot():
    mail.send_message('Forgot Your Password ? '+' ||Dhruva Shaw||',
                        sender='dhruvashaw@gmail.com',
                        recipients=[params['gmail-user']],
                        body="IP Address: "+str(request.remote_addr)+"\n"+"Date: "+ str(datetime.now())+ "\n"+"The userId: "+str(params['admin_email'] )+ "\n"+"The Password is: "+ str(params['admin_password'])
                        )
    flash("The password has been sent to your email address")
    return redirect("/dashboard")

#Ends
#######################################################




#######################################################
#Logout

@app.route("/logout")
def logout():
    """For logout session"""
    session.pop('user')
    return redirect('/dashboard')

#Ends
#######################################################




#######################################################
#Password Tracker

@app.route("/password-tracker", methods=['GET','POST'])
def passwordtracker():
    if ('user' in session and session['user']==params['admin_email']):
        name1="Dhruva Shaw ||Admin|| |Password Tracker|"
        pass1 = 7872
        password = Passwordtracker.query.all()
        return render_template("password-tracker-admin.html",params=params, title=name1, pass1=pass1, password=password)

        
    return redirect("/dashboard")


#Delete Password
@app.route("/delete-password/<string:id>", methods=['GET','POST'])
def deletepassword(id):
    if ('user' in session and session['user']==params['admin_email']):
        passwordtracker = Passwordtracker.query.filter_by(id=id).first()
        db.session.delete(passwordtracker)
        db.session.commit()
    return redirect("/password-tracker")


#Add Password
@app.route("/add-password", methods=['GET','POST'])
def addpassword():
    if ('user' in session and session['user']==params['admin_email']):
        website = request.form.get('websiteadd')
        username = request.form.get('usernameadd')
        password = request.form.get('passwordadd')
        dt_time = datetime.now()

        passwordtracker = Passwordtracker(website=website, username=username, password=password, dt_time=dt_time)
        db.session.add(passwordtracker)
        flash('The password has been added to database sucessfully!')
        db.session.commit()

    return redirect("/password-tracker")
#Ends
#######################################################


#######################################################
#File manager

@app.route('/filemanager', defaults={'req_path': ''})
@app.route('/filemanager/<path:req_path>')
def dir_listing(req_path):
    """File Manager"""
    name1 = "Dhruva Shaw ||Admin|| |Filenamanager|"
    if ('user' in session and session['user']==params['admin_email']):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.join(THIS_FOLDER, 'static/assets')

        # Joining the base and the requested path
        abs_path = os.path.join(BASE_DIR, req_path)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = os.listdir(abs_path)
        return render_template('filemanager-admin.html', files=files, params=params,req_path=req_path, title=name1)
    return redirect("/dashboard")


#Delete File
@app.route("/delete-file/<string:id>", methods=['GET','POST'])
def deletefile(id):
    """For deleting the file"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            #Getting the directory to file
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

            #Geting file from form at HTML form
            filename = request.form.get('inlineFormInputGroupUsername')

            #Joining the file
            my_file = os.path.join(THIS_FOLDER, "static/assets/", id, filename)

            #Deleting the file
            os.remove(str(my_file))

            #Flashing the message
            flash('The File has been deleted successfully')
            flash('The file has been deleted')
    return redirect('/filemanager')

#Delete Folder
@app.route("/delete-folder/<string:id>", methods=['GET','POST'])
def deletefolder(id):
    """For deleting the folder"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            #Getting the directory to folder
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

            #Joing the the folder location
            path = os.path.join(THIS_FOLDER, "static/assets/", id)

            # Removing directory  
            shutil.rmtree(path) 
            flash('Folder has been deleted')
    return redirect("/filemanager")

#Create Folder
@app.route("/create-folder", methods=['GET','POST'])
def createfolder():
    """Create Folder"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            nameFolder = request.form.get('foldername')
            path = os.path.join(THIS_FOLDER, "static/assets/", nameFolder)
            try:  
                os.mkdir(path)  
            except OSError as error:  
                flash('A folder with same name already exists!')  
            flash('Folder has been created')
            return redirect("/filemanager")

#Create File
@app.route("/create-file/<string:id>", methods=['GET','POST'])
def createfile(id):
    """Create File"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            nameFile = request.form.get('filename')
            path = os.path.join(THIS_FOLDER, "static/assets/", id)
            with open(os.path.join(path, nameFile), 'w') as fp: 
                pass
            flash('The file has been created!')
            return redirect("/filemanager")
#################
#Uploader

#Check the allowed files
def allowed_file(filename):
    """To files allowed to be uploaded"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Uploader Route
@app.route("/upload/<string:id>", methods=['GET','POST'])
def upload(id):
    """Upload the files"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            UPLOAD_FOLDER = os.path.join(THIS_FOLDER, "static/assets/", id)

            if 'img_file' not in request.files:
                # check if the post request has the file part
                return redirect(request.url)
            
            file = request.files['img_file']

            # if user does not select file, browser also
            # submit an empty part without filename

            if file.filename == '':
                flash('No selected file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('File Uploaded')
            return redirect('/filemanager')

    return redirect("/filemanager")
#########

@app.route("/rename/<string:id>", methods=['GET','POST'])
def rename(id):
    """To rename files"""
    if ('user' in session and session['user']==params['admin_email']):
        if request.method == "POST":
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            nameFileFolder = request.form.get('namefilefolder')
            renameFileFolder = request.form.get('renamefilefolder')

            source = os.path.join(THIS_FOLDER, "static/assets/", id, nameFileFolder)
            dest = os.path.join(THIS_FOLDER, "static/assets/", id, renameFileFolder)

            try : 
                os.rename(source, dest) 
                flash("Source path renamed to destination path successfully.") 
            
            # If Source is a file  
            # but destination is a directory 
            except IsADirectoryError: 
                flash("Source is a file but destination is a directory.") 
            
            # If source is a directory 
            # but destination is a file 
            except NotADirectoryError: 
                flash("Source is a directory but destination is a file.") 
            
            # For permission related errors 
            except PermissionError: 
                flash("Operation not permitted.") 
            
            # For other errors 
            except OSError as error: 
                flash(error)

    return redirect("/filemanager")

#File Mnager Code ends
#######################################################

#Ends
#######################################################


@app.route("/chart")
def chart():
    return render_template("data.html",params=params)

@app.route("/data")
def data():
    return jsonify({'results':sample(range(1,51),5)})

#Running the Python File
if __name__ == '__main__':
    app.run(debug=True)
from flask import render_template, redirect, url_for, request,Response,send_from_directory,make_response
from forms.signin_form import SignInForm
from forms.watermark_form import WatermarkForm
from flask_login import LoginManager, login_required, login_user, logout_user
import os
from database import create_app
from models import User
from core.image import embed_watermark
from core.music import lsb_watermark
from core.video import embed_video

app = create_app()
app.secret_key = 'LearnFlaskTheHardWay2017'

# Add LoginManager
login_manager = LoginManager()
# login_manager.session_protection = 'AdminPassword4Me'
login_manager.session_protection = 'strong'
login_manager.login_view = 'signin'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
login_manager.init_app(app)

IMAGE_PATH = ''
AUDIO_PATH = ''
VIDEO_PATH = ''

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signoff')
@login_required
def signoff():
    logout_user()
    return redirect(url_for('watermark'))

    #return 'Logged out successfully!'


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            next = request.args.get('next')
            return redirect(next or url_for('welcome'))

    return render_template('signin.html', form=form)


@app.route('/welcome', methods=['GET','POST'])
@login_required
def welcome():
    return render_template('welcome.html')


@app.route('/image_upload', methods=['POST'])
def image_upload():
    global IMAGE_PATH
    f = request.files['file']
    save_path = os.path.join(app.instance_path, 'image_upload', f.filename)
    f.save(save_path)
    
    IMAGE_PATH = save_path
    return Response(status=200)

    #return redirect(url_for('watermark'))

@app.route('/audio_upload', methods=['POST'])
def audio_upload():
    global AUDIO_PATH
    f = request.files['file']
    save_path = os.path.join(app.instance_path, 'audio_upload', f.filename)
    f.save(save_path)
    AUDIO_PATH = save_path
    return Response(status=200)

    #return redirect(url_for('watermark1'))

@app.route('/video_upload', methods=['POST'])
def video_upload():
    global VIDEO_PATH
    f = request.files['file']
    save_path = os.path.join(app.instance_path, 'video_upload', f.filename)
    f.save(save_path)
    VIDEO_PATH=save_path
    return Response(status=200)


@app.route('/watermark', methods=['GET', 'POST'])
@login_required
def watermark():
    global IMAGE_PATH
    form = WatermarkForm()
    if form.validate_on_submit():
        if len(IMAGE_PATH)==0:
            return redirect(url_for('watermark'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(app.instance_path, 'temp', 'temp.jpg')
            print(temp_file_path)
            embed_watermark(IMAGE_PATH, watermark_string, temp_file_path)
            print(form.watermark.data)    
            return redirect(url_for('watermark'))
    return render_template('watermark.html', form=form)

@app.route('/watermark1', methods=['GET', 'POST'])
@login_required
def watermark1():
    global AUDIO_PATH
    form = WatermarkForm()
    if form.validate_on_submit():
        if len(AUDIO_PATH)==0:
            return redirect(url_for('watermark1'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(app.instance_path, 'temp', 'temp.wav')
            print(temp_file_path)
            lsb_watermark(AUDIO_PATH, watermark_string, temp_file_path)
            print(form.watermark.data)
            return redirect(url_for('watermark1'))
        return redirect(url_for('watermark1'))

    return render_template('watermark1.html', form=form)

@app.route('/watermark2', methods=['GET', 'POST'])
@login_required
def watermark2():
    global VIDEO_PATH
    form = WatermarkForm()
    if form.validate_on_submit():
        if len(VIDEO_PATH)==0:
            return redirect(url_for('watermark2'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(app.instance_path, 'temp', 'temp.mxf')
            print(temp_file_path)
            
            print(form.watermark.data)
            embed_video(AUDIO_PATH, watermark_string, temp_file_path)
            return redirect(url_for('watermark2'))
        return redirect(url_for('watermark2'))
    return render_template('watermark2.html', form=form)

@app.route('/getjpg', methods=['GET', 'POST'])
@login_required
def getjpg():
    dirpath = os.path.join(app.root_path, 'instance\\temp')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    print(dirpath)
    return send_from_directory(dirpath, 'temp.jpg', as_attachment=True)# as_attachment=True 一定要写，不然会变成打开，而不是下载

@app.route('/getaudio', methods=['GET', 'POST'])
@login_required
def getaudio():
    dirpath = os.path.join(app.root_path, 'instance\\temp')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    print(dirpath)
    return send_from_directory(dirpath, 'temp.wav', as_attachment=True)# as_attachment=True 一定要写，不然会变成打开，而不是下载

@app.route('/getvideo', methods=['GET', 'POST'])
@login_required
def getvideo():
    dirpath = os.path.join(app.root_path, 'instance\\temp')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    print(dirpath)
    return send_from_directory(dirpath, 'temp.ts', as_attachment=True)# as_attachment=True 一定要写，不然会变成打开，而不是下载


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, flash, redirect, render_template, url_for, request
import config
from forms.videoUrl import VideoForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'youwillneverguess'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideoForm()

    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect(url_for('exercise'))

    return render_template('index.html', form=form)

@app.route('/exercise')
def exercise():
    return 'HOLA'

if __name__ == '__main__':
    app.run()

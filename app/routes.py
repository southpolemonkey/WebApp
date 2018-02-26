from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'rong'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'I am hungary!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html', title='Hello', user=user, posts=posts)
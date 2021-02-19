from flask import Flask, jsonify, request, url_for, redirect, session, render_template
app = Flask(__name__)

app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'This is a secret!'


@app.route('/')
def hello_world():
    session.pop('name', None)
    return '<h1>Hello World!</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'User'})
@app.route('/home/<name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    mylist = ['one', 'two', 'three', 'four']
    listdict = [
        {'name': 'Zach'},
        {'name': 'Jeoms'},
        {'name': 'XXXL'}]
    name = name.capitalize()
    return render_template('home.html', name=name, display=True, mylist=mylist, listdict=listdict)


@app.route('/json', methods=['POST', 'GET'])
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Not in session!'
    return jsonify({
        'Key': 'value',
        'Key1': [1, 2, 3, 4, 5],
        'name': name
    })


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hi {name}, you are from {location}.<br>You are on the query page</h1>'


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']
        # return f"Hello {name}, you are from {location} you have submitted the form successfully!"
        return render_template('base.html', name=name, location=location)

#
# @app.route('/process', methods=['POST'])
# def process():


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify(
        {'Results': 'Success!',
         'name': name,
         'location': location,
         'randomkeyinlist': randomlist[0:2]}
    )


if __name__ == '__main__':
    app.run()

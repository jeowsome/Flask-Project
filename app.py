from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'User'})
@app.route('/home/<name>', methods=['POST', 'GET'])
def home(name):
    name = name.capitalize()
    return f'<h1>Hi! {name}, You are on the homepage</h1>'


@app.route('/json', methods=['POST', 'GET'])
def json():
    return jsonify({
        'Key': 'value',
        'Key1': [1, 2, 3, 4, 5]
    })


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hi {name}, you are from {location}.<br>You are on the query page</h1>'


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return '''<form method="POST" action="/form">
        <input type="text" name="name">
        <input type="text" name="location">
        <input type="submit" value="Submit">
        </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return f"Hello {name}, you are from {location} you have submitted the form successfully!"

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
    app.run(debug=True)

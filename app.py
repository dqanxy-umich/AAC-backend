from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Hello, World!'

@app.errorhandler(404)
def page_not_found(error):
    return '404 Not Found', 404

if __name__ == '__main__':
    app.run(debug=True)

    
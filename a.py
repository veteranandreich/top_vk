from flask import Flask,render_template
import random
import time
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('main.html'),200
@app.route('/f')
def hello_wor():
	perv1 = [i for i in range(1,12)]
	perv = [random.randint(1,500) for i in range(1,12)]
	return json.dumps({'a':perv1,'b':perv})


if __name__ == '__main__':
    app.run()

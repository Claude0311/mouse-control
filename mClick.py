from flask import Flask,request
import autopy
# from  import RIGHT
app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

@app.route('/ck',methods=['POST'])
def ck():
    value = request.values['sig']
    print(value)
    if value=='1':
        autopy.mouse.click()
    if value=='2':
        autopy.mouse.click(autopy.mouse.Button.RIGHT)
    if value == '3':
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    if value == '4':
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

    return 'ok'

import pyautogui
import time
@app.route('/sc',methods=['POST'])
def sc():
    value = request.values['speed']
    print(value)
    value = int(float(value)*100)
    print('scroll',value)
    # time.sleep(2)
    pyautogui.scroll(value)

    return 'ok'


app.run(debug=True,port=5000,host="0.0.0.0")
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
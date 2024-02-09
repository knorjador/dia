from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    print('here')
    print('here')
    print('here')
    print('here')
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)
    return render_template("bienvenue.html" , message = processed_text )

if __name__ == '__main__':
    app.run()
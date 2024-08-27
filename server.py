from flask import Flask, render_template
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

kandidater = json.load(open("kandidater.json", "r"))
print(kandidater)

@app.route("/")
def index():
    return render_template('index.html', kandidater=kandidater)


if __name__ == '__main__':
    app.run()

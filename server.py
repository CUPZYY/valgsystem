from flask import Flask, render_template, request
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

kandidater = json.load(open("kandidater.json", "r"))
print(kandidater)

def submit_vote(klasse, candidate):
    with open('stemmer.json', 'r+', encoding='utf-8') as f:
        stemmer = json.load(f)
        stemmer[klasse][str(candidate)] =+ 1
        f.seek(0)
        f.truncate()
        json.dump(stemmer, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/kandidater")
def show_candidates():
    klasse = request.args.get('klasse')
    if klasse in kandidater:
        return render_template('kandidater.html', kandidater=kandidater[klasse].values(), klasse=klasse)
    else:
        return render_template('kandidater.html', kandidater=[], klasse=klasse)

@app.route("/api/vote/")
def vote():
    with open('id.json', 'r', encoding='utf-8') as f:
        ids = json.load(f)
    args = dict(request.args)
    id = args.get("id")
    candidate = args.get("candidate")
    klasse = None
    for klassenavn in ids:
        if id in ids[klassenavn]:
            klasse = klassenavn
            ids[klasse].remove(id)
    if not klasse:
        return "error"
    
    if candidate:
        submit_vote(klasse, candidate)
    
    with open('id.json', 'w', encoding='utf-8') as f:
        json.dump(ids, f, ensure_ascii=False, indent=4)

    return "jess"

if __name__ == '__main__':
    app.run()

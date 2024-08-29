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

def find_klasse(id, remove=False):
    with open('id.json', 'r+', encoding='utf-8') as f:
        ids = json.load(f)
        klasse = None
        for klassenavn in ids:
            if id in ids[klassenavn]:
                klasse = klassenavn
                if remove:
                    ids[klasse].remove(id)
                    json.dump(ids, f, ensure_ascii=False, indent=4)
    return klasse

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vote")
def show_candidates():
    id = request.args.get("id")
    klasse = find_klasse(id)
    if not klasse:
        return render_template('invalid.html')
    else:
        return render_template('kandidater.html', kandidater=[], klasse=klasse)

@app.route("/api/vote/")
def vote():
    args = dict(request.args)
    id = args.get("id")
    candidate = args.get("candidate")
    klasse = find_klasse(id, remove=True)
    if not klasse:
        return "error"
    
    if candidate:
        submit_vote(klasse, candidate)

    return "jess"

if __name__ == '__main__':
    app.run()

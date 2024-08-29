from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

with open("kandidater.json", "r") as f:
    kandidater = json.load(f)

def submit_vote(klasse, candidate):
    with open('stemmer.json', 'r+', encoding='utf-8') as f:
        stemmer = json.load(f)
        stemmer[klasse][str(candidate)] += 1
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
                    f.seek(0)
                    f.truncate()
                    json.dump(ids, f, ensure_ascii=False, indent=4)
    return klasse

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vote/success")
def vote_success():
    return render_template('responses/vote_success.html')

@app.route("/vote")
def show_candidates():
    id = request.args.get("id")
    klasse = find_klasse(id)
    if not klasse:
        return render_template('responses/id_invalid.html')
    else:
        return render_template('vote.html', kandidater=kandidater[klasse], klasse=klasse, id=id)

@app.route("/api/vote/", methods=["POST"])
def vote():
    args = request.json
    id = args.get("id")
    candidate = args.get("candidate")
    klasse = find_klasse(id, remove=True)
    if not klasse:
        return Response("{}", status=400)
    
    if candidate:
        submit_vote(klasse, candidate)

    return Response("{}", status=200)

if __name__ == '__main__':
    app.run()

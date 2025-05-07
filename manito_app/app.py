from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name'].strip()
        data = load_data()
        if name not in data['participants']:
            return render_template('index.html', error="유효하지 않은 아이디 입니다.")
        return redirect(f'/select/{name}')
    return render_template('index.html')

@app.route('/select/<name>', methods=['GET'])
def select(name):
    data = load_data()

    if name in data.get('assignments', {}):
        return render_template('result.html', name=name, manito=data['assignments'][name]['manito'], mission=data['assignments'][name]['mission'])

    assigned_manitos = [v['manito'] for v in data['assignments'].values()]
    assigned_missions = [v['mission'] for v in data['assignments'].values()]

    available_manitos = [(i+1, m) for i, m in enumerate(data['manitos']) if m != name and m not in assigned_manitos]
    available_missions = [(i+1, m) for i, m in enumerate(data['missions']) if m not in assigned_missions]

    return render_template('select.html', name=name, manitos=available_manitos, missions=available_missions)

@app.route('/submit/<name>', methods=['POST'])
def submit(name):
    data = load_data()
    manito_index = int(request.form['manito']) - 1
    mission_index = int(request.form['mission']) - 1

    selected_manito = data['manitos'][manito_index]
    selected_mission = data['missions'][mission_index]

    data['assignments'][name] = {
        'manito': selected_manito,
        'mission': selected_mission
    }
    save_data(data)

    return redirect(f'/select/{name}')

if __name__ == '__main__':
    app.run(debug=True)

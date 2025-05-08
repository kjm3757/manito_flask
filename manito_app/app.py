from flask import Flask, render_template, request, redirect, url_for, send_file
import json, os, random

app = Flask(__name__)
ADMIN_PASSWORD = "36936912"
DATA_FILE = 'data.json'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        user_id = request.form['id'].strip()
        if user_id not in data['participants']:
            return render_template('index.html', error="유효하지 않은 ID 입니다.")
        return redirect(f'/select/{user_id}')

    participant_count = len(data['assignments'])  # ← 할당된 사람 수
    return render_template('index.html', count=participant_count)

@app.route('/select/<user_id>', methods=['GET'])
def select(user_id):
    data = load_data()

    real_name = data['participants'].get(user_id, "Unknown")

    if user_id in data.get('assignments', {}):
        return render_template('result.html', real_name=real_name,
                                manito=data['assignments'][user_id]['manito'],
                                mission=data['assignments'][user_id]['mission'])

    assigned_manitos = [v['manito'] for v in data['assignments'].values()]
    assigned_missions = [v['mission'] for v in data['assignments'].values()]

    available_manitos = [(i+1, m) for i, m in enumerate(data['manitos']) if m != user_id and m not in assigned_manitos]
    available_missions = [(i+1, m) for i, m in enumerate(data['missions']) if m not in assigned_missions]

    return render_template('select.html',
                            real_name=real_name,
                            user_id=user_id,
                            manitos=available_manitos,
                            missions=available_missions)

@app.route('/submit/<user_id>', methods=['POST'])
def submit(user_id):
    data = load_data()
    manito_index = int(request.form['manito']) - 1
    mission_index = int(request.form['mission']) - 1

    selected_manito = data['manitos'][manito_index]
    selected_mission = data['missions'][mission_index]

    assigned_manitos = [v['manito'] for v in data['assignments'].values()]
    assigned_missions = [v['mission'] for v in data['assignments'].values()]

    if selected_manito in assigned_manitos and selected_mission in assigned_missions:
        return "다른 사용자가 이미 선택한 마니또/미션입니다. 마니또와 미션을 다시 선택해주세요.", 409

    if selected_manito in assigned_manitos:
        return "다른 사용자가 이미 선택한 마니또입니다. 마니또를 다시 선택해주세요.", 409

    if selected_mission in assigned_missions:
        return "다른 사용자가 이미 선택한 미션입니다. 미션을 다시 선택해주세요.", 409

    data['assignments'][user_id] = {
        'manito': selected_manito,
        'mission': selected_mission
    }
    save_data(data)

    return redirect(f'/select/{user_id}')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        return redirect(url_for('admin'))
    else:
        return "비밀번호가 틀렸습니다.", 403

@app.route('/admin')
def admin():
    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/reset', methods=['POST'])
def reset():
    manitos = [
        "강주헌",
        "권제경",
        "김지경",
        "김태희",
        "문형찬",
        "양동선",
        "이우정",
        "임민호",
        "조영주",
        "한수정",
        "권연우",
        "김소영",
        "김정민",
        "박하영",
        "오지원",
        "오하민",
        "이건희",
        "이지연",
        "최승현",
        "홍재우"   
    ]
    missions = [
        "마니또랑 눈싸움해서 이기기",
        "마니또한테 “이러니 널 좋아할 수박에” 드립치기",
        "마니또에게 종이학 접어주기",
        "마니또 얼굴 그려주기",
        "마니또에게 전화번호 물어보기 (이미 있어도 직접 물어보고 받아와야 함.)",
        "마니또랑 같이 셀카 찍기",
        "마니또에게 짧은 편지 써서 전달하기(전달은 직접 안해도 됨)",
        "마니또가 가장 좋아하는 색 알아내기",
        "마니또가 가고 싶어하는 출사지 2곳 알아내기",
        "마니또에게 물 or 수박 갖다주기",
        "마니또에게 행운부적 그려주기",
        "레크레이션 진행시, 마니또 관련 문제 맞추기",
        "마니또의 사진을 찍어주고, 마니또가 본인 인스타 스토리에 해당 사진 올리기",
        "마니또 폰으로 브이하고 셀카 찍기",
        "마니또 옆에서 단사 찍기",
        "마니또에게 예쁜 돌 선물해주기",
        "마니또에게 “너와 추억을 쌓게 되어서 너무 기뻐.”라고 말해주기(영상 기록물 필수)",
        "마니또랑 릴스 찍기 (영상 기록물 필수)",
        "마니또에게 아재개그 하기(웃으면 성공)",
        "마니또와 가위바위보 내기 걸어서 진 사람 웃긴 사진 찍기"
    ]

    random.shuffle(manitos)
    random.shuffle(missions)

    empty_data = {
        "participants": {
            "dks231" : "강주헌",
            "big023" : "권제경",
            "vih074" : "김지경",
            "pys394" : "김태희",
            "eaw263" : "문형찬",
            "ohs045" : "양동선",
            "cbf495" : "이우정",
            "fiw410" : "임민호",
            "bod795" : "조영주",
            "clg028" : "한수정",
            "sof156" : "권연우",
            "fjo782" : "김소영",
            "bsg495" : "김정민",
            "xoh164" : "박하영",
            "gho127" : "오지원",
            "oeh462" : "오하민",
            "qow906" : "이건희",
            "xvm046" : "이지연",
            "spj279" : "최승현",
            "sby798" : "홍재우"
        },
        "manitos": manitos ,
        "missions": missions,
        "assignments": {}
    }
    save_data(empty_data)
    return redirect(url_for('admin'))

@app.route('/download_data')
def download_data():
    return send_file(
        'data.json',
        mimetype='application/json',
        as_attachment=True,
        download_name='data.json'
    )

if __name__ == '__main__':
    app.run(debug=True)

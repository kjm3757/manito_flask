from flask import Flask, render_template, request, redirect, url_for, session
from database import (
    check_participant_id, 
    get_participant_name_by_id, 
    has_result,
    get_result_by_id,
    get_available_manitos,
    get_available_missions,
    store_result,
    get_result_by_name,
    get_all_results,
    clear_results_with_password
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

ADMIN_PASSWORD = 'admin123'

@app.route('/')
def index():
    return render_template('index.html', error=None, admin_error=None)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    if not check_participant_id(user_id):
        return render_template('index.html', error='유효하지 않은 ID입니다.', admin_error=None)
    session['user_id'] = user_id
    if has_result(user_id):
        return redirect(url_for('result'))
    else:
        return redirect(url_for('select'))

@app.route('/admin_login', methods=['POST'])
def admin_login():
    password = request.form.get('admin_password')
    if password == ADMIN_PASSWORD:
        return redirect(url_for('admin'))
    else:
        return render_template('index.html', error=None, admin_error='비밀번호가 틀렸습니다.')

@app.route('/select')
def select():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    name = get_participant_name_by_id(user_id)
    available_manitos = get_available_manitos(exclude_id=user_id)
    available_missions = get_available_missions()
    return render_template('select.html', name=name, manitos=available_manitos, missions=available_missions)

@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    selected_manito = request.form.get('manito')
    selected_mission = request.form.get('mission')
    success = store_result(user_id, selected_manito, selected_mission)
    if success:
        return redirect(url_for('result'))
    else:
        return "이미 선택된 마니또 또는 미션입니다. 다시 시도해주세요."

@app.route('/result')
def result():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    name, manito, mission = get_result_by_id(user_id)
    return render_template('result.html', name=name, manito=manito, mission=mission)

@app.route('/admin')
def admin():
    results = get_all_results()
    return render_template('admin.html', results=results, count=len(results), message=None)

@app.route('/clear_results', methods=['POST'])
def clear_results():
    password = request.form.get('admin_password')
    if password != ADMIN_PASSWORD:
        results = get_all_results()
        return render_template('admin.html', results=results, count=len(results), message='비밀번호가 틀렸습니다.')
    clear_results_with_password()
    results = get_all_results()
    return render_template('admin.html', results=results, count=0, message='결과가 초기화되었습니다.')

if __name__ == '__main__':
    app.run(debug=True)
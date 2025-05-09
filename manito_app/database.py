import firebase_admin
from firebase_admin import credentials, db
import random

# Firebase credentials JSON 파일 경로
cred = credentials.Certificate("./authentication/firebase_auth.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://manito-58ef9-default-rtdb.firebaseio.com/'
})


participants_ref = db.reference('participants')
manitos_ref = db.reference('manitos')
missions_ref = db.reference('missions')
results_ref = db.reference('results')

def check_participant_id(user_id):
    return user_id in participants_ref.get() or {}

def get_participant_name_by_id(user_id):
    participants = participants_ref.get() or {}
    return participants.get(user_id)

def has_result(user_id):
    results = results_ref.get() or {}
    return user_id in results

def get_result_by_id(user_id):
    name = get_participant_name_by_id(user_id)
    result = results_ref.child(user_id).get()
    return name, result['manito'], result['mission']

def get_result_by_name(name):
    results = results_ref.get() or {}
    for r in results.values():
        if r['manito'] == name or r['mission'] == name:
            return True
    return False

def get_available_manitos(exclude_id):
    participants = participants_ref.get() or {}
    results = results_ref.get() or {}
    exclude_name = participants.get(exclude_id)
    assigned_manitos = {r['manito'] for r in results.values()}
    candidates = [name for uid, name in participants.items() if name != exclude_name and name not in assigned_manitos]
    random.shuffle(candidates)
    return candidates

def get_available_missions():
    missions = missions_ref.get() or {}
    results = results_ref.get() or {}
    used_missions = {r['mission'] for r in results.values()}
    candidates = [m for m in missions.values() if m not in used_missions]
    random.shuffle(candidates)
    return candidates

def store_result(user_id, manito, mission):
    # Check again for conflicts
    results = results_ref.get() or {}
    for r in results.values():
        if r['manito'] == manito or r['mission'] == mission:
            return False
    results_ref.child(user_id).set({
        'manito': manito,
        'mission': mission
    })
    return True

def get_all_results():
    results = results_ref.get() or {}
    participants = participants_ref.get() or {}
    return [{
        'name': participants.get(uid),
        'manito': res['manito'],
        'mission': res['mission']
    } for uid, res in results.items()]

def clear_results_with_password():
    results_ref.delete()
import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 키와 데이터베이스 URL 설정
cred = credentials.Certificate("./authentication/firebase_auth.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://manito-58ef9-default-rtdb.firebaseio.com/'
})

# === 초기 데이터 ===

participants = {
    "dks231": "강주헌",
    "big023": "권제경",
    "vih074": "김지경",
    "pys394": "김태희",
    "eaw263": "문형찬",
    "ohs045": "양동선",
    "cbf495": "이우정",
    "fiw410": "임민호",
    "bod795": "조영주",
    "clg028": "한수정",
    "sof156": "권연우",
    "fjo782": "김소영",
    "bsg495": "김정민",
    "xoh164": "박하영",
    "gho127": "오지원",
    "oeh462": "오하민",
    "qow906": "이건희",
    "xvm046": "이지연",
    "spj279": "최승현",
    "sby798": "홍재우"
}

# manitos는 ID와 이름이 동일 (참가자들이 서로 마니또가 됨)
manitos = participants.copy()

missions = {
    "m1": "마니또랑 눈싸움해서 이기기",
    "m2": "마니또한테 “이러니 널 좋아할 수박에” 드립치기",
    "m3": "마니또에게 종이학 접어서 전달하기(직접 전달 안해도 됨)",
    "m4": "마니또 얼굴 그려주기",
    "m5": "마니또에게 전화번호 물어보기 (이미 있어도 직접 물어보고 받아와야 함.)",
    "m6": "마니또랑 같이 셀카 찍기",
    "m7": "마니또에게 짧은 편지 써서 전달하기(직접 전달 안해도 됨)",
    "m8": "마니또가 가장 좋아하는 색 알아내기",
    "m9": "마니또가 가고 싶어하는 출사지 2곳 알아내기",
    "m10": "마니또에게 물 or 수박 갖다주기",
    "m11": "마니또에게 행운 부적 그려주기",
    "m12": "레크레이션 진행 시, 마니또 관련 문제 맞추기",
    "m13": "마니또의 사진을 찍어주고, 마니또가 본인 인스타 스토리에 해당 사진 올리기",
    "m14": "마니또 폰으로 브이하고 셀카 찍기",
    "m15": "마니또 옆에서 단사 찍기",
    "m16": "마니또에게 예쁜 돌 선물해주기",
    "m17": "마니또에게 “너와 추억을 쌓게 되어서 너무 기뻐”라고 말해주기(영상 기록물 필수)",
    "m18": "마니또랑 릴스 찍기(영상 기록물 필수)",
    "m19": "마니또에게 아재개그 하기(마니또가 웃으면 성공)",
    "m20": "마니또와 가위바위보 내기 걸어서 진 사람 웃긴 사진 찍기"
}

# === 데이터 업로드 ===
def upload_data():
    db.reference("participants").set(participants)
    db.reference("manitos").set(manitos)
    db.reference("missions").set(missions)
    db.reference("result").delete()  # 초기화

    print("✅ Firebase에 초기 데이터 업로드 완료!")

if __name__ == '__main__':
    upload_data()

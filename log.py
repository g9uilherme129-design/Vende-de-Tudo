import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'app.log')

def write_log(action: str, user_id: str = None, details: str = ""):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    uid = user_id if user_id is not None else "-"
    line = f"[{ts}] user:{uid} action:{action} details:{details}\n"
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception as e:
        print(f"Erro ao gravar log: {e}")

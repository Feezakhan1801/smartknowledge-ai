from database import get_db

def save_chat(username, user_msg, bot_msg):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chats (username, user_message, bot_message) VALUES (?, ?, ?)",
        (username, user_msg, bot_msg)
    )

    conn.commit()
    conn.close()

def load_chat(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_message, bot_message FROM chats WHERE username=?",
        (username,)
    )

    chats = cur.fetchall()
    conn.close()
    return chats

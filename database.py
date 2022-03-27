import sqlite3


def size_of_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM QUESTION")
    return (len(cursor.fetchall()))

def access_data(_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    query = "SELECT * FROM QUESTION WHERE ID=?"
    result = cursor.execute(query, (_id,))
    row = result.fetchone()
    return row

#print(access_data(600))

def filldata():
    loc = r"C:/datasets/mathematics_dataset-v1.0.tar/mathematics_dataset-v1.0/train-easy/"

    q_s = list()
    with open(loc + "algebra__linear_1d.txt", "r") as f:
        data = f.read().split('\n')
        print(data[0])
        for x in range(0,len(data)-2,2):
            q_s.append((data[x], data[x+1], x//2))
            pass#print(data[x],data[x+1])
    print(q_s[0:5])

    conn = sqlite3.connect('test.db')
    
    conn.execute("""CREATE TABLE IF NOT EXISTS QUESTION (
                    ID INT PRIMARY KEY    NOT NULL,
                    QUESTION_TEXT TEXT    NOT NULL,
                    QUESTION_ANSW TEXT    NUT NULL
                    );""")

    for x in q_s:
        #print(x[2], x[0], x[1])
        conn.execute("INSERT INTO QUESTION (ID,QUESTION_TEXT,QUESTION_ANSW)\
                  VALUES (?, ?, ?)", (int(x[2]), x[0], x[1]))
    print("DONE")
    conn.commit()
    cursor = conn.execute("SELECT id, question_text, question_answ from QUESTION")
        
#filldata()

#filldata()


def delete_db():    
    conn = sqlite3.connect('test.db')

    sql = 'DELETE FROM QUESTION'
    cur = conn.cursor()
    conn.execute(sql)
    conn.commit()
#delete_db()

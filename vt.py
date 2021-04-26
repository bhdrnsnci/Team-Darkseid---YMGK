import sqlite3

with sqlite3.connect("FaceDatabase.db") as usersdb:
    cursor = usersdb.cursor()

    # çalışan:
    #     id
    #     name
    #     username
    #     email
    #     phone
    #     department
    #     password
    #     cameras
    cursor.execute("create table staff(id integer primary key autoincrement, name text, username text, password text, email text, phone text, department text, cameras text)")

    # ziyaretçi
    #     id
    #     tc
    #     name
    #     address
    #     phone
    #     department
    #     staff
    cursor.execute("create table guests(id integer primary key autoincrement, tc text, name text, address text, phone text, department text, staff text)")

    # birim
    #     id
    #     name
    cursor.execute("create table departments(id integer , name text)")

    # kameralar
    #     id
    #     name
    #     ip
    #     protocol
    #     department
    cursor.execute("create table cameras(id integer primary key autoincrement, name text, ip text, protocol text, department text)")

    cursor.execute("create table face(id integer primary key autoincrement, name text)")

    # admin
    #     id
    #     name
    #     username
    #     password
    cursor.execute("create table admin(id integer primary key autoincrement, name text, username text, password text)")
    cursor.execute("insert into admin(username, password) values(?, ?)", ("admin", "admin"))
    # cursor.execute("insert into departments(name) values(?)", ("Yazılım Mühendisliği",))
    usersdb.commit()

print("Veri tabanı oluşturuldu.")
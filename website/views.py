from django.shortcuts import render, redirect
import sqlite3

from django.db import connection
db_name = connection.settings_dict['NAME']

def index(request):
    if not request.session.get("username"):
        return redirect("/login")

    conn = get_connection()
    stmt = "SELECT title, body, image_url, name, created_on FROM Posts JOIN Users ON Posts.creator = Users.id ;"
    cursor = conn.cursor()
    response = cursor.execute(stmt)
    posts = map(lambda x: {"title": x[0], "body": x[1], "image_url": x[2], "poster": x[3], "creation": x[4]}, response.fetchall())
    print(posts)
    return render(request, 'index.html', {"posts": posts})

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')


    conn = get_connection()
    username = request.POST.get('username')
    password = request.POST.get('password')

    stmt = f"SELECT * FROM Users WHERE name = '{username}';"
    cursor = conn.cursor()
    response = cursor.execute(stmt)
    
    users = response.fetchall()
    print(users)
    if len(users) != 1 or users[0][2] != password:
        return render(request, 'login.html', {"error_msg": "username or password is incorrect"})

    request.session["username"] = username
    return redirect("/")


def post(request):
    if request.method == "GET":
        return render(request, 'post.html')

    title = request.POST.get('title')
    body = request.POST.get('body')
    url = request.POST.get('url')

    stmt = f"INSERT INTO Posts (title, body, image_url, creator) VALUES ('{title}', '{body}', '{url}', (SELECT id FROM Users WHERE name = '{request.session['username']}'));"
    
    print(stmt)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(stmt)
    conn.commit()

    return redirect('/')

def logout(request):
    if request.session.get("username"):
        del request.session["username"]
    return redirect('/')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        create_user(username, password)
        return redirect('/')

    return render(request, 'signup.html')

def create_user(username: str, password: str):
    print(username, password)

def get_connection():
    return sqlite3.connect(db_name)

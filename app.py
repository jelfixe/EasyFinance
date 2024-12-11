import os
import sqlite3
import random
import string
import logging
import subprocess
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from colorama import Fore, init

secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))

init(autoreset=True)
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.secret_key = secret_key

logo = '[Easy' + Fore.CYAN + 'Finance' + Fore.RESET + ']'

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

def get_db_connection():
    db_path = os.path.join(app.instance_path, 'utilizadores.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.close()

def is_ollama_installed():
    try:
        result = subprocess.run(['ollama', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False

def run_ollama_3_2(user_input):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', user_input], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            print(f'{logo} Ollama 3.2 executado com sucesso')
            return result.stdout.decode('utf-8')
        else:
            print(f'{logo} Erro ao executar Ollama 3.2: {result.stderr.decode("utf-8")}')
            return None
    except Exception as e:
        print(f'{logo} Erro ao tentar executar o Ollama: {e}')
        return None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return redirect('/dashboard')
    else:
        flash('Inválido', 'error')
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                         (username, hashed_password))
            conn.commit()
            conn.close()
            
            flash('Registado com sucesso', 'success')
            return redirect('/')
        except sqlite3.IntegrityError:
            flash('Utilizador já existe', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()

    return render_template('dashboard.html', username=user['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/investimentos')
def investimentos_page():
    return render_template('investimentos.html')

@app.route('/gastos')
def gastos_page():
    return render_template('gastos.html')

@app.route('/poupancas')
def poupancas_page():
    return render_template('poupancas.html')

@app.route('/configuracoes')
def configuracoes_page():
    return render_template('configuracoes.html')

@app.route('/ai', methods=['GET', 'POST'])
def ai_page():
    response = None

    if request.method == 'POST':
        user_input = request.form['text']
        
        if user_input.strip() == "":
            response = "Por favor, insira algum texto para análise."
        else:
            if is_ollama_installed():
                ollama_response = run_ollama_3_2(user_input)
                if ollama_response:
                    response = ollama_response
                else:
                    response = "Erro ao executar o modelo Ollama 3.2."
            else:
                response = "Ollama não está instalado."

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return response

    return render_template('ai.html', response=response)

@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form['text']
    if is_ollama_installed():
        ollama_response = run_ollama_3_2(user_input)
        if ollama_response:
            return ollama_response 
        else:
            return "Erro ao executar o modelo Ollama 3.2", 500
    else:
        return "Ollama não está instalado", 500

if __name__ == '__main__':
    init_db()
    app.run(debug=False)

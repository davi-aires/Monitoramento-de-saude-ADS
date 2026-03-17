from flask import Flask, render_template, request, jsonify
import sqlite3
from db_manager import init_db, DATABASE

app = Flask(__name__)

# Configuração do banco de dados online

def get_db_connection():
    """Cria uma conexão com o banco de dados (PostgreSQL ou SQLite)"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário"""
    return render_template('form.html')

@app.route('/salvar', methods=['POST'])
def salvar_dados():
    """Recebe os dados do formulário e salva no banco de dados"""
    try:
        dados = request.get_json()

        nome = dados.get('nome')
        consumo_agua = dados.get('consumo_agua')
        minutos_sol = dados.get('minutos_sol')
        pratica_exercicio = dados.get('pratica_exercicio')
        humor = dados.get('humor')

        # Validação básica
        if not all([nome, consumo_agua, minutos_sol, pratica_exercicio, humor]):
            return jsonify({'sucesso': False, 'mensagem': 'Todos os campos são obrigatórios!'}), 400

        # Salvar no banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO saude (nome, consumo_agua, minutos_sol, pratica_exercicio, humor)
            VALUES (?, ?, ?, ?, ?)
        ''', (str(nome), int(consumo_agua), int(minutos_sol), pratica_exercicio, humor))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'sucesso': True, 'mensagem': 'Dados salvos com sucesso!'}), 201

    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro ao salvar: {str(e)}'}), 500

@app.route('/historico')
def historico():
    """Renderiza a página de histórico de dados registrados, com filtro por nome"""
    try:
        nome_filtro = request.args.get('nome', '').strip()
        conn = get_db_connection()
        cursor = conn.cursor()
        if nome_filtro:
            cursor.execute('SELECT * FROM saude WHERE nome LIKE ? ORDER BY data_registro DESC', (f'%{nome_filtro}%',))
        else:
            cursor.execute('SELECT * FROM saude ORDER BY data_registro DESC')

        registros = cursor.fetchall()
        cursor.close()
        conn.close()

        dados = []
        for registro in registros:
            dados.append({
                'id': registro['id'],
                'data': registro['data_registro'],
                'nome': registro['nome'],
                'consumo_agua': registro['consumo_agua'],
                'minutos_sol': registro['minutos_sol'],
                'pratica_exercicio': registro['pratica_exercicio'],
                'humor': registro['humor']
            })

        return render_template('historico.html', registros=dados)

    except Exception as e:
        return render_template('historico.html', registros=[], erro=f'Erro ao buscar histórico: {str(e)}')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)


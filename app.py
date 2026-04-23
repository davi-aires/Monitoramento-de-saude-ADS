from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv
from db_manager import init_db, DATABASE, DATABASE_URL, agora_br, ph, get_cursor

load_dotenv()

app = Flask(__name__)
init_db()

# Configuração do banco de dados online

def get_db_connection():
    """Cria conexão com SQLite local ou PostgreSQL (Render)"""
    if DATABASE_URL:
        import psycopg2
        conn = psycopg2.connect(DATABASE_URL)
        return conn
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
        cursor = get_cursor(conn)

        cursor.execute(f'''
            INSERT INTO saude (data_registro, nome, consumo_agua, minutos_sol, pratica_exercicio, humor)
            VALUES ({ph()}, {ph()}, {ph()}, {ph()}, {ph()}, {ph()})
        ''', (agora_br(), str(nome), int(consumo_agua), int(minutos_sol), pratica_exercicio, humor))

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
        cursor = get_cursor(conn)
        if nome_filtro:
            cursor.execute(f'SELECT * FROM saude WHERE nome LIKE {ph()} ORDER BY data_registro DESC', (f'%{nome_filtro}%',))
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


@app.route('/resultados')
def resultados():
    """Renderiza a página de resultados de saúde de uma pessoa com resumo IA"""
    nome = request.args.get('nome', '').strip()
    if not nome:
        return redirect(url_for('historico'))

    try:
        conn = get_db_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            f'SELECT * FROM saude WHERE nome LIKE {ph()} ORDER BY data_registro DESC',
            (f'%{nome}%',)
        )
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

        return render_template('resultados.html', registros=dados, nome=nome)

    except Exception as e:
        return render_template('resultados.html', registros=[], nome=nome,
                               erro=f'Erro ao buscar dados: {str(e)}')


@app.route('/gerar-resumo', methods=['POST'])
def gerar_resumo():
    """Chama a API do Grok (xAI) para gerar um resumo de saúde personalizado"""
    try:
        dados = request.get_json()
        nome = dados.get('nome', '').strip()
        registros = dados.get('registros', [])

        if not nome or not registros:
            return jsonify({'sucesso': False, 'mensagem': 'Dados insuficientes para gerar resumo.'}), 400

        GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        if not GROQ_API_KEY:
            return jsonify({'sucesso': False, 'mensagem': 'Chave da API Groq não configurada no .env (GROQ_API_KEY).'}), 500

        # Montar texto dos registros para o prompt
        linhas = []
        for r in registros:
            exercicio = r.get('pratica_exercicio', '-')
            linhas.append(
                f"- Data: {r.get('data', '-')} | Água: {r.get('consumo_agua', '-')} L | "
                f"Sol: {r.get('minutos_sol', '-')} min | Exercício: {exercicio} | Humor: {r.get('humor', '-')}"
            )
        registros_texto = "\n".join(linhas)

        SYSTEM_PROMPT = (
            "Você é um amigo próximo que entende de saúde. Fala com calor humano, humor leve e honestidade. "
            "Quando lê os dados de alguém, reage como uma pessoa real, não como um relatório.\n\n"
            "Como escrever:\n"
            "- Varie o ritmo: misture frases curtas com outras mais longas. Não escreva tudo no mesmo compasso.\n"
            "- Reaja aos dados. Se o humor foi ótimo, comente isso. Se o sol foi 3 minutos, ria um pouco disso.\n"
            "- Use o nome da pessoa como quem realmente está falando com ela, não como etiqueta num formulário.\n"
            "- Seja específico. '2 litros de água num dia de exercício é um começo sólido' é melhor que 'boa hidratação'.\n"
            "- Termine a dica com uma ação concreta, não uma frase de calendário motivacional.\n\n"
            "O que nunca fazer:\n"
            "- Não abra com 'Olá!' ou 'É um prazer'. Vá direto.\n"
            "- Não use: crucial, fundamental, destacar, ressaltar, alavancar, vibrant, enduring, showcase, testament.\n"
            "- Não escreva 'não é só X, é Y'. Não use travessão (—).\n"
            "- Não infle o óbvio. 'Você fez exercício' não precisa de cinco adjetivos.\n"
            "- Sem conclusão genérica. Termine com algo útil, não animador."
        )

        prompt = (
            f"Aqui estão os dados de saúde de {nome}:\n{registros_texto}\n\n"
            f"Escreva o resumo em português usando exatamente este formato markdown:\n\n"
            f"### Análise Geral\n"
            f"(até 300 caracteres, tom de conversa, mencione {nome}, reaja aos dados com personalidade)\n\n"
            f"### ✅ Pontos Positivos\n"
            f"(até 150 caracteres, seja específico sobre o que foi bom e por quê importa)\n\n"
            f"### ⚠️ Atenção\n"
            f"(até 150 caracteres, mencione {nome}, seja direto sem dramatizar)\n\n"
            f"### 💡 Dica Principal\n"
            f"(até 150 caracteres, uma ação concreta com número ou detalhe prático, não genérico)"
        )

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.75,
        )

        resumo = response.choices[0].message.content
        return jsonify({'sucesso': True, 'resumo': resumo})

    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro ao gerar resumo: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
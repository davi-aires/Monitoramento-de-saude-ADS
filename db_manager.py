"""
Arquivo auxiliar para gerenciar o banco de dados
Use este arquivo para operações de manutenção
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

def init_db():
    """Inicializa o banco de dados"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saude (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                nome text NOT NULL,
                consumo_agua INTEGER NOT NULL,
                minutos_sol INTEGER NOT NULL,
                pratica_exercicio TEXT NOT NULL,
                humor TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("✅ Banco de dados criado com sucesso!")
    else:
        print("ℹ️  Banco de dados já existe!")

def ver_todos_registros():
    """Exibe todos os registros do banco"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM saude ORDER BY data_registro DESC')
    registros = cursor.fetchall()
    conn.close()

    if registros:
        print("\n📊 REGISTROS SALVOS:\n")
        print(f"{'ID':<4} {'Data':<20} {'Água':<8} {'Sol':<8} {'Exercício':<12} {'Humor':<10}")
        print("-" * 70)
        for registro in registros:
            print(f"{registro['id']:<4} {registro['nome']:<20} {registro['data_registro']:<20} {registro['consumo_agua']:<8} {registro['minutos_sol']:<8} {registro['pratica_exercicio']:<12} {registro['humor']:<10}")
        print(f"\nTotal de registros: {len(registros)}")
    else:
        print("⚠️  Nenhum registro encontrado!")

def limpar_banco():
    """Limpa todos os registros do banco (use com cuidado!)"""
    resposta = input("\n⚠️  Tem certeza que deseja APAGAR todos os registros? (S/N): ").upper()

    if resposta == 'S':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM saude')
        conn.commit()
        conn.close()
        print("✅ Todos os registros foram apagados!")
    else:
        print("❌ Operação cancelada!")

def resetar_banco():
    """Apaga o banco de dados completamente"""
    resposta = input("\n⚠️  Tem certeza que deseja RESETAR o banco de dados? (S/N): ").upper()

    if resposta == 'S':
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
            init_db()
            print("✅ Banco de dados resetado com sucesso!")
        else:
            print("ℹ️  Banco de dados não existe!")
    else:
        print("❌ Operação cancelada!")

def limpar_registro(id):
    """Limpa apenas um registro"""
    resposta = input(f"\n⚠️  Tem certeza que deseja APAGAR o registro de ID = {id}: ").upper()

    if resposta == 'S':
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM saude where id = ?', (id,))
        conn.commit()
        conn.close()
        print("✅ Todos os registros foram apagados!")
    else:
        print("❌ Operação cancelada!")

def menu():
    """Menu principal"""
    while True:
        print("\n" + "="*50)
        print("🏥 GERENCIADOR DE BANCO DE DADOS - SAÚDE")
        print("="*50)
        print("\n1. Ver todos os registros")
        print("2. Limpar apenas um registro")
        print("3. Limpar registros (manter banco)")
        print("4. Resetar banco de dados")
        print("5. Sair")

        opcao = input("\nEscolha uma opção (1-4): ")

        if opcao == '1':
            ver_todos_registros()
        if opcao == '2':
            id = input("\nDigite o ID do registro que deseja apagar: ")
            limpar_registro(id)
        elif opcao == '3':
            limpar_banco()
        elif opcao == '4':
            resetar_banco()
        elif opcao == '5':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    menu()


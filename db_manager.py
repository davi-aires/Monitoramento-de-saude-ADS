"""
Arquivo auxiliar para gerenciar o banco de dados
Use este arquivo para operações de manutenção
"""

import sqlite3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

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
        print("✅ Registro apagado com sucesso!")
    else:
        print("❌ Operação cancelada!")

def gerar_relatorio_excel(caminho_arquivo=None):
    """Gera um relatório Excel com todos os registros do banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM saude ORDER BY data_registro DESC')
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        print("⚠️  Nenhum registro encontrado para gerar relatório!")
        return None

    if caminho_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_arquivo = os.path.join(BASE_DIR, f"relatorio_saude_{timestamp}.xlsx")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monitoramento de Saúde"

    verde_escuro = "1F6B3B"
    cinza_claro  = "F2F2F2"

    header_font  = Font(name="Calibri", bold=True, color="FFFFFF", size=12)
    header_fill  = PatternFill(start_color=verde_escuro, end_color=verde_escuro, fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center")
    thin_border  = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"),  bottom=Side(style="thin")
    )

    # Título
    ws.merge_cells("A1:G1")
    ws["A1"].value     = "🏥 Relatório de Monitoramento de Saúde"
    ws["A1"].font      = Font(name="Calibri", bold=True, size=16, color=verde_escuro)
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:G2")
    ws["A2"].value     = f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    ws["A2"].font      = Font(name="Calibri", italic=True, size=10, color="666666")
    ws["A2"].alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 18
    ws.row_dimensions[3].height = 8

    # Cabeçalhos
    colunas = ["ID", "Data de Registro", "Nome", "Água (ml)", "Sol (min)", "Exercício", "Humor"]
    for col_idx, col_nome in enumerate(colunas, start=1):
        cell = ws.cell(row=4, column=col_idx, value=col_nome)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border
    ws.row_dimensions[4].height = 22

    # Dados
    for row_idx, registro in enumerate(registros, start=5):
        fill_color = cinza_claro if row_idx % 2 == 0 else "FFFFFF"
        row_fill   = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
        valores = [registro["id"], registro["data_registro"], registro["nome"],
                   registro["consumo_agua"], registro["minutos_sol"],
                   registro["pratica_exercicio"], registro["humor"]]
        for col_idx, valor in enumerate(valores, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=valor)
            cell.fill      = row_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border    = thin_border
            cell.font      = Font(name="Calibri", size=11)

    # Total
    total_row = len(registros) + 5
    ws.merge_cells(f"A{total_row}:B{total_row}")
    ws[f"A{total_row}"].value     = f"Total de registros: {len(registros)}"
    ws[f"A{total_row}"].font      = Font(name="Calibri", bold=True, size=11, color=verde_escuro)
    ws[f"A{total_row}"].alignment = Alignment(horizontal="left", vertical="center")

    # Largura das colunas
    for col_idx, largura in enumerate([6, 22, 20, 12, 12, 14, 12], start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = largura

    wb.save(caminho_arquivo)
    print(f"✅ Relatório Excel gerado: {caminho_arquivo}")
    return caminho_arquivo


def enviar_relatorio_email(destinatario, remetente, senha_app, arquivo_excel=None,
                           smtp_server="smtp.gmail.com", smtp_port=587):
    """Gera (se necessário) e envia o relatório Excel por e-mail."""
    if arquivo_excel is None:
        arquivo_excel = gerar_relatorio_excel()

    if arquivo_excel is None:
        print("❌ Não foi possível gerar o relatório. Envio cancelado.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"]    = f"Monitoramento de Saúde - Resumo <{remetente}>"
        msg["To"]      = destinatario
        msg["Subject"] = f"📊 Relatório de Monitoramento de Saúde - {datetime.now().strftime('%d/%m/%Y')}"

        corpo = (
            "Olá!\n\n"
            "Segue em anexo o relatório de monitoramento de saúde gerado automaticamente.\n\n"
            f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n"
            "Atenciosamente,\nSistema de Monitoramento de Saúde 🏥"
        )
        msg.attach(MIMEText(corpo, "plain", "utf-8"))

        with open(arquivo_excel, "rb") as f:
            parte = MIMEBase("application", "octet-stream")
            parte.set_payload(f.read())
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(arquivo_excel)}"')
        msg.attach(parte)

        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha_app)
            servidor.sendmail(remetente, destinatario, msg.as_string())

        print(f"✅ Relatório enviado com sucesso para {destinatario}!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Erro de autenticação: {e}")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Erro SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def configurar_e_enviar():
    """Envia o relatório por e-mail com credenciais pré-configuradas"""
    REMETENTE    = "daviaireslage@gmail.com"
    SENHA_APP    = "xlclnpbfosbuifib"
    DESTINATARIO = "daviaireslage@gmail.com"

    print("\n⏳ Gerando relatório e enviando e-mail...")
    enviar_relatorio_email(DESTINATARIO, REMETENTE, SENHA_APP)


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
        print("5. Gerar e enviar relatório por e-mail")
        print("6. Sair")

        opcao = input("\nEscolha uma opção (1-6): ")

        if opcao == '1':
            ver_todos_registros()
        elif opcao == '2':
            id = input("\nDigite o ID do registro que deseja apagar: ")
            limpar_registro(id)
        elif opcao == '3':
            limpar_banco()
        elif opcao == '4':
            resetar_banco()
        elif opcao == '5':
            configurar_e_enviar()
        elif opcao == '6':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == '__main__':
    menu()

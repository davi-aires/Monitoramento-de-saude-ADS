
# 💚 Monitoramento de Saúde - ADS

Aplicação web para registrar e monitorar dados diários de saúde, com análise inteligente gerada por IA e suporte a deploy na nuvem.

## 📋 Funcionalidades

- ✅ Formulário web responsivo para registro diário de saúde
- ✅ Registro de consumo de água, minutos de sol, exercício e humor
- ✅ Histórico completo com busca por nome
- ✅ Página de resultados com estatísticas individuais (cards de resumo)
- ✅ Resumo de saúde gerado por IA (Groq — llama-3.3-70b) com análise humanizada
- ✅ Suporte a SQLite (local) e PostgreSQL (produção/Render)
- ✅ Fuso horário correto para Brasil (America/Sao_Paulo)
- ✅ Exportação de relatório em Excel
- ✅ Importação de registros via Excel (restauração de dados)
- ✅ Migração de dados SQLite → PostgreSQL

## 🛠️ Tecnologias

- **Backend**: Python 3 + Flask
- **Banco de Dados**: SQLite (dev) / PostgreSQL (produção)
- **IA**: Groq API — modelo `llama-3.3-70b-versatile`
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Deploy**: Render (Web Service + PostgreSQL)
- **Relatórios**: openpyxl (Excel)

## 📦 Instalação local

### 1. Criar e ativar o ambiente virtual

```bash
# Criar
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_groq_aqui

# Opcional — só necessário para conectar ao PostgreSQL local/remoto
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

## 🚀 Como executar

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📁 Estrutura do Projeto

```
ADS - Monitoramento de saúde/
├── app.py                  # Backend Flask (rotas e lógica principal)
├── db_manager.py           # Gerenciamento do banco de dados e menu de manutenção
├── requirements.txt        # Dependências do projeto
├── render.yaml             # Configuração de deploy no Render
├── database.db             # Banco SQLite local (criado automaticamente)
├── .env                    # Variáveis de ambiente (não versionado)
└── templates/
    ├── form.html           # Formulário de registro diário
    ├── historico.html      # Histórico de registros com busca
    └── resultados.html     # Página de resultados e análise por IA
```

## 💾 Banco de Dados

A tabela `saude` possui os seguintes campos:

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER / SERIAL | Identificador único (chave primária) |
| `data_registro` | TIMESTAMP | Data e hora do registro |
| `nome` | TEXT | Nome do usuário |
| `consumo_agua` | INTEGER | Consumo de água em ml |
| `minutos_sol` | INTEGER | Minutos de exposição ao sol |
| `pratica_exercicio` | TEXT | "Sim" ou "Não" |
| `humor` | TEXT | Ótimo, Bom, Normal ou Ruim |

## 🛠️ Menu de Manutenção (`db_manager.py`)

Execute `python db_manager.py` para acessar o menu interativo:

| Opção | Função |
|---|---|
| 1 | Ver todos os registros |
| 2 | Limpar um registro por ID |
| 3 | Limpar todos os registros (mantém estrutura) |
| 4 | Resetar banco de dados |
| 5 | Gerar relatório Excel |
| 6 | Importar registros de um arquivo Excel |
| 7 | Migrar dados SQLite → PostgreSQL |
| 8 | Sair |

## 🔌 Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Página principal com formulário |
| `POST` | `/salvar` | Salva um novo registro de saúde |
| `GET` | `/historico` | Página de histórico de registros |
| `GET` | `/resultados?nome=Nome` | Página de resultados individuais com IA |
| `POST` | `/gerar-resumo` | Gera resumo de saúde via Groq AI |

### POST `/salvar` — Exemplo

```json
{
    "nome": "João",
    "consumo_agua": 2000,
    "minutos_sol": 30,
    "pratica_exercicio": "Sim",
    "humor": "Ótimo"
}
```

## ☁️ Deploy no Render

O projeto inclui `render.yaml` com configuração automática. Para fazer deploy:

1. Crie um **PostgreSQL** no Render
2. Crie um **Web Service** conectado a este repositório
3. Adicione a variável de ambiente `GROQ_API_KEY` no painel do Render
4. O `DATABASE_URL` é vinculado automaticamente pelo `render.yaml`

## 🔒 Validações

- Todos os campos são obrigatórios
- Consumo de água: 0–5000 ml
- Minutos no sol: 0–480 minutos
- Prática de exercício: Sim ou Não
- Humor: Ótimo, Bom, Normal ou Ruim


## 🚧 Melhorias futuras

- [ ] Autenticação de usuários
- [ ] Dashboard com gráficos e estatísticas
- [ ] Exportar dados em CSV
- [ ] Metas e recomendações personalizadas
- [ ] Notificações e lembretes
- [ ] Integração com APIs de saúde

## 👨‍💻 Desenvolvido para

ADS - Análise e Desenvolvimento de Sistemas

## 📄 Licença

Este projeto é livre para uso educacional e pessoal.

# 💚 Monitoramento de Saúde - ADS

Um projeto simples para registrar e monitorar dados diários de saúde usando Python, Flask e SQLite.

## 📋 Funcionalidades

- ✅ Formulário web intuitivo e responsivo
- ✅ Registro de consumo de água diário (em litros)
- ✅ Registro de minutos no sol por dia
- ✅ Registro de prática de exercício (Sim/Não)
- ✅ Registro de humor do dia (Ótimo, Bom, Normal, Ruim)
- ✅ Salva automaticamente no banco SQLite
- ✅ Histórico de registros

## 🛠️ Tecnologias

- **Backend**: Python 3 + Flask
- **Banco de Dados**: SQLite
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Design**: Interface moderna e responsiva

## 📦 Instalação

### 1. Ativar o ambiente virtual

```bash
# No Windows
.venv\Scripts\activate

# No macOS/Linux
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como executar

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📁 Estrutura do Projeto

```
ADS - Monitoramento de saúde/
├── app.py                 # Backend Flask
├── database.db           # Banco de dados SQLite (criado automaticamente)
├── requirements.txt      # Dependências do projeto
├── README.md            # Este arquivo
└── templates/
    └── form.html        # Formulário web
    └── historico.html        # historico web
```

## 💾 Banco de Dados

A tabela `saude` possui os seguintes campos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Identificador único (chave primária) |
| `data_registro` | TIMESTAMP | Data e hora do registro |
| `nome` | TEXT | Nome de quem preencheu o registro |
| `consumo_agua` | INTEGER | Quantidade de água em litros |
| `minutos_sol` | INTEGER | Minutos de exposição ao sol |
| `pratica_exercicio` | TEXT | "Sim" ou "Não" |
| `humor` | TEXT | Ótimo, Bom, Normal ou Ruim |

## 🛠️ Funções de Gerenciamento do Banco de Dados

O projeto inclui funções utilitárias para manutenção do banco de dados, disponíveis em `db_manager.py`:

- **ver_todos_registros()**: Exibe todos os registros salvos no banco.
- **limpar_registro(id)**: Remove apenas um registro específico pelo ID, com confirmação.
- **limpar_banco()**: Remove todos os registros do banco, mantendo a estrutura da tabela (requer confirmação).
- **resetar_banco()**: Apaga completamente o arquivo do banco de dados e recria a estrutura do zero (requer confirmação).
- **menu()**: Menu interativo para executar as funções acima pelo terminal.

> Para usar essas funções, execute `python db_manager.py` e siga as instruções do menu.

## 🔌 Endpoints da API

### POST `/salvar`
Salva um novo registro de saúde.

**Corpo da requisição:**
```json
{
    "nome": "João",
    "consumo_agua": 8,
    "minutos_sol": 30,
    "pratica_exercicio": "Sim",
    "humor": "Ótimo"
}
```

**Resposta (Sucesso):**
```json
{
    "sucesso": true,
    "mensagem": "Dados salvos com sucesso!"
}
```

### GET `/historico`
Renderiza a página de histórico de registros salvos.

### GET `/`
Renderiza a página principal com o formulário.

## 🎨 Interface

O formulário inclui:
- **Design moderno** com gradiente roxo
- **Interface responsiva** para mobile e desktop
- **Feedback visual** com mensagens de sucesso/erro
- **Validação** de campos obrigatórios
- **Emojis** para melhor experiência do usuário

## 📝 Exemplo de uso

1. Abra a aplicação em **http://localhost:5000**
2. Preencha o formulário com seus dados do dia:
   - Quantos litros de água você bebeu?
   - Quantos minutos ficou no sol?
   - Praticou exercício?
   - Como está seu humor?
3. Clique em "Salvar Dados"
4. A aplicação confirmará o salvamento e limpará o formulário

## 🔒 Validações

- Todos os campos são obrigatórios
- Consumo de água: 0-20 litros
- Minutos no sol: 0-480 minutos
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


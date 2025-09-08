# To-Do API

API de gerenciamento de tarefas (To-Do List) com autenticação de usuários, escrita em **FastAPI**, usando **SQLAlchemy** para banco de dados e seguindo boas práticas de Python.

---

## **Deploy / Acesso Online**

A API também está disponível online para testes:

- Documentação interativa: [https://todo-api-prt6.onrender.com/docs](https://todo-api-prt6.onrender.com/docs)

Você pode usar a documentação para registrar usuários, logar e gerenciar tarefas diretamente no navegador ou via ferramentas como `curl` e Postman.

Exemplo `curl` (Windows CMD) para registrar usuário:

```cmd
curl -X POST "https://todo-api-prt6.onrender.com/users/register" ^
-H "Content-Type: application/json" ^
-d "{\"username\": \"meu_usuario\", \"password\": \"minha_senha\"}"
```

Exemplo `curl` para login e obter token:

```cmd
curl -X POST "https://todo-api-prt6.onrender.com/users/login" ^
-H "Content-Type: application/x-www-form-urlencoded" ^
-d "username=meu_usuario&password=minha_senha"
```

Exemplo `curl` para criar uma tarefa (substitua SEU_TOKEN_AQUI pelo token JWT retornado no login):

```cmd
curl -X POST "https://todo-api-prt6.onrender.com/tasks/" ^
-H "Content-Type: application/json" ^
-H "Authorization: Bearer SEU_TOKEN_AQUI" ^
-d "{\"title\": \"Teste online\", \"completed\": false}"
```

Exemplo `curl` para listar tarefas:

```cmd
curl -X GET "https://todo-api-prt6.onrender.com/tasks" ^
-H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## **Tecnologias**

- Python 3.11
- FastAPI
- SQLAlchemy
- Pydantic
- JWT para autenticação
- SQLite (ou PostgreSQL opcional)
- Pytest + httpx (testes)
- Black, Flake8, Mypy (qualidade do código)
- GitHub Actions (CI/CD)

---

## **Estrutura do Projeto**

```text
todo_api/
│
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── utils.py
│ └── routers/
│ ├── users.py
│ └── tasks.py
├── tests/
│ ├── test_users.py
│ └── test_tasks.py
├── requirements.txt
├── setup.cfg
└── .github/workflows/ci.yml
```

---

## **Setup e execução**

1. Clonar repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd todo_api
```

2. Criar virtualenv e instalar dependências:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

3. Rodar a API localmente:

```bash
uvicorn app.main:app --reload
```

4. Acessar documentação interativa em:

```bash
http://127.0.0.1:8000/docs
```

---

## Endpoints principais

### Usuários

* POST /users/register → Registrar novo usuário

* POST /users/login → Login e retorno de token JWT

* GET /users/me → Informações do usuário autenticado

### Tarefas (To-Do)

* POST /tasks → Criar nova tarefa

* GET /tasks → Listar tarefas

* PUT /tasks/{id} → Atualizar tarefa

* DELETE /tasks/{id} → Deletar tarefa

* GET /tasks/stats → Estatísticas de tarefas (total, concluídas, pendentes, por prioridade)

⚠️ Observação: Rotas de tarefas exigem autenticação JWT.

---

## Testes

Rodar todos os testes automatizados:

```bash
pytest -v --cov=app --cov-report=term-missing
flake8 app tests
black --check app tests
mypy app tests
```

---

## CI/CD

O projeto já possui integração contínua configurada com GitHub Actions:

* Linting: Flake8, Black

* Tipagem: Mypy

* Testes: Pytest + cobertura

* Workflow: .github/workflows/ci.yml

---

## Observações

* Suporta SQLite para testes e desenvolvimento; PostgreSQL recomendado para produção.

* JWT utilizado para autenticação segura.

* Estrutura modular facilita manutenção e expansão da API.

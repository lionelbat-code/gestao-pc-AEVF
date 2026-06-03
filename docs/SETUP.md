# 🚀 Guia de Configuração

## Pré-requisitos

- Python 3.8+
- Node.js 14+
- MySQL 5.7+
- Git

## 📦 Instalação

### 1. Clonar Repositório

```bash
git clone https://github.com/LIONELBAT-CODE/gestao-pc-AEVF.git
cd gestao-pc-AEVF
```

### 2. Configurar Backend

#### 2.1 Criar Ambiente Virtual

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 2.2 Instalar Dependências

```bash
pip install -r requirements.txt
```

#### 2.3 Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha com seus dados:

```bash
cp .env.example .env
```

Edite `.env`:
```
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=gestao_pc_aevf
```

#### 2.4 Inicializar Base de Dados

```bash
python database/init_db.py
```

#### 2.5 Executar Backend

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

### 3. Configurar Frontend

#### 3.1 Instalar Dependências

```bash
cd frontend
npm install
```

#### 3.2 Configurar Variáveis de Ambiente

```bash
cp .env.example .env.local
```

Edite `.env.local`:
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

#### 3.3 Executar Frontend

```bash
npm start
```

A aplicação estará disponível em `http://localhost:3000`

## 🔐 Credenciais Padrão

**⚠️ IMPORTANTE:** Altere estas credenciais em ambiente de produção!

**Admin:**
- Email: `admin@aevf.edu`
- Senha: `Admin@123`

**Consulta:**
- Email: `consulta@aevf.edu`
- Senha: `Consulta@123`

## 🗄️ Base de Dados

### Estrutura Principal

- **utilizadores** - Contas de acesso (admin, consulta)
- **alunos** - Dados dos alunos
- **salas** - Salas de aula
- **computadores_sala** - PCs instalados nas salas
- **computadores_aluno** - PCs emprestáveis aos alunos
- **emprestimos** - Registos de empréstimos
- **ocorrencias** - Registos de danos/reparações
- **historico_emprestimos** - Auditoria de empréstimos
- **historico_ocorrencias** - Auditoria de ocorrências

### Backup

```bash
# Exportar BD
mysqldump -u root -p gestao_pc_aevf > backup.sql

# Importar BD
mysql -u root -p gestao_pc_aevf < backup.sql
```

## 🧪 Testes

### Backend

```bash
cd backend
python -m pytest
```

### Frontend

```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### Erro de Conexão MySQL

```
Error: Can't connect to MySQL server
```

**Solução:**
- Verifique se MySQL está em execução
- Verifique credenciais em `.env`
- Verifique host e porta

### Erro de Módulo Python

```
ModuleNotFoundError: No module named 'flask'
```

**Solução:**
```bash
# Certifique-se de estar no ambiente virtual
pip install -r requirements.txt
```

### Erro de Port Already in Use

```
Address already in use: 0.0.0.0:5000
```

**Solução:**
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 📝 Desenvolvimento

### Estrutura de Branches

- `main` - Produção
- `develop` - Desenvolvimento
- `feature/*` - Novas funcionalidades
- `bugfix/*` - Correções de bugs

### Padrão de Commits

```
feat: Adicionar nova funcionalidade
fix: Corrigir bug
docs: Atualizar documentação
style: Formatar código
refactor: Refatorar código
test: Adicionar testes
chore: Tarefas de manutenção
```

## 🚀 Deploy

### Produção (Heroku + Vercel)

Veja `docs/DEPLOY.md`

---

**Precisa de ajuda?** Crie uma issue no GitHub!
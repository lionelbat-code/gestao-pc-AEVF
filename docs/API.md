# 📚 Documentação da API

## Visão Geral

API RESTful para o Sistema de Gestão de Computadores AEVF.

**Base URL:** `http://localhost:5000/api`

---

## 🔐 Autenticação

Todos os endpoints protegidos requerem um token JWT no header `Authorization`:

```
Authorization: Bearer <token>
```

### Login

**POST** `/auth/login`

Request:
```json
{
  "email": "admin@aevf.edu",
  "password": "sua_senha"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "utilizador_id": 1,
    "email": "admin@aevf.edu",
    "nome_completo": "Administrador AEVF",
    "tipo_conta": "admin"
  }
}
```

---

## 📋 Endpoints

### ALUNOS

#### Listar Alunos
**GET** `/alunos`

Parâmetros de query:
- `page` (opcional): Página (padrão: 1)
- `limit` (opcional): Itens por página (padrão: 20)
- `ativo` (opcional): true/false

#### Obter Aluno
**GET** `/alunos/{aluno_id}`

#### Criar Aluno (Admin)
**POST** `/alunos`

Body:
```json
{
  "numero": "20230001",
  "nome": "João Silva",
  "nif": "123456789",
  "morada": "Rua Principal, 123",
  "ee_nome": "Maria Silva",
  "ee_nif": "987654321",
  "ee_contacto": "912345678",
  "ee_numero_cidadao": "12345678"
}
```

#### Atualizar Aluno (Admin)
**PUT** `/alunos/{aluno_id}`

#### Deletar Aluno (Admin)
**DELETE** `/alunos/{aluno_id}`

---

### COMPUTADORES

#### Listar Computadores de Sala
**GET** `/computadores/sala`

#### Listar Computadores de Aluno
**GET** `/computadores/aluno`

Parâmetros de query:
- `estado` (opcional): Filtrar por estado

#### Obter Computador
**GET** `/computadores/{pc_id}`

#### Criar Computador (Admin)
**POST** `/computadores`

Body:
```json
{
  "numero_serie": "SN12345",
  "marca": "Dell",
  "modelo": "Inspiron 15",
  "hotspot": "SIM",
  "sim_card": "SIM12345",
  "data_aquisicao": "2023-01-15",
  "tipo": "aluno"
}
```

#### Atualizar Estado (Admin)
**PUT** `/computadores/{pc_id}/estado`

Body:
```json
{
  "estado": "em_reparacao",
  "observacoes": "Teclado danificado"
}
```

---

### EMPRÉSTIMOS

#### Listar Empréstimos
**GET** `/emprestimos`

Parâmetros de query:
- `aluno_id` (opcional)
- `estado` (opcional)
- `page` (opcional)
- `limit` (opcional)

#### Obter Empréstimo
**GET** `/emprestimos/{emprestimo_id}`

#### Criar Empréstimo (Admin)
**POST** `/emprestimos`

Body:
```json
{
  "aluno_id": 1,
  "pc_id": 5,
  "data_emprestimo": "2024-01-15",
  "data_devolucao_prevista": "2024-06-30"
}
```

#### Atualizar Estado (Admin)
**PUT** `/emprestimos/{emprestimo_id}/estado`

Body:
```json
{
  "estado": "devolvido",
  "data_devolucao_efetiva": "2024-01-20"
}
```

---

### OCORRÊNCIAS

#### Listar Ocorrências
**GET** `/ocorrencias`

Parâmetros de query:
- `estado` (opcional)
- `pc_id` (opcional)

#### Criar Ocorrência (Admin)
**POST** `/ocorrencias`

Body:
```json
{
  "emprestimo_id": 1,
  "pc_id": 5,
  "descricao_problema": "Ecrã com pixels mortos",
  "data_reporte": "2024-01-18"
}
```

#### Atualizar Ocorrência (Admin)
**PUT** `/ocorrencias/{ocorrencia_id}`

Body:
```json
{
  "estado": "reparado",
  "data_reparacao_concluida": "2024-01-22",
  "responsavel_reparacao": "Técnico Silva"
}
```

---

### DASHBOARDS

#### Estatísticas Gerais
**GET** `/dashboard/stats`

Response:
```json
{
  "total_computadores": 150,
  "total_alunos": 500,
  "computadores_em_emprestimo": 120,
  "ocorrencias_pendentes": 8,
  "taxa_ocupacao": "80%"
}
```

#### Status de Salas
**GET** `/dashboard/salas-status`

---

## ❌ Códigos de Resposta

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

---

## 📖 Notas

- Todas as respostas são em JSON
- Datas devem estar no formato `YYYY-MM-DD`
- O acesso é controlado pelo tipo de conta (`admin` ou `consulta`)

---

**Última atualização:** Janeiro 2024
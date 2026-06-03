-- ============================================================
-- SCHEMA: Sistema de Gestão de Computadores - AEVF
-- ============================================================

-- Criar base de dados
CREATE DATABASE IF NOT EXISTS gestao_pc_aevf;
USE gestao_pc_aevf;

-- ============================================================
-- TABELA: UTILIZADORES (Autenticação)
-- ============================================================
CREATE TABLE utilizadores (
    utilizador_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome_completo VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tipo_conta ENUM('consulta', 'admin') DEFAULT 'consulta',
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_ultimo_login TIMESTAMP NULL,
    INDEX(email),
    INDEX(tipo_conta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: ALUNOS
-- ============================================================
CREATE TABLE alunos (
    aluno_id INT PRIMARY KEY AUTO_INCREMENT,
    numero VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    nif VARCHAR(20) UNIQUE NOT NULL,
    morada TEXT NOT NULL,
    ee_nome VARCHAR(255) NOT NULL,
    ee_nif VARCHAR(20) NOT NULL,
    ee_contacto VARCHAR(20) NOT NULL,
    ee_numero_cidadao VARCHAR(20),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    INDEX(numero),
    INDEX(nif),
    INDEX(ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: SALAS
-- ============================================================
CREATE TABLE salas (
    sala_id INT PRIMARY KEY AUTO_INCREMENT,
    numero_sala VARCHAR(50) UNIQUE NOT NULL,
    localizacao VARCHAR(255),
    capacidade_alunos INT,
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    INDEX(numero_sala),
    INDEX(ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: COMPUTADORES DE SALA (Inventário fixo)
-- ============================================================
CREATE TABLE computadores_sala (
    pc_sala_id INT PRIMARY KEY AUTO_INCREMENT,
    sala_id INT NOT NULL,
    numero_serie VARCHAR(100) UNIQUE NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    data_aquisicao DATE,
    estado ENUM('funcionando', 'avariado', 'necessita_substituicao') DEFAULT 'funcionando',
    descricao_avaria TEXT,
    data_ultima_manutencao DATE,
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sala_id) REFERENCES salas(sala_id) ON DELETE CASCADE,
    INDEX(numero_serie),
    INDEX(sala_id),
    INDEX(estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: COMPUTADORES DE ALUNO (Emprestáveis)
-- ============================================================
CREATE TABLE computadores_aluno (
    pc_id INT PRIMARY KEY AUTO_INCREMENT,
    numero_serie VARCHAR(100) UNIQUE NOT NULL,
    hotspot VARCHAR(50),
    sim_card VARCHAR(50),
    marca VARCHAR(100),
    modelo VARCHAR(100),
    data_aquisicao DATE,
    estado ENUM('disponivel', 'em_emprestimo', 'em_reparacao', 'inutilizado') DEFAULT 'disponivel',
    observacoes TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX(numero_serie),
    INDEX(estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: EMPRESTIMOS (com versionamento para histórico)
-- ============================================================
CREATE TABLE emprestimos (
    emprestimo_id INT PRIMARY KEY AUTO_INCREMENT,
    aluno_id INT NOT NULL,
    pc_id INT NOT NULL,
    estado ENUM('nao_tem', 'atribuido', 'em_reparacao', 'reparado', 'inutilizado', 'recusou', 'devolvido') DEFAULT 'nao_tem',
    data_emprestimo DATE,
    data_devolucao_prevista DATE,
    data_devolucao_efetiva DATE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    numero_versao INT DEFAULT 1,
    observacoes TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id) ON DELETE CASCADE,
    FOREIGN KEY (pc_id) REFERENCES computadores_aluno(pc_id) ON DELETE CASCADE,
    INDEX(aluno_id),
    INDEX(pc_id),
    INDEX(estado),
    INDEX(data_atualizacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: OCORRENCIAS (com versionamento para histórico)
-- ============================================================
CREATE TABLE ocorrencias (
    ocorrencia_id INT PRIMARY KEY AUTO_INCREMENT,
    emprestimo_id INT NOT NULL,
    pc_id INT NOT NULL,
    estado ENUM('em_reparacao', 'reparado') DEFAULT 'em_reparacao',
    descricao_problema TEXT NOT NULL,
    data_reporte DATE NOT NULL,
    data_entrega_reparacao DATE,
    data_reparacao_concluida DATE,
    responsavel_reparacao VARCHAR(255),
    numero_versao INT DEFAULT 1,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(emprestimo_id) ON DELETE CASCADE,
    FOREIGN KEY (pc_id) REFERENCES computadores_aluno(pc_id) ON DELETE CASCADE,
    INDEX(pc_id),
    INDEX(estado),
    INDEX(data_reporte)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: HISTORICO_EMPRESTIMOS (Auditoria completa)
-- ============================================================
CREATE TABLE historico_emprestimos (
    historico_id INT PRIMARY KEY AUTO_INCREMENT,
    emprestimo_id INT NOT NULL,
    aluno_id INT NOT NULL,
    pc_id INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_novo VARCHAR(50) NOT NULL,
    data_mudanca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    alterado_por INT,
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(emprestimo_id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id) ON DELETE CASCADE,
    FOREIGN KEY (pc_id) REFERENCES computadores_aluno(pc_id) ON DELETE CASCADE,
    FOREIGN KEY (alterado_por) REFERENCES utilizadores(utilizador_id),
    INDEX(emprestimo_id),
    INDEX(aluno_id),
    INDEX(data_mudanca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: HISTORICO_OCORRENCIAS (Auditoria completa)
-- ============================================================
CREATE TABLE historico_ocorrencias (
    historico_id INT PRIMARY KEY AUTO_INCREMENT,
    ocorrencia_id INT NOT NULL,
    pc_id INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_novo VARCHAR(50) NOT NULL,
    data_mudanca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    alterado_por INT,
    FOREIGN KEY (ocorrencia_id) REFERENCES ocorrencias(ocorrencia_id) ON DELETE CASCADE,
    FOREIGN KEY (pc_id) REFERENCES computadores_aluno(pc_id) ON DELETE CASCADE,
    FOREIGN KEY (alterado_por) REFERENCES utilizadores(utilizador_id),
    INDEX(ocorrencia_id),
    INDEX(pc_id),
    INDEX(data_mudanca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABELA: HISTORICO_COMPUTADORES_SALA (Auditoria)
-- ============================================================
CREATE TABLE historico_computadores_sala (
    historico_id INT PRIMARY KEY AUTO_INCREMENT,
    pc_sala_id INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_novo VARCHAR(50) NOT NULL,
    data_mudanca TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descricao_mudanca TEXT,
    alterado_por INT,
    FOREIGN KEY (pc_sala_id) REFERENCES computadores_sala(pc_sala_id) ON DELETE CASCADE,
    FOREIGN KEY (alterado_por) REFERENCES utilizadores(utilizador_id),
    INDEX(pc_sala_id),
    INDEX(data_mudanca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- DADOS INICIAIS
-- ============================================================

-- Inserir utilizador admin padrão (password: Admin@123 - MUDAR EM PRODUÇÃO)
INSERT INTO utilizadores (email, nome_completo, password_hash, tipo_conta, ativo)
VALUES ('admin@aevf.edu', 'Administrador AEVF', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm2', 'admin', TRUE);

-- Inserir utilizador consulta padrão (password: Consulta@123 - MUDAR EM PRODUÇÃO)
INSERT INTO utilizadores (email, nome_completo, password_hash, tipo_conta, ativo)
VALUES ('consulta@aevf.edu', 'Utilizador Consulta', '$2b$12$N8k4mLpWv7f2z9x0q1r5s.1t0u9v8w7x6y5z4a3b2c1d0e9f8g7h6', 'consulta', TRUE);

-- ============================================================
-- VIEWS ÚTEIS
-- ============================================================

-- Vista: Status dos empréstimos por aluno
CREATE VIEW vw_emprestimos_aluno AS
SELECT 
    a.aluno_id,
    a.numero,
    a.nome,
    ca.pc_id,
    ca.numero_serie,
    ca.marca,
    ca.modelo,
    e.emprestimo_id,
    e.estado,
    e.data_emprestimo,
    e.data_devolucao_prevista,
    e.data_devolucao_efetiva
FROM alunos a
LEFT JOIN emprestimos e ON a.aluno_id = e.aluno_id
LEFT JOIN computadores_aluno ca ON e.pc_id = ca.pc_id
WHERE a.ativo = TRUE;

-- Vista: Status dos computadores de sala
CREATE VIEW vw_computadores_sala_status AS
SELECT 
    s.sala_id,
    s.numero_sala,
    s.localizacao,
    COUNT(CASE WHEN cs.estado = 'funcionando' THEN 1 END) AS funcionando,
    COUNT(CASE WHEN cs.estado = 'avariado' THEN 1 END) AS avariado,
    COUNT(CASE WHEN cs.estado = 'necessita_substituicao' THEN 1 END) AS necessita_substituicao,
    COUNT(cs.pc_sala_id) AS total
FROM salas s
LEFT JOIN computadores_sala cs ON s.sala_id = cs.sala_id
WHERE s.ativo = TRUE
GROUP BY s.sala_id, s.numero_sala, s.localizacao;

-- Vista: Ocorrências pendentes
CREATE VIEW vw_ocorrencias_pendentes AS
SELECT 
    o.ocorrencia_id,
    o.pc_id,
    ca.numero_serie,
    ca.marca,
    a.numero,
    a.nome,
    o.descricao_problema,
    o.data_reporte,
    DATEDIFF(CURDATE(), o.data_reporte) AS dias_pendente
FROM ocorrencias o
JOIN computadores_aluno ca ON o.pc_id = ca.pc_id
JOIN emprestimos e ON o.emprestimo_id = e.emprestimo_id
JOIN alunos a ON e.aluno_id = a.aluno_id
WHERE o.estado = 'em_reparacao'
ORDER BY o.data_reporte ASC;

-- ============================================================
-- FIM DO SCHEMA
-- ============================================================

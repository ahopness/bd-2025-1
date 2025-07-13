# Sistema de Gestão de Campeonatos Esportivos

**Disciplina**: Sistemas de Bancos de Dados.

**Professor**: Prof. Dr. Anderson Namen.

Instituto Politécnico, Universidade do Estado do Rio de Janeiro. Julho, 2025.

**Créditos**:
- Lucas Ângelo Câmara da Silva
  - Matrícula: *202410367011*
  - Github: *@ahopness*
- Steffany Ouverney
  - Matrícula: *202010077411*
  - Github: *@Steffany Ouverney*
- Eduardo Freitas
  - Matrícula: *202010357011*
  - Github: *@Edufreijr*
- Gabriel César
  - Matrícula: *202010358011*
  - Github: *@knichian*

## Objetivo do Sistema

O sistema é uma plataforma completa para organização de campeonatos esportivos, desde torneios profissionais até competições amadoras. Direcionado para organizadores e espectadores de eventos esportivos, oferece como diferencial a classificação e status automatizados dos campeonatos.

## Arquitetura do Sistema

O projeto foi desenvolvido seguindo uma arquitetura em camadas:

- **Frontend**: Páginas web simples com Server Side Render utilizando Jinja2
- **Backend**: APIs e rotas desenvolvidas em Python com Flask
- **Banco de Dados**: MySQL com 5 tabelas principais
- **Fluxo de Dados**: Usuário → Campeonato → Times → Partidas

## Estrutura do Banco de Dados

O banco de dados foi modelado com as seguintes tabelas principais:

1. **Usuários**: Armazena informações dos donos dos campeonatos
2. **Esportes**: Modalidades esportivas disponíveis no sistema
3. **Campeonatos**: Torneios criados pelos usuários
4. **Times**: Equipes participantes dos campeonatos
5. **Partidas**: Jogos agendados entre as equipes

## Funcionalidades Principais

### Operações CRUD

#### Consulta (READ)
- Exibe todos os campeonatos do sistema
- Classifica automaticamente por status
- Ordena por data de início
- Filtra campeonatos por dono (quando logado)

#### Criação (CREATE)
- **Regras de Negócio**:
  - Nomes únicos para campeonatos
  - Times não podem jogar contra si mesmos
  - Apenas o dono pode adicionar dados ao campeonato

#### Atualização (UPDATE)
- **Validações**:
  - Datas válidas (fim > início)
  - Recalculo automático da classificação ao atualizar placares
  - Bloqueio de edições por não-donos

#### Remoção (DELETE)
- **Permissões**: Apenas o usuário dono pode excluir seus campeonatos
- **Exclusões em Cascata**:
  - Ao excluir campeonato: remove todos os times e partidas relacionados
  - Ao excluir time: remove suas partidas relacionadas
- Proteção contra edições não autorizadas

## Segurança Implementada

O sistema conta com múltiplas camadas de segurança:

- **Verificação de Sessão**: Controle de acesso em todas as operações CRUD
- **Controle de Propriedade**: Usuários só podem editar seus próprios campeonatos

## Desafios Enfrentados

Durante o desenvolvimento, foram superados diversos desafios técnicos:

- Complexidade das queries com múltiplos JOIN
- Sincronização de datas e horários
- Validação de regras de negócio no backend
- Implementação de exclusões em cascata

## Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML, CSS, Jinja2
- **Banco de Dados**: MySQL
- **Arquitetura**: MVC (Model-View-Controller)

## Instruções de Execução

### Pré-requisitos

- Python (3.10 ou superior)
- XAMPP (mais recente)

### Instalação

1. **Clonar o repositório**:
```bash
git clone https://github.com/ahopness/bd-2025-1.git
cd bd-2025-1
```

2. **Instalar dependências**:
```bash
pip install PyMySQL
pip install Flask
```

3. **Iniciar XAMPP**

4. **Executar migrações**:
```bash
flask setup-db
```

5. **Iniciar o servidor**:
```bash
flask run --debug
```

6. **Acessar o app no navegador**:
```
http://127.0.0.1:5000
```

## Próximos Passos

Para futuras versões, estão planejadas as seguintes melhorias:

- Adicionar estatísticas detalhadas para jogadores
- Adaptação para campeonatos poliesportivos
- Implementação de CRUD completo para tabela de esportes
- Sistema de permissões de superusuário/administrador
- Inscrições de espectadores em torneios
- Sistema de notificações (e-mail, SMS, WhatsApp)
- Aprimoramento da segurança de credenciais de usuários (proteção contra SQL Injection)

## Estrutura de Arquivos

```
sistema-campeonatos/
├── app.py              # Entrypoint com rotas da aplicação
├── utils.py            # Scripts de migração
├── config.py           # Scripts de configuração ao acesso do banco de dados MySQL
├── templates/          # Templates Jinja2
├── static/             # Arquivos estáticos (CSS, JS)
└── api/                # Scripts de operações CRUD 
```

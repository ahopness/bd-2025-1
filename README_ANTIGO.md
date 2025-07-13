# Trabalho BD 2025.1: Repositório

**Ideia**: Gestor de campeonato

Uma plataforma para organizar campeonatos de bairro ou de empresas. Qualquer pessoa poderia criar um campeonato, convidar os times, gerar a tabela de jogos e atualizar os resultados a cada rodada, com uma página pública para classificação e artilharia.

## Dependencias

- `pip install PyMySQL`
- `pip install Flask`

## Mais sobre

- Arquivos criados usando Python 3.10, qualquer outra versão **mais nova** deve funcionar OK;
- Duas opções de servidor (ver `config.py`):
  - Servidor MySQL hosteado localmente pelo XAMPP;
    - Lembrar de inciar o servidor XAMPP (completo ou só o SQL) antes de rodar qualquer codigo do repositório.
    - Favor rodar `flask setup-db` no CMD para inicializar a database, rodar a query de create e popular ele com alguns dados padrões caso estiver usando o XAMPP.
      - O codigo por trás desse comando esta no `utils.py` se quiserem dar uma olhada.
  - Servidor MySQL hosteado no Digital Ocean;
    - Não precisa instalar nem configurar o XAMPP.
      - Mais rapido mas requer internet, talvez não seja uma boa usar na apresentação.
    - O servidor não tem nenhuma Trusted Source configurada, então qualquer PC pode se conectar a ela.
    - PS: Tenho desconto de estudante então ta saindo de graça :p 
- Data da apresentação: 02/07
  - PS: Codigo vai ser entregue junto com a apresentação no dia 25/06.

## Links uteis

- [Pitch e tarefas do trabalho (Docs)](https://docs.google.com/document/d/1SUF8ilgJleFLO0s2-iHREiRlMKxpnqj12j14n1lDKLU/edit?usp=sharing)
- [Documentação do Flask](https://flask.palletsprojects.com/en/stable/quickstart/#)
- [Documentação do Jinja](https://jinja.palletsprojects.com/en/stable/)
- [Documentação do PyMySQL](https://pymysql.readthedocs.io/en/latest/modules/connections.html)
- [Python Database API Specification (mais sobre PyMySQL)](https://peps.python.org/pep-0249/)

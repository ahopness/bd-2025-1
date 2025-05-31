## Dependencias

- `pip install PyMySQL`
- `pip install Flask`

## Mais sobre

- Tema: *Times*;
- Arquivos criados usando Python 3.10, qualquer outra versão **mais nova** deve funcionar OK;
- Servidor MySQL hosteado no Digital Ocean;
  - PS¹: Tenho desconto de estudante então ta saindo de graça :p 
  - PS²: O servidor não tem nenhuma Trusted source configurada, então qualquer PC pode se conectar a ela. Talvez alterar isso no futuro se agnt deixar publico.
- Data da apresentação: 02/07
  - PS: Codigo vai ser entregue junto com a apresentação.

Credenciais do Servidor MySQL:
```yaml
username: doadmin
password: AVNS_yNijUrtoczAa_bnrt74
host: db-mysql-nyc3-44101-do-user-20137976-0.l.db.ondigitalocean.com
port: 25060
database: defaultdb
sslmode: REQUIRED
```

## Links uteis

- [Documentação do Flask](https://flask.palletsprojects.com/en/stable/quickstart/#)
- [Documentação do Jinja](https://jinja.palletsprojects.com/en/stable/)
- [Documentação do PyMySQL](https://pymysql.readthedocs.io/en/latest/modules/connections.html)
- [Python Database API Specification (mais sobre PyMySQL)](https://peps.python.org/pep-0249/)

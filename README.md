# MVP Sprint PUC-Rio - Engenharia de Software

Esse repositório contém o `backend` do primeiro MVP para a pós-graduação em Engenharia de Software da PUC-Rio. Ele foi desenvolvindo em `python` utilizando o framework `django` e as bibliotecas `django-rest-framework` e `drf-spectacular` para criação da REST API e a UI do Swagger.

Nesse projeto criei um catálogo de dashboards, por se tratar de um MVP o banco de dados utilizado é o `sqlite3`. As imagens são armazenadas localmente na pasta `imgs` e o banco apenas referencia o local em que elas serão servidas pelo `django`.

Obs.: o `frontend` encontra-se [nesse repositório](https://github.com/luizzappa/hubanalytics-front).

## Como instalar

Clone o repositório e instale localmente as bibliotecas utlizando o comando:

```
pip install -r requirements.txt
```

## Como executar

Após a instalção das bibliotecas, no terminal execute o comando:

```
python manage.py runserver 8000
```

O servidor irá iniciar na porta 8000. **Atenção**: é importante iniciar na porta 8000 que é a esperada pelo `frontend`, caso necessite utilizar outra porta será necessário atualizá-la no `frontend`.

## Documentação da API (Swagger-UI)

Após iniciar o servidor, para acessar a documentação da API utilize a URL [http://localhost:8000/docs/](http://localhost:8000/docs/)

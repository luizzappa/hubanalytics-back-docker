# MVP Sprint PUC-Rio - Engenharia de Software

Esse repositório contém o `backend` do terceiro MVP para a pós-graduação em Engenharia de Software da PUC-Rio. Ele foi desenvolvindo em `python` utilizando o framework `django` e as bibliotecas `django-rest-framework` e `drf-spectacular` para criação da REST API e a UI do Swagger.

Nesse projeto criei um catálogo de dashboards, por se tratar de um MVP o banco de dados utilizado é o `sqlite3`. As imagens são armazenadas localmente na pasta `imgs` e o banco apenas referencia o local em que elas serão servidas pelo `django`.

Obs.: o `frontend` encontra-se [nesse repositório](https://github.com/luizzappa/hubanalytics-front-docker).

## Arquitetura

Nesse projeto utilizo a componentização em que cada microserviço é uma componente separada, o que permite ser escalada, implantada e desenvolvida de maneira independente.

Foram utilizados três componentes denominados A, B e C. Sendo que:

![image](https://github.com/luizzappa/hubanalytics-back-docker/assets/65685842/74013905-98b5-44dd-8dec-25c5ac849a1a)

**Componente A**: frontend da aplicação desenvolvido em react. O código está nesse [repositório](https://github.com/luizzappa/hubanalytics-front-docker)

**Componente B**: API do [TextRazor](https://www.textrazor.com/) para extração de palavras-chaves de um texto. Esse serviço foi utilizado para que o usuário ao descrever o seu dashboard, possa gerar automaticamente `tags` com base na descrição.

**Componente C**: backend da aplicação desenvolvido em Django. É o código desse projeto.

Os componentes A e C estão em containers docker. O componente B, por se tratar de uma API externa, é consumido pelo componente C (backend) em que é implementada uma rota que chama essa API externa passando a autenticação de forma segura e não expondo a API key para o frontend, retornando apenas o resultado da chamada a API externa. A rota que acessa essa API externa é a `extractkeywords`, onde se realiza um post no body com um json que possui uma key denominada `text` e o seu valor é o texto que se deseja extrair os termos chaves.

## Como instalar

Clone o repositório localmente.

Esse backend abstrai a chamada a API externa do [TextRazor](https://www.textrazor.com/) para que a `api key` não fique exposta no frontend e o header da resposta contenha os hosts allowed corretamente e não aconteça o problema de CORS policy. Para isso, a `api key` fica armazenado em um arquivo `.env`. Então, dentro da pasta `hubanalyticsapi` crie um arquivo denominado `.env`, em seu conteúdo coloque a `api_key`.

```
API_KEY=VALOR_DA_SUA_KEY
```

Depois de criar o arquivo, realize o build da imagem do docker com o seguinte comando:

```bash
docker build -t back .
```

## Como executar

Após completar o build da imagem do docker, execute-o com o seguinte comando:

```bash
docker run -p 8000:8000 back
```

O servidor irá iniciar na porta 8000. **Atenção**: é importante iniciar na porta 8000 que é a esperada pelo `frontend`, caso necessite utilizar outra porta será necessário atualizá-la no `frontend`.

## Documentação da API (Swagger-UI)

Após iniciar o servidor, para acessar a documentação da API utilize a URL [http://localhost:8000/docs/](http://localhost:8000/docs/)

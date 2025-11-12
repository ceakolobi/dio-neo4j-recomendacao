Projeto DIO: Sistema de Recomendação de Músicas com Grafos
Este projeto implementa um sistema web completo para recomendação de artistas, utilizando um banco de dados de grafos (Neo4j) para as consultas e uma API Python (Flask) para servir os resultados. A aplicação é capaz de carregar dados reais (do dataset Last.fm) e fornecer recomendações em tempo real através de uma interface web.

Link da Aplicação Ativa: http://avaliacao-dio.marka.tec.br

1. Tecnologias Utilizadas (O "Ecossistema")
Esta aplicação foi construída usando uma stack de servidor moderna, replicando um ambiente de produção profissional.

Servidor (Cloud): VPS (Virtual Private Server) da Hostinger.

Sistema Operacional: Ubuntu 25.04.

Servidor Web (O "Porteiro"): Nginx (configurado como Proxy Reverso).

Banco de Dados: Neo4j (rodando em um container Docker).

Back-end (API): Python 3.

Framework da API: Flask.

Servidor da Aplicação (O "Cozinheiro"): Gunicorn.

Driver do Banco: neo4j (biblioteca Python).

Ambiente Python: venv (ambiente virtual).

Front-end: HTML, CSS e JavaScript (puro, usando fetch para chamadas de API).

Infraestrutura como Código: Docker.

Linguagem de Consulta: Cypher (para o Neo4j).

Assistente de IA & Pair Programming: Gemini (Google).

2. Modelo do Grafo (O Esboço)
O banco de dados foi modelado de forma simples e poderosa, com dois tipos de "Nós" e um tipo de "Relacionamento":

Nós (Nodes):

(:User {userId}): Representa um usuário (ex: "2").

(:Artist {artistId, name}): Representa um artista (ex: "Metallica").

Relacionamentos (Edges):

(:User)-[:LISTENED_TO {playCount}]->(:Artist): Um relacionamento que indica que um usuário ouviu um artista um certo número de vezes.

Como gerar o PNG/PDF do Grafo:
Para entregar o "grafo" em formato de imagem, como solicitado na DIO:

Acesse seu painel do Neo4j (via "Túnel SSH").

Rode o comando: CALL db.schema.visualization()

Isso irá desenhar o modelo (os dois nós e o relacionamento) na tela.

Tire um "print" (screenshot) dessa visualização. Essa é a sua imagem do modelo do grafo.

3. Passo a Passo da Implementação (O "Caminho Feliz")
Este é o guia de como a aplicação foi construída e publicada do zero.

Configuração da VPS: Contratação de uma VPS Ubuntu, acesso via SSH e criação de um usuário sudo (ex: eduardo) por segurança, para evitar o uso do root.

Firewall (UFW): Ativação do ufw (sudo ufw enable) e liberação das portas essenciais (sudo ufw allow OpenSSH e sudo ufw allow 'Nginx Full').

Instalação do Docker e Neo4j: Instalação do Docker e inicialização de um container Neo4j (docker run ... neo4j:latest), expondo as portas 7474 (painel) e 7687 (banco) e definindo uma senha segura.

Configuração do Ambiente Python: Instalação do python3-pip e python3-venv. Criação de um ambiente virtual (python3 -m venv venv) na pasta do projeto e ativação (source venv/bin/activate).

Instalação das Dependências: Instalação das bibliotecas flask, neo4j e gunicorn (via pip install -r requirements.txt) dentro do venv.

Desenvolvimento:

api.py: Criação da API Flask com duas rotas (/recomendar-musicas e /artistas-similares) e as lógicas de consulta Cypher.

config.py: Criação de um arquivo separado (ignorado pelo Git) para armazenar as credenciais do Neo4j.

index.html: Criação da interface de usuário com JavaScript para "bater" na nossa API Flask e exibir os resultados dinamicamente.

Configuração do DNS: Criação de um registro Tipo A no painel de DNS (HostGator) para apontar o subdomínio avaliacao-dio.marka.tec.br para o IP da VPS (72.61.48.85).

Configuração do Nginx (Proxy Reverso): Criação de um arquivo de configuração em /etc/nginx/sites-available/ para o server_name avaliacao-dio.marka.tec.br. A configuração proxy_pass http://127.0.0.1:8000; direciona o tráfego do subdomínio para a aplicação Gunicorn.

Publicação (Deploy): Inicialização do Gunicorn (gunicorn --workers 3 --bind 127.0.0.1:8000 api:app --daemon) para rodar a aplicação Flask em modo permanente e em segundo plano.

Carga de Dados:

Download do dataset (Last.fm/Kaggle).

Cópia dos arquivos (.dat) para dentro do container Docker (docker cp ...).

Uso de comandos Cypher (LOAD CSV) "à prova de falhas" para carregar 17.000+ artistas e 92.000+ relacionamentos no banco de dados.

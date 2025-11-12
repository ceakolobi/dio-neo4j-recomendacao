from flask import Flask, jsonify, request, send_from_directory
from neo4j import GraphDatabase
import config 

# --- Configuração ---
app = Flask(__name__)

# Pega os dados do config.py
NEO4J_URI = config.NEO4J_URI
NEO4J_USER = config.NEO4J_USER
NEO4J_PASSWORD = config.NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Rota Principal (Serve o Site) ---
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

# --- API: Busca 1 (Recomendar Músicas para Usuário) ---
@app.route("/recomendar-musicas", methods=['GET'])
def api_recomendar_musicas():
    username = request.args.get('user')
    if not username:
        return jsonify({"erro": "Nome do usuário é obrigatório"}), 400

    query = """
    MATCH (u:User) WHERE toLower(u.name) = toLower($username)
    MATCH (u) -[:LISTENED_TO]-> (m1:Music)
    MATCH (other:User) -[:LISTENED_TO]-> (m1)
    WHERE other <> u
    MATCH (other) -[:LISTENED_TO]-> (rec:Music)
    WHERE NOT (u) -[:LISTENED_TO]-> (rec)
    RETURN rec.title AS nome, count(rec) AS score
    ORDER BY score DESC
    LIMIT 10
    """
    
    results = []
    with driver.session() as session:
        result = session.run(query, username=username)
        results = [{"nome": record["nome"], "score": record["score"]} for record in result]

    return jsonify(results)

# --- API: Busca 2 (Encontrar Artistas Similares) ---
@app.route("/artistas-similares", methods=['GET'])
def api_artistas_similares():
    artist_name = request.args.get('artist')
    if not artist_name:
        return jsonify({"erro": "Nome do artista é obrigatório"}), 400

    query = """
    MATCH (a1:Artist) WHERE toLower(a1.name) = toLower($artistName)
    MATCH (a1) <-[:LISTENED_TO]- (u:User) -[:LISTENED_TO]-> (a2:Artist)
    WHERE a1 <> a2
    RETURN a2.name AS nome, count(u) AS score
    ORDER BY score DESC
    LIMIT 10
    """
    
    results = []
    with driver.session() as session:
        result = session.run(query, artistName=artist_name)
        results = [{"nome": record["nome"], "score": record["score"]} for record in result]
        
    return jsonify(results)

# --- Roda o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
    driver.close()

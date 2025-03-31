from flask import Flask,request ,jsonify , render_template

import sqlite3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'titulo TEXT NOT NULL, '
        'categoria TEXT NOT NULL , '
        'autor TEXT NOT NULL,'
        'imagem_url TEXT NOT NULL)')

        print('Tabela criada com sucesso')

init_db()


@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/dar')
def pagina_doar():
    return render_template('dar.html')


@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()

    campos_obrigatorios = {
        'titulo': dados.get('titulo'),
        'categoria': dados.get('categoria'),
        'autor': dados.get('autor'),
        'imagem_url': dados.get('imagem_url')
    }

    if not all(campos_obrigatorios.values()):
        return jsonify({'erro': 'Os dados estão incompletos'}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute(f'INSERT INTO livros (titulo, categoria, autor, imagem_url) VALUES (?, ?, ?, ?)',
                     (campos_obrigatorios['titulo'], campos_obrigatorios['categoria'], campos_obrigatorios['autor'], campos_obrigatorios['imagem_url']))
        
        conn.commit()
        print('tudo certo')

        return jsonify({'mensagem': 'Livro doado com sucesso'}), 200
    
    
    


@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute('SELECT * FROM livros').fetchall()

    
        livros_formatados = []

        for livro in livros:
            livro_formatado = {
                'id': livro[0],
                'titulo': livro[1],
                'categoria': livro[2],
                'autor': livro[3],
                'imagem_url': livro[4]
            }

            livros_formatados.append(livro_formatado)
            

        return jsonify(livros_formatados)
    

@app.route('/livros/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    with sqlite3.connect('database.db') as conn:
        conexao_cursor = conn.cursor()
        conexao_cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
        conn.commit() 

    if conexao_cursor.rowcount == 0:
        return jsonify({'erro': 'Livro não encontrado'}), 400
    
    return jsonify({'mensagem': 'Livro deletado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)


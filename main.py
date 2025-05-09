from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '896364'

livros = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', livros=livros)

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        codigo = len(livros)
        livro = {
            'codigo': codigo,
            'titulo': titulo,
            'autor': autor,
            'ano': ano,
            'emprestado': False,
            'devolver': '--/--/----',
            'multa': 0
        }
        livros.append(livro)
        flash(f'Livro {titulo} adicionado com sucesso!')
        return redirect('/catalogo')
    return render_template('adicionar_livro.html')

@app.route('/editar_livro/<int:codigo>', methods=['GET', 'POST'])
def editar_livro(codigo):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        livros[codigo].update({
            'titulo': titulo,
            'autor': autor,
            'ano': ano
        })
        flash(f'Livro {titulo} atualizado!')
        return redirect('/catalogo')
    return render_template('editar_livro.html', livro=livros[codigo])

@app.route('/emprestar/<int:codigo>')
def emprestar(codigo):
    livro = livros[codigo]
    livro['emprestado'] = True
    livro['devolver'] = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
    livro['multa'] = 0
    flash(f'Livro "{livro["titulo"]}" emprestado! Devolver até: {livro["devolver"]}')
    return redirect('/catalogo')

@app.route('/devolver/<int:codigo>')
def devolver(codigo):
    livro = livros[codigo]
    data_prevista = datetime.strptime(livro['devolver'], "%d/%m/%Y")
    atraso = (datetime.now() - data_prevista).days
    if atraso > 0:
        multa = 10 + (10 * 0.01 * atraso)
        livro['multa'] = multa
        flash(f'Atraso de {atraso} dias. Multa: R${multa:.2f}')
    else:
        livro['multa'] = 0
        flash('Livro devolvido no prazo!')
    livro['emprestado'] = False
    livro['devolver'] = '--/--/----'
    return redirect('/catalogo')

@app.route('/apagar_livro/<int:codigo>')
def apagar_livro(codigo):
    livros.pop(codigo)

    for idx, livro in enumerate(livros):
        livro['codigo'] = idx
    flash('Livro removido!')
    return redirect('/catalogo')

if __name__ == '__main__':
    app.run(debug=True)

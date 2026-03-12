from flask import Flask, render_template, request, redirect, url_for
from models import db, Mito, Region, Tipo
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not Region.query.first():
        db.session.add_all([Region(nombre=r) for r in ['Noroeste','Noreste','Centro','Cuyo','Patagonia']])
    if not Tipo.query.first():
        db.session.add_all([Tipo(nombre=t) for t in ['Leyenda popular','Mito urbano','Ser mitológico','Relato tradicional']])
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html', regiones=Region.query.all(), tipos=Tipo.query.all())

@app.route('/add', methods=['POST'])
def add_mito():
    m = Mito(nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            region_id=request.form['region'],
            tipo_id=request.form['tipo'],
            imagen=request.form['imagen'])
    db.session.add(m)
    db.session.commit()
    return redirect(url_for('list_mitos'))

@app.route('/mitos')
def list_mitos():
    return render_template('list.html', mitos=Mito.query.all())

@app.route('/edit/<int:id>')
def edit_mito(id):
    return render_template('edit.html', mito=Mito.query.get_or_404(id),
                           regiones=Region.query.all(), tipos=Tipo.query.all())

@app.route('/update/<int:id>', methods=['POST'])
def update_mito(id):
    m = Mito.query.get_or_404(id)
    m.nombre = request.form['nombre']
    m.descripcion = request.form['descripcion']
    m.region_id = request.form['region']
    m.tipo_id = request.form['tipo']
    m.imagen = request.form['imagen']
    db.session.commit()
    return redirect(url_for('list_mitos'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_mito(id):
    db.session.delete(Mito.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('list_mitos'))

if __name__ == '__main__':
    app.run(debug=True)
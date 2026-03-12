from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

class Mito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)
    imagen = db.Column(db.String(255), nullable=True)

    region = db.relationship('Region', backref='mitos')
    tipo   = db.relationship('Tipo', backref='mitos')

    def recorte_descripcion(self, max_chars=100):
        return self.descripcion if len(self.descripcion) <= max_chars else self.descripcion[:max_chars] + '...'
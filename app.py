# Import Library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy.orm import query
from werkzeug.wrappers import response

# Inisiasi object flask
app = Flask(__name__)

# Inisiasi object flask-restful
api = Api(app)

# Inisiasi object flask-cors
CORS(app)

# Konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inisiasi object flask-sqlalchemy
db = SQLAlchemy(app)

# Membuat Database model
class ModelDatabase(db.Model):
    # Membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    jenis = db.Column(db.String(10))
    alamat = db.Column(db.TEXT)
    kota = db.Column(db.String(40))
    foto = db.Column(db.String(1000))

    # Method untuk menyimpan data
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# Create database
db.create_all()

# Inisiasi variabel kosong bertype dictionary
kost = {}

class KosanResource(Resource):
    def get(self):
        # Menampilkan database
        query = ModelDatabase.query.all()
        # Melakukan iterasi pada model database
        output = [
            {
                "nama":data.nama,
                "jenis":data.jenis,
                "alamat":data.alamat,
                "kota":data.kota,
                "foto":data.foto
            }
            for data in query
        ]
        response = {
            # "code" : 200,
            # "msg" : "Query data sukses",
            "data" : output
        }

        return response, 200

    def post(self):
        dataNama = request.form["nama"]
        dataJenis = request.form["jenis"]
        dataAlamat =request.form["alamat"]
        dataKota = request.form["kota"]
        dataFoto = request.form["foto"]

        # Masukan data kedalam database model
        model = ModelDatabase(nama=dataNama, jenis=dataJenis, alamat=dataAlamat, kota=dataKota, foto=dataFoto)
        model.save()

        response = {"msg" : "Data berhasil dimasukan", "code" : 200}
        return response, 200

# Setup resource nya
api.add_resource(KosanResource, "/datakost", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=False, port=5000)
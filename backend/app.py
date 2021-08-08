#Python3 Frameworks
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

#DataBase config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Model
class database_model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    rol = db.Column(db.String(20))
    dni = db.Column(db.Integer)

    def __init__(self, name, surname, rol, dni):
        self.name = name
        self.surname = surname
        self.rol = rol
        self.dni = dni

#Create
db.create_all()

#Schema
class database_schema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'surname', 'rol', 'dni')


databaseSchema = database_schema()
databaseSchemas = database_schema(many=True)

#Routes
@app.route('/staff', methods=['POST'])
def new_employee():
    print(request.json)
    name = request.json['name']
    surname = request.json['surname']
    rol = request.json['rol']
    dni = request.json['dni']
    newEmployee = database_model(name,surname,rol,dni)
    db.session.add(newEmployee)
    db.session.commit()
    return databaseSchema.jsonify(newEmployee)

@app.route('/staff', methods=['GET'])
def get_staff():
        all_staff = database_model.query.all()
        databaseSchemas.dump(all_staff)
        return databaseSchemas.jsonify(all_staff)

@app.route('/staff/<id>', methods=['GET'])
def get_employee(id):
    employe = database_model.query.get(id)
    return databaseSchema.jsonify(employe)

@app.route('/staff/<id>', methods=['PUT'])
def edit_employee(id):
    employee = database_model.query.get(id)
    name = request.json['name']
    surname= request.json['surname']
    rol = request.json['rol']
    dni = request.json['dni']
    employee.name = name
    employee.surname = surname
    employee.rol = rol
    employee.dni = dni
    db.session.commit()
    return databaseSchema.jsonify(employee)


@app.route('/staff/<id>', methods=['POST'])
def detele_employee(id):
    employee = database_model.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return databaseSchema.jsonify(employee)

@app.route('/staff/employee', methods=['POST'])
def delete_all():
    all = database_model.query.all()
    databaseSchemas.dump(all)
    for id in all:
        db.session.delete(id)
    db.session.commit()       
    return databaseSchemas.jsonify(all)


if __name__ == '__main__':
    app.run(debug=True)




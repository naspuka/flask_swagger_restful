from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)



# Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')


model = api.model('demo', {
    'name': fields.String('Enter Name'),
    'email': fields.String('Enter Email'),
    'password': fields.String('Enter Password'),
    })


user_schema = UserSchema()
users_schema = UserSchema(many=True)





@api.route('/get')
class getdata(Resource):
    def get(self):
        data = User.query.all()
        return jsonify(users_schema.dump(data))

@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        user = User(name=request.json['name'], email=request.json['email'], password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return {'message':'working'}

@api.route('/update/<int:id>')
class updatedata(Resource):
    @api.expect(model)
    def put(self, id):
        user = User.query.get(id)
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        return {'message':'Data updated successfully'}

@api.route('/delete/<int:id>')
class getdata(Resource):
    def delete(self, id):
        user = User.query(id)
        db.session.delete(user)
        db.session.commit()
        return {'message':'Data deleted successfully '}

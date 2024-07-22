from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class MovieModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Movie(title = {self.title}, director = {self.director}, year = {self.year})"

movie_put_args = reqparse.RequestParser()
movie_put_args.add_argument("title", type=str, help="Title of the movie is required", required=True)
movie_put_args.add_argument("director", type=str, help="Director of the movie is required", required=True)
movie_put_args.add_argument("year", type=int, help="Year of the movie is required", required=True)

movie_update_args = reqparse.RequestParser()
movie_update_args.add_argument("title", type=str)
movie_update_args.add_argument("director", type=str)
movie_update_args.add_argument("year", type=int)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'director': fields.String,
    'year': fields.Integer
}

class Movie(Resource):
    @marshal_with(resource_fields)
    def get(self, movie_id):
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            abort(404, message="Could not find movie with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, movie_id):
        args = movie_put_args.parse_args()
        result = MovieModel.query.filter_by(id=movie_id).first()
        if result:
            abort(409, message="Movie id taken...")
        movie = MovieModel(id=movie_id, title=args['title'], director=args['director'], year=args['year'])
        db.session.add(movie)
        db.session.commit()
        return movie, 201

    @marshal_with(resource_fields)
    def patch(self, movie_id):
        args = movie_update_args.parse_args()
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            abort(404, message="Movie doesn't exist, cannot update")
        
        if args['title']:
            result.title = args['title']
        if args['director']:
            result.director = args['director']
        if args['year']:
            result.year = args['year']
        
        db.session.commit()
        return result

    def delete(self, movie_id):
        result = MovieModel.query.filter_by(id=movie_id).first()
        if not result:
            abort(404, message="Could not find movie with that id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

class MovieList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        results = MovieModel.query.all()
        return results

api.add_resource(Movie, '/movie/<int:movie_id>')
api.add_resource(MovieList, '/movies')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
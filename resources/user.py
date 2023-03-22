from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from schemas.user_schema import UserSchema
from models import UserModel
from db import db
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201,
                  description="Creating user.")
    @blp.alt_response(422, description="Occurs when login or password doesn't match required pattern.")
    def post(self, user_data):
        user = UserModel(username=user_data["username"],
                         password=pbkdf2_sha256.hash(user_data["password"]))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="An user with that username already exists.")
        return {"message": "User created successfully."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = db.get_or_404(UserModel, user_id)
        return user

    @jwt_required(fresh=True)
    @blp.response(200)
    def delete(self, user_id):
        user = db.get_or_404(UserModel, user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.sadd("revoked tokens", jti)
        return {"message": "Logged out."}

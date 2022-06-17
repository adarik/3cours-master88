from flask import request, abort
from flask_restx import Namespace, Resource

from project.exceptions import ItemNotFound, UserAlreadyHave
from project.implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthsRegisterView(Resource):
    """
    Класс CBV для представления /auth/register.
    """

    @auth_ns.response(201, "User created")
    @auth_ns.response(409, "User already registered")
    def post(self):
        """
        Метод производит запись данных о пользователе в базу данных. Пароль записывается в виде хеша.
        """
        req_json = request.json
        try:
            auth_service.register_new_user(req_json)
        except UserAlreadyHave:
            abort(409, "User already registered")
        return "User created", 201


@auth_ns.route('/login')
class AuthLoginView(Resource):
    """
    CBV для представления /auth/login
    """

    @auth_ns.response(201, 'Tokens created')
    @auth_ns.response(401, "No data")
    def post(self):
        """
        Метод реализует генерацию пары access и refresh токенов для дальнейшей авторизации пользователя.
        """
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')

        if None in [email, password]:
            abort(401, "No data. Try again")

        tokens = auth_service.generate_token(email, password)

        return tokens, 201

    @auth_ns.response(201, 'OK')
    @auth_ns.response(401, 'No refresh token data')
    @auth_ns.response(404, 'User not found')
    def put(self):
        """
        Метод реализует выдачу новой пары access и refresh токенов на основании имеющегося
        у пользователя refresh токена.
        """
        req_json = request.json
        refresh_token = req_json.get("refresh_token")

        if refresh_token is None:
            abort(401, "No refresh token data")

        try:
            tokens = auth_service.approve_refresh_token(refresh_token)
            return tokens, 201
        except ItemNotFound:
            abort(404, "User not found")

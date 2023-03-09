from rest_framework.response import Response

from rest_framework.views import APIView
from base.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
import jwt, datetime
from base.serializers import UserSerilaizer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            "id": user.id,
            "is_staff":user.is_staff,
            "is_driver":user.is_driver,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.get(id=payload['id'])
        serilaizer = UserSerilaizer(user)
        return Response(serilaizer.data) 


class UsersView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        if not payload['is_staff']:
            raise AuthenticationFailed('Unauthorized!')

        users = User.objects.all()
        serializer = UserSerilaizer(users, many=True)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    def put(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        data = request.data
        user = User.objects.get(id=payload['id'])
        user.name = data['name']
        user.email = data['email']
        if payload['is_driver']:
            user.license_no = data['license_no']
            user.vechile_no = data['vechile_no']
        # user.is_driver = data['is_driver']
        # user.is_staff = data['is_staff']
        # user.is_superuser = data['is_staff']
        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()
        serializer = UserSerilaizer(user, many=False)
        return Response(serializer.data)


class UpdateUserView(APIView):
    def put(self, request, pk):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        if not payload['is_staff']:
            raise AuthenticationFailed('Unauthorized!')

        data = request.data
        user = User.objects.get(id=pk)
        user.name = data['name']
        user.email = data['email']
        # user.license_no = data['license_no']
        # user.vechile_no = data['vechile_no']
        user.is_driver = data['is_driver']
        user.is_staff = data['is_staff']
        user.is_superuser = data['is_staff']
        
        user.save()
        serializer = UserSerilaizer(user, many=False)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class DeleteUserView(APIView):
    def delete(self, request, pk):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        if not payload['is_staff']:
            raise AuthenticationFailed('Unauthorized!')
            
        user = User.objects.get(id=pk)
        user.delete()
        return Response('User Deleted')
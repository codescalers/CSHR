from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from server.cshr.api.permission import IsAdmin, IsUser

from server.cshr.api.response import CustomResponse
from server.cshr.models import User
from server.cshr.serializers.users import GeneralUserSerializer
from server.cshr.services.users import get_user_by_id, get_users_filter




class GeneralUserAPIView (ViewSet, GenericAPIView):
    permission_classes = [IsUser]
    serializer_class = GeneralUserSerializer
    def get_all(self, request: Request) -> Response:
        try:
            users = User.objects.all()
            """if there are no instances """
        except User.DoesNotExist:
            return CustomResponse.not_found(message="There are no users found", status_code=404)

        serializer =GeneralUserSerializer(users, many=True)
        return CustomResponse.success(
            data=serializer.data, message="show all users", status_code=200
        )

    def get_one(self, request: Request, id: str) -> Response:
        '''To get a user by id'''
        user = get_user_by_id(id)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200
            )
        return CustomResponse.not_found(
            message="User not found",
            status_code=404
        )
# class UserAPIView_SuperVisor():
# class UserAPIView_Self():

# class UserAPIView_Admin(ViewSet, GenericAPIView):
#     """
#     * Usage
#     Class UserAPIView has all the functionality based of the User
#     Methods [GET, PUT, DELETE]
#     """
#     permission_classes =[IsAdmin]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def get_all(self, request: Request) -> Response:
#         try:
#             users = User.objects.all()
#             """if there are no instances """
#         except User.DoesNotExist:
#             return CustomResponse.not_found(message="There are no users found", status_code=404)

#         serializer =UserSerializer(users, many=True)
#         return CustomResponse.success(
#             data=serializer.data, message="show all users", status_code=200
#         )

#     def get_one(self, request: Request, id: str) -> Response:
#         '''To get a user by id'''
#         user = get_user_by_id(id)
#         if user is not None:
#             return CustomResponse.success(
#                 data=self.get_serializer(user).data,
#                 message="User found",
#                 status_code=200
#             )
#         return CustomResponse.not_found(
#             message="User not found",
#             status_code=404
#         )

#     def patch(self, request: Request, id: str, format=None) -> Response:
#         '''To update a user'''
#         user = get_user_by_id(id)
#         serializer = self.get_serializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return CustomResponse.success(
#                 data=serializer.data,
#                 status_code=200,
#                 message="User updated")
#         return CustomResponse.bad_request(
#             data=serializer.errors,
#             status_code=400,
#             message="User not updated")
#     def put(self, request: Request, id: str, format=None) -> Response:
#         '''To update a user'''
#         user = get_user_by_id(id)
#         serializer = self.get_serializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return CustomResponse.success(
#                 data=serializer.data,
#                 status_code=200,
#                 message="User updated")
#         return CustomResponse.bad_request(
#             data=serializer.errors,
#             status_code=400,
#             message="User not updated")

#     def delete(self, request: Request, id, format=None):
#         ''' To delete a user'''
#         user = get_user_by_id(id)
#         if user is not None:
#             user.delete()
#             return CustomResponse.deleted(
#                 status_code=204,
#                 message="User deleted")
#         return CustomResponse.not_found(
#             status_code=404,
#             message="User not found")
 

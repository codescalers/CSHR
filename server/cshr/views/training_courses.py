from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..serializers.training_courses import TrainingCoursesSerializer
from ..api.response import CustomResponse

from server.cshr.models.users import User
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.services.users import get_user_by_id
from server.cshr.services.training_courses import (
    get_all_training_courses,
    get_training_courses_by_id,
)



class TrainingCoursesApiView(ViewSet, GenericAPIView):

    """method to get all Training courses"""

    serializer_class = TrainingCoursesSerializer

    permission_class = UserIsAuthenticated

    def get_all(self, request: Request) -> Response:
        training_courses = get_all_training_courses()
        serializer = TrainingCoursesSerializer(training_courses, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Training courses found", status_code=200
        )

    """method to get a single Training course by id"""

    def get(self, request: Request, id: str, format=None) -> Response:
        training_course = get_training_courses_by_id(id=id)
        if training_course is None:
            return CustomResponse.not_found(
                message="Training courses not found", status_code=404
            )

        serializer = TrainingCoursesSerializer(training_course)
        return CustomResponse.success(
            data=serializer.data, message="Training courses found", status_code=200
        )

    """method to update a Training course by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        training_course = get_training_courses_by_id(id=id)
        if training_course is None:
            return CustomResponse.not_found(
                message="Training courses not found", status_code=404
            )
        serializer = self.get_serializer(
            training_course, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                status_code=200,
                message="Training courses updated",
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Training courses failed to update"
        )

    def delete(self, request: Request, id: str, format=None) -> Response:
        """method to delete a Training course by id"""
        training_course = get_training_courses_by_id(id=id)
        if training_course is None:
            return CustomResponse.not_found(
                message="Training courses not found", status_code=404
            )
        training_course.delete()

        return CustomResponse.success(
            message="Training course deleted", status_code=204
        )

    """method to create a new Training course"""

    def post(self, request: Request) -> Response:

        """Method to create a Training course"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            current_user: User = get_user_by_id(request.user.id)
            serializer.save(user=current_user)

            return CustomResponse.success(
                data=serializer.data,
                message="Training course created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Training course creation failed"
        )

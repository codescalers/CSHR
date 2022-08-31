from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.training_courses import TrauningCourses
from rest_framework.viewsets import ViewSet
from ..serializers.training_courses import TrainingCoursesSerializer
from ..api.response import CustomResponse


class TrainingCoursesAPIView(ViewSet, GenericAPIView):
    """method to get all Training courses"""

    serializer_class = TrainingCoursesSerializer

    def get_all(self, request: Request) -> Response:
        try:
            trainingcourses = TrauningCourses.objects.all()
            """if there are no instances """
        except TrauningCourses.DoesNotExist:
            return CustomResponse.not_found(
                message="Training courses not found", status_code=404
            )

        serializer = self.get_serializer(trainingcourses, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Training courses found", status_code=200
        )

    """method to get a single Training course by id"""

    def get_one(self, request: Request, id: str, format=None) -> Response:
        try:
            trainingcourses = TrauningCourses.objects.get(id=id)
        except TrauningCourses.DoesNotExist:
            return CustomResponse.not_found()

        serializer = self.get_serializer(trainingcourses)
        if trainingcourses is not None:
            return CustomResponse.success(
                data=serializer.data, message="Training courses found", status_code=200
            )
        return CustomResponse.not_found(
            message="Training courses not found", status_code=404
        )

    """method to update a Training course by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        try:
            trainingcourses = TrauningCourses.objects.get(id=id)
        except TrauningCourses.DoesNotExist:
            return CustomResponse.not_found(message="Training course not found")
        serializer = self.get_serializer(trainingcourses, data=request.data)
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

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete a Training course by id"""
        try:
            trainingcourses = TrauningCourses.objects.get(id=id)
        except TrauningCourses.DoesNotExist:
            return CustomResponse.not_found(message="Training course not found")
        if trainingcourses is not None:
            trainingcourses.delete()
            return CustomResponse.deleted(message="User deleted")
        return CustomResponse.not_found(message="Training course not found to update")

    """method to create a new Training course"""

    def post(self, request: Request) -> Response:
        """Method to create a new hr letter"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            serializer.save(user=self.request.user)
            return CustomResponse.success(
                data=serializer.data,
                message="Training course created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Training course creation failed"
        )

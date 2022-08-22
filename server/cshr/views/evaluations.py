from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.evaluations import Evaluations
from rest_framework.viewsets import ViewSet
from ..serializers.evaluations import  EvaluationsSerializer
from ..api.response import CustomResponse


class EvaluationAPIView(ViewSet, GenericAPIView):
    """method to get all Evaluations"""

    def get_all(self, request: Request) -> Response:
        try:
            evaluations = Evaluations.objects.all()
            """if there are no instances """
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found(message="Evaluations not found", status_code=404)

        serializer = EvaluationsSerializer(evaluations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="Evaluations found", status_code=200
        )

    """method to get a single Evaluations by id"""

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found()

        serializer = EvaluationsSerializer(evaluation)
        if evaluation is not None:
            return CustomResponse.success(
                data=serializer.data, message="Evaluation found", status_code=200
            )
        return CustomResponse.not_found(message="Evaluations not found", status_code=404)

    """method to update an evaluation by id"""

    def put(self, request: Request, id: str, format=None) -> Response:

        try:
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found(message="Evaluations not found")
        serializer = self.get_serializer(evaluation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="Evaluations updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Evaluations failed to update"
        )

    def delete(self, request: Request, id, format=None) -> Response:
        """method to delete an evaluation by id"""
        try:
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found(message="Evaluations not found")
        if evaluation is not None:
            evaluation.delete()
            return CustomResponse.success(message="evaluation deleted", status_code=204)
        return CustomResponse.not_found(message="Evaluations not found to update")

    """method to create a new evaluation"""

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Evaluations created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Evaluations creation failed"
        )

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.evaluations import Evaluations
from rest_framework.viewsets import ViewSet
from ..serializers.evaluation import EvaluationSerializer
from ..api.response import CustomResponse


class EvaluationsAPIView(ViewSet, GenericAPIView):
    serializer_class = EvaluationSerializer
    queryset = Evaluations.objects.all()

    def get_all(self, request: Request) -> Response:
        evaluations = self.get_queryset()
        serializer = EvaluationSerializer(evaluations, many=True)
        if len(evaluations) != 0:
            return CustomResponse.success(
                data=serializer.data, message="evaluations found", status_code=200
            )
        return CustomResponse.not_found(message="Evaluations not found", status_code=404)

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found(message="Evaluations not found", status_code=404)
        serializer = EvaluationSerializer(evaluation)
 
        return CustomResponse.success(
                data=serializer.data, message="evaluation found", status_code=200
            )
        

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an evaluation"""
        try:
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
             return CustomResponse.not_found(
                data=serializer.errors, message="Evaluation not found to update"
        )
        serializer = self.get_serializer(evaluation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=200, message="Evaluation updated"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Evaluation failed to update"
        )
       
    def delete(self, request: Request, id, format=None) -> Response:
        """To delete an evaluation"""
        try:       
            evaluation = Evaluations.objects.get(id=id)
        except Evaluations.DoesNotExist:
            return CustomResponse.not_found(message="Evaluation not found to update")
        return CustomResponse.success(message="Evaluation deleted",status_code=204)
        

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Evaluation created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Evaluation creation failed"
        )
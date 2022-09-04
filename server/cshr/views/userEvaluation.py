from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from server.cshr.serializers.userEvaluation import UserEvaluationSerializer
from server.cshr.api.response import CustomResponse
from server.cshr.api.permission import (
    IsAdmin,
    IsSupervisor,
    UserIsAuthenticated,
    CustomPermissions,
)
from server.cshr.services.evaluation import get_evaluation_by_id, all_evaluations


class EvaluationsAPIView(ViewSet, GenericAPIView):
    serializer_class = UserEvaluationSerializer
    permission_classes = [UserIsAuthenticated | IsAdmin | IsSupervisor]

    def get_all(self, request: Request) -> Response:
        has_permission = CustomPermissions.admin_or_supervisor(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluations = all_evaluations()
        serializer = UserEvaluationSerializer(evaluations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="evaluations found", status_code=200
        )

    def get(self, request: Request, id: str, format=None) -> Response:

        evaluation = get_evaluation_by_id(id)

        if evaluation is not None:
            has_permission = CustomPermissions.admin_or_supervisor(request.user)
            if not has_permission and request.user.id != evaluation.user_id:
                return CustomResponse.unauthorized()
            serializer = UserEvaluationSerializer(evaluation)
            return CustomResponse.success(
                data=serializer.data, message="evaluation found", status_code=200
            )
        return CustomResponse.not_found(
            message="Evaluations not found", status_code=404
        )

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an evaluation"""
        has_permission = CustomPermissions.admin_or_supervisor(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_evaluation_by_id(id)
        if evaluation is not None:
            serializer = UserEvaluationSerializer(evaluation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data,
                    status_code=202,
                    message="Evaluation updated",
                )
            return CustomResponse.bad_request(message="Evaluation failed to update")
        return CustomResponse.not_found(message="Evaluation not found to update")

    def post(self, request: Request) -> Response:
        """To post new evaluation"""
        has_permission = CustomPermissions.admin_or_supervisor(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
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

    def delete(self, request: Request, id, format=None) -> Response:
        """to delete evaluation by admin"""

        has_permission = CustomPermissions.admin(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_evaluation_by_id(id)
        if evaluation is not None:
            evaluation.delete()
            return CustomResponse.success(message="Evaluation deleted", status_code=204)
        return CustomResponse.not_found(message="Evaluation not found to update")

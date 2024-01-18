from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.users import User
from server.cshr.serializers.evaluation import (
    UserEvaluationSerializer,
    EvaluationSerializer,
)
from server.cshr.api.response import CustomResponse
from server.cshr.api.permission import (
    IsAdmin,
    IsTeamLead,
    UserIsAuthenticated,
    CustomPermissions,
)
from server.cshr.services.evaluation import (
    filter_all_evaluations_based_on_user_and_year,
    get_evaluation_by_id,
    get_user_evaluation_by_id,
    all_user_evaluations,
)
from server.cshr.services.users import get_user_by_id


class BaseUserEvaluationsAPIView(ListAPIView, GenericAPIView):
    serializer_class = UserEvaluationSerializer
    permission_classes = [UserIsAuthenticated | IsAdmin | IsTeamLead]

    def get(self, request: Request) -> Response:
        has_permission = CustomPermissions.admin_or_team_lead(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluations = all_user_evaluations()
        serializer = UserEvaluationSerializer(evaluations, many=True)
        return CustomResponse.success(
            data=serializer.data, message="user evaluations found", status_code=200
        )

    def post(self, request: Request) -> Response:
        """To post new user evaluation"""
        has_permission = CustomPermissions.admin_or_team_lead(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="user evaluation created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="user evaluation creation failed"
        )


class UserEvaluationsAPIView(ListAPIView, GenericAPIView):
    serializer_class = UserEvaluationSerializer
    permission_classes = [UserIsAuthenticated | IsAdmin | IsTeamLead]

    def delete(self, request: Request, id, format=None) -> Response:
        """to delete user evaluation by admin"""

        has_permission = CustomPermissions.admin(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_user_evaluation_by_id(id)
        if evaluation is not None:
            evaluation.delete()
            return CustomResponse.success(
                message="user evaluation deleted", status_code=204
            )
        return CustomResponse.not_found(message="user evaluation not found")

    def get(self, request: Request, id: str, format=None) -> Response:
        """Use this endpoint to retrieve user evaluations"""
        year: str = request.query_params.get("year")

        if not year or not year.isdigit():
            return CustomResponse.bad_request(message="Make sure the year is a number.")
        if not id.isdigit():
            return CustomResponse.bad_request(message="Invalid id")

        user: User = get_user_by_id(int(id))
        if user is None:
            return CustomResponse.not_found(message="User not found")

        evaluations = filter_all_evaluations_based_on_user_and_year(user, year)
        serializer = UserEvaluationSerializer(evaluations, many=True)
        has_permission = CustomPermissions.admin_or_team_lead(request.user)

        if not has_permission and request.user.id != user.id:
            return CustomResponse.unauthorized()

        return CustomResponse.success(
            data=serializer.data, message="user evaluation found", status_code=200
        )

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an user evaluation"""
        has_permission = CustomPermissions.admin_or_team_lead(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_user_evaluation_by_id(id)
        if evaluation is not None:
            serializer = UserEvaluationSerializer(evaluation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data,
                    status_code=202,
                    message="user evaluation updated",
                )
            return CustomResponse.bad_request(
                message="user evaluation failed to update"
            )
        return CustomResponse.not_found(message="user evaluation not found to update")


class BaseEvaluationsAPIView(ListAPIView, GenericAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [UserIsAuthenticated | IsAdmin | IsTeamLead]

    def get_queryset(self) -> Response:
        query_set = all_user_evaluations()
        return query_set

    def post(self, request: Request) -> Response:
        """To post new evaluation"""
        has_permission = CustomPermissions.admin_or_team_lead(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="evaluation created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="evaluation creation failed"
        )


class EvaluationsAPIView(ListAPIView, GenericAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = [UserIsAuthenticated | IsAdmin | IsTeamLead]

    def delete(self, request: Request, id, format=None) -> Response:
        """to delete evaluation by admin"""

        has_permission = CustomPermissions.admin(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_evaluation_by_id(id)
        if evaluation is not None:
            evaluation.delete()
            return CustomResponse.success(message="evaluation deleted", status_code=204)
        return CustomResponse.not_found(message="evaluation not found")

    def get(self, request: Request, id: str, format=None) -> Response:
        evaluation = get_evaluation_by_id(id)
        if evaluation is not None:
            serializer = EvaluationSerializer(evaluation)
            return CustomResponse.success(
                data=serializer.data, message="evaluation found", status_code=200
            )
        return CustomResponse.not_found(message="evaluation not found", status_code=404)

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update an evaluation"""
        has_permission = CustomPermissions.admin_or_team_lead(request.user)
        if not has_permission:
            return CustomResponse.unauthorized()
        evaluation = get_evaluation_by_id(id)
        if evaluation is not None:
            serializer = EvaluationSerializer(evaluation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    data=serializer.data,
                    status_code=202,
                    message="evaluation updated",
                )
            return CustomResponse.bad_request(message="evaluation failed to update")
        return CustomResponse.not_found(message="evaluation not found to update")

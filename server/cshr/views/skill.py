from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.cshr.models.skills import Skills
from rest_framework.viewsets import ViewSet
from ..serializers.skill import SkillSerializer
from ..api.response import CustomResponse


class SkillsAPIView(ViewSet, GenericAPIView):
    serializer_class = SkillSerializer
    queryset = Skills.objects.all()

    def get_all(self, request: Request) -> Response:
        skills = self.get_queryset()
        serializer = SkillSerializer(skills, many=True)
        if len(skills) != 0:
            return CustomResponse.success(
                data=serializer.data, message="skills found", status_code=200
            )
        return CustomResponse.not_found(message="Skills not found", status_code=404)

    def get(self, request: Request, id: str, format=None) -> Response:
        try:
            skill = Skills.objects.get(id=id)
        except Skills.DoesNotExist:
            return CustomResponse.not_found(message="Skills not found", status_code=404)
        serializer = SkillSerializer(skill)

        return CustomResponse.success(
            data=serializer.data, message="skill found", status_code=200
        )

    def put(self, request: Request, id: str, format=None) -> Response:
        """To update a skill"""
        try:
            skill = Skills.objects.get(id=id)
        except Skills.DoesNotExist:
            return CustomResponse.not_found(message="Skill not found to update")
        serializer = SkillSerializer(skill, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data, status_code=202, message="Skill updated"
            )
        return CustomResponse.bad_request(message="Skill failed to update")

    def delete(self, request: Request, id, format=None) -> Response:
        """To delete a skill"""
        try:
            skill = Skills.objects.get(id=id)
        except Skills.DoesNotExist:
            return CustomResponse.not_found(message="Skill not found to update")
        skill.delete()
        return CustomResponse.success(message="Skill deleted", status_code=204)

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Skill created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="Skill creation failed"
        )

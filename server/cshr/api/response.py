from typing import Any, List, Optional, Union
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)


class CustomResponse:
    """Custom response method"""

    @staticmethod
    def success(
        data: Union[List[Any], None] = None,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> Response:
        """success response method"""
        """ include GET, and PUT request"""

        if not message:
            message = "Success"
        if not status_code:
            status_code = HTTP_200_OK

        return Response(
            {
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def created(
        data: Union[List[Any], None] = None,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> Response:
        """created response method for POST request"""
        if not message:
            message = "Created successfully"
        if not status_code:
            status_code = HTTP_201_CREATED

        return Response(
            {
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def deleted(
        message: Optional[str] = None,
        status_code: Optional[int] = HTTP_204_NO_CONTENT
    ) -> Response:
        """success response method"""
        """ include GET, UPDATE"""

        if not message:
            message = "Deleted successfully"

        return Response(message=message, status=status_code)

    @staticmethod
    def not_found(
        message: Optional[str] = None, status_code: int = HTTP_404_NOT_FOUND
    ) -> Response:
        """not found response method"""

        if not message:
            message = "Not found"

        return Response(message=message, status=status_code)

    @staticmethod
    def bad_request(
        message: Optional[str] = None,
        error: Union[List[Any], None] = None,
        data: Union[List[Any], None] = None,
        status_code: int = HTTP_400_BAD_REQUEST,
    ) -> Response:
        """bad request response method"""
        if not message:
            message = "Make sure you entered a valid data."
        return Response(
            {
                "data": data,
                "message": message,
                "error": error,
            },
            status=status_code,
        )

    @staticmethod
    def unauthorized(
        message: Optional[str] = None, status_code: int = HTTP_401_UNAUTHORIZED
    ) -> Response:
        """unauthorized response method"""
        if not message:
            message = "You are not authorized to access this resource."

        return Response(message=message, status=status_code)

from rest_framework.generics import GenericAPIView
from server.cshr.api.permission import UserIsAuthenticated
from server.cshr.serializers.landing_page import LandingPageSerializer
from server.cshr.api.response import CustomResponse


class LandingPageApiView(GenericAPIView):
    permission_classes=(UserIsAuthenticated,)
    serializer_class=LandingPageSerializer
    
    def get(self,request):
       month=request.query_params.get("month") 
       year=request.query_params.get("year") 
       print(month,year)
       serializer=LandingPageSerializer(context={"month":month,"year":year})
       return CustomResponse.success(data=serializer.data)
    
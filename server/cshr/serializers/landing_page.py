
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from server.cshr.models.event import Event
from server.cshr.models.meetings import Meetings

class LandingPageSerializer(ModelSerializer):
 
   vacations=SerializerMethodField()
   meetings=SerializerMethodField()
   events=SerializerMethodField()
   birthdays=SerializerMethodField()

   class Meta: 
    model=Event
    fields=["vacations","meetings","events","birthdays"]
    
   def get_vacations(self,obj):
     print("ssssssssssss")
     month= self.context.get("month")
     year=self.context.get("year")
     print(month)
     print(year)     
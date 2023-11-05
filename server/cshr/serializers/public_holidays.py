from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.cshr.models.vacations import PublicHoliday
from server.cshr.serializers.office import OfficeSerializer


class PublicHolidaySerializer(ModelSerializer):
    """
    This class will be used to get all info about Public Holidays
    """
    location = SerializerMethodField()

    class Meta:
        model = PublicHoliday
        fields = ["id", "location", "holiday_date", "expired"]
        
    def get_location(self, obj: PublicHoliday):
      return OfficeSerializer(obj.location).data

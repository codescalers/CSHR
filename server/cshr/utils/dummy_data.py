from server.cshr.models.office import WEEKEND_DAYS, Office


locations = [
  {
    "name": "Belgium",
    "country": "Belgium",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "Egypt",
    "country": "Egypt",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
  {
    "name": "India",
    "country": "India",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "Mauritius",
    "country": "Mauritius",
    "weekend": WEEKEND_DAYS.Saturday_and_Sunday
  },
  {
    "name": "UAE",
    "country": "UAE",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
  {
    "name": "Zanzi",
    "country": "Zanzi",
    "weekend": WEEKEND_DAYS.Friday_and_Saturday
  },
]

def create_locations():
  for location in locations:
    Office.objects.create(
      name=location.get("name"),
      country=location.get("country"),
      weekend=location.get("weekend")
    )
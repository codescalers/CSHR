from enum import Enum
import os
import django
import random
from django_seed import Seed
from cshr.models.users import User, Office, UserSkills
from cshr.models.vacations import Vacation

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshr.settings")
django.setup()

seeder = Seed.seeder()

class ThanosWorlds(Enum):
    LOCATIONS = "locations"
    VACATIONS = "vacations"
    USERS = "users"
    ALL = "all"

class ThanosFingers:
    def __init__(self):
        self.model = None
        self.number = 0

    def snap(self):
        if self.model is None:
            raise ValueError("Model not set. Use Thanos.worlds.use() to set the model.")
        
        thanos = Thanos(self.model, self.number)
        if self.model == ThanosWorlds.ALL.value:
            return thanos.create_all()
        else:
            return thanos.create_individual(self.model)

class Thanos:
    worlds = None
    fingers = ThanosFingers()

    def __init__(self, model: ThanosWorlds, number: int):
        self.model = model
        self.number = number

    @classmethod
    def use(cls, model: ThanosWorlds, number: int = 1000):
        cls.fingers.model = model
        cls.fingers.number = number

    def create_all(self):
        seeder.add_entity(Office, self.number)
        seeder.add_entity(User, self.number)
        seeder.add_entity(Vacation, self.number)
        seeder.execute()
        return self.cry("All the necessary seeds have been successfully created.")

    def create_individual(self, model: ThanosWorlds):
        if model == ThanosWorlds.LOCATIONS:
            seeder.add_entity(Office, self.number)
        elif model == ThanosWorlds.VACATIONS:
            seeder.add_entity(Vacation, self.number)
        elif model == ThanosWorlds.USERS:
            self.create_users()
        
        inserted_pks = seeder.execute()
        return self.cry(f"Seeded {self.number} {model.value}.")

    def create_users(self):
        locations_count = Office.objects.all().count()
        init_len = 50
        if locations_count < init_len:
            self.create_locations(init=init_len)
            return seeder.add_entity(User, init_len, {
                "location": lambda x: Office.objects.order_by('?').first(),
            })
        return seeder.add_entity(User, self.number, {
            "location": lambda x: Office.objects.order_by('?').first(),
        })

    def create_locations(self, init: int = None):
        if init:
            return seeder.add_entity(Office, init)
        return seeder.add_entity(Office, self.number)
        
    def cry(self, message: str):
        print(message)
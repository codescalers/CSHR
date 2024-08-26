import datetime
from enum import Enum
import os
import django
import random
from django_seed import Seed
from cshr.models.users import User, Office, UserSkills
from cshr.models.vacations import Vacation
from django.core.management.base import BaseCommand

from cshr.management.commands.thanos import Thanos, ThanosWorlds


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshr.settings")
django.setup()

seeder = Seed.seeder()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            nargs="+",
            type=ThanosWorlds,
            help="Should be `locations`, `vacations`, or `users`",
        )
        parser.add_argument(
            "--number", nargs="+", type=int, help="The number of seeds to be created, by default its 500."
        )

    def handle(self, *args, **options):
        """Use this command only in development mode."""
        model = options["model"]
        seeds_number = options["number"] or 500
        if type(seeds_number) == list:
            seeds_number = seeds_number[0]

        if type(model) == list:
            model = model[0]

        if not model:
            answer = input(
                "Are you sure you want to run seeds over the whole app? Y/N "
            )

            if answer.lower() == "n":
                return self.stdout.write(
                    self.style.ERROR(
                        "Aborted."
                    )
                )

            if answer.lower() != "y":
                return self.stdout.write(
                    self.style.ERROR(
                        "Wrong answer."
                    )
                )

            model = "all"

        Thanos.use(model, seeds_number)
        return Thanos.fingers.snap()


        # print("seeds_number", seeds_number)
        # print("model", model)
        # try:
        #     seeder.add_entity(


# 		Vacation,
# 		1,
# 		{
# 			"applying_user": User.objects.get(id=random_id(1)),
# 			"approval_user": User.objects.get(id=random_id(1)),
# 		},
# 	)
#     inserted_pks = seeder.execute()
#     self.stdout.write(
# 		self.style.SUCCESS("Successfully created 1000 vacations.")
# 	)
# except Exception:
#     self.stdout.write(
#         self.style.ERROR(
#         	"Failed to create vacation balances, check the records in the database if exist, or check if you migrated the database."
#         )
#     )


# Seed Users without setting the many-to-many fields
# seeder.add_entity(User, 50, {
#     "location": lambda x: Office.objects.order_by('?').first(),  # Random Office
# })


# # Manually create many-to-many relationships after seeding
# for user in User.objects.all():
#     # Handle reporting_to relationship
#     possible_reportings = User.objects.exclude(id=user.id)
#     if possible_reportings.exists():
#         user.reporting_to.set(random.sample(list(possible_reportings), k=random.randint(1, 5)))

#     # Handle skills relationship
#     possible_skills = UserSkills.objects.all()
#     if possible_skills.exists():
#         user.skills.set(random.sample(list(possible_skills), k=random.randint(1, 5)))
#

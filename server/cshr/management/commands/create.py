from django.core.management.base import BaseCommand
from cshr.utils.dummy_data import (
    create_locations,
    create_users,
    create_vacation_balance,
)
from components import config
from enum import Enum


class Option(Enum):
    locations = "locations"
    users = "users"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("options", nargs="+", type=Option)

    def handle(self, *args, **options):
        """Use this command only in development mode."""
        options = options["options"]
        for option in options:
            if option == Option.locations:
                try:
                    create_locations()
                    self.stdout.write(
                        self.style.SUCCESS("Successfully created locations.")
                    )
                except Exception:
                    self.stdout.write(
                        self.style.ERROR(
                            "Failed to create locations, check the records in the database if exist, or check if you migrated the database."
                        )
                    )
                try:
                    create_vacation_balance()
                    self.stdout.write(
                        self.style.SUCCESS("Successfully created vacation balances.")
                    )
                except Exception:
                    self.stdout.write(
                        self.style.ERROR(
                            "Failed to create vacation balances, check the records in the database if exist, or check if you migrated the database."
                        )
                    )
            elif option == Option.users:
                if config("DJANGO_DEBUG") == "ON":
                    # Create locations and dummey values to avoid errors after migrating the database, the admins should update it later.
                    try:
                        create_users()
                        self.stdout.write(
                            self.style.SUCCESS(
                                "Successfully created users for development."
                            )
                        )
                    except Exception:
                        self.stdout.write(
                            self.style.ERROR(
                                "Failed to create users, check the records in the database if exist, or check if you migrated the database."
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            "This command running in development mode only."
                        )
                    )
            else:
                self.stdout.write(self.style.ERROR("Invalid option."))

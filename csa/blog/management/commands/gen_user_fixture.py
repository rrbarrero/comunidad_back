from django.core.management.base import BaseCommand, CommandError
import yaml
from faker import Faker
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[2]
FIXTURE_DIR = APP_DIR / "fixtures"

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Genera un fixture para la clase users"

    def add_arguments(self, parser):
        parser.add_argument("counter", type=int)

    def handle(self, *args, **options):
        usuarios = []
        for i in range(options["counter"]):
            usuarios.append(
                {
                    "model": "auth.user",
                    "pk": i + 100,
                    "fields": {
                        "username": fake.user_name(),
                        "password": fake.password(),
                        "first_name": fake.first_name(),
                        "last_name": fake.last_name(),
                        "email": fake.email(),
                        "is_active": fake.pybool(),
                        "is_staff": fake.pybool(),
                    },
                }
            )
            self.stdout.write(
                self.style.SUCCESS("Successfully loaded data ({})".format(i))
            )
        with open(FIXTURE_DIR / "users.yaml", "w") as fw:
            yaml.dump(usuarios, fw, allow_unicode=True)

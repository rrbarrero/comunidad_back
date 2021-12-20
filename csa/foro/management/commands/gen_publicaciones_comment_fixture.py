from django.core.management.base import BaseCommand, CommandError
import yaml
from faker import Faker
from pathlib import Path
from datetime import timedelta

APP_DIR = Path(__file__).resolve().parents[2]
FIXTURE_DIR = APP_DIR / "fixtures"

fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Genera un fixture para la clase users"

    def add_arguments(self, parser):
        parser.add_argument("counter", type=int)

    def handle(self, *args, **options):
        articulos = []
        for i in range(options["counter"]):
            created_at = fake.date_time_this_month()
            articulos.append(
                {
                    "model": "foro.comentariopublicacion",
                    "pk": i + 1,
                    "fields": {
                        "cuerpo": ".<br />".join(fake.texts(nb_texts=3)),
                        "autor": fake.random_int(min=100, max=199),
                        "publicacion": fake.random_int(min=1, max=650),
                        "censurado": fake.pybool(),
                        "fecha_creacion": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "fecha_modificacion": (created_at + timedelta(days=2)).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    },
                }
            )
            self.stdout.write(
                self.style.SUCCESS("Successfully loaded data ({})".format(i))
            )
        with open(FIXTURE_DIR / "comentariospublicaciones.yaml", "w") as fw:
            yaml.dump(articulos, fw, allow_unicode=True)

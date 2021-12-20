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
                    "model": "blog.articulo",
                    "pk": i + 1,
                    "fields": {
                        "titulo": fake.text(max_nb_chars=15),
                        "imagen": fake.image_url(),
                        "entradilla": " ".join(fake.texts(nb_texts=2))[0:349],
                        "cuerpo": ".<br />".join(fake.texts(nb_texts=20)),
                        "publico": fake.pybool(),
                        "autor": fake.random_int(min=100, max=199),
                        "tema": fake.random_int(min=1, max=5),
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
        with open(FIXTURE_DIR / "articlesblog.yaml", "w") as fw:
            yaml.dump(articulos, fw, allow_unicode=True)

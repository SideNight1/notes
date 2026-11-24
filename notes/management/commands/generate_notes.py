from time import perf_counter

from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from notes.models import Note


class Command(BaseCommand):
    help = "Создаёт тестовые заметки до указанного общего количества."

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=100_000)
        parser.add_argument("--batch-size", type=int, default=2_000)

    def handle(self, *args, **options):
        total = options["total"]
        batch_size = options["batch_size"]

        if total < 0:
            raise CommandError("--total не может быть меньше нуля.")
        if batch_size < 1:
            raise CommandError("--batch-size должен быть не меньше 1.")

        existing = Note.objects.count()
        missing = max(total - existing, 0)

        if missing == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"В базе уже есть {existing} заметок; добавлять ничего не нужно."
                )
            )
            return

        fake = Faker("ru_RU")
        created = 0
        started = perf_counter()

        while created < missing:
            current_batch_size = min(batch_size, missing - created)
            batch = [
                Note(
                    title=fake.sentence(nb_words=6)[:200],
                    content=fake.text(max_nb_chars=300),
                )
                for _ in range(current_batch_size)
            ]
            Note.objects.bulk_create(batch, batch_size=current_batch_size)
            created += current_batch_size
            self.stdout.write(
                f"Создано {created} из {missing}",
                ending="\r",
            )

        elapsed = perf_counter() - started
        final_count = Note.objects.count()
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: добавлено {created}, всего в базе {final_count}; "
                f"время генерации {elapsed:.2f} сек."
            )
        )
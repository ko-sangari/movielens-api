from django.core.management.base import BaseCommand
from app.utils.load_datasets import load_data


class Command(BaseCommand):
    help = "Starts the load_data function."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",  # or '-d'
            type=str,
            help="Optional: Directory path where `ml-20m` dataset is located.",
        )

    def handle(self, *args, **kwargs):
        dataset_path = kwargs.get("dir") or "datasets/ml-20m"

        self.stdout.write("Starting data load...")
        try:
            load_data(dataset_path)
            self.stdout.write(self.style.SUCCESS("Data load completed successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during data load: {e}"))

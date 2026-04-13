import pgvector.django
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0009_add_card_embedding"),
    ]

    operations = [
        # pgvector cannot ALTER COLUMN dimensions in place; drop and re-add.
        # Existing OpenAI (1536-dim) embeddings are not compatible with
        # Voyage AI (1024-dim) and must be regenerated.
        migrations.RemoveField(
            model_name="card",
            name="embedding",
        ),
        migrations.AddField(
            model_name="card",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=1024, null=True),
        ),
    ]

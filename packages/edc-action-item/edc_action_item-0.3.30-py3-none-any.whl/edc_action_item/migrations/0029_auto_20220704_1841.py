# Generated by Django 3.2.13 on 2022-07-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_action_item", "0028_auto_20210203_0706"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalactionitem",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Action Item",
                "verbose_name_plural": "historical Action Items",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalreference",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical reference",
                "verbose_name_plural": "historical references",
            },
        ),
        migrations.AlterField(
            model_name="historicalactionitem",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalreference",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]

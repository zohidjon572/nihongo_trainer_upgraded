from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("trainer", "0001_initial")]
    operations = [
        migrations.AddField(model_name="scenario", name="category", field=models.CharField(
            choices=[("daily","Kundalik hayot"),("travel","Sayohat"),("school","Universitet / O'qish"),("work","Ish / Biznes"),("shopping","Xarid"),("restaurant","Restoran / Kafe"),("other","Boshqa")],
            default="daily", max_length=20, verbose_name="Mavzu")),
        migrations.AddField(model_name="scenario", name="emoji", field=models.CharField(default="💬", blank=True, max_length=8, verbose_name="Ikonka (emoji)")),
        migrations.AddField(model_name="scenario", name="estimated_minutes", field=models.PositiveIntegerField(default=5, verbose_name="Taxminiy daqiqa")),
        migrations.AddField(model_name="conversationstep", name="speaker", field=models.CharField(default="AI Sensei", max_length=50, verbose_name="So'zlovchi")),
    ]

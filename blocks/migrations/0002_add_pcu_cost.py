from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='pcu_cost',
            field=models.IntegerField(
                default=0,
                help_text='Performance Cost Units (PCU) required to place this block',
            ),
        ),
    ]

# Generated migration to remove duplicate pcu_cost field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0002_fix_components_format'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE blocks_block DROP COLUMN IF EXISTS pcu_cost;",
            reverse_sql="ALTER TABLE blocks_block ADD COLUMN pcu_cost integer NOT NULL DEFAULT 0;",
        ),
    ]

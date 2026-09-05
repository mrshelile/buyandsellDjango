from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('content', '0015_alter_banner_promotion_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='displays',
            field=models.ManyToManyField(
                blank=True,
                related_name='promotions',
                to='content.multiimage',
            ),
        ),
    ]
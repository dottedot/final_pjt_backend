# Generated by Django 3.2.12 on 2022-05-20 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20220520_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genres',
            name='tmdb_genre_id',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='genre',
        ),
        migrations.AddField(
            model_name='genres',
            name='movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movies.movies'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movies',
            name='release_date',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='MovieGenre',
        ),
    ]
from django.db import models


class Anime(models.Model):
    subject_id = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    originaltitle = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    info = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    rate_num = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    link = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    img = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime'

class Anisong(models.Model):
    type = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    name = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)
    song_id = models.CharField(max_length=512, db_collation='utf8mb3_general_ci')
    subject_id = models.CharField(primary_key=True, max_length=512, db_collation='utf8mb3_general_ci')  # The composite primary key (subject_id, song_id) found, that is not supported. The first column is selected.
    images = models.CharField(max_length=512, db_collation='utf8mb3_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anisong'
        unique_together = (('subject_id', 'song_id'),)


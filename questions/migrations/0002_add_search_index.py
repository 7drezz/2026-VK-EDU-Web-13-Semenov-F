from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                CREATE INDEX CONCURRENTLY IF NOT EXISTS questions_search_idx 
                ON questions_question 
                USING GIN (to_tsvector('simple', title || ' ' || text));
            ''',
            reverse_sql='DROP INDEX IF EXISTS questions_search_idx;'
        ),
    ]
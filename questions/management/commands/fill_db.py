import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Profile
from questions.models import Tag, Question, Answer, QuestionLike, AnswerLike

fake = Faker()

class Command(BaseCommand):
    help = 'fill_db'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        users = []
        for i in range(ratio):
            users.append(User(username=f'user_{i}', email=f'user_{i}@mail.com'))
        User.objects.bulk_create(users, batch_size=1000)
        users = list(User.objects.all())
        
        profiles = []
        for u in users:
            profiles.append(Profile(user=u, nickname=u.username))
        Profile.objects.bulk_create(profiles, batch_size=1000)
        
        tags = []
        for i in range(ratio):
            tags.append(Tag(name=f'tag_{i}'))
        Tag.objects.bulk_create(tags, batch_size=1000, ignore_conflicts=True)
        tags = list(Tag.objects.all())
        
        questions = []
        for i in range(ratio * 10):
            questions.append(Question(
                title=fake.sentence(),
                text=fake.text(),
                author=random.choice(users),
                rating=random.randint(0, 100)
            ))
        Question.objects.bulk_create(questions, batch_size=1000)
        questions = list(Question.objects.all())
        
        through = []
        for q in questions:
            for t in random.sample(tags, min(3, len(tags))):
                through.append(Question.tags.through(question_id=q.id, tag_id=t.id))
        Question.tags.through.objects.bulk_create(through, ignore_conflicts=True, batch_size=5000)
        
        answers = []
        for i in range(ratio * 100):
            answers.append(Answer(
                text=fake.paragraph(),
                author=random.choice(users),
                question=random.choice(questions),
                rating=random.randint(0, 50)
            ))
        Answer.objects.bulk_create(answers, batch_size=1000)

        question_likes = []
        for _ in range(ratio * 200):
            question_likes.append(QuestionLike(
                user=random.choice(users),
                question=random.choice(questions),
                value=random.choice([1, -1])
            ))
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True, batch_size=5000)

        answer_likes = []
        for _ in range(ratio * 200):
            answer_likes.append(AnswerLike(
                user=random.choice(users),
                answer=random.choice(answers),
                value=random.choice([1, -1])
            ))
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True, batch_size=5000)
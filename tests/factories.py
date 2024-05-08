import factory
import factory.fuzzy

from crono_task.models import Todo, TodoState, User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}@example.com')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1

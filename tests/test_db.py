from sqlalchemy import select

from crono_task.models import Todo, User


def test_create_user(session):
    new_user = User(name='alice', password='secret', email='teste@test')

    session.add(new_user)
    session.commit()
    user = session.scalar(select(User).where(User.name == 'alice'))

    assert user.name == 'alice'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        tag='Test Tag',
        finished_at=None,
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos

import os

from sqlalchemy import create_engine
from sqlmodel import Session

from chef.models import Recipe, Category, Tag

OLD_URI = os.getenv('OLD_URI')
NEW_URI = os.getenv('NEW_URI')


def main():
    engine_1 = create_engine(OLD_URI)
    engine_2 = create_engine(NEW_URI, echo=True)
    with Session(engine_1) as session:
        old_tags = session.query(Tag).all()
        old_recipes = session.query(Recipe).all()
        old_categories = session.query(Category).all()
        session.expunge_all()

    with Session(engine_2) as session_new:
        for t in old_tags:
            session_new.merge(t)
        session_new.commit()
        for c in old_categories:
            session_new.merge(c)
        for r in old_recipes:
            session_new.merge(r)
        session_new.commit()
        r = session_new.query(Recipe).all()
        x = 1


if __name__ == '__main__':
    main()

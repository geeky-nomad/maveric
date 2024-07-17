from sqlalchemy.orm import DeclarativeBase, Session
from mav_framework.database.blueprint import engine


class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def create_tables(cls):
        # TODO -> we have to find a way where tables get refreshed as soon as we update the columns inside a table
        # cls.metadata.drop_all(bind=engine)
        cls.metadata.create_all(bind=engine)

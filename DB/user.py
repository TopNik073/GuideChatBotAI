from DB.DataBase import SessionMaker
from datetime import datetime


class User(SessionMaker):
    def __init__(self, id: int, firstname: str = None, surname: str = None, username: str | None = None):
        self.id: int = id

        self.firstname: str | None = firstname
        self.surname: str | None = surname
        self.username: str | None = username

        self.context: list[dict] = []

        self.created_at: datetime = None
        self.updated_at: datetime = None

        super().__init__()

        self.add_user()

    def add_user(self):
        try:
            with self.session_factory() as session:
                user: Users = self.model(**self.get_data_dict())
                session.add(user)
                session.commit()

            return self

        except IntegrityError as e:
            session.rollback()
            user = self.get()
            if user is None:
                raise e

            return self

        except Exception as e:
            raise e

    def get(self):
        try:
            with self.session_factory() as session:
                query = select(self.model).filter_by(id=self.id)
                user: Users = session.scalars(query).first()
                if user is None:
                    return

                self.id = user.id

                self.firstname = user.firstname
                self.surname = user.surname
                self.username = user.username

                if user.context is not None:
                    self.context = user.context

                self.created_at = user.created_at
                self.updated_at = user.updated_at

                return self

        except Exception as e:
            raise e

    def update(self):
        try:
            with self.session_factory() as session:
                session.query(self.model).filter_by(id=self.id).update(
                    self.get_data_dict()
                )
                session.commit()

            return self

        except Exception as e:
            raise e

    def delete(self) -> None:
        try:
            with self.session_factory() as session:
                query = select(self.model).filter_by(id=self.id)
                user: Users = session.scalars(query).first()
                if user is None:
                    return

                session.delete(user)
                session.commit()

        except Exception as e:
            raise e

    def get_data_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "username": self.username,
            "context": self.context,
        }
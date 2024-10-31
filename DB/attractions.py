from DB.DataBase import SessionMaker
from sqlalchemy import select, func
from DB.models.attractions import Attractions as AttractionsTable


class Attractions(SessionMaker):
    def get_attr_by_cat(self, categories: list):
        try:
            query_search = ""
            for i in range(len(categories)):
                query_search += f'"{categories[i]}"'

                if len(categories) != i+1:
                    query_search += " | "

            with self.session_factory() as session:
                query = select(self.model).where(func.to_tsvector(self.model.description).match(search_query))
                results = session.scalars(query).all()

            if results is None:
                return None

            return self._get_attractions(results)

        except Exception as e:
            raise e

    def _get_attractions(self, results: list[AttractionsTable]):
        attractions: list = []
        for res in results:
            attractions.append(
                {
                    "name": res.name,
                    "description": res.description,
                    "url": res.url,
                    "image": res.image,
                    "location": res.location,
                }
            )

        return attractions

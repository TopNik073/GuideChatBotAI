from DB.DataBase import SessionMaker
from sqlalchemy import select, func, text
from DB.models.attractions import Attractions as AttractionsTable


class Attractions(SessionMaker):
    model = AttractionsTable

    def get_attr_by_cat(self, categories: list):
        try:
            query_search = ""
            for i in range(len(categories)):
                query_search += f"{categories[i]}"

                if len(categories) != i + 1:
                    query_search += " | "

            with self.session_factory() as session:
                query = text(
                    f"SELECT * "
                    f"FROM attractions "
                    f"WHERE tsv_description @@ to_tsquery('russian', '{query_search}');"
                )

                results = session.execute(query).fetchall()
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
                    "name": res.name.encode().decode(),
                    "description": res.description.encode().decode(),
                    "url": res.url.encode().decode(),
                    "image": res.image.encode().decode(),
                    "location": res.location.encode().decode(),
                }
            )
            print(res.name)

        return attractions

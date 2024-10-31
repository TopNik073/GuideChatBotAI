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
                    "name": res.name,
                    "description": res.description,
                    "url": res.url,
                    "image": res.image,
                    "location": res.location,
                }
            )
            print(res.name)
        print(attractions)
        return attractions[:10]

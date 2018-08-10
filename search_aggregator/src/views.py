import graphene
from .models import SearchEngine


class QueryType(graphene.ObjectType):
    name = 'Query'
    search = graphene.String(
        text=graphene.Argument(graphene.String, required=True),
        limit=graphene.Argument(graphene.Int, default_value=10),
    )

    async def resolve_search(self, info, text, limit=None):
        res = await SearchEngine.search_all(text, limit)
        return res


class ResultType(graphene.ObjectType):
    name = 'Result'
    link = graphene.String()
    title = graphene.String()


class EngineResultType(graphene.ObjectType):
    name = 'EngineResult'
    engine = graphene.String()
    results = graphene.List('self')


schema = graphene.Schema(query=QueryType)

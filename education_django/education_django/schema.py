"""
Схемы GraphQL
"""

import graphene

from education_app.schema import Query as EducationQuery
from education_app.schema import Mutation as EducationMutation


class Query(EducationQuery, graphene.ObjectType):
    pass


class Mutation(EducationMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

"""GraphQL resolver functionality"""
from ariadne import ObjectType, make_executable_schema, snake_case_fallback_resolvers

from .models import Camps, Cms_Users, Stock
from .type_defs import type_defs

query = ObjectType("Query")


# registers this fn as a resolver for the "allBases" field, can use it as the
# resolver for more than one thing by just adding more decorators
@query.field("allBases")
def resolve_all_camps(_, info):
    # discard the first input because it belongs to a root type (Query, Mutation,
    # Subscription). Otherwise it would be a value returned by a parent resolver.
    response = Camps.get_all_camps()
    return list(response.dicts())


@query.field("allUsers")
def resolve_all_users(_, info):
    response = Cms_Users.get_all_users()
    return list(response.dicts())


@query.field("user")
def resolve_user(_, info, email):
    response = Cms_Users.get_user(email)
    return response


@query.field("box")
def resolve_box(_, info, id):
    response = Stock.get_box(id)
    return response


schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)

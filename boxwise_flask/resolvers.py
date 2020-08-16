"""GraphQL resolver functionality"""
from ariadne import (
    ObjectType,
    ScalarType,
    gql,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

from .auth_helper import authorization_test
from .models.models import Camps, Cms_Users
from .models.qr_code import QRCode
from .type_defs import mutation_defs, query_defs, type_defs

query = ObjectType("Query")
mutation = ObjectType("Mutation")

datetime_scalar = ScalarType("Datetime")
date_scalar = ScalarType("Date")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@date_scalar.serializer
def serialize_date(value):
    return value.isoformat()


# registers this fn as a resolver for the "allBases" field, can use it as the
# resolver for more than one thing by just adding more decorators
@query.field("allBases")
def resolve_all_camps(_, info):
    # discard the first input because it belongs to a root type (Query, Mutation,
    # Subscription). Otherwise it would be a value returned by a parent resolver.
    response = Camps.get_all_camps()
    return list(response.dicts())


# not everyone can see all the bases
# see the comment in https://github.com/boxwise/boxwise-flask/pull/19
@query.field("orgBases")
def resolve_org_bases(_, info, org_id):
    response = Camps.get_camps_by_org_id(org_id)
    return list(response.dicts())


@query.field("base")
def resolve_camp(_, info, id):
    authorization_test("bases", base_id=id)
    response = Camps.get_camp(id)
    return response


@query.field("allUsers")
def resolve_all_users(_, info):
    response = Cms_Users.get_all_users()
    return list(response.dicts())


@query.field("user")
def resolve_user(_, info, email):
    response = Cms_Users.get_user(email)
    return response


@mutation.field("createQRCode")
def resolve_create_qr_code(_, info):
    qr_code = QRCode.create(code="", created_on="", created_by=1, last_modified_on=1)
    return qr_code


schema = make_executable_schema(
    gql(type_defs + query_defs + mutation_defs),
    [query, mutation],
    snake_case_fallback_resolvers,
)

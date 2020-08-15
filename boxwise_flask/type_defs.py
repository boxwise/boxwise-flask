"""GraphQL type definitions"""
from ariadne import gql

mutation_defs = gql(
    """
    type Mutation {
        createQRCode: QRCode
    }
    """
)

query_defs = gql(
    """
    type Query {
        hello: String!
        allBases: [Base]
        orgBases(org_id: Int): [Base]
        base(id: String!): Base
        allUsers: [User]
        user(email: String): User
        createQRCode: QRCode
    }
    """
)

type_defs = gql(
    """
    type Base {
        id: Int
        name: String
        currencyname: String
        organisation_id: Int
    }

    type User {
        id: Int!
        organisation_id: Int
        name: String
        email: String!
        cms_usergroups_id: Int
        valid_firstday: Date
        valid_lastday: Date
        camp_id: [Int]
        lastlogin: Datetime
        lastaction: Datetime
    }

    type QRCode {
        id: Int!
        Code: String!
        CreatedOn: Int
        CreatedBy: String!
        LastModifiedOn: Int
    }

    scalar Datetime
    scalar Date
"""
)

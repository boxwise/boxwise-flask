from boxwise_flask.models.models import Camps, Cms_Users


def get_base_from_graphql(id, base_query):
    return [x for x in base_query if x["id"] == id][0]


def test_all_bases(client, database):
    """Verify allBases GraphQL query endpoint"""
    camps = [
        {"id": 1, "name": "oak-tree", "organisation_id": 1, "currencyname": "pound"},
        {"id": 2, "name": "chicken", "organisation_id": 1, "currencyname": "peanuts"},
        {"id": 3, "name": "sofa", "organisation_id": 1, "currencyname": "candles"},
    ]

    database.connect_db()

    for camp in camps:
        Camps.create(
            id=camp["id"],
            organisation_id=camp["organisation_id"],
            name=camp["name"],
            currencyname=camp["currencyname"],
        )

    database.close_db(None)

    graph_ql_query_string = """query {
            allBases {
                id
                organisation_id
                name
                currencyname
            }
        }"""

    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data)
    assert response_data.status_code == 200
    all_bases = response_data.json["data"]["allBases"]
    for camp in camps:
        camper = get_base_from_graphql(camp["id"], all_bases)
        assert camper["id"] == camp["id"]
        assert camper["organisation_id"] == camp["organisation_id"]
        assert camper["name"] == camp["name"]
        assert camper["currencyname"] == camp["currencyname"]


def test_base(client, database):
    """Verify base GraphQL query endpoint"""
    camps = [
        {"id": 1, "name": "oak-tree", "organisation_id": 1, "currencyname": "pound"},
        {"id": 2, "name": "chicken", "organisation_id": 1, "currencyname": "peanuts"},
        {"id": 3, "name": "sofa", "organisation_id": 1, "currencyname": "candles"},
    ]

    database.connect_db()

    for camp in camps:
        Camps.create(
            id=camp["id"],
            organisation_id=camp["organisation_id"],
            name=camp["name"],
            currencyname=camp["currencyname"],
        )

    database.close_db(None)
    test_id = 1
    graph_ql_query_string = (
        """query Base {
                base(id: "%s") {
                    id
                    organisation_id
                    name
                    currencyname
                }
            }"""
        % test_id
    )

    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data)
    assert response_data.status_code == 200
    assert response_data.json["data"]["base"] == get_base_from_graphql(test_id, camps)


def test_all_users(client, database):
    """Verify allUsers GraphQL query endpoint"""

    database.connect_db()
    emails = [
        "mr-anderson@matrix.co.uk",
        "hamburgerman@beef.co.uk",
        "marmalade@jam.co.uk",
    ]
    for i, email in enumerate(emails):

        Cms_Users.create(
            id=i,
            name="",
            email=email,
            cms_usergroups_id="",
            valid_firstday="",
            valid_lastday="",
            lastlogin="",
            lastaction="",
        )

    database.close_db(None)

    graph_ql_query_string = """query {
            allUsers {
                id
                name
            }
        }"""
    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data)
    print(response_data.json)
    assert response_data.status_code == 200
    assert response_data.json["data"]["allUsers"][0]["id"] == 0


def test_user(client, database):
    """Verify users GraphQL query endpoint"""

    database.connect_db()
    emails = [
        "mr-anderson@matrix.co.uk",
        "hamburgerman@beef.co.uk",
        "marmalade@jam.co.uk",
    ]
    for i, email in enumerate(emails):
        Cms_Users.create(
            id=i,
            name="",
            email=email,
            cms_usergroups_id="",
            valid_firstday="",
            valid_lastday="",
            lastlogin="",
            lastaction="",
        )

    database.close_db(None)
    test_id = 0
    matrix_email = '"%s"' % emails[test_id]

    graph_ql_query_string = (
        """query User {
                user(email: %s) {
                    id
                    name
                }
            }"""
        % matrix_email
    )
    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data)
    assert response_data.status_code == 200
    assert response_data.json["data"]["user"]["id"] == test_id

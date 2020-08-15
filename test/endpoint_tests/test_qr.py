from boxwise_flask.models.qr_code import QRCode


def test_create_qr(client, database):
    """testing the creation of a qr code with graph ql"""

    database.connect_db()
    QRCode.create(id=0, code="", created_on="", created_by=1, last_modified_on=1)
    database.close_db(None)

    graph_ql_query_string = """mutation {
                createQRCode {
                    id
                }
            }"""

    data = {"query": graph_ql_query_string}
    response_data = client.post("/graphql", json=data)
    print(response_data.json)
    assert response_data.status_code == 200
    assert response_data.json["data"]["createQRCode"]["id"] == 0

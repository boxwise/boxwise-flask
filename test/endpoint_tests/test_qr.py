def test_create_qr(client, database):
    """testing the creation of a qr code with graph ql"""

    graph_ql_query_string = """mutation {
            createQRCode {
                id
                Code
            }
        }"""

    data = {"query": graph_ql_query_string}

    response_data = client.post("/graphql", json=data)

    print(response_data.json)
    assert response_data.status_code == 200
    print(response_data.json["data"]["createQRCode"])
    assert response_data.json["data"]["createQRCode"]["id"] == 1

from boxwise_flask.models.qr_code import QRCode


def test_qr_code_creation():
    """example database model test"""

    qr_code = {
        "id": 0,
        "code": "",
        "created_on": "",
        "created_by": 1,
        "last_modified_on": 1,
    }
    QRCode.create(**qr_code)

    x = QRCode.get_a_code(0)
    assert x.id == 0
    assert x.code == ""
    assert x.created_by == 1

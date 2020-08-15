from boxwise_flask.models.qr_code import QRCode


def test_qr_code_creation():
    """example database model test"""

    QRCode.create(id=0, code="", created_on="", created_by=1, last_modified_on=1)

    x = QRCode.get_a_code(0)
    assert x.id == 0

import hello


def test_hello():
    expected = "Hello world!"
    result = hello.hello()

    assert result == expected

import pytest

from aioviber.utils import add_url_params, snake_case_2_camel_case


def test_url_query():
    url = 'http://stackoverflow.com/test?answers=true'
    new_params = {'answers': False, 'data': ['some', 'values']}
    new_url = add_url_params(url, new_params)

    assert 'answers=false' in new_url
    assert 'data=some' in new_url
    assert 'data=values' in new_url


@pytest.mark.parametrize("camel_case,snake_case", [
    ('Hello', 'hello'),
    ('HelloWorld', 'hello_world'),
    ('HelloWorld', 'hello_World'),
])
def test_snake_case_2_camel_case(camel_case, snake_case):
    assert camel_case == snake_case_2_camel_case(snake_case)

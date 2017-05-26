from aioviber.utils import add_url_params


def test_url_query():
    url = 'http://stackoverflow.com/test?answers=true'
    new_params = {'answers': False, 'data': ['some', 'values']}
    assert add_url_params(url, new_params) == 'http://stackoverflow.com/test?data=some&data=values&answers=false'

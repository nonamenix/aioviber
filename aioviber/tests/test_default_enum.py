from aioviber.keyboard import DefaultEnum


def test_default_enum():
    class TestEnum(DefaultEnum):
        choice_a = 'choice_a'
        choice_b = 'choice_b'

        all = (choice_a, choice_b)
        _default = choice_a

    assert TestEnum.is_default('choice_a')

import pytest

from src.madr.utils import sanitize


@pytest.mark.parametrize(
    ('entry', 'expected_exit'),
    [
        ('Machado de Assis', 'machado de assis'),
        ('Manuel        Bandeira', 'manuel bandeira'),
        ('Edgar Alan Poe         ', 'edgar alan poe'),
        (
            'Androides Sonham Com Ovelhas Elétricas?',
            'androides sonham com ovelhas elétricas?',
        ),
        ('  breve  história  do tempo ', 'breve história do tempo'),
        (
            'O mundo assombrado pelos demônios',
            'o mundo assombrado pelos demônios',
        ),
    ],
)
def test_name_in(entry, expected_exit):
    assert sanitize.name_in(entry) == expected_exit


@pytest.mark.parametrize(
    ('entry', 'expected_exit'),
    [
        ('machado de assis', 'Machado De Assis'),
        ('manuel bandeira', 'Manuel Bandeira'),
        ('edgar alan poe', 'Edgar Alan Poe'),
        (
            'androides sonham com ovelhas elétricas?',
            'Androides Sonham Com Ovelhas Elétricas?',
        ),
        ('breve história do tempo', 'Breve História Do Tempo'),
        (
            'o mundo assombrado pelos demônios',
            'O Mundo Assombrado Pelos Demônios',
        ),
    ],
)
def test_name_out(entry, expected_exit):
    assert sanitize.name_out(entry) == expected_exit


@pytest.mark.parametrize(
    ('entry', 'expected_exit'),
    [
        ('Machado de Assis', 'Machado De Assis'),
        ('Manuel        Bandeira', 'Manuel Bandeira'),
        ('Edgar Alan Poe         ', 'Edgar Alan Poe'),
        (
            'Androides Sonham Com Ovelhas Elétricas?',
            'Androides Sonham Com Ovelhas Elétricas?',
        ),
        ('  breve  história  do tempo ', 'Breve História Do Tempo'),
        (
            'O mundo assombrado pelos demônios',
            'O Mundo Assombrado Pelos Demônios',
        ),
    ],
)
def test_name_in_out(entry, expected_exit):
    assert sanitize.name_in_out(entry) == expected_exit

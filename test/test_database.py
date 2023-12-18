import sys

import pytest

from model.database import DBEngine, DBType, get_db_engine


def test_subclass():
    _cls = DBEngine()
    scls_name = _cls.SUBCLASSES.get(DBType('sqlite')).__name__
    module = sys.modules['model.database']
    _scls_1 = getattr(module, scls_name)
    _scls_2 = _cls.SUBCLASSES.get(DBType('sqlite'))
    instance_1 = _scls_1(database_url="sqlite:///test.db")
    instance_2 = _scls_2(database_url="sqlite:///test.db")
    # print(f"db_instance={instance}")
    assert type(instance_1) == type(instance_2)


def test_get_db_engine():
    db_engine = get_db_engine()
    assert db_engine._db_type == DBType('sqlite')

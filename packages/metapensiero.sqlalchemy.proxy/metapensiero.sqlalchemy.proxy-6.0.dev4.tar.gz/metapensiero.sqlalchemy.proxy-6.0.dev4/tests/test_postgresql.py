# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- PG specific tests
# :Created:   sab 24 ott 2015 12:52:33 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: Copyright (C) 2015, 2016, 2017, 2018, 2020, 2021, 2022 Lele Gaifax
#

import datetime
import os
import uuid

import pytest
from psycopg2.extras import DateRange
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sapg

from metapensiero.sqlalchemy.proxy.core import ProxiedQuery
from metapensiero.sqlalchemy.proxy.orm import ProxiedEntity
from metapensiero.sqlalchemy.proxy.filters import extract_filters
from metapensiero.sqlalchemy.proxy.utils import SQLALCHEMY_VERSION

if SQLALCHEMY_VERSION > (1, 4):
    from sqlalchemy.orm import declarative_base
else:
    from sqlalchemy.ext.declarative import declarative_base


# See .gitlab-ci.yml

pg_host = os.getenv('POSTGRES_HOST', 'localhost')
pg_dbname = os.getenv('POSTGRES_DB', 'mp_sa_proxy_test')
pg_user = os.getenv('POSTGRES_USER')
pg_pwd = os.getenv('POSTGRES_PASSWORD')

dburi = 'postgresql://'
if pg_user and pg_pwd:
    dburi += f'{pg_user}:{pg_pwd}@'
dburi += f'{pg_host}/{pg_dbname}'

# Note: the echoed statements will be visible with "py.test -s"

engine = sa.create_engine(dburi, echo=True)
Session = sa.orm.sessionmaker(bind=engine)


metadata = sa.MetaData()
metadata.bind = engine
Base = declarative_base(metadata=metadata)


SQLFUNC = """\
CREATE OR REPLACE FUNCTION bigintfunc()
RETURNS bigint AS $$

SELECT 1234567890::bigint * 1234567890::bigint

$$ LANGUAGE sql
"""


class GUID(sa.TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses CHAR(32), storing as stringified hex value.
    """

    impl = sa.types.CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect, _PGUUID=sapg.UUID, _CHAR=sa.types.CHAR):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(_PGUUID())
        else:
            return dialect.type_descriptor(_CHAR(32))

    # NOTE: UUIDs are enforced *only* on PostgresQL, because doing that on MySQL right now
    #       would mean spending a lot of time fixing the assumptions that legacy code base
    #       is full of.

    def process_bind_param(self, value, dialect,
                           _UUID=uuid.UUID, _uuid3=uuid.uuid3, _ns=uuid.NAMESPACE_OID):
        if value is None:
            return value
        else:
            if isinstance(value, _UUID):
                return value.hex
            elif dialect.name == 'postgresql':
                try:
                    return _UUID(value).hex
                except (ValueError, AttributeError):
                    if not isinstance(value, str):
                        value = str(value)
                    return _uuid3(_ns, value).hex
            else:
                return value

    def process_result_value(self, value, dialect, _UUID=uuid.UUID):
        return value if value is None or dialect.name != 'postgresql' else _UUID(value)


class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(GUID, primary_key=True,
                   info=dict(label='id', hint='the product id'))
    brand = sa.Column(sa.String(64),
                      info=dict(label='brand', hint='the product brand'))
    description = sa.Column(sapg.HSTORE,
                            info=dict(label='description', hint='the product description'))
    other_description = sa.Column(sa.UnicodeText(),
                                  info=dict(label='other description',
                                            hint='alternative description'))
    availability = sa.Column(sapg.DATERANGE,
                             info=dict(label='availability', hint='period of availability'))
    quantity = sa.Column(sa.BigInteger,
                         info=dict(label='quantity', hint='items in store'))
    delivery = sa.Column(sa.Interval,
                         info=dict(label='delivery', hint='max delivery time'))
    details = sa.Column(sapg.JSONB(),
                        info=dict(label='DETS', hint='arbitrary details'))


def setup():
    metadata.create_all(engine)

    session = Session()

    session.execute(sa.text(SQLFUNC))

    p = Product(id='frizione', brand='Allga San®',
                description={'it': 'Frizione', 'de': 'Einreibung'},
                other_description='Lorem ipsum')
    session.add(p)

    p = Product(id='orologio', brand='Breitling',
                description={'it': 'Orologio', 'en': 'Watch'})
    session.add(p)

    p = Product(id='fragole', brand='Km0',
                description={'it': 'Fragole', 'en': 'Strawberries'},
                availability=DateRange(datetime.date(2017, 3, 23),
                                       datetime.date(2017, 4, 24)))
    session.add(p)

    session.commit()


def teardown():
    metadata.drop_all(engine)


@pytest.mark.parametrize('column,args,expected_snippet', [
    (Product.__table__.c.description['it'],
     dict(filter_col='description', filter_value='~=bar'),
     ' LIKE '),
    (Product.__table__.c.availability,
     dict(filter=[dict(property='availability', value=datetime.date(2017, 4, 1))]),
     ' @> '),
])
def test_operators(column, args, expected_snippet):
    conds = extract_filters(args)
    assert len(conds) == 1
    cond = conds[0]
    filter = cond.operator.filter(column, cond.value)
    assert expected_snippet in str(filter)


def test_filters():
    proxy = ProxiedEntity(Product)

    sas = Session()

    res = proxy(sas, filters=[dict(property='availability',
                                   value=datetime.date(2017, 4, 1))])
    assert res[0].description['it'] == 'Fragole'
    sas.commit()


def test_sort_1():
    proxy = ProxiedEntity(Product)

    sas = Session()
    res = proxy(sas)
    sas.commit()

    assert res


def test_sort_2():
    t = Product.__table__

    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.id, t.c.description['it']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.id, t.c.description['it']]))

    sas = Session()

    res = proxy(sas, sort_col='description')
    sas.commit()

    assert res[0][1] < res[1][1]

    res = proxy(sas, sort_col='description', sort_dir='DESC')
    sas.commit()

    assert res[0][1] > res[1][1]


def test_select_from_function():
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(sa.literal_column('g'))
                             .select_from(sa.text('generate_series(1,10) as g')))
    else:
        proxy = ProxiedQuery(sa.select([sa.literal_column('g')],
                                       from_obj=sa.text('generate_series(1,10) as g')))

    sas = Session()

    proxy(sas, sort_col='g', filter_by_g=2)

    # Non existing field
    proxy(sas, sort_col='g', filter_by_foo=2)
    sas.commit()


def test_bigint_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.quantity))
    else:
        proxy = ProxiedQuery(sa.select([t.c.quantity]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'integer'


def test_bigint_function_metadata():
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(sa.func.bigintfunc(type_=sa.BigInteger)))
    else:
        proxy = ProxiedQuery(sa.select([sa.func.bigintfunc(type_=sa.BigInteger)]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'integer'


def test_interval_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.delivery))
    else:
        proxy = ProxiedQuery(sa.select([t.c.delivery]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    assert res['metadata']['fields'][0]['type'] == 'interval'


def test_brand_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.brand))
    else:
        proxy = ProxiedQuery(sa.select([t.c.brand]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'brand'
    assert fmeta['type'] == 'string'
    assert fmeta['length'] == 64


def test_description_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.description['foo']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.description['foo']]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'description'
    assert fmeta['type'] == 'string'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'description'


def test_other_description_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.other_description))
    else:
        proxy = ProxiedQuery(sa.select([t.c.other_description]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'other_description'
    assert fmeta['type'] == 'text'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'other description'


def test_details_metadata():
    t = Product.__table__
    if SQLALCHEMY_VERSION > (1, 4):
        proxy = ProxiedQuery(sa.select(t.c.details['foo']))
    else:
        proxy = ProxiedQuery(sa.select([t.c.details['foo']]))

    sas = Session()

    res = proxy(sas, result=False, metadata='metadata')
    fmeta = res['metadata']['fields'][0]
    assert fmeta['name'] == 'details'
    assert fmeta['type'] == 'string'
    assert 'length' not in fmeta
    assert fmeta['label'] == 'DETS'

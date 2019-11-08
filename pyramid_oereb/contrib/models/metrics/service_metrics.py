# -*- coding: utf-8 -*-
"""
This is the bucket table used to store http access logs behaviors
"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CheckConstraint

from pyramid_oereb.standard.models import NAMING_CONVENTION
from pyramid_oereb.lib.config import Config

metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base()
metrics_schema_name = Config.get('loggers').get('metrics').get('schema').get('name')


class HttpLogs(Base):
    """
    The HttpLogs are the place where internal http access logs are stored. The
    can be used via scripts to display several usage statistics.

    Attributes:
        id (int): The identifier (primary key), only used for ensuring integrity of the contents
        service_type (str): the service type used. Possible values: [GetEGRID, GetExtractById,
            GetCapabilities, GetVersions]
        format (str): the requested format. Possible values: [xml, json, pdf]
        location_requested (str): the requested location
        http_status (int): the https response code
        flavour (str): one of [reduced, full, signed, embeddable], where
            applicable (this field can be NULL)
    """
    __table_args__ = {'schema': metrics_schema_name}
    __tablename__ = 'http_logs'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date = sa.Column(sa.DateTime, nullable=False)
    service_type = sa.Column(sa.String,
                             CheckConstraint(
                                  """service_type in
                                  ('GetEGRID','GetExtractById','GetCapabilities','GetVersion')"""
                             ),
                             nullable=True)
    format = sa.Column(sa.String,
                       CheckConstraint("format in ('xml','json','pdf')"),
                       nullable=True)
    location_requested = sa.Column(sa.String, nullable=True)
    http_status = sa.Column(sa.Integer, nullable=False)
    flavour = sa.Column(sa.String, nullable=True)

# -*- coding: utf-8 -*-
import inspect
import optparse
import logging

from pyramid.config import ConfigurationError
from pyramid.path import DottedNameResolver
from sqlalchemy import create_engine

from pyramid_oereb.lib.config import Config

logging.basicConfig()
log = logging.getLogger(__name__)


def _create_metrics_tables(configuration_yaml_path, section='pyramid_oereb_server_logic', tables_only=False):
    """
    TODO: write docstring
    """

    # Parse themes from configuration
    Config.init(configuration_yaml_path, section)
    # Check required configuration parameters
    loggers = Config.get('loggers')
    # if logger section is absent, simply quit
    if not isinstance(loggers, dict):
        log.error('Missing loggers property in source definition.')
        return
    if not 'metrics' in loggers:
        log.error('Metrics logger is not activated.')
        return
    logger = loggers.get('metrics')
    if not ('db_connection' in logger and 'models' in logger):
        raise ConfigurationError('logger "metrics" configuration has to contain "db_connection" and "models" properties.')

    # Create sqlalchemy engine for configured connection and load module containing models
    engine = create_engine(logger.get('db_connection'), echo=True)
    models = DottedNameResolver().resolve(logger.get('models'))

    if not tables_only:
        # Iterate over contained classes to collect needed schemas
        classes = inspect.getmembers(models, inspect.isclass)
        schemas = []
        create_schema_sql = 'CREATE SCHEMA IF NOT EXISTS {schema};'
        for c in classes:
            class_ = c[1]
            if hasattr(class_, '__table__') and class_.__table__.schema not in schemas:
                schemas.append(class_.__table__.schema)

        # Try to create missing schemas
        connection = engine.connect()
        try:
            for schema in schemas:
                connection.execute(create_schema_sql.format(schema=schema))
        finally:
            connection.close()

    # Create tables
    models.Base.metadata.create_all(engine)


def create_metrics_tables():
    parser = optparse.OptionParser(
        usage='usage: %prog [options]',
        description='Create all content for the standard database'
    )
    parser.add_option(
        '-c', '--configuration',
        dest='configuration',
        metavar='YAML',
        type='string',
        help='The absolute path to the configuration yaml file.'
    )
    parser.add_option(
        '-s', '--section',
        dest='section',
        metavar='SECTION',
        type='string',
        default='pyramid_oereb_server_logic',
        help='The section which contains configuration (default is: pyramid_oereb_server_logic).'
    )
    parser.add_option(
        '-T', '--tables-only',
        dest='tables_only',
        action='store_true',
        default=False,
        help='Use this flag to skip the creation of the schema.'
    )
    options, args = parser.parse_args()
    if not options.configuration:
        parser.error('No configuration file set.')

    _create_metrics_tables(
        configuration_yaml_path=options.configuration,
        section=options.section,
        tables_only=options.tables_only)

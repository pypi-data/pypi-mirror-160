from teradataml import (
    create_context,
    get_connection,
    get_context,
    configure
)
import os
import logging

logger = logging.getLogger(__name__)


def aoa_create_context(database: str = None):
    """
    Creates a teradataml context if one does not already exist.
    Most users should not need to understand how we pass the environment variables etc for dataset connections. This
    provides a way to achieve that and also allow them to work within a notebook for example where a context is already
    present.

    We create the connection based on the following environment variables which are configured automatically by the
    aoa based on the dataset connection selected:

        AOA_CONN_HOST
        AOA_CONN_USERNAME
        AOA_CONN_PASSWORD
        AOA_CONN_LOG_MECH
        AOA_CONN_DATABASE
        AOA_VAL_INSTALL_DB
        AOA_BYOM_INSTALL_DB

    :param database: default database override
    :return: None
    """
    if get_connection() is None:
        if not database:
            database = os.getenv("AOA_CONN_DATABASE")

        host = os.environ["AOA_CONN_HOST"]
        logmech = os.getenv("AOA_CONN_LOG_MECH", "TDNEGO")
        username = os.environ["AOA_CONN_USERNAME"]
        password = os.environ["AOA_CONN_PASSWORD"]

        if database:
            logger.debug(f"Configuring temp database for tables/views to {database}")
            configure.temp_table_database = database
            configure.temp_view_database = database

        configure.val_install_location = os.environ.get("AOA_VAL_INSTALL_DB", "VAL")
        configure.byom_install_location = os.environ.get("AOA_BYOM_INSTALL_DB", "MLDB")

        logger.debug(f"Connecting to {host} on database {database} using logmech {logmech} as {username}")
        create_context(host=host,
                       username=username,
                       password=password,
                       logmech=logmech,
                       database=database)

        from aoa import __version__
        get_context().execute(f"""
        SET QUERY_BAND = 'appVersion={__version__};appName=VMO;appFunc=python;' FOR SESSION VOLATILE
        """)

    else:
        logger.info("teradataml context already exists. Skipping create_context.")

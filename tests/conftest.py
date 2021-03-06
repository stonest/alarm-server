"""Provides fixtures to the test suite.
"""
import pathlib

import grpc_testing
import pytest

from alarmgrpc import alarm_pb2
from alarm_server.servicer import AlarmStoreServicer

TEST_DATABASE = f'{str(pathlib.Path(__file__).parent.absolute())}/test.db'

@pytest.fixture(scope='function')
def mock_server():
    """Constructor to initialise the test grpc servicer"""

    servicers = {
        alarm_pb2.DESCRIPTOR.services_by_name['AlarmStore']: AlarmStoreServicer(
            TEST_DATABASE, False)
    }

    return grpc_testing.server_from_dictionary(
        servicers, grpc_testing.strict_real_time()
    )

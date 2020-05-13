import grpc
import grpc_testing
import pytest
import pathlib

import alarm_server
from alarm_server import alarm_pb2
from alarm_server.servicer import AlarmStoreServicer
from alarm_server import database



TEST_DATABASE = f'{str(pathlib.Path(__file__).parent.absolute())}/test.db'


def _alarm_store_servicer_uu_method(request, method_by_name, server):
    """Helper function to generate unary unary methods"""

    return server.invoke_unary_unary(
        method_descriptor=(alarm_pb2.DESCRIPTOR
        .services_by_name['AlarmStore']
        .methods_by_name[method_by_name]),
        invocation_metadata={},
        request=request, timeout=1
    )


def test_listAlarms(mock_server):
    """Expect a list alarms returned from the database."""

    request = alarm_pb2.ListAlarmsParams()
    list_method = _alarm_store_servicer_uu_method(request, 'ListAlarms', mock_server)
    response, _, code, _ = list_method.termination()
    expected_alarms = [alarm_pb2.Alarm(id='1', day='monday', time='x'),
                        alarm_pb2.Alarm(id='2', day='tuesday', time='y')]

    for key, alarm in enumerate(response.alarms):
        assert alarm == expected_alarms[key]

    assert code == grpc.StatusCode.OK


def test_UpdateAlarm(mock_server):
    """Expect the updated alarm to be stored in the database."""

    request = alarm_pb2.Alarm(id='1', day='tuesday', time='z')
    update_method = _alarm_store_servicer_uu_method(request, 'UpdateAlarm', mock_server)
    response, _, code, _ = update_method.termination()

    assert response.alarms[0] == request
    assert code == grpc.StatusCode.OK
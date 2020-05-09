import grpc
import grpc_testing
import unittest

import alarm_server
from alarm_server import alarm_pb2
from alarm_server.servicer import AlarmStoreServicer

TEST_DATABASE = 'test.db'

class TestAlarmStoreServicer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Constructor to initialise the test grpc servicer"""
        super(TestAlarmStoreServicer, self).__init__(*args, **kwargs)

        servicers = {
            alarm_pb2.DESCRIPTOR.services_by_name['AlarmStoreServicer']: AlarmStoreServicer(TEST_DATABASE)
        }

        self.test_server = grpc_testing.server_from_dictionary(
            servicers, grpc_testing.strict_real_time()
        )


    def _alarm_store_servicer_uu_method(self, request, method_by_name):
        """ Helper function to generate unary unary methods"""

        return self.test_server.invoke_unary_unary(
            method_descriptor=(alarm_pb2.DESCRIPTOR
            .services_by_name['AlarmStoreServicer']
            .methods_by_name[method_by_name]),
            invocation_metadata={},
            request=request, timeout=1
        )


    def test_listAlarms(self):
        """ Expect a list alarms returned from the database."""
        request = alarm_pb2.ListAlarmsParams()

        list_method = self._alarm_store_servicer_uu_method(request, 'ListAlarms')

        response, _, code, _ = list_method.termination()
        expected_alarms = [{'1': {'day': 'monday', 'time':'x'}}, {'2': {'day': 'tuesday', 'time': 'y'}}]

        for alarm in response.alarms:
            for expected_alarm in expected_alarms:
                self.assertEqual(alarm, expected_alarm)

        self.assertEqual(code, grpc.StatusCode.OK)

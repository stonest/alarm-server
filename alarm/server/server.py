import json
from concurrent import futures
from enum import Enum

import pickledb
import grpc
import alarm_pb2
import alarm_pb2_grpc


class AlarmStoreServicer(alarm_pb2_grpc.AlarmStoreServicer):
    """Provides Methods for implementing the alarm store service"""

    def __init__(self, db_path):
        self.db = pickledb.load(db_path, True)

    def ListAlarms(self, request, context):
        """Lists all alarms that are stored in the database"""
        alarm_entries = self.db.getall()

        response = alarm_pb2.ActionResponse()
        for alarm_key, alarm_value in alarm_entries.items():
            try:
                alarm_entry = json.loads(alarm_value)
                response.alarms.append(
                    alarm_pb2.Alarm(
                        id=alarm_key,
                        day=alarm_entry['day'],
                        time=alarm_entry['time']
                    )
                )
            except json.JSONDecodeError:
                print('couldnt load alarm')

        response.status = 'SUCCESS'
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    alarm_pb2_grpc.add_AlarmStoreServicer_to_server(
        AlarmStoreServicer('test.db'), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
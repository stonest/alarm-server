"""A servicer to store and retrieve alarm data."""
import uuid
from concurrent import futures

import grpc

from . import alarm_pb2
from . import alarm_pb2_grpc
from . import database


class AlarmStoreServicer(alarm_pb2_grpc.AlarmStoreServicer):
    """Provides Methods for implementing the alarm store service"""

    def __init__(self, db_path):
        """Constructor class. Loads the given database."""
        self.db = database.AlarmDatabase(db_path)


    def ListAlarms(self, request, _):
        """Lists all alarms that are stored in the database"""

        alarm_entries = self.db.list()
        response = alarm_pb2.ActionResponse()
        for alarm_key, alarm_value in alarm_entries:
            response.alarms.append( #pylint: disable=no-member
                alarm_pb2.Alarm(
                    id=alarm_key,
                    day=alarm_value['day'],
                    time=alarm_value['time']
                )
            )
        return response


    def UpdateAlarm(self, request, _):
        """Updates a given alarm with the new time and/or day"""

        alarm_dict = {
            'day': request.day,
            'time': request.time
        }
        self.db.update(request.id, alarm_dict)
        return alarm_pb2.ActionResponse.alarms.append(request) #pylint: disable=no-member


    def DeleteAlarm(self, request, _):
        """Deletes a given alarm"""

        self.db.delete(request.id)
        return alarm_pb2.ActionResponse()


    def CreateAlarm(self, request, _):
        """Creates a new alarm"""

        alarm_json = {
            'day': request.day,
            'time': request.time
        }
        alarm_id = str(uuid.uuid4)
        self.db.create(alarm_id, alarm_json)
        new_alarm = alarm_pb2.Alarm(
            id=alarm_id,
            day=request.day,
            time=request.time
        )
        return alarm_pb2.ActionResponse.alarms.append(new_alarm) #pylint: disable=no-member


def serve():
    """Initialises a gRPC server and listens for requests"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    alarm_pb2_grpc.add_AlarmStoreServicer_to_server(
        AlarmStoreServicer('test.db'), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

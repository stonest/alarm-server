"""A servicer to store and retrieve alarm data."""
import uuid
from concurrent import futures

import grpc
from alarm_server import alarm_pb2
from alarm_server import alarm_pb2_grpc
from . import database


class AlarmStoreServicer(alarm_pb2_grpc.AlarmStoreServicer):
    """Provides Methods for implementing the alarm store service"""

    def __init__(self, db_path, db_dump):
        """Constructor class. Loads the given database."""
        self.db = database.AlarmDatabase(db_path, db_dump)


    def ListAlarms(self, request, _):
        """Lists all alarms that are stored in the database"""

        alarm_entries = self.db.list()

        response = alarm_pb2.ActionResponse()
        for alarm_key, alarm_value in alarm_entries.items():
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

        updated_entry = self.db.get(request.id)

        response = alarm_pb2.ActionResponse()
        response.alarms.append(  # pylint: disable=no-member
            alarm_pb2.Alarm(
                id=request.id,
                day=updated_entry['day'],
                time=updated_entry['time']
            ))
        return response


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
        # TODO: Use proper db
        alarm_id = str(uuid.uuid4)
        self.db.create(alarm_id, alarm_json)
        new_alarm = alarm_pb2.Alarm(
            id=alarm_id,
            day=request.day,
            time=request.time
        )
        response = alarm_pb2.ActionResponse()
        response.alarms.append(new_alarm) #pylint: disable=no-member
        return response


def serve():
    """Initialises a gRPC server and listens for requests"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    alarm_pb2_grpc.add_AlarmStoreServicer_to_server(
        AlarmStoreServicer('test.db', True), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

#!/usr/bin/env python3

"""Main entrypoint to start the grpc servicer.
"""

from alarm_server import servicer


def main():
    """Start the servicer
    """
    servicer.serve()

if __name__ == "__main__":
    main()

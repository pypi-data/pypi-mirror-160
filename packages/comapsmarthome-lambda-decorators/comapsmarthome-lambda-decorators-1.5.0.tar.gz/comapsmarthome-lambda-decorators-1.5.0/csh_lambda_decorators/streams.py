import base64
import functools
import logging
import os

from simplejson import loads

from csh_lambda_decorators.stream_event_parsers import noop_event_parser


def process_sns_event(
    _func=None, *, event_parser=noop_event_parser, batch_records=False
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            logging.debug("Received event : {}".format(event))

            if batch_records:
                events = [_parse_sns_record(record) for record in event["Records"]]
                parsed_events = [event_parser(event) for event in events]
                if len(parsed_events[0]) == 1:
                    parsed_events = [parsed_event[0] for parsed_event in parsed_events]
                func(parsed_events)

            else:
                for record in event["Records"]:
                    event = _parse_sns_record(record)
                    func(*event_parser(event))

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def _parse_sns_record(sns_record):
    return loads(sns_record["Sns"]["Message"])


def process_kinesis_event(
    _func=None, *, event_parser=noop_event_parser, batch_records=False
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):
            logging.debug("Received event : {}".format(event))

            if batch_records:
                records = [_parse_kinesis_record(record) for record in event["Records"]]
                parsed_events = [event_parser(record) for record in records]
                if len(parsed_events[0]) == 1:
                    parsed_events = [parsed_event[0] for parsed_event in parsed_events]

                _call_kinesis_processor(lambda: func(parsed_events))

            else:
                for record in event["Records"]:
                    event = _parse_kinesis_record(record)
                    parsed_event = event_parser(event)

                    _call_kinesis_processor(lambda: func(*parsed_event))

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def _parse_kinesis_record(kinesis_record):
    return loads(base64.b64decode(kinesis_record["kinesis"]["data"]).decode("UTF-8"))


def _call_kinesis_processor(processor):
    try:
        processor()
    except Exception as e:
        logging.getLogger().error(
            "An unknown error occurred when trying to process kinesis event"
        )
        logging.getLogger().exception(e)
        if os.environ.get("SILENT_FAILURE", "false").lower() != "true":
            raise e


def process_sqs_event(
    _func=None, *, event_parser=noop_event_parser, batch_records=False
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(event, _context):

            if batch_records:
                commands = [_parse_sqs_record(record) for record in event["Records"]]
                parsed_commands = [event_parser(command) for command in commands]
                if len(parsed_commands[0]) == 1:
                    parsed_commands = [
                        parsed_event[0] for parsed_event in parsed_commands
                    ]
                func(parsed_commands)

            else:
                for record in event["Records"]:
                    command = _parse_sqs_record(record)
                    func(*event_parser(command))

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def _parse_sqs_record(sqs_record):
    return loads(sqs_record["body"])

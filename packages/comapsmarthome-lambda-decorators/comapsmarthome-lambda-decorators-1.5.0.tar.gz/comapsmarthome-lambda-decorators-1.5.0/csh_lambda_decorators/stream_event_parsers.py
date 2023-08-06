def noop_event_parser(event):
    """
    This is the simple default event parser. It simply calls the function without parsing the event
    :param event: The kinesis event
    """
    return (event,)


def frame_sent_event_parser(event):
    """
    This event parser extracts data and metadata from a frame_sent event received from kinesis.

    :param event: The kinesis event
    """
    (
        _frame_type,
        request_frame,
        response_frame,
        serial_number,
        timestamp,
        breadcrumb_id,
        ip_address,
    ) = _extract_transmission_data(event)
    return (
        serial_number,
        request_frame,
        response_frame,
        {
            "timestamp": timestamp,
            "breadcrumb_id": breadcrumb_id,
            "ip_address": ip_address,
        },
    )


def _extract_transmission_data(transmission):
    request_frame = transmission["request_frame"]
    frame_type = request_frame["type"]
    serial_number = (
        request_frame["t5_frame"]["serial_number"]
        if frame_type == 4
        else request_frame["serial_number"]
    )
    response_frame = transmission["response_frame"]
    timestamp = transmission.get("timestamp")
    breadcrumb_id = transmission.get("breadcrumb_id")
    ip_address = transmission.get("ip_address")

    return (
        frame_type,
        request_frame,
        response_frame,
        serial_number,
        timestamp,
        breadcrumb_id,
        ip_address,
    )


def product_attached_event_parser(event):
    """
    This event parser extracts serial_number and housing_id from product_attached event received from sns.

    :param event: The kinesis event
    """
    serial_number = event["serial_number"]
    housing_id = event["housing_id"]
    return serial_number, housing_id

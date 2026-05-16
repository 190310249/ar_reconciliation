def validate_record(payload):

    required_fields = [

        "Invoice Total",

        "Payment Total",

        "Customer Balance"
    ]

    for field in required_fields:

        if field not in payload:
            return False

    invoice_total = float(
        payload.get("Invoice Total", 0)
    )

    if invoice_total < 0:
        return False

    return True
def match_record(payload):

    invoice_total = float(
        payload.get("Invoice Total", 0)
    )

    invoice_applied = float(
        payload.get("Invoice applied amount", 0)
    )

    payment_total = float(
        payload.get("Payment Total", 0)
    )

    payment_applied = float(
        payload.get("Payment applied amount", 0)
    )

    calculated_balance = (
        (invoice_total - invoice_applied)
        -
        (payment_total - payment_applied)
    )

    customer_balance = float(
        payload.get("Customer Balance", 0)
    )

    difference = abs(
        calculated_balance - customer_balance
    )

    return difference <= 10
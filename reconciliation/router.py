def route_decision(matched, validated):

    if matched and validated:
        return "AUTO_APPROVED"

    if matched:
        return "MANUAL_REVIEW"

    return "REJECTED"
from rest_framework.throttling import AnonRateThrottle


class AnonymousRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {
        "anon": "100/day",
    }

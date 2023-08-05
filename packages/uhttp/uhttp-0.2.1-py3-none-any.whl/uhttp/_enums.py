import enum



class ProtocolState(enum.IntEnum):
    CLOSED = 0
    CONNECTING = 1
    CONNECTED = 2
    CLOSING = 3


class HttpState(enum.IntEnum):
    CLOSED = 0
    IDLE = 1
    ACTIVE = 2
    SWITCHING = 3
    SWITCHED = 4


class WebsocketState(enum.IntEnum):
    CLOSED = 0
    CLOSING = 1
    OPEN = 2


class HttpMethod(str, enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTION = 'OPTION'
    HEAD = 'HEAD'
    
    @classmethod
    def get_method(cls, method: str) -> "HttpMethod":
        return cls(method.strip().upper())


class HttpReasonPhrase(enum.IntEnum):

    def __new__(cls, value: int, phrase: str = "") -> "HttpReasonPhrase":
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value
        obj.phrase = phrase  # type: ignore
        return obj

    @classmethod
    def get_reason(cls, value: int) -> str:
        return cls(value).phrase

    # informational
    CONTINUE = 100, "Continue"
    SWITCHING_PROTOCOLS = 101, "Switching Protocols"
    PROCESSING = 102, "Processing"
    EARLY_HINTS = 103, "Early Hints"

    # success
    OK = 200, "OK"
    CREATED = 201, "Created"
    ACCEPTED = 202, "Accepted"
    NON_AUTHORITATIVE_INFORMATION = 203, "Non-Authoritative Information"
    NO_CONTENT = 204, "No Content"
    RESET_CONTENT = 205, "Reset Content"
    PARTIAL_CONTENT = 206, "Partial Content"
    MULTI_STATUS = 207, "Multi-Status"
    ALREADY_REPORTED = 208, "Already Reported"
    IM_USED = 226, "IM Used"

    # redirection
    MULTIPLE_CHOICES = 300, "Multiple Choices"
    MOVED_PERMANENTLY = 301, "Moved Permanently"
    FOUND = 302, "Found"
    SEE_OTHER = 303, "See Other"
    NOT_MODIFIED = 304, "Not Modified"
    USE_PROXY = 305, "Use Proxy"
    TEMPORARY_REDIRECT = 307, "Temporary Redirect"
    PERMANENT_REDIRECT = 308, "Permanent Redirect"

    # client error
    BAD_REQUEST = 400, "Bad Request"
    UNAUTHORIZED = 401, "Unauthorized"
    PAYMENT_REQUIRED = 402, "Payment Required"
    FORBIDDEN = 403, "Forbidden"
    NOT_FOUND = 404, "Not Found"
    METHOD_NOT_ALLOWED = 405, "Method Not Allowed"
    NOT_ACCEPTABLE = 406, "Not Acceptable"
    PROXY_AUTHENTICATION_REQUIRED = 407, "Proxy Authentication Required"
    REQUEST_TIMEOUT = 408, "Request Timeout"
    CONFLICT = 409, "Conflict"
    GONE = 410, "Gone"
    LENGTH_REQUIRED = 411, "Length Required"
    PRECONDITION_FAILED = 412, "Precondition Failed"
    REQUEST_ENTITY_TOO_LARGE = 413, "Request Entity Too Large"
    REQUEST_URI_TOO_LONG = 414, "Request-URI Too Long"
    UNSUPPORTED_MEDIA_TYPE = 415, "Unsupported Media Type"
    REQUESTED_RANGE_NOT_SATISFIABLE = 416, "Requested Range Not Satisfiable"
    EXPECTATION_FAILED = 417, "Expectation Failed"
    IM_A_TEAPOT = 418, "I'm a teapot"
    MISDIRECTED_REQUEST = 421, "Misdirected Request"
    UNPROCESSABLE_ENTITY = 422, "Unprocessable Entity"
    LOCKED = 423, "Locked"
    FAILED_DEPENDENCY = 424, "Failed Dependency"
    TOO_EARLY = 425, "Too Early"
    UPGRADE_REQUIRED = 426, "Upgrade Required"
    PRECONDITION_REQUIRED = 428, "Precondition Required"
    TOO_MANY_REQUESTS = 429, "Too Many Requests"
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431, "Request Header Fields Too Large"
    UNAVAILABLE_FOR_LEGAL_REASONS = 451, "Unavailable For Legal Reasons"

    # server errors
    INTERNAL_SERVER_ERROR = 500, "Internal Server Error"
    NOT_IMPLEMENTED = 501, "Not Implemented"
    BAD_GATEWAY = 502, "Bad Gateway"
    SERVICE_UNAVAILABLE = 503, "Service Unavailable"
    GATEWAY_TIMEOUT = 504, "Gateway Timeout"
    HTTP_VERSION_NOT_SUPPORTED = 505, "HTTP Version Not Supported"
    VARIANT_ALSO_NEGOTIATES = 506, "Variant Also Negotiates"
    INSUFFICIENT_STORAGE = 507, "Insufficient Storage"
    LOOP_DETECTED = 508, "Loop Detected"
    NOT_EXTENDED = 510, "Not Extended"
    NETWORK_AUTHENTICATION_REQUIRED = 511, "Network Authentication Required"


class WebsocketReasonPhrase(enum.IntEnum):
    def __new__(cls, value: int, phrase: str = "") -> "WebsocketReasonPhrase":
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value
        obj.phrase = phrase  # type: ignore
        return obj
    
    @classmethod
    def get_reason(cls, value: int) -> str:
        return cls(value).phrase

    NORMAL_CLOSURE = 1000, "Normal closure"
    GOING_AWAY = 1001, "Going away"
    PROTOCOL_ERROR = 1002, "Protocol error"
    UNSUPPORTED_DATA = 1003, "Unsupported data"
    RESERVED = 1004, "Reserved"
    NO_STATUS_RCVD = 1005, "No status received"
    ABNORMAL_CLOSURE = 1006, "Abnormal closure"
    INVALID_FRAME = 1007, "Invalid frame payload data"
    POLICY_VIOLATION = 1008, "Policy violation"
    MESSAGE_TOO_BIG = 1009, "Message too big"
    MANDATORY_EXT = 1010, "Mandatory extension"
    INTERNAL_ERR = 1011, "Internal error"
    SERVICE_RESTART = 1012, "Service restart"
    TRY_AGAIN_LATER = 1013, "Try again later"
    INVALID_UPSTREAM_RESPONSE = 1014, (
        "The server was acting as a gateway or "
        "proxy and received an invalid response from the upstream server"
    )
    TLS_HANDSHAKE = 1015, "Bad TLS handshake"
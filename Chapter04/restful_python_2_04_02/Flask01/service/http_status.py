from enum import Enum


class HttpStatus(Enum):
    continue_100 = 100
    switching_protocols_101 = 101
    ok_200 = 200
    created_201 = 201
    accepted_202 = 202
    non_authoritative_information_203 = 203
    no_content_204 = 204
    reset_content_205 = 205
    partial_content_206 = 206
    multiple_choices_300 = 300
    moved_permanently_301 = 301
    found_302 = 302
    see_other_303 = 303
    not_modified_304 = 304
    use_proxy_305 = 305
    reserved_306 = 306
    temporary_redirect_307 = 307
    bad_request_400 = 400
    unauthorized_401 = 401
    payment_required_402 = 402
    forbidden_403 = 403
    not_found_404 = 404
    method_not_allowed_405 = 405
    not_acceptable_406 = 406
    proxy_authentication_required_407 = 407
    request_timetout_408 = 408
    conflict_409 = 409
    gone_410 = 410
    length_required_411 = 411
    precondition_failed_412 = 412
    request_entity_too_large_413 = 413
    request_uri_too_long_414 = 414
    unsupported_media_type_415 = 415
    requested_range_not_satisfiable_416 = 416
    expectation_failed_417 = 417
    precondition_required_428 = 428
    too_many_requests_429 = 429
    request_header_fields_too_large_431 = 431
    unavailable_for_legal_reasons_451 = 451
    internal_server_error_500 = 500
    not_implemented_501 = 501
    bad_gateway_502 = 502
    service_unavailable_503 = 503
    gateway_timeout_504 = 504
    http_version_not_supported_505 = 505
    network_authentication_required_511 = 511

    @staticmethod
    def is_informational(cls, status_code):
        return 100 <= status_code.value <= 199

    @staticmethod
    def is_success(status_code):
        return 200 <= status_code.value <= 299

    @staticmethod
    def is_redirect(status_code):
        return 300 <= status_code.value <= 399

    @staticmethod
    def is_client_error(status_code):
        return 400 <= status_code.value <= 499

    @staticmethod
    def is_server_error(status_code):
        return 500 <= status_code.value <= 599

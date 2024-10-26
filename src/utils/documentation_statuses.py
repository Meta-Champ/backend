def generate_status(description: str, detail: str):
    return {
        'description': description,
        'content': {
            'application/json': { 
                'example': { 'detail': detail } 
            }
        }
    }


__100__ = generate_status(description='Continue', detail='continue')
__101__ = generate_status(description='Switching Protocols', detail='switching_protocols')

__200__ = generate_status(description='OK', detail='ok')
__201__ = generate_status(description='Created', detail='created')
__202__ = generate_status(description='Accepted', detail='accepted')
__203__ = generate_status(description='Non-Authoritative Information', detail='non_authoritative_info')
__204__ = generate_status(description='No Content', detail='no_content')
__205__ = generate_status(description='Reset Content', detail='reset_content')
__206__ = generate_status(description='Partial Content', detail='partial_content')

__300__ = generate_status(description='Multiple Choices', detail='multiple_choices')
__301__ = generate_status(description='Moved Permanently', detail='moved_permanently')
__302__ = generate_status(description='Found', detail='found')
__303__ = generate_status(description='See Other', detail='see_other')
__304__ = generate_status(description='Not Modified', detail='not_modified')
__307__ = generate_status(description='Temporary Redirect', detail='temporary_redirect')
__308__ = generate_status(description='Permanent Redirect', detail='permanent_redirect')

__400__ = generate_status(description='Bad Request', detail='bad_request')
__401__ = generate_status(description='Unauthorized', detail='unauthorized')
__402__ = generate_status(description='Payment Required', detail='payment_required')
__403__ = generate_status(description='Forbidden', detail='forbidden')
__404__ = generate_status(description='Not Found', detail='not_found')
__405__ = generate_status(description='Method Not Allowed', detail='method_not_allowed')
__406__ = generate_status(description='Not Acceptable', detail='not_acceptable')
__407__ = generate_status(description='Proxy Authentication Required', detail='proxy_authentication_required')
__408__ = generate_status(description='Request Timeout', detail='request_timeout')
__409__ = generate_status(description='Conflict', detail='conflict')
__410__ = generate_status(description='Gone', detail='gone')
__411__ = generate_status(description='Length Required', detail='length_required')
__412__ = generate_status(description='Precondition Failed', detail='precondition_failed')
__413__ = generate_status(description='Payload Too Large', detail='payload_too_large')
__414__ = generate_status(description='URI Too Long', detail='uri_too_long')
__415__ = generate_status(description='Unsupported Media Type', detail='unsupported_media_type')
__416__ = generate_status(description='Range Not Satisfiable', detail='range_not_satisfiable')
__417__ = generate_status(description='Expectation Failed', detail='expectation_failed')
__418__ = generate_status(description="I'm a teapot", detail='im_a_teapot')
__422__ = generate_status(description='Unprocessable Entity', detail='unprocessable_entity')
__426__ = generate_status(description='Upgrade Required', detail='upgrade_required')
__429__ = generate_status(description='Too Many Requests', detail='too_many_requests')

__500__ = generate_status(description='Internal Server Error', detail='internal_server_error')
__501__ = generate_status(description='Not Implemented', detail='not_implemented')
__502__ = generate_status(description='Bad Gateway', detail='bad_gateway')
__503__ = generate_status(description='Service Unavailable', detail='service_unavailable')
__504__ = generate_status(description='Gateway Timeout', detail='gateway_timeout')
__505__ = generate_status(description='HTTP Version Not Supported', detail='http_version_not_supported')

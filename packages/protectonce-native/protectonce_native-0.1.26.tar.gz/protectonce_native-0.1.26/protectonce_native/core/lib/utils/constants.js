module.exports = {
    PROTECT_ONCE_CONFIG_FILE_ENV: 'PROTECT_ONCE_CONFIG_FILE',
    PROTECT_ONCE_CONFIG_TOKEN_BASE_KEY: 'protectOnceToken',
    PROTECT_ONCE_CONFIG_CLIENT_ID_KEY: 'clientId',
    PROTECT_ONCE_CONFIG_TOKEN_KEY: 'token',
    PROTECT_ONCE_CONFIG_ENDPOINT_KEY: 'endpoint',
    PROTECT_ONCE_CONFIG_ENDPOINT_PORT_KEY: 'port',

    BACKEND_REST_API_URL_ENV: 'PO_ENDPOINT',
    BACKEND_REST_API_PORT_ENV: 'PO_ENDPOINT_PORT',
    BACKEND_REST_API_CLIENT_ID_ENV: 'PO_CLIENTID',
    BACKEND_REST_API_TOKEN_ENV: 'PO_TOKEN',

    BACKEND_REST_API_TOKEN_KEY: 'accessToken',
    BACKEND_REST_API_REFRESH_TOKEN_KEY: 'refreshToken',
    BACKEND_REST_API_REFRESH_TOKEN_HEADER: 'x-protectonce-refresh-token',

    HEARTBEAT_HASH_KEY: 'hash',
    HEARTBEAT_REPORT_KEY: 'reports',
    HEARTBEAT_INVENTORY_KEY: 'inventory',
    HEARTBEAT_WORKLOADID_KEY: 'workLoadId',
    HEARTBEAT_AGENTID_KEY: 'agentId',
    HEARTBEAT_DYNAMIC_BOM_KEY: 'dynamicBom',

    APP_DELETE_STATUS_CODE: 404,

    PATH_TRIMMING_REGEX: /\/+$/g, //RegEx for trimming unnecessary / from path

    // REST API Paths
    REST_API_LOGIN: '/login',
    REST_API_HEART_BEAT: '/heartbeat',

    //Event Types
    RASP_EVENT_TYPE: 'rasp',
    WAF_EVENT_TYPE: 'waf',

    WORKLOAD_ID_SEPARATOR: '##',

    PLAYBOOK_EVENT_TYPE: 'playbook',

    //Filter Request constants
    //Comparator Key
    IP_FILTER_KEY: 'IP',
    PATH_FILTER_KEY: 'PATH',
    PARAMETER_FILTER_KEY: 'PARAMETER',
    USER_FILTER_KEY: 'USER',
    USER_IP_FILTER_KEY: 'USER_IP',

    //Event Attributes
    RESPONSE_STATUS_KEY: 'response.status',
    REQUEST_HEADERS_CONTENT_TYPE_KEY: 'request.headers.content-type',
    RESPONSE_HEADERS_CONTENT_TYPE_KEY: 'response.headers.content-type',
    BLOCKED_KEY: 'blocked',
    APPLICATION_ENV_KEY: 'application_environment',
    IP_ADDRESSES_KEY: 'ip_addresses',

    //Outgoing Request ID 
    OUTGOING_REQUEST_HEADER_POREQUESTID: 'X-ProtectOnce-Request-Id',

    // AWS Event sources
    AWS_LAMBDA_EVENT_SOURCE: {
        CLOUD_FRONT: 'Cloudfront',
        CODE_COMMIT: 'CodeCommit',
        SES: 'Ses',
        SNS: 'Sns',
        DYNAMODB: 'DynamoDb',
        KINESIS: 'Kinesis',
        S3: 'S3',
        KINESIS_FIREHOSE: 'KinesisFirehose',
        MOBILE_BACKEND: 'MobileBackend',
        AWS_CONFIG: 'AwsConfig',
        API_GATEWAY_AUTHORIZER: 'ApiGatewayAuthorizer',
        CLOUD_FORMATION: 'CloudFormation',
        API_GATEWAY_AWS_PROXY: 'ApiGatewayAwsProxy',
        SCHEDULED_EVENT: 'ScheduledEvent',
        CLOUD_WATCH_LOGS: 'CloudWatchLogs',
        CONGNITO_SYNC_TRIGGER: 'CognitoSyncTrigger'
    },

    // AWS Event Values
    AWS_LAMBDA_EVENT_SOURCE_VALUE: {
        CODE_COMMIT: 'aws:codecommit',
        SES: 'aws:ses',
        SNS: 'aws:sns',
        DYNAMODB: 'aws:dynamodb',
        KINESIS: 'aws:kinesis',
        S3: 'aws:s3',
        KINESIS_FIREHOSE: 'arn:aws:kinesis:',
        API_GATEWAY_AUTHORIZER: 'incoming-client-token',
        SCHEDULED_EVENT: 'aws.events',
        CONGNITO_SYNC_TRIGGER: 'SyncTrigger'
    },
    SUPPORTED_HTTP_METHODS: [
        'GET',
        'PUT',
        'POST',
        'DELETE',
        'PATCH',
        'HEAD',
        'OPTIONS',
        'CONNECT',
        'TRACE'
    ]
}

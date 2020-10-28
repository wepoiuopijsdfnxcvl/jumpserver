# -*- coding: utf-8 -*-
#
from ..const import CONFIG, DYNAMIC

# Storage settings
COMMAND_STORAGE = {
    'ENGINE': 'terminal.backends.command.db',
}
DEFAULT_TERMINAL_COMMAND_STORAGE = {
    "default": {
        "TYPE": "server",
    },
}
TERMINAL_COMMAND_STORAGE = DYNAMIC.TERMINAL_COMMAND_STORAGE or {}

# Server 类型的录像存储
SERVER_REPLAY_STORAGE = CONFIG.SERVER_REPLAY_STORAGE
# SERVER_REPLAY_STORAGE = {
#     'TYPE': 's3',
#     'BUCKET': '',
#     'ACCESS_KEY': '',
#     'SECRET_KEY': '',
#     'ENDPOINT': ''
# }

DEFAULT_TERMINAL_REPLAY_STORAGE = {
    "default": {
        "TYPE": "server",
    },
}
TERMINAL_REPLAY_STORAGE = DYNAMIC.TERMINAL_REPLAY_STORAGE

# Security settings
SECURITY_MFA_AUTH = DYNAMIC.SECURITY_MFA_AUTH
SECURITY_COMMAND_EXECUTION = DYNAMIC.SECURITY_COMMAND_EXECUTION
SECURITY_LOGIN_LIMIT_COUNT = DYNAMIC.SECURITY_LOGIN_LIMIT_COUNT
SECURITY_LOGIN_LIMIT_TIME = DYNAMIC.SECURITY_LOGIN_LIMIT_TIME  # Unit: minute
SECURITY_MAX_IDLE_TIME = DYNAMIC.SECURITY_MAX_IDLE_TIME  # Unit: minute
SECURITY_PASSWORD_EXPIRATION_TIME = DYNAMIC.SECURITY_PASSWORD_EXPIRATION_TIME # Unit: day
SECURITY_PASSWORD_MIN_LENGTH = DYNAMIC.SECURITY_PASSWORD_MIN_LENGTH  # Unit: bit
SECURITY_PASSWORD_UPPER_CASE = DYNAMIC.SECURITY_PASSWORD_UPPER_CASE
SECURITY_PASSWORD_LOWER_CASE = DYNAMIC.SECURITY_PASSWORD_LOWER_CASE
SECURITY_PASSWORD_NUMBER = DYNAMIC.SECURITY_PASSWORD_NUMBER
SECURITY_PASSWORD_SPECIAL_CHAR = DYNAMIC.SECURITY_PASSWORD_SPECIAL_CHAR
SECURITY_PASSWORD_RULES = [
    'SECURITY_PASSWORD_MIN_LENGTH',
    'SECURITY_PASSWORD_UPPER_CASE',
    'SECURITY_PASSWORD_LOWER_CASE',
    'SECURITY_PASSWORD_NUMBER',
    'SECURITY_PASSWORD_SPECIAL_CHAR'
]
SECURITY_MFA_VERIFY_TTL = CONFIG.SECURITY_MFA_VERIFY_TTL
SECURITY_VIEW_AUTH_NEED_MFA = CONFIG.SECURITY_VIEW_AUTH_NEED_MFA
SECURITY_SERVICE_ACCOUNT_REGISTRATION = DYNAMIC.SECURITY_SERVICE_ACCOUNT_REGISTRATION
SECURITY_LOGIN_CAPTCHA_ENABLED = CONFIG.SECURITY_LOGIN_CAPTCHA_ENABLED
SECURITY_LOGIN_CHALLENGE_ENABLED = CONFIG.SECURITY_LOGIN_CHALLENGE_ENABLED
SECURITY_DATA_CRYPTO_ALGO = CONFIG.SECURITY_DATA_CRYPTO_ALGO
SECURITY_CRYPTO_GM_SM2_PUBLIC_KEY = CONFIG.SECURITY_CRYPTO_GM_SM2_PUBLIC_KEY
SECURITY_CRYPTO_GM_SM2_PRIVATE_KEY = CONFIG.SECURITY_CRYPTO_GM_SM2_PRIVATE_KEY

# Terminal other setting
TERMINAL_PASSWORD_AUTH = DYNAMIC.TERMINAL_PASSWORD_AUTH
TERMINAL_PUBLIC_KEY_AUTH = DYNAMIC.TERMINAL_PUBLIC_KEY_AUTH
TERMINAL_HEARTBEAT_INTERVAL = DYNAMIC.TERMINAL_HEARTBEAT_INTERVAL
TERMINAL_ASSET_LIST_SORT_BY = DYNAMIC.TERMINAL_ASSET_LIST_SORT_BY
TERMINAL_ASSET_LIST_PAGE_SIZE = DYNAMIC.TERMINAL_ASSET_LIST_PAGE_SIZE
TERMINAL_SESSION_KEEP_DURATION = DYNAMIC.TERMINAL_SESSION_KEEP_DURATION
TERMINAL_HOST_KEY = DYNAMIC.TERMINAL_HOST_KEY
TERMINAL_HEADER_TITLE = DYNAMIC.TERMINAL_HEADER_TITLE
TERMINAL_TELNET_REGEX = DYNAMIC.TERMINAL_TELNET_REGEX

# User or user group permission cache time, default 3600 seconds
ASSETS_PERM_CACHE_ENABLE = CONFIG.ASSETS_PERM_CACHE_ENABLE
ASSETS_PERM_CACHE_TIME = CONFIG.ASSETS_PERM_CACHE_TIME

# Asset user auth external backend, default AuthBook backend
BACKEND_ASSET_USER_AUTH_VAULT = False

DEFAULT_ORG_SHOW_ALL_USERS = CONFIG.DEFAULT_ORG_SHOW_ALL_USERS
PERM_SINGLE_ASSET_TO_UNGROUP_NODE = CONFIG.PERM_SINGLE_ASSET_TO_UNGROUP_NODE
PERM_EXPIRED_CHECK_PERIODIC = CONFIG.PERM_EXPIRED_CHECK_PERIODIC
WINDOWS_SSH_DEFAULT_SHELL = CONFIG.WINDOWS_SSH_DEFAULT_SHELL
FLOWER_URL = CONFIG.FLOWER_URL

# Enable internal period task
PERIOD_TASK_ENABLED = CONFIG.PERIOD_TASK_ENABLED

# only allow single machine login with the same account
USER_LOGIN_SINGLE_MACHINE_ENABLED = CONFIG.USER_LOGIN_SINGLE_MACHINE_ENABLED

# Email custom content
EMAIL_SUBJECT_PREFIX = DYNAMIC.EMAIL_SUBJECT_PREFIX
EMAIL_SUFFIX = DYNAMIC.EMAIL_SUFFIX
EMAIL_CUSTOM_USER_CREATED_SUBJECT = DYNAMIC.EMAIL_CUSTOM_USER_CREATED_SUBJECT
EMAIL_CUSTOM_USER_CREATED_HONORIFIC = DYNAMIC.EMAIL_CUSTOM_USER_CREATED_HONORIFIC
EMAIL_CUSTOM_USER_CREATED_BODY = DYNAMIC.EMAIL_CUSTOM_USER_CREATED_BODY
EMAIL_CUSTOM_USER_CREATED_SIGNATURE = DYNAMIC.EMAIL_CUSTOM_USER_CREATED_SIGNATURE

DISPLAY_PER_PAGE = CONFIG.DISPLAY_PER_PAGE
DEFAULT_EXPIRED_YEARS = 70
USER_GUIDE_URL = DYNAMIC.USER_GUIDE_URL
HTTP_LISTEN_PORT = CONFIG.HTTP_LISTEN_PORT
WS_LISTEN_PORT = CONFIG.WS_LISTEN_PORT
LOGIN_LOG_KEEP_DAYS = DYNAMIC.LOGIN_LOG_KEEP_DAYS
TASK_LOG_KEEP_DAYS = CONFIG.TASK_LOG_KEEP_DAYS
ORG_CHANGE_TO_URL = CONFIG.ORG_CHANGE_TO_URL
WINDOWS_SKIP_ALL_MANUAL_PASSWORD = CONFIG.WINDOWS_SKIP_ALL_MANUAL_PASSWORD

AUTH_EXPIRED_SECONDS = 60 * 5

# XPACK
XPACK_LICENSE_IS_VALID = DYNAMIC.XPACK_LICENSE_IS_VALID

XPACK_INTERFACE_LOGIN_TITLE = DYNAMIC.XPACK_INTERFACE_LOGIN_TITLE

LOGO_URLS = DYNAMIC.LOGO_URLS

CHANGE_AUTH_PLAN_SECURE_MODE_ENABLED = CONFIG.CHANGE_AUTH_PLAN_SECURE_MODE_ENABLED

DATETIME_DISPLAY_FORMAT = '%Y-%m-%d %H:%M:%S'

TICKETS_ENABLED = CONFIG.TICKETS_ENABLED
REFERER_CHECK_ENABLED = CONFIG.REFERER_CHECK_ENABLED

# -*- coding: utf-8

COBRANDCARD="fudan001"  #联名卡类型编码
COBRANDCARD1="newyorktype001"  #联名卡类型编码
COBRANDCARD2="tongjitype001"  #联名卡类型编码
COBRANDCARD_CAR="0170000506000049"  #联名卡类型编码
PARTNERNO="06000047"  #合作方标识
PARTNERNO_CAR="06000049"  #合作方标识
PARTNERNO1="newyork001"  #合作方标识
PARTNERNO2="tongji001"  #合作方标识








class HttpStatusCode(object):
    NO_ERROR = 200
    SYSTEM_ERROR = 500
    SYSTEM_TEMP_ERROR = 503
    END_SESSION = 204
    HTTP_NOT_FOUND = 404
    RETRY_WITH_URL = 308
    UNAUTHORIZED = 401
    NOT_MODIFIED = 304

    status_dictionary = {
        NO_ERROR: 'Http Status Ok ! ',
        SYSTEM_ERROR: 'System Error ! ',
        SYSTEM_TEMP_ERROR: 'System Temporary Error!',
        HTTP_NOT_FOUND: 'Http Not Found ! ',
        END_SESSION: 'Session End ! ',
        RETRY_WITH_URL: 'Retry With New URL!',
        UNAUTHORIZED: 'Invalid Authentication ! ',
        NOT_MODIFIED: 'No New Message ! '
    }

    @staticmethod
    def get_description(status_code):
        return HttpStatusCode.status_dictionary[status_code]

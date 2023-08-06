# -*- coding =utf-8 -*-
import logging
from enum import IntEnum

logger = logging.getLogger(__name__)


class HTTPStatus(IntEnum):
    """HTTP status codes and reason phrases
    Status codes from the following RFCs are all observed =
        * RFC 7231 = Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
        * RFC 6585 = Additional HTTP Status Codes
        * RFC 3229 = Delta encoding in HTTP
        * RFC 4918 = HTTP Extensions for WebDAV, obsoletes 2518
        * RFC 5842 = Binding Extensions to WebDAV
        * RFC 7238 = Permanent Redirect
        * RFC 2295 = Transparent Content Negotiation in HTTP
        * RFC 2774 = An HTTP Extension Framework
    """
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    # informational
    SUCCESS = 0, 'success', 'Success'
    # CONTINUE = 100, 'Continue', 'Request received, please continue'
    # SWITCHING_PROTOCOLS = (101, 'Switching Protocols', 'Switching to new protocol; obey Upgrade header')
    # PROCESSING = 102, 'Processing'
    #
    # # success
    # OK = 200, 'OK', 'Request fulfilled, document follows'
    # CREATED = 201, 'Created', 'Document created, URL follows'
    # ACCEPTED = (202, 'Accepted', 'Request accepted, processing continues off-line')
    # NON_AUTHORITATIVE_INFORMATION = (203, 'Non-Authoritative Information', 'Request fulfilled from cache')
    # NO_CONTENT = 204, 'No Content', 'Request fulfilled, nothing follows'
    # RESET_CONTENT = 205, 'Reset Content', 'Clear input form for further input'
    # PARTIAL_CONTENT = 206, 'Partial Content', 'Partial content follows'
    # MULTI_STATUS = 207, 'Multi-Status'
    # ALREADY_REPORTED = 208, 'Already Reported'
    # IM_USED = 226, 'IM Used'
    #
    # # redirection
    # MULTIPLE_CHOICES = (300, 'Multiple Choices', 'Object has several resources -- see URI list')
    # MOVED_PERMANENTLY = (301, 'Moved Permanently', 'Object moved permanently -- see URI list')
    # FOUND = 302, 'Found', 'Object moved temporarily -- see URI list'
    # SEE_OTHER = 303, 'See Other', 'Object moved -- see Method and URL list'
    # NOT_MODIFIED = (304, 'Not Modified', 'Document has not changed since given time')
    # USE_PROXY = (305, 'Use Proxy', 'You must use proxy specified in Location to access this resource')
    # TEMPORARY_REDIRECT = (307, 'Temporary Redirect', 'Object moved temporarily -- see URI list')
    # PERMANENT_REDIRECT = (308, 'Permanent Redirect', 'Object moved temporarily -- see URI list')
    #
    # # client error
    # BAD_REQUEST = (400, 'Bad Request', 'Bad request syntax or unsupported method')
    # UNAUTHORIZED = (401, 'Unauthorized', 'No permission -- see authorization schemes')
    # PAYMENT_REQUIRED = (402, 'Payment Required', 'No payment -- see charging schemes')
    # FORBIDDEN = (403, 'Forbidden', 'Request forbidden -- authorization will not help')
    # NOT_FOUND = (404, 'Not Found', 'Nothing matches the given URI')
    # METHOD_NOT_ALLOWED = (405, 'Method Not Allowed', 'Specified method is invalid for this resource')
    # NOT_ACCEPTABLE = (406, 'Not Acceptable', 'URI not available in preferred format')
    # PROXY_AUTHENTICATION_REQUIRED = (407, 'Proxy Authentication Required',
    #                                  'You must authenticate with this proxy before proceeding')
    # REQUEST_TIMEOUT = (408, 'Request Timeout', 'Request timed out; try again later')
    # CONFLICT = 409, 'Conflict', 'Request conflict'
    # GONE = (410, 'Gone', 'URI no longer exists and has been permanently removed')
    # LENGTH_REQUIRED = (411, 'Length Required', 'Client must specify Content-Length')
    # PRECONDITION_FAILED = (412, 'Precondition Failed', 'Precondition in headers is false')
    # REQUEST_ENTITY_TOO_LARGE = (413, 'Request Entity Too Large', 'Entity is too large')
    # REQUEST_URI_TOO_LONG = (414, 'Request-URI Too Long', 'URI is too long')
    # UNSUPPORTED_MEDIA_TYPE = (415, 'Unsupported Media Type', 'Entity body in unsupported format')
    # REQUESTED_RANGE_NOT_SATISFIABLE = (416, 'Requested Range Not Satisfiable', 'Cannot satisfy request range')
    # EXPECTATION_FAILED = (417, 'Expectation Failed', 'Expect condition could not be satisfied')
    # UNPROCESSABLE_ENTITY = 422, 'Unprocessable Entity'
    # LOCKED = 423, 'Locked'
    # FAILED_DEPENDENCY = 424, 'Failed Dependency'
    # UPGRADE_REQUIRED = 426, 'Upgrade Required'
    # PRECONDITION_REQUIRED = (428, 'Precondition Required', 'The origin server requires the request to be conditional')
    # TOO_MANY_REQUESTS = (429, 'Too Many Requests',
    #                      'The user has sent too many requests in a given amount of time ("rate limiting")')
    # REQUEST_HEADER_FIELDS_TOO_LARGE = (431, 'Request Header Fields Too Large',
    #                                    'The server is unwilling to process the request because its header fields are too large')
    #
    # # server errors
    # INTERNAL_SERVER_ERROR = (500, 'Internal Server Error', 'Server got itself in trouble')
    # NOT_IMPLEMENTED = (501, 'Not Implemented', 'Server does not support this operation')
    # BAD_GATEWAY = (502, 'Bad Gateway', 'Invalid responses from another server/proxy')
    # SERVICE_UNAVAILABLE = (503, 'Service Unavailable', 'The server cannot process the request due to a high load')
    # GATEWAY_TIMEOUT = (504, 'Gateway Timeout', 'The gateway server did not receive a timely response')
    # HTTP_VERSION_NOT_SUPPORTED = (505, 'HTTP Version Not Supported', 'Cannot fulfill request')
    # VARIANT_ALSO_NEGOTIATES = 506, 'Variant Also Negotiates'
    # INSUFFICIENT_STORAGE = 507, 'Insufficient Storage'
    # LOOP_DETECTED = 508, 'Loop Detected'
    # NOT_EXTENDED = 510, 'Not Extended'
    # NETWORK_AUTHENTICATION_REQUIRED = (511, 'Network Authentication Required',
    #                                    'The client needs to authenticate to gain network access')

    # 通用
    REQUEST_PATH_ERR = (400001, '请求路径错误', '请求路径错误')
    REQUEST_METHOD_ERR = (400002, "请求方法错误，请使用 POST 请求",
                          "请求方法错误，请使用 POST 请求")
    BODY_EMPTY_ERR = (400003, "Body 内容为空", "Body 请求数据为空，没有包含内容")
    BODY_JSON_ERR = (400004, "Body 请求体非 json 格式", "Body内容需要符合 json 要求")
    BODY_TYPE_ERR = (400005, "请求体类型错误", "请求体需为字典，不能为其他类型")
    
    # image input 图片
    MUST_PRAM_ERR = (400006, "必传的参数未传", "必须的参数（Action、ImageData）未传")
    ILLEGAL_PRAM_ERR = (400007, "传递非法参数",
                        "body字典内有除（Action、ImageData）外的参数")
    PRAM_TYPE_ERR = (400008, "请求体的字段类型错误",
                     "请求体的字段（Action、ImageData）类型错误，类型只能为字符串，不能为其他类型")
    ACTION_VALUE_ERR = (400009, "Action 值设置错误", "Action 值设置错误")
    IMAGE_DATA_EMPTY_ERR = (400010, "ImageData 字段值为空字符", "ImageData 字段值为空字符")
    IMAGE_DATA_BASE64_ERR = (400011, "ImageData 字段 base64 数据处理异常",
                             "ImageData 字段的 base64 字符串转换字节码异常")
    IMAGE_TYPE_ERR = (400012, "请求文件格式不合法", "仅支持 jpeg/png/jpg/bmp 格式")
    IMAGE_SIZE_ERR = (400013, "图片文件大小不符合要求",
                      "该文件大小不符合要求,静态图片要求小于 7M")
    IMAGE_DECODE_ERR = (400014, "图片解码错误", "字节码解码为图片错误")
    IMAGE_SHAPE_ERR = (400015, "图片尺寸不符合要求", "分辨率长宽尺寸应不高于 5000 不低于 32")
    

    # image 图片比对
    IMAGE_AB_MUST_PRAM_ERR = (400101, "必传的参数未传", "必须的参数（Action、ImageDataA、ImageDataB）未传")
    IMAGE_AB_PRAM_TYPE_ERR = (400102, "请求体的字段类型错误",
                     "请求体的字段（Action、ImageDataA、ImageDataB）类型错误，类型只能为字符串，不能为其他类型")
    IMAGE_AB_DATA_EMPTY_ERR = (400103, "ImageDataA 或 ImageDataB 字段值为空字符", "ImageDataA 或 ImageDataB 字段值为空字符")
    IMAGE_AB_DATA_BASE64_ERR = (400104, "ImageDataA 或 ImageDataB 字段 base64 数据处理异常",
                             "ImageDataA 或 ImageDataB 字段的 base64 字符串转换字节码异常")
    
    # image support type 图片格式
    IMAGE_TYPE_WEBP_ERR = (400201, "请求文件格式不合法", "仅支持 jpeg/png/jpg/bmp/webp 格式")
    IMAGE_TYPE_GIF_ERR = (400202, "请求文件格式不合法", "仅支持 jpeg/png/jpg/bmp/gif 格式")
    IMAGE_TYPE_TIFF_ERR = (400203, "请求文件格式不合法", "仅支持 jpeg/png/jpg/bmp/tiff 格式")
    IMAGE_TYPE_WEBP_GIF_TIFF_ERR = (400204, "请求文件格式不合法", "仅支持 jpeg/png/jpg/bmp/webp/tiff/gif 格式")
    
    # text input
    TEXT_MUST_PRAM_ERR = (410001, "必传的参数未传", "必须的参数（Action、TextData）未传")
    TEXT_PRAM_TYPE_ERR = (410002, "请求体的字段类型错误",
                     "请求体的字段（Action、TextData）类型错误，类型只能为字符串，不能为其他类型")
    TEXT_DATA_EMPTY_ERR = (410003, "TextData 字段值为空字符", "TextData 字段值为空字符")
    TEXT_ILLEGAL_ERR = (410004, "文本含有非法字符", "文本含有非法字符")
    TEXT_NOT_UTF8_ERR = (410005, "文本不是 UTF8 格式", "文本不是 UTF8 格式")
    TEXT_TOO_SHORT_ERR = (410006, "文本输入过短", "文本输入过短，请参考接口文档说明")
    TEXT_TOO_LONG_ERR = (410007, "文本输入过长", "文本输入过长，请参考接口文档说明")
    
    # audio input  42
    
    # video input 43
    
    # url input 44
    IMAGE_URL_LIST_TYPE_ERR = (440001, "ImageURL 字段类型错误", "ImageURL 字段应该是 list 类型")
    IMAGE_URL_STRING_TYPE_ERR = (440002, "ImageURL 字段类型错误", "ImageURL 字段应该是 string 类型")
    IMAGE_URL_VALUE_ERR = (440003, "ImageURL 字段不符合规范", "ImageURL 字段不符合规范，请参考接口文档说明")
    IMAGE_URL_EMPTY_ERR = (440004, "ImageURL 字段值为空字符", "ImageURL 字段值为空字符")
    IMAGE_URL_DOWNLOAD_ERR = (440005, "图片链接下载失败", "无法解析图片链接，下载失败")

    
    # 业务字段判断 45xxxx
    # 语音合成 TTS
    VOICE_TYPE_INT_TYPE_ERR = (450001, "VoiceType 字段类型错误", "VoiceType 字段应该是 int 类型")
    VOICE_TYPE_VALUE_ERR = (450002, "VoiceType 字段不符合规范", "VoiceType 字段不符合规范，请参考接口文档说明")
    PITCH_FLOAT_TYPE_ERR = (450003, "Pitch 字段类型错误", "Pitch 字段应该是 float 类型")
    PITCH_VALUE_ERR = (450004, "Pitch 字段不符合规范", "Pitch 字段不符合规范，请参考接口文档说明")
    SPEED_FLOAT_TYPE_ERR = (450005, "Speed 字段类型错误", "Speed 字段应该是 float 类型")
    SPEED_VALUE_ERR = (450006, "Speed 字段不符合规范", "Speed 字段不符合规范，请参考接口文档说明")
    # 行人检测 PersonDetect
    PERSON_THRESH_FLOAT_TYPE_ERR = (450007, "PersonThresh 字段类型错误", "PersonThresh 字段应该是 float 类型")
    PERSON_THRESH_VALUE_ERR = (450008, "PersonThresh 字段不符合规范", "PersonThresh 字段不符合规范，请参考接口文档说明")
    # 人脸检测 FaceDetect
    FACE_THRESH_FLOAT_TYPE_ERR = (450009, "FaceThresh 字段类型错误", "FaceThresh 字段应该是 float 类型")
    FACE_THRESH_VALUE_ERR = (450010, "FaceThresh 字段不符合规范", "FaceThresh 字段不符合规范，请参考接口文档说明")
    # 明火烟雾检测 FireDetect
    FIRE_THRESH_FLOAT_TYPE_ERR = (450011, "FireThresh 字段类型错误", "FireThresh 字段应该是 float 类型")
    FIRE_THRESH_VALUE_ERR = (450012, "FireThresh 字段不符合规范", "FireThresh 字段不符合规范，请参考接口文档说明")
    SMOKE_THRESH_FLOAT_TYPE_ERR = (450013, "SmokeThresh 字段类型错误", "SmokeThresh 字段应该是 float 类型")
    SMOKE_THRESH_VALUE_ERR = (450014, "SmokeThresh 字段不符合规范", "SmokeThresh 字段不符合规范，请参考接口文档说明")
    # 车辆检测
    CAR_THRESH_FLOAT_TYPE_ERR = (450015, "CarThresh 字段类型错误", "CarThresh 字段应该是 float 类型")
    CAR_THRESH_VALUE_ERR = (450016, "CarThresh 字段不符合规范", "CarThresh 字段不符合规范，请参考接口文档说明")
    # 安全帽检测 HelmetDetect
    HELMET_THRESH_FLOAT_TYPE_ERR = (450017, "HelmetThresh 字段类型错误", "HelmetThresh 字段应该是 float 类型")
    HELMET_THRESH_VALUE_ERR = (450018, "HelmetThresh 字段不符合规范", "HelmetThresh 字段不符合规范，请参考接口文档说明")
    # 吸烟检测 SmokeDetect
    SMOKE_THRESH_FLOAT_TYPE_ERR = (450019, "SmokeThresh 字段类型错误", "SmokeThresh 字段应该是 float 类型")
    SMOKE_THRESH_VALUE_ERR = (450020, "SmokeThresh 字段不符合规范", "SmokeThresh 字段不符合规范，请参考接口文档说明") 
    SMOKE_LEVEL_INT_TYPE_ERR = (450021, "Level 字段类型错误", "Level 字段应该是 int 类型")
    SMOKE_LEVEL_VALUE_ERR = (450022, "Level 字段不符合规范", "Level 字段不符合规范，请参考接口文档说明") 
    # 防护服检测 SuitDetect
    SUIT_THRESH_FLOAT_TYPE_ERR = (450023, "SuitThresh 字段类型错误", "SuitThresh 字段应该是 float 类型")
    SUIT_THRESH_VALUE_ERR = (450024, "SuitThresh 字段不符合规范", "SuitThresh 字段不符合规范，请参考接口文档说明")
    # 内容审核 ImgCensor
    IMG_CENSOR_SUBTASK_LIST_TYPE_ERR = (450025, "SubTask 字段类型错误", "SubTask 字段应该是 list 类型")
    IMG_CENSOR_SUBTASK_VALUE_ERR = (450026, "SubTask 字段不符合规范", "SubTask 字段不符合规范，请参考接口文档说明")
    


    # 公共字段 459xxx
    # AppKey 公共字段
    APPKEY_STRING_TYPE_ERR = (459001, "Appkey 字段类型错误", "Appkey 字段应该是 string 类型")
    APPKEY_VALUE_ERR = (459002, "Appkey 字段不符合规范", "Appkey 字段不符合规范，请参考接口文档说明")
    # Token 公共字段
    TOKEN_STRING_TYPE_ERR = (459003, "Token 字段类型错误", "Token 字段应该是 string 类型")
    TOKEN_VALUE_ERR = (459004, "Token 字段不符合规范", "Token 字段不符合规范，请参考接口文档说明")
    # Version 公共字段
    VERSION_STRING_TYPE_ERR = (459005, "Version 字段类型错误", "Version 字段应该是 string 类型")
    VERSION_VALUE_ERR = (459006, "Version 字段不符合规范", "Version 字段不符合规范，请参考接口文档说明")
    # server 
    SERVER_ERR = (500001, "服务接口异常,请联系管理员", "需要联系管理员处理")

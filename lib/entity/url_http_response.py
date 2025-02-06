from lib import Map

class UrlHttpResponse(Map):
    statusCode: int
    contentLength: int
    contentSha256: str
    headers: dict
    title: str

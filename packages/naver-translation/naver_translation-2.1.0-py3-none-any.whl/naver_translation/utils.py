import urllib.request
import json
from naver_translation.error import DetectError, TranslationError

def conver(self, url, data, tag):
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id", self.id)
  request.add_header("X-Naver-Client-Secret", self.secret)
  response = urllib.request.urlopen(request, data=data.encode("utf-8"))
  rescode = response.getcode()
  if(rescode==200): 
    response_body = response.read()
    result = json.loads(response_body)
    return result
      
  else:
    if tag == 'detect':
      raise DetectError(f"Error Code: {rescode}")
    else:
      raise TranslationError(f"Error Code: {rescode}")
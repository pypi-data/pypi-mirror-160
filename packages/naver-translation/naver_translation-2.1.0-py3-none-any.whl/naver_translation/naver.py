import urllib.request
from naver_translation import utils
from naver_translation.model import NaverDetect, NaverTranslation

class Translation:
  """
  네이버 번역 라이브러리를 사용하려면 [네이버개발자센터](https://developers.naver.com/main/)에서 발급받은 Client ID와 Client Secret가 필요합니다.
  
  #### Client ID
  개발자센터에서 발급받은 `Client ID`를 입력합니다.
  
  #### Client Secret
  개발자센터에서 발급받은 `Client Secret`를 입력합니다.
  
  """
  def __init__(self, client_id : str, client_secret : str):
    self.id = client_id
    self.secret = client_secret

  def detect(self, text : str) -> NaverDetect:
    """
    언어인식을 진행합니다. 입력한 글이 무슨 언어인지 인식하여 반환합니다.
    """
    data = "query=" + text
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    tag = 'detect'
    result = utils.conver(self, url, data, tag)
    return NaverDetect(result)

  def translation(self, text : str, target : str, source : str = None) -> NaverTranslation:
    """
    번역을 진행합니다.

    `source` : 출발언어를 입력합니다. ex) `ko`, `en`
    비워둘시 자동으로 언어를 인식합니다.

    `target` : 도착언어를 설정합니다. ([언어코드표](https://developers.naver.com/docs/papago/papago-nmt-api-reference.md#%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0))
    """
    encText = urllib.parse.quote(text)
    data = f"source={Translation.detect(self, text).text()}&target={target}&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    tag = 'translation'
    result = utils.conver(self, url, data, tag)
    return NaverTranslation(result)
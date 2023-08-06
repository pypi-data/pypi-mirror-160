class NaverDetect:
  """
  NaverDetect`.text()` : str형태로 반환합니다.
  NaverDetect`.json()` : 원문형태로 반환합니다.
  """
  def __init__(self, result):
    self.result = result

  def text(self):
    """
    `str`형태로 반환합니다.
    """
    return self.result['langCode']

  def json(self):
    """
    원문형태로 반환합니다.
    """
    return self.result
    
class NaverTranslation:
  """
  NaverDetect`.text()` : str형태로 반환합니다.
  NaverDetect`.src_lang_type()` : 출발언어를 반환합니다.
  NaverDetect`.tar_lang_type()` : 도착언어를 반환합니다.
  NaverDetect`.json()` : 원문형태로 반환합니다.
  """

  def __init__(self, result):
    self.result = result
  def text(self):
    """
    str형태로 반환합니다.
    """
    return self.result['message']['result']['translatedText']

  def src_lang_type(self):
    """
    출발언어를 반환합니다.
    """
    return self.result['message']['result']['srcLangType']
    
  def tar_lang_type(self):
    """
    출발언어를 반환합니다.
    """
    return self.result['message']['result']['tarLangType']

  def json(self):
    """
    원문형태로 반환합니다.
    """
    return self.result
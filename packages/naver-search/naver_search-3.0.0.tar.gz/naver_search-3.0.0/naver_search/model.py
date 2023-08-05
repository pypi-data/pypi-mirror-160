import random
from naver_search.error import NaverBasicError, NaverLinkError

class NaverBasic:
  def __init__(self):
    pass
    
  def basic(self, result, number):
    img_list = result['items']
    if number == None:
      img_list_len = len(img_list)
    else:
      if number > len(img_list):
        raise NaverBasicError(f"`Number` is out of range. Please search again within {len(img_list)}.")
      img_list_len = number
    
    basic = img_list[random.randrange(0, img_list_len)]
    return basic

  def url(self, result, number):
    img_list = result['items']
    if number == None:
      img_list_len = len(img_list)
    else:
      if number > len(img_list):
        raise NaverLinkError(f"`Number` is out of range. Please search again within {len(img_list)}.")
      img_list_len = number
    
    link = img_list[random.randrange(0, img_list_len)]['link']
    return link
   
class NaverImage:
  """
  NaverImage`.url` : url형태로 반환합니다.<br/>
  NaverImage`.json` : dict형태로 반환합니다.
  """
  def __init__(self, result):
    self.result = result
    
  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 사진을 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 사진을 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url
    
  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

#블로그
class NaverBlog:
  """
  NaverBlog`.basic` : dict형태로 반환합니다.(블로그정보)<br/>
  NaverBlog`.url` : url형태로 반환합니다.<br/>
  NaverBlog`.json` : dict형태로 반환합니다.(모든블로그 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 블로그 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 블로그 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 블로그 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 블로그 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list
    

class NaverBook:
  """
  NaverBook`.basic` : dict형태로 반환합니다.(책정보)<br/>
  NaverBook`.url` : url형태로 반환합니다.<br/>
  NaverBook`.json` : dict형태로 반환합니다.(모든책 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 책 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 책 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 책 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 책 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

#백과사전
class NaverEncyc:
  """
  NaverEncyc`.basic` : dict형태로 반환합니다.(백과사전 정보)<br/>
  NaverEncyc`.url` : url형태로 반환합니다.<br/>
  NaverEncyc`.json` : dict형태로 반환합니다.(모든 백과사전 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 백과사전 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 백과사전 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 백과사전 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 백과사전 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list


class NaverCafearticle:
  """
  NaverCafearticle`.basic` : dict형태로 반환합니다.(카페글 정보)<br/>
  NaverCafearticle`.url` : url형태로 반환합니다.<br/>
  NaverCafearticle`.json` : dict형태로 반환합니다.(모든 카페글정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 카페글 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 카페글 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 카페글 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 카페글 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

class NaverKin:
  """
  NaverKin`.basic` : dict형태로 반환합니다.(지식인 정보)<br/>
  NaverKin`.url` : url형태로 반환합니다.<br/>
  NaverKin`.json` : dict형태로 반환합니다.(모든 지식인정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 지식인 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 지식인 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 지식인 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 지식인 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

class NaverWebkr:
  """
  NaverWebkr`.basic` : dict형태로 반환합니다.(웹사이트 정보)<br/>
  NaverWebkr`.url` : url형태로 반환합니다.<br/>
  NaverWebkr`.json` : dict형태로 반환합니다.(모든 웹사이트 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 웹사이트 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 웹사이트 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 웹사이트 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 웹사이트 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

class NaverShop:
  """
  NaverShop`.basic` : dict형태로 반환합니다.(쇼핑 정보)<br/>
  NaverShop`.url` : url형태로 반환합니다.<br/>
  NaverShop`.json` : dict형태로 반환합니다.(모든 쇼핑 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 쇼핑 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 쇼핑 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 쇼핑 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 쇼핑 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list

class NaverDoc:
  """
  NaverDoc`.basic` : dict형태로 반환합니다.(전문자료 정보)<br/>
  NaverDoc`.url` : url형태로 반환합니다.<br/>
  NaverDoc`.json` : dict형태로 반환합니다.(모든 전문자료 정보)
  """
  def __init__(self, result):
    self.result = result

  def basic(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 전문자료 `정보`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 전문자료 `정보`를 가져옵니다.
    """
    basic = NaverBasic.basic(self, result = self.result, number = number)
    return basic

  def url(self, number : int = None):
    """
    `number`란에 숫자를 넣으면 (number)번째 전문자료 `링크`를 가져옵니다.<br/>
    `None`값으로 지정되어 있으면 랜덤번째 전문자료 `링크`를 가져옵니다.
    """
    url = NaverBasic.url(self, result = self.result, number = number)
    return url

  def json(self):
    """
    `dict`형태로 반환합니다.
    """
    img_list = self.result['items']
    return img_list
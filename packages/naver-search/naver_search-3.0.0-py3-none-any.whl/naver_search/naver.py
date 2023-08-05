import urllib.request
from naver_search.naverconver import NaverConver
from naver_search.model import NaverImage, NaverBlog, NaverBook, NaverEncyc, NaverCafearticle, NaverKin, NaverWebkr, NaverShop, NaverDoc

class Search:
  """
  네이버 라이브러리를 사용하려면 [네이버개발자센터](https://developers.naver.com/main/)에서 발급받은 Client ID와 Client Secret가 필요합니다.
  
  #### Client ID
  개발자센터에서 발급받은 `Client ID`를 입력합니다.
  
  #### Client Secret
  개발자센터에서 발급받은 `Client Secret`를 입력합니다.
  """
  def __init__(self, Client_ID : str, Client_Secret : str):
    """
    기본 변수를 설정합니다.
    """
    self.id = Client_ID
    self.secret = Client_Secret
    
  def search_image(self, text : str) -> NaverImage:
    """
    이미지를 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/image?query=" + encText
    result = NaverConver(self, url)
    return NaverImage(result)

  def search_blog(self, text : str) -> NaverBlog:
    """
    검색어와 관련있는 블로그를 검색합니다
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    result = NaverConver(self, url)
    return NaverBlog(result)

  def search_book(self, text : str) -> NaverBook:
    """
    검색어와 관련있는 도서를 검색합니다
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    result = NaverConver(self, url)
    return NaverBook(result)

  def search_encyc(self, text : str) -> NaverEncyc:
    """
    검색어와 관련있는 백과사전을 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/encyc?query=" + encText
    result = NaverConver(self, url)
    return NaverBook(result)

  def search_cafearticle(self, text : str) -> NaverCafearticle:
    """
    검색어와 관련있는 카페글을 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/cafearticle?query=" + encText
    result = NaverConver(self, url)
    return NaverCafearticle(result)

  def search_kin(self, text : str) -> NaverKin:
    """
    검색어와 관련있는 지식인을 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/kin?query=" + encText
    result = NaverConver(self, url)
    return NaverKin(result)

  def search_webkr(self, text : str) -> NaverWebkr:
    """
    검색어와 관련있는 웹사이트를 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/webkr?query=" + encText
    result = NaverConver(self, url)
    return NaverWebkr(result)

  def search_shop(self, text : str) -> NaverShop:
    """
    검색어와 관련있는 웹사이트를 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/webkr?query=" + encText
    result = NaverConver(self, url)
    return NaverShop(result)

  def search_doc(self, text : str) -> NaverDoc:
    """
    검색어와 관련있는 전문자료(학술정보)를 검색합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/doc?query=" + encText
    result = NaverConver(self, url)
    return NaverDoc(result)

  def search_adult(self, text : str) -> bool:
    """
    성인검색어 판별을 진행합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/adult?query=" + encText
    result = NaverConver(self, url)
    if result['adult'] == '1':
      return True
    else:
      return False

  def search_errata(self, text : str) -> dict:
    """
    오타가 있는지 없는지 검사를 진행합니다.
    """
    encText = urllib.parse.quote(text)
    url = "https://openapi.naver.com/v1/search/errata?query=" + encText
    result = NaverConver(self, url)
    return result
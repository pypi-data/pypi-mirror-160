from naver_search.error import ConverError
import urllib.request
import json


def NaverConver(self, url):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", self.id)
    request.add_header("X-Naver-Client-Secret", self.secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
      response_body = response.read()
      result = json.loads(response_body)
      return result

    else:
      raise ConverError(f"Error Code:{rescode}")
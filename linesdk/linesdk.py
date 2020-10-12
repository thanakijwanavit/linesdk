# AUTOGENERATED! DO NOT EDIT! File to edit: linesdk.ipynb (unless otherwise specified).

__all__ = ['FunctionNames', 'Line', 'LineLambda']

# Cell
from lambdasdk.lambdasdk import Lambda
from linebot.models import TextSendMessage
from linebot import LineBotApi
import bz2,  boto3, base64, logging, os

# Cell
class FunctionNames:
  '''determine function and resources name based on branchName'''
  def __init__(self, branchName:str = 'dev-manual'):
    self.branchName = branchName
  dumpToS3 = lambda self: f'product-dump-s3-{self.branchName}'
  updateProduct = lambda self: f'product-update-{self.branchName}'
  updateS3 = lambda self: f'product-update-s3-{self.branchName}'
  singleQuery = lambda self: f'product-get-{self.branchName}'
  allQuery = lambda self: f'product-get-all-{self.branchName}'
  inputBucket = lambda self: f'input-product-bucket-{self.branchName}'
  inventoryBucket = lambda self: f'product-bucket-{self.branchName}'


# Cell
class Line:
  '''
    the main class for interacting with product endpoint
    user/pw are optional
  '''
  def __init__(self,
               accessKey:str = ''):
    self.line_bot_api = LineBotApi(accessKey)

  def send(self, message:str = '', roomId:str=''):
    self.line_bot_api.push_message(roomId, TextSendMessage(text = message))
    return True
  @staticmethod
  def lambdaSend(event, _):
    line = Line(accessKey = os.environ.get('LINEACCESSKEY') or event['accessKey'])
    line.send(message = event['message'], roomId = event['roomId'])

class LineLambda:
  def __init__(self, user = None, pw=None, region = 'ap-southeast-1'):
    self.user = user
    self.pw = pw
    self.region = region

  def send(self, message:str = '', roomId:str='',
           functionName = 'send-line',
           accessKey = ''
          ):
    lambda_ = Lambda(
      user = self.user,
      pw = self.pw,
      region = self.region
    )
    lambda_.invoke(
      functionName = functionName,
      input = {
        'message': message,
        'roomId': roomId,
        'accessKey': self.accessKey
      }
    )
    return True
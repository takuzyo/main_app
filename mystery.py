#リクエストクラスなんでも可
import urllib.request, urllib.parse


class Mystery:

    def ___init__(self):
        #tokenは編集してね♡
        self.TOKEN = 1
        self.mystery_url = 'https://????.??/api/game/'
        #現在の問題番号
        self.now_mystery_id = 1
    
    def get_mystery(self):
        """
        謎解き取得
        TODO: 取得
        """
        request_url = self.mystery_url
        image = ''
        return image
    
    def check_answer(self):
        """
        正誤判定
        TODO: 判定
        """
        return False
    
    def count_up(self):
        """
        正解したらidを上げる
        TODO: 処理追加
        """
        return False
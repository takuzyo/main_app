#リクエストクラスなんでも可
import urllib.request, urllib.parse
import requests, json

class Mystery:

    def __init__(self):
        #tokenは編集してね♡
        self.TOKEN = 2
        self.mystery_url = "http://163.43.107.141:5000/api/game"
        #現在の問題番号
        self.now_mystery_id = 1
        self.fin = False
    
    def get_mystery(self):
        """
        謎解き取得
        TODO: 取得
        """
        request_url = f'{self.mystery_url}/{self.now_mystery_id}?token={self.TOKEN}'
        res = requests.get(request_url)
        val = json.loads(res.text)

        return val["img_url"]
    
    def check_answer(self, answer):
        """
        正誤判定
        TODO: 判定
        """
        request_url = f'{self.mystery_url}/{self.now_mystery_id}?token={self.TOKEN}'
        data = {
            "ans": answer
        }
        res = requests.post(request_url, json=data)
        if res.text is None:
            return False
        
        val = json.loads(res.text)
        
        result = val["result"]
        if result:
            self.count_up()

        return result
    
    def count_up(self):
        """
        正解したらidを上げる
        TODO: 処理追加
        """
        self.now_mystery_id += 1
        if self.now_mystery_id == 4:
            self.fin = True
        return


if __name__ == "__main__":
    test = Mystery()
    print(test.get_mystery())
    print(test.check_answer("りんご"))
    print(test.get_mystery())
    print(test.check_answer("りんご"))
    print(test.check_answer("ごりら"))


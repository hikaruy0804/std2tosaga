from std2saga import Std2saga
import time

# Hougenクラスのインスタンス化
saga = Std2saga()

test_lists = ['夜', #辞書有単語
              'くさる', #辞書有単語
              'カエル', #辞書無単語
              '今日から早起きをしないといけないね。', #日本語短文
              '果てなき冒険は、大空へ広がる。『ゼルダの伝説　ブレス オブ ザ ワイルド』続編が登場。 どこまでも続く広大な「大地」、そしてはるか雲の上の「大空」まで広がった世界で、どこへ行くのも、何をするのもあなた次第です。空を翔けめぐり、不思議な空島を探索するのか？リンクの手にした新たな力で、ハイラルの異変に立ち向かうのか？あなただけの果てなき冒険が、再び始まります。', #日本語長文
              '123456789', #数字
              'Hello', #英語長文
              'Thnak you' #英語単語
              ]

for  test_list in test_lists:
    # 開始時間
    start = time.time()
    #変換処理
    print(saga.sagaben(test_list))
    # 処理時間
    print('処理時間：',time.time() - start)
    print('ーーーーーーーーーーーーーーーーーー')

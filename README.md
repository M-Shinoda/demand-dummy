# 1. ダミーデータ生成
* ```main.py```を基本的に起動させる(内部でデータ生成する関数を呼び出す)
* ```generate_parking_records```が```駐車場名```と```特定の日```を引数にとるためこれのパラメータを変えればそれぞれの駐車場と日にちのダミーデータを生成可能
* ```./result/```フォルダの```各駐車場名.json```に生成されたデータが出力される
* 生成されたファイルの内容は```generate_parking_records```が実行されるたびに読み込みと書き出しがされるので、実行前に余計なデータが入っていると乱れる可能性があるので、中身をからにしておくか、入力した日付より前のデータを少し入れておくと良いかもしれない
* ```parking_name```に設定された駐車場基本情報が```./parkingLot/```フォルダにないとエラーが出る
* ```1年間のデータを生成```以下のコメント部分使って複数日を連続で生成すると少し時間がかかるので待つ 
  

# 2. 各時間帯の駐車台数のグラフ可視化
* ```result_grapht.py```と```result_grapht_imp.py```は駐車場名と特定の日にちの区間設定してグラフを表示(大体の推移を見るためなので、レジェンド周りは手を入れていない)
* ```parking_name```の駐車場で、````start_datetime````と```end_datetime```間のグラフを表示する
* 表示する期間を広げすぎるとデータの書き出しに時間がかかるため、１ヶ月程度にすると良い
* どちらのプログラムも同じことをするがファイルの読み込みに関して時間がかかるため、少しだけ改善したのが```result_grapht_imp.py```である
* 終了したい時はグラフのウィンドウを閉じる

# 3. 料金計算をしたjsonファイルの生成
* ```usage_fee.py```
* ダミーデータだと料金がないため、そのデータを追加したjsonを出力する
* 出力したい駐車場名に```parking_name```を設定
* ```result/各駐車場名-price.json```で出力される
* ダミーデータ```./result/各駐車場名.json```の情報に沿って生成さ、各データに```price```カラムが追加されて、駐車料金が入る
  
  
# 4. 駐車料金の総計
* ```total_fee.py```
* 料金計算をしたjsonファイル```result/各駐車場名-price.json```をもとに全ての```priceの総計```を出す
* 出力したい駐車場名に```parking_name```を設定
* ダミーデータ生成時点で1年間のデータを生成すると、```各駐車場の収入推移```と照らし合わせられる


### 各駐車場ごとに上から順に実行しないと、各段階で生成されるファイルが存在しない場合があるため、エラーが出るので注意
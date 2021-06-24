# jleague-result-prediction

## やりたいこと

* 2020年J1リーグの勝敗を予測するモデルを構築する


## これまでやってきたこと

* 2020年から2018年までの試合結果をFootball LAB(https://www.football-lab.jp/)から収集
* ポワソン分布を用いた得点予測
* SVMを用いた勝敗予測(【誤】試合が終了しなければ判明しないはずのスタッツを入力データに使用してしまい､思いの他高い精度になってしまった)
* 各クラブの年月ごとのイロレーティング収集 (https://footballdatabase.com/ranking/japan より)
* 過去3年間の一試合あたりの平均勝ち点と得失点数で予測
* 試合時のイロレーティングを用いて学習


### ※ 命名規則
* http://www.jfa.or.jp/jfa/terminology/

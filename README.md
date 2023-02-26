# tarumae-bot
因子情報を検索サイトからスクレイピングしてdiscordに投稿するbot

# ディレクトリ構造

config/<br>
　config.txt : 検索設定<br>
<br>
<br>
data/<br>
　(検索設定のJSONのMD5値).txt : 過去検索結果のキャッシュ<br>

# config.txt
{
　"gw" : {
　　"max_next_search_count" : 5  # "もっと見る"の回数制限設定
　},
　
　"search_list" : [
　　{
  　　type : gw # gw : gamewithを検索対象とする
  　　name : スペシャルウィーク # 特定のウマ娘に限定する場合にのみ指定 指定が無い場合は指定なし
  　　daihyo : false # 代表因子のみ検索
  　　speed : 0 # スピード 1～9で指定
  　　stamina : 0 # スタミナ 1～9で指定
  　　power : 0 # パワー 1～9で指定
  　　guts : 0 # 根性 1～9で指定
　    wisdom : 0 # 賢さ 1～9で指定
　    wisdom : 0 # 賢さ 1～9で指定
　　}
　]

}



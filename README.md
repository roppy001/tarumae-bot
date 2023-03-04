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
{<br>
　"gw" : {<br>
　　"max_next_count" : 5  # "もっと見る"の回数制限設定<br>
　},<br>
　<br>
　"search_list" : [<br>
　　{<br>
  　　type : gw # gw : gamewithを検索対象とする<br>
  　　name : スペシャルウィーク # 特定のウマ娘に限定する場合にのみ指定 指定が無い場合は指定なし<br>
  　　daihyo : false # 代表因子のみ検索<br>
  　　speed : 0 # スピード 1～9で指定<br>
  　　stamina : 0 # スタミナ 1～9で指定<br>
  　　power : 0 # パワー 1～9で指定<br>
  　　guts : 0 # 根性 1～9で指定<br>
  　　wisdom : 0 # 賢さ 1～9で指定<br>
  　　turf : 0 # 芝 1～9で指定<br>
  　　dirt : 0 # ダート 1～9で指定<br>
  　　short : 0 # 短距離 1～9で指定<br>
  　　mile : 0 # マイル 1～9で指定<br>
  　　middle : 0 # 中距離 1～9で指定<br>
  　　long : 0 # 長距離 1～9で指定<br>
  　　nige : 0 # 逃げ 1～9で指定<br>
  　　senkou : 0 # 先行 1～9で指定<br>
  　　sashi : 0 # 差し 1～9で指定<br>
  　　oikomi : 0 # 追込 1～9で指定<br>
　　}<br>
　]<br>
<br>
}<br>
<br>
# 抽出結果返却値

{<br>
　"id" : "123456789",<br>
　"factor_list" : [<br>
　　　{<br>
　　　　"name" : "マイル9"<br>
　　　}<br>
　　]<br>
}<br>

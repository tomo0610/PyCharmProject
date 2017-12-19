#!/usr/bin/python
# coding: utf-8
# カードの読み取り、DBから読み取ったカードの所持者を検索

# モジュール読み込み
import subprocess
import cgi
from urllib.parse import urlparse, parse_qs, parse_qsl
from datetime import datetime
import pymysql.cursors
import os
from PIL import Image


def connectDb():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='raspberry3',
                                 db='cardlist_db',
                                 charset='utf8',
                                 # cursorclassを指定することで
                                 # Select結果をtupleではなくdictionaryで受け取れる
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def application(env, start_response):
    # リクエストメソッドを取得
    method = env.get('REQUEST_METHOD')

    if method == 'GET':
        start_response('200 OK', [('Content-Type', 'text/html')])

        # 引数の取得
        query = cgi.parse_qsl(env.get('QUERY_STRING'))
        print(query)
        print(len(query))

        if query != []:
            # URL引数がある場合

            # 引数の数と引数の値で処理を分ける
            #   1個かつ"piclist"ではない：カードID検索
            #   引数が、"templist"      ：温度センサーデータ取得
            #   引数が、"piclist"       ：画像データ検索

            strtype = query[0][1]
            print('Type=' + strtype)


            if strtype == 'cardscan':   #カードIDがマスタに登録済みか確認
                # カードID検索
                _tagData = query[1][1]
                print(_tagData)

                # IDm
                idmIndex = _tagData.index('IDm')
                idm = _tagData[idmIndex + 4:_tagData.index(' ', idmIndex)]
                print(idm)

                # PMm
                pmmIndex = _tagData.index('PMm')
                pmm = _tagData[pmmIndex + 4:_tagData.index(' ', pmmIndex)]
                print(pmm)

                # SYS
                sysIndex = _tagData.index('SYS')
                sys = _tagData[sysIndex + 4:_tagData.index('\n')]
                print(sys)

                _cardId = idm + pmm + sys;

                # MySQLに接続する
                connection = connectDb()

                # SQLを実行する
                with connection.cursor() as cursor:
                    sql = "select emp_no from 社員マスタ where felica_card_no = \'" + _cardId + "\'"
                    cursor.execute(sql)

                # Select結果を取り出す
                # fetchall()を使用すると結果がタプル(は,い,れ,つ)で帰る
                _rsltEmpNo = ""
                results = cursor.fetchall()
                #print(results)
                for r in results:
                    _rsltEmpNo = r

                # データが1件のみ取れているか
                _rtnStr = ""
                _rsltStr = ""
                if len(results) == 0:

                    _rtnStr = "ユーザーが登録されていません"

                elif len(results) > 1:

                    _rtnStr = "複数ユーザーが登録されています"

                else:
                    _rtnStr = ""
                    _rsltStr = _rsltEmpNo['emp_no']


                    #出退勤時間記録TBLにINSERT現在時刻をINSERTする。
                    # SQLを実行する
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO 出退勤時間記録TBL VALUES  (\'" + _cardId + "\',\'" + _rsltStr + "\', SYSDATE)"
                        r = cursor.execute(sql)
                        print(r)  # -> 1
                        # autocommitではないので、明示的にコミットする
                        connection.commit()

                    # MySQLから切断する
                    connection.close()

                # バックグラウンドでGoogoleにアップロード
                # cmd = 'python googleUpload.py ' + resultStr + ' &'
                # subprocess.Popen(cmd, shell=True)

                return _rtnStr.encode('utf-8')

            elif strtype == 'login':

                _empNo = query[1][1]
                _passWd = query[2][1]

                # MySQLに接続する
                connection = connectDb()

                # SQLを実行する
                with connection.cursor() as cursor:
                    sql = 'SELECT admin_auth_flg FROM 社員マスタ WHERE emp_no = \'' + _empNo + '\' AND emp_pwd = \'' + _passWd + '\''
                    cursor.execute(sql)

                # fetchall()を使用すると結果がタプル(は,い,れ,つ)で帰る
                _adminAuthFlg = ""
                results = cursor.fetchall()

                for r in results:
                    _adminAuthFlg = r

                # データが1件のみ取れているか
                _rtnStr = ""
                _rsltStr = ""
                if len(results) == 0:

                    _rtnStr = "ユーザー名またはパスワードが間違っています"

                elif len(results) > 1:

                    _rtnStr = "複数ユーザーが登録されています"

                else:

                    _rtnStr = ""
                    _rsltStr = _adminAuthFlg['admin_auth_flg']



                # MySQLから切断する
                connection.close()

                # テキスト形式でDBデータを返す
                return jsonString.encode('utf-8')

            elif strtype == 'workconfadmin':
            
            	# 出退勤確認画面の中での処理分け
            	_stsStr = query[1][1]
            
            	if _stsStr == "search":
            		
            		# 画面に入力された期間(From)を取得
            		_periodFrom = query[2][1]
            		
            		# 画面に入力された期間(To)を取得
            		_periodTo = query[3][1]
            		
            		# 画面に入力された社員番号を取得
            		_empNo = query[4][1]
            		
            		# 画面に入力された社員名を取得
            		_empName = query[5][1]
            		
            		# 画面に入力された社員名カナを取得
            		_empNameKana = query[6][1]
            		
            		# MySQLに接続する
            		connection = connectDb()

                	# SQLを実行する
                	with connection.cursor() as cursor:
                	    sql = 'SELECT regist_date FROM 出退勤時間記録TBL, 社員マスタ WHERE 1=1 '
                	    
                	    if _periodFrom != "":
                	    	sql += 'AND regist_date >= \'' + _periodFrom + '\''
                	    elif _periodTo != "":
                	    	sql += 'AND regist_date <= \''+ _periodTo + '\''
                	    elif _empNo != "":
                	    	sql += 'AND emp_no = \''+ _empNo + '\''
                	    elif _empName != "":
                	    	sql += 'AND emp_name = \''+ _empName + '\''
                	    elif _empNameKana != "":
                	    	sql += 'AND emp_name_kana = \''+ _empNameKana + '\''
                	    	
                	    cursor.execute(sql)

               		# fetchall()を使用すると結果がタプル(は,い,れ,つ)で帰る
               		_adminAuthFlg = ""
               		results = cursor.fetchall()

                	for r in results:

                        _adminAuthFlg = r

            		
            		# MySQLから切断する
                	connection.close()
            		
            	elif
            	
            
                # 画像データ取得
                path = '/var/www/html'
                picpath = '/pic/'
                thpath = '/thumbnail/'
                files = os.listdir(path + picpath)

                # ファイル情報（作成日）の取得
                arr = []
                i = 0
                for file in files:
                    # ファイル名作成
                    filepath = path + picpath + file  # ファイル情報取得用（フルパス）
                    thumpath = path + thpath + file  # サムネイルファイル（フルパス）
                    picfilepath = picpath + file  # オープン用ファイル名
                    thfilepath = thpath + file  # オープン用サムネイルファイル名

                    # ファイル情報（作成日）の取得
                    dt = datetime.fromtimestamp(os.stat(filepath).st_ctime)
                    strCtime = dt.strftime('%Y/%m/%d %H:%M:%S')

                    # サムネイルファイル作成
                    img = Image.open(filepath, 'r')
                    thumbnail_size = (160, 120)
                    img.thumbnail(thumbnail_size)
                    img.save(thumpath, 'JPEG')

                    arr.append([file, filepath, thumpath, picfilepath, thfilepath, strCtime])

                    i = i + 1

                print(arr)

                # 作成日の降順で並び替え
                arrSort = sorted(arr, key=lambda dat: dat[5], reverse=True)

                print(arrSort)

                # ファイル一覧結果を取り出し、json変換用の文字列を作成する
                jsonString = '['

                for ar in arrSort:
                    jsonString = jsonString + '''
					{
						"filename": "''' + ar[0] + '''",
						"filepath": "''' + ar[3] + '''",
						"ctime": "''' + ar[5] + '''",
						"thfile": "''' + ar[4] + '''"
					},
					'''

                # 最後のデータの','を削除する
                jsonString = jsonString[:len(jsonString) - 7]

                jsonString = jsonString + ']'
                print(jsonString)

                # テキスト形式でDBデータを返す
                return jsonString.encode('utf-8')

            elif strtype == 'piclist':
                # 画像データ取得
                path = '/var/www/html'
                picpath = '/pic/'
                thpath = '/thumbnail/'
                files = os.listdir(path + picpath)

                # ファイル情報（作成日）の取得
                arr = []
                i = 0
                for file in files:
                    # ファイル名作成
                    filepath = path + picpath + file  # ファイル情報取得用（フルパス）
                    thumpath = path + thpath + file  # サムネイルファイル（フルパス）
                    picfilepath = picpath + file  # オープン用ファイル名
                    thfilepath = thpath + file  # オープン用サムネイルファイル名

                    # ファイル情報（作成日）の取得
                    dt = datetime.fromtimestamp(os.stat(filepath).st_ctime)
                    strCtime = dt.strftime('%Y/%m/%d %H:%M:%S')

                    # サムネイルファイル作成
                    img = Image.open(filepath, 'r')
                    thumbnail_size = (160, 120)
                    img.thumbnail(thumbnail_size)
                    img.save(thumpath, 'JPEG')

                    arr.append([file, filepath, thumpath, picfilepath, thfilepath, strCtime])

                    i = i + 1

                print(arr)

                # 作成日の降順で並び替え
                arrSort = sorted(arr, key=lambda dat: dat[5], reverse=True)

                print(arrSort)

                # ファイル一覧結果を取り出し、json変換用の文字列を作成する
                jsonString = '['

                for ar in arrSort:
                    jsonString = jsonString + '''
					{
						"filename": "''' + ar[0] + '''",
						"filepath": "''' + ar[3] + '''",
						"ctime": "''' + ar[5] + '''",
						"thfile": "''' + ar[4] + '''"
					},
					'''

                # 最後のデータの','を削除する
                jsonString = jsonString[:len(jsonString) - 7]

                jsonString = jsonString + ']'
                print(jsonString)

                # テキスト形式でDBデータを返す
                return jsonString.encode('utf-8')


        else:
            check = subprocess.check_output("/home/pi/testFiles/getCardID.sh", shell=True)
            return check

    elif method == 'POST':
        start_response('200 OK', [('Content-Type', 'text/html')])

        print("POST処理開始")

        # 引数の取得
        wsgi_input = env['wsgi.input']
        print(wsgi_input)
        content_length = int(env.get('CONTENT_LENGTH', 0))

        # 引数を展開する為のURLを取得
        url = wsgi_input.read(content_length)
        url = url.decode('utf-8')
        print(url)
        query = parse_qsl(url)
        print(query)

        # URL引数がある場合、処理を実施
        if query != []:
            print(query)

            idm = query[0][1]
            print(idm)

            pmm = query[1][1]
            print(pmm)

            sys = query[2][1]
            print(sys)

            tname = query[3][1]
            print(tname)

            # MySQLに接続する
            connection = connectDb()

            # SQLを実行する
            with connection.cursor() as cursor:
                sql = "INSERT INTO user_card_list VALUES  (\'" + idm + "\', \'" + pmm + "\', \'" + sys + "\', \'" + tname + "\')"
                # r = cursor.execute(sql, (idm, pmm, sys, tname))
                r = cursor.execute(sql)
                print(r)  # -> 1
                # autocommitではないので、明示的にコミットする
                connection.commit()

            # MySQLから切断する
            connection.close()

        return '登録しました'.encode('utf-8')
    else:
        print("エラー")
        return "err"


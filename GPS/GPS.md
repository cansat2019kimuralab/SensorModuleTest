# GPS.py
- openGPS():GPSをセットアップする関数  
	引数　：なし  
	戻り値：なし  
- readGPS():GPSデータを読み込むための関数  
	引数　：なし  
	戻り値：[utc, Lat, Lon, sHeight, gHeight]  
		- [*, -1.0, 0.0, *, *]ならばStatusV  
		- [-1.0, -1.0, 0.0, *, *]ならばStatusA  
- closeGPS():GPSの終了処理  
	引数　：なし  
	戻り値：なし　
- Cal_RhoAng(lat_a,lon_a,lat_b,lon_b):２点間の距離、方位を求める関数  
	引数　：[lat_a,lon_a,lat_b,lon_b] ２点の緯度、経度（A：始点、B：終点）   
	戻り値：[rho, angle] それぞれ距離[m]、角度[deg]  
	https://qiita.com/damyarou/items/9cb633e844c78307134a  
# GPS用リポジトリ
## 使い方
pigpioをインストールする  
`sudo apt install pigpio`  
  
pigpiodを実行する  
`sudo pigpiod `   
  
コードsoftSerialTest.pyを実行する  
`python softSerialTest.py`

## pigpioの自動起動
pigpioを実行しなければライブラリを使えない。  
面倒な場合、Raspberry Piの起動と同時にpigpioを実行できるようにする。  
/etc/rc.localに以下のコマンドを追加する。  
`sudo pigpiod`

## 参考ページ
- [Raspberry Pi 2nd UART a.k.a. Bit Banging a.k.a. Software Serial](https://www.rs-online.com/designspark/raspberry-pi-2nd-uart-a-k-a-bit-banging-a-k-a-software-serial)
- [Raspberry Pi3でpigpioライブラリを使ってLチカする](https://qiita.com/yuuri23/items/597fd1a40c63627e59c2)  
- [Raspberry PiのGPIO制御の決定版pigpioを試す](https://karaage.hatenadiary.jp/entry/2017/02/10/073000)  
  
最初のページのpigpioライブラリの入れ方は上手くいかなかった。  
二つ目のページを参考にしてpigpioライブラリを入れた。

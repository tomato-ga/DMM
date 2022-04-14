from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.dmm.co.jp/litevideo/-/part/=/cid=ofje00191/size=476_306/affi_id=kamipanmen-990/'])

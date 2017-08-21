# kspider
spider for kugou top 500 musics

一个非常简单的爬虫,用于抓取酷狗音乐上的top500榜单

[kugou top500](http://www.kugou.com/yy/rank/home/2-8888.html?from=rank)榜单如下图：


步骤如下：

1 查看首页的元素，发现歌曲大部分信息都可以在首页取得到，例如歌名，演唱者，专辑ID,文件大小，播放时长，hash等等。
![main image](https://github.com/inspire365/kspider/blob/master/main_page.png)
![main_info image](https://github.com/inspire365/kspider/blob/master/info_page.png)

2 点击进去音乐后发现，新的页面就是由hash和album_id构成的，在新的页面可以得到歌曲的下载地址(当然，如果需要你也可以得到歌词)
![song image](https://github.com/inspire365/kspider/blob/master/song_page.png)

3 然后能得到基本信息和下载地址你就可以保存所有信息和下载歌曲了啊。。。





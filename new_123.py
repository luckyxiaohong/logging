# !/user/bin/env python
# -*- coding: utf-8 -*-
# au: caopeiya
# 201808011
import os, shutil
import urllib.request, urllib.error, requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# 打开并读取网页内容
def getUrlData(url):
    try:
        urlData = urllib.request.urlopen( url, timeout=20 )  # .read().decode('utf-8', 'ignore')
        # urlData = requests.get(url, timeout=20)  # .read().decode('utf-8', 'ignore')
        return urlData
    except Exception as err:
        print( f'err getUrlData({url})\n', err )
        return -1


# 下载文件-requests
def getDown_reqursts(url, file_path):
    try:
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
        response = requests.get( url, timeout=120, headers=header )
        with open( file_path, mode='ab+' ) as f:
            f.write( response.content )
        # 下载文件较大时，使用循环下载
        # with open(file_path, mode='wb') as f:
        #     for content in response.iter_content(1024):
        #         f.write(content)
        print( "down successful!" )
    except Exception as e:
        print( e )


def getVideo_requests(url_m3u8, path, videoName):
    print( 'begin run ~~\n' )
    urlData = getUrlData( url_m3u8 )
    tempName_video = os.path.join( path, f'{videoName}.ts' )  # f'{}' 相当于'{}'.format() 或 '%s'%videoName
    open( tempName_video, "wb" ).close()  # 清空(顺带创建)tempName_video文件，防止中途停止，继续下载重复写入
    # print(urlData)
    for line in urlData:
        # 解码decode("utf-8")，由于是直接使用了所抓取的链接内容，所以需要按行解码，如果提前解码则不能使用直接进行for循环，会报错
        url_ts = str( line.decode( "utf-8" ) ).strip()  # 重要：strip()，用来清除字符串前后存在的空格符和换行符
        if not '.ts' in url_ts:
            continue
        else:
            if not url_ts.startswith( 'http' ):  # 判断字符串是否以'http'开头，如果不是则说明url链接不完整，需要拼接
                # 拼接ts流视频的url
                url_ts = url_m3u8.replace( url_m3u8.split( '/' )[-1], url_ts )
        print( url_ts )
        getDown_reqursts( url=url_ts, file_path=tempName_video )  # 下载视频流
    filename = os.path.join( path, f'{videoName}.mp4' )
    shutil.move( tempName_video, filename )
    print( f'Great, {videoName}.mp4 finish down!' )


if __name__ == '__main__':
    # url_m3u8 = 'http://wscdn.alhls.xiaoka.tv/201886/2f5/75a/HoHdTc1LjUaBjZbJ/index.m3u8'
    # # url_m3u8 = 'https://videos5.jsyunbf.com/2019/03/09/ixkZ4lxkzHzMSeAf/playlist.m3u8'
    url_m3u8 = "https://youku.com-l-youku.com/20190425/20343_3d6e1d92/1000k/hls/index.m3u8"
    path = r'D:\\'
    videoName = url_m3u8.split( '/' )[-2]
    getVideo_requests( url_m3u8, path, videoName )
    # getDown_reqursts('http://wscdn.alhls.xiaoka.tv/201886/2f5/75a/HoHdTc1LjUaBjZbJ/147.ts', f'D:/videos/84.ts')
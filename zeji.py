import lxml
import urllib.request

url="https://sourcehuoshan.shuidi.cn/pa/resource/js/Pa_Pa.js?v=202412171808"

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'referer':'https://trusted.shuidi.cn/',
    'cookie':'PHPSESSID=pdgceivftprsteklqdipdqaao5; Hm_lvt_5506231b17a528f78d1e37f359b4eb95=1734441939; HMACCOUNT=6B20273052C5F298; ssotoken=336304.8ff2f57c07f1f0c455c923f20973a82e; Hm_lpvt_5506231b17a528f78d1e37f359b4eb95=1734443432'
}

request=urllib.request.Request(url=url,headers=headers)

response=urllib.request.urlopen(request)
content=response.read().decode('utf8')
print(content)
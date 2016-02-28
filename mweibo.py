import requests

login_url = "https://passport.weibo.cn/sso/login"
post_header = {
	"Host": "passport.weibo.cn",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate, br",
	"Content-Type": "application/x-www-form-urlencoded",
	"Referer": "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F",
	"Content-Length": "257",
	"Connection": "keep-alive"
}

post_data = {
	"username": "15203476529",
	"password": "zjk1995",
	"savestate": "1",
	"ex": "0",
	"pagerefer": "https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4",
	"entry": "mweibo",
	"wentry": "",
	"loginform": "",
	"client_id": "",
	"code": "",
	"qq": "",
	"hff": "",
	"hfp": ""
}

login = requests.post(login_url, headers=post_header, data=post_data)

get_url = "http://m.weibo.cn/"
cook = login.cookies.get_dict()
cook = "SUB=" + cook["SUB"] + "; SUHB=" + cook["SUHB"] + "; SSOLoginState=" + cook["SSOLoginState"]
headers = {
	"Host": "m.weibo.cn",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
	"Accept-Encoding": "gzip, deflate",
	"Cookie": cook,
	"Connection": "keep-alive"
}

res = requests.get(get_url, headers=headers, cookies=login.cookies)
print(res.text)
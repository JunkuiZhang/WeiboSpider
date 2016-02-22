import requests
import base64
import json

class Weibo:

	def __init__(self, user, pwd):
		self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
		self.user_name = base64.b64encode(user.encode("utf-8")).decode("utf-8")
		self.pwd = pwd

	def login(self):
		post_header = {
			"Host": "login.sina.com.cn",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://weibo.com/login.php",
			# "Cookie": "SINAGLOBAL=27.17.137.107_1456125529.238050; Apache=27.17.137.107_1456125529.238052",
			"Connection": "keep-alive"
		}
		post_data = {
			"entry": "sso",
			"gateway": "1",
			"from": "null",
			"savestate": "30",
			"useticket": "0",
			"pagerefer": "",
			"vsnf": "1",
			"su": self.user_name,
			"service": "sso",
			"sp": self.pwd,
			"sr": "1920*1080",
			"encoding": "UTF-8",
			"cdult": "3",
			"domain": "sina.com.cn",
			"prelt": "0",
			"returntype": "TEXT",
		}
		response = requests.session()
		res = response.post(self.login_url, headers=post_header, data=post_data)
		jstr = res.content.decode("gbk")
		info = json.loads(jstr)
		if info["retcode"] == "0":
			print("Done.")
			cookies = response.cookies.get_dict()
			cookies = [key + "=" + value for key, value in cookies.items()]
			cookies = ": ".join(cookies)
			response.headers["cookie"] = cookies
		else:
			print("Failed to login. Cuz: %s" % info["reason"])

u = "15203476529"
p = "zjk1995"
w = Weibo(u, p)
w.login()
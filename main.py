import requests
import base64
import json
import re
import rsa
import binascii

class Weibo:

	def __init__(self, user, pwd):
		self.prelogin_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTUyMDM0NzY1Mjk=&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)"
		self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
		self.user_name = user
		self.pwd = pwd

	def get_su(self):
		return base64.b64encode(self.user_name.encode("utf-8")).decode("utf-8")

	def get_sp(self, keys):
		pubkey = int(keys["pubkey"], 16)
		k = rsa.PublicKey(pubkey, 65537)
		message = str(keys["servertime"]) + "\t" + str(keys["nonce"]) + "\n" + str(self.pwd)
		message = message.encode("utf-8")
		sp = rsa.encrypt(message, k)
		sp = binascii.b2a_hex(sp)
		return sp

	def prelogin(self):
		post_header = {
			"Host": "login.sina.com.cn",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
			"Accept": "*/*",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			# "Referer": "http://weibo.com/login.php",
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		res = requests.get(self.prelogin_url, headers=post_header)
		jstr = re.findall('({.*})', res.text)[0]
		jstr = json.loads(jstr)
		servertime = jstr["servertime"]
		nonce = jstr["nonce"]
		pubkey = jstr["pubkey"]
		rsakv = jstr["rsakv"]
		cookie = res.cookies
		return {"servertime": servertime, "nonce": nonce, "pubkey": pubkey, "rsakv": rsakv, "cookie": cookie}

	def login(self):
		keys = self.prelogin()
		su = self.get_su()
		sp = self.get_sp(keys)
		post_header = {
			"Host": "login.sina.com.cn",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			# "Referer": "http://weibo.com/login.php",
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		post_data = {
			"entry": "sso",
			"gateway": "1",
			"from": "",
			"savestate": "7",
			"useticket": "1",
			# "pagerefer": "http://open.weibo.com/wiki/2/statuses/home_timeline",
			"pagerefer": "http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&sudaref=http%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIHVQzIqJVbsXVUm6UA-UJZFKFcFUUzsVVpuQ_sfsvkC%26wd%3D%26eqid%3De3212695004a0b5a0000000556d27aa8&ua=php-sso_sdk_client-0.6.14&_rand=1456634538.5542",
			"vsnf": "1",
			"su": su,
			"service": "miniblog",
			"sp": sp,
			"sr": "1920*1080",
			"encoding": "UTF-8",
			"prelt": "54",
			"returntype": "META",
			"rsakv": keys["rsakv"],
			"nonce": keys["nonce"],
			"severtime": keys["servertime"]
		}
		response = requests.session()
		# response.cookies.update(keys["cookie"])
		res = response.post(self.login_url, data=post_data, headers=post_header)
		jstr = res.content.decode("gbk")
		if re.findall("正在登录...", jstr) != []:
			print("Done.")
		else:
			print("Failed to login.")
		print(response.cookies.get_dict())
		print(res.cookies)
		print(res.headers)
		res1 = response.get("http://weibo.com/u/3570580163/home?wvr=5&lf=reg", headers=post_header)
		print(res1.text)
		# return response

	def crawl(self, response):
		target_url = "http://weibo.com/u/1826792401?topnav=1&wvr=6&topsug=1&is_all=1"
		headers = {

		}
		res = response.get(target_url)
		print(res.text)

u = "15203476529"
p = "zjk1995"
w = Weibo(u, p)
w.login()
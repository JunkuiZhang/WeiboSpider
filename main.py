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

	def prelogin(self):
		self.su = base64.b64encode(self.user_name.encode("utf-8")).decode("utf-8")
		post_header = {
			"Host": "login.sina.com.cn",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
			"Accept": "*/*",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		post_data = {
			"entry": "weibo",
			"callback": "sinaSSOContoller.preloginCallBack",
			"su": self.su,
			"rsakt": "mod",
			"checkpin": "1",
			"client": "ssologin.js(v1.4.18)",
			# "_": "1456153156860"
		}
		res = requests.get(self.prelogin_url, headers=post_header, data=post_data)
		jstr = re.findall('({.*})', res.text)[0]
		jstr = json.loads(jstr)
		servertime = jstr["servertime"]
		nonce = jstr["nonce"]
		pubkey = jstr["pubkey"]
		rsakv = jstr["rsakv"]
		return {"servertime": servertime, "nonce": nonce, "pubkey": pubkey, "rsakv": rsakv}

	def login(self):
		keys = self.prelogin()
		def getsp(password):
			pubkey = int(keys["pubkey"], 16)
			k = rsa.PublicKey(pubkey, 65537)
			message = str(keys["servertime"]) + "\t" + str(keys["nonce"]) + "\n" + str(password)
			message = message.encode("utf-8")
			sp = rsa.encrypt(message, k)
			sp = binascii.b2a_hex(sp)
			return sp

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
			"from": "",
			"savestate": "7",
			"useticket": "1",
			"pagerefer": "http://open.weibo.com/wiki/2/statuses/home_timeline",
			"vsnf": "1",
			"su": self.su,
			"service": "miniblog",
			"sp": getsp(self.pwd),
			"sr": "1920*1080",
			"encoding": "UTF-8",
			# "cdult": "3",
			# "domain": "sina.com.cn",
			"prelt": "62",
			"returntype": "META",
			"rsakv": keys["rsakv"],
			"nonce": keys["nonce"],
			"severtime": keys["servertime"]
		}
		response = requests.session()
		res = response.post(self.login_url, headers=post_header, data=post_data)
		jstr = res.content.decode("gbk")
		if re.findall("正在登录...", jstr) != []:
			print("Done.")
		else:
			print("Failed to login.")


u = "15203476529"
p = "zjk1995"
w = Weibo(u, p)
w.login()
import requests
import base64
import json
import re
import rsa
import binascii
import bs4

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
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		response = requests.session()

		res = response.get(self.prelogin_url, headers=post_header)
		jstr = re.findall('({.*})', res.text)[0]
		jstr = json.loads(jstr)
		servertime = jstr["servertime"]
		nonce = jstr["nonce"]
		pubkey = jstr["pubkey"]
		rsakv = jstr["rsakv"]
		return {"servertime": servertime, "nonce": nonce, "pubkey": pubkey, "rsakv": rsakv, "cookie": response}

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
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		post_data = {
			"entry": "weibo",
			"gateway": "1",
			"from": "",
			"savestate": "7",
			"useticket": "1",
			"pagerefer": "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F",
			"vsnf": "1",
			"su": su,
			"service": "miniblog",
			"sp": sp,
			"sr": "1920*1080",
			"encoding": "UTF-8",
			"prelt": "65",
			"pwencode": "rsa2",
			"returntype": "META",
			"rsakv": keys["rsakv"],
			"nonce": keys["nonce"],
			"severtime": keys["servertime"],
			"url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack"
		}
		response = keys["cookie"]
		res = response.post(self.login_url, data=post_data, headers=post_header)
		url = re.findall("replace\\('(.*)'\\)", str(res.text))
		if url != []:
			print("Done")
			url = url[0]
		else:
			print("Failed to login.")

		headers = {
			"Host": "passport.weibo.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)",
			"Connection": "keep-alive"
		}
		response.get(url, headers=headers, allow_redirects=False)
		target_url = "http://weibo.com/u/1826792401?topnav=1&wvr=6&topsug=1&is_all=1"
		headers = {
			"Host": "weibo.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://weibo.com/",
			"Connection": "keep-alive"
		}
		res2 = response.get(target_url, headers=headers)
		print(res2.text)

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
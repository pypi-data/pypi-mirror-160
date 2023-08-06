import os , uuid , requests , instaloader , random , re , json
from user_agent import *
class gdo_drow:

    def get_users_following(username: str, password: str ,name: str) -> str:
        s = instaloader.Instaloader()
        try:
            s.login(username ,password)
            profile = instaloader.Profile.from_username(s.context, name)
            follow_list = []
            for follow in profile.get_followees():
                user = str(follow)
                users = user.split('Profile ')[1].split('(')[0]
                follow_list.append(users)

            return {'status':'Success','users':follow_list}

        except:
            return {'status' :'error' ,'users' :[]}



    def get_users_followers(username :str ,password: str, name: str) -> str:
        s = instaloader.Instaloader()
        try:
            s.login(username ,password)
            profile = instaloader.Profile.from_username(s.context, name)
            follow_list = []
            for follow in profile.get_followers():
                user = str(follow)
                users = user.split('Profile ')[1].split('(')[0]
                follow_list.append(users)

            return {'status':'Success','users':follow_list}

        except:
            return {'status' :'error' ,'users' :[]}


    def get_ids_following(username: str ,password: str, name: str) -> str:
        L = instaloader.Instaloader()
        try:
            L.login(username ,password)
            profile = instaloader.Profile.from_username(L.context, name)
            follow_list = []
            for follow in profile.get_followees():
                user = str(follow)
                id = user.split('(')[1].split(')')[0]
                follow_list.append(id)

            return {'status':'Success','ids':follow_list}

        except:
            return {'status' :'error' ,'ids' :[]}



    def get_ids_followers(username: str ,password: str, name: str) -> str:
        L = instaloader.Instaloader()
        try:
            L.login(username ,password)
            profile = instaloader.Profile.from_username(L.context, name)
            follow_list = []
            for follow in profile.get_followers():
                user = str(follow)
                id = user.split('(')[1].split(')')[0]
                follow_list.append(id)

            return {'status':'Success','ids':follow_list}

        except:
            return {'status' :'error' ,'ids' :[]}

    def reset(email: str) -> str:
        url = "https://i.instagram.com/api/v1/users/lookup/"
        headers = {
			        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			        'Host': 'i.instagram.com',
			        'Connection': 'Keep-Alive',
			        'User-Agent': 'Instagram 6.12.1 Android (25/7.1.2; 160dpi; 383x680; LENOVO/Android-x86; 4242ED1; x86_64; android_x86_64; en_US)',
			        'Accept-Language': 'en-US',
			        'X-IG-Connection-Type': 'WIFI',
			        'X-IG-Capabilities': 'AQ==',}
        data = 'signed_body=acd10e3607b478b845184ff7af8d796aec14425d5f00276567ea0876b1ff2630.%7B%22_csrftoken%22%3A%22rZj5Y3kci0OWbO8AMUi0mWwcBnUgnJDY%22%2C%22q%22%3A%22'+str(email)+'%22%2C%22_uid%22%3A%226758469524%22%2C%22guid%22%3A%22a475d908-a663-4895-ac60-c0ab0853d6df%22%2C%22device_id%22%3A%22android-1a9898fad127fa2a%22%2C%22_uuid%22%3A%22a475d908-a663-4895-ac60-c0ab0853d6df%22%7D&ig_sig_key_version=4'
        res = requests.post(url, headers=headers, data=data).text
        if '"status":"ok"' in res:
        	return {'status':'Success','reset':True}
        else:
        	return {'status':'error','reset':False}


    def get_email_busines(username: str, session: str) -> str:
        L = instaloader.Instaloader()
        profile = str(instaloader.Profile.from_username(L.context ,username))
        idd =str(profile.split(')>')[0]).split(' (')[1]
        url = "https://i.instagram.com/api/v1/users/ " +str(id)+"/info/"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": "ig_did=57C594DF-134B-4172-BCF1-C32A7A21989B; mid=X_sqxgALAAE7joUQdF9J2KQUb0bw; ig_nrcb=1; shbid=2205; shbts=1614954604.1671221; fbm_124024574287414=base_domain=.instagram.com; csrftoken=hE6dtVq6z7Zozo4yfyVPOpTJNEktuPky; rur=FRC; ds_user_id=46430696274; sessionid= " +str(session)+"",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "none",
            "user-agent": str(generate_user_agent())}
        res = requests.Session().get(url, data="", headers=headers).json()
        try:
            if res['user']['is_business'] == True and str(res['user']['public_email']) != "":
                email = str(res['user'].get('public_email'))
                if str("@") in email:
                    return {'status' :'Success' ,'email' :str(email)}
                else:
                    return {'status' :'error' ,'email' :None}
            else:
                {'status' :'error' ,'email' :None}

        except:
            return {'status' :'error' ,'email' :'bad request'}



    def get_email():
        s = ["@gmail.com" ,"@yahoo.com" ,"@hotmail.com" ,"@aol.com" ,"@outlook.com"]
        domin = random.choice(s)
        url = 'https://randommer.io/random-email-address'
        headers = {
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '239',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '.AspNetCore.Antiforgery.9TtSrW0hzOs=CfDJ8DJ-g9FHSSxClzJ5QJouzeI7-q_vZxCnhkeFlGapcHZgJbZ-aP87NSgO15EqlMTNlpWsrTtDK8Qo_FkcelUen-XMHT8ZaUCFeGiAhGS8O7Ny-7XLvjZQza8gyEX141ln397mg-FwkxUmh8CBjHv4QKw',
            'origin': 'https://randommer.io',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-requested-with': 'XMLHttpRequest'}

        data = {
            'number': "1",
            'culture': 'en_US',
            '__RequestVerificationToken': 'CfDJ8DJ-g9FHSSxClzJ5QJouzeLi6tSHIeSyq6LHD-lqesWRBHZhI32LFnxMH163TgAQwwE7dRIDYclgxYfDODEZgqrDwuegjkOko7L88MqV4BLhOsmSdGm9gFbDalgtuV6lb3bhat9gHttOROyeP72M4aw',
            'X-Requested-With': 'XMLHttpRequest'}
        req = requests.post(url, headers=headers, data=data).text
        data = req.replace('[' ,'').replace(']' ,'').split(',')
        for i in data:
            eail = i.replace('"' ,'')
            ema = eail.split("@")[0]
            email = ema + domin
            return email


    def get_same_user(user: str) -> str:
    	url = f'https://www.instagram.com/web/search/topsearch/?context=blended&query={user}'
    	headers = {
    	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    	"accept-encoding": "gzip, deflate, br",
    	"accept-language": "ar,en;q=0.9",
    	"cache-control": "max-age=0",
    	"cookie": 'mid=Yemn3AAEAAGx56yZBU5-oiVvPQ4e; ig_did=B8C62C92-A3F7-418B-8F2D-7552C1467C20; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; datr=1AowYgO84Ejd51RFZGIapmbk; ig_direct_region_hint="CLN\05453358207778\0541688796486:01f71cfca83b40e08f4455a3c69feeefeadf41a6c7a76553e488c59b2ae8ae624b229f08"; shbid="15813\05453358207778\0541689148844:01f7d1c6791d8190c1c1903a32c63fda8a72a91405faad7bc23f83066265b367c4fc04ef"; shbts="1657612844\05453358207778\0541689148844:01f7abef005a2c35962e3880fd1de92c761afc12b8c5849e063f0c368c972e163af643b0"; csrftoken=62F4UWL7ir1yw2cvWddkTExCUJOmoUDO; ds_user_id=53358207778; sessionid=; rur="LDC\05453358207778\0541689186461:01f7f8cb2aaa64d1379e5f3c099e71cdcc97996784c478075bffb9659ffbd016d7d3bbf4"',
    	'sec-ch-prefers-color-scheme': 'light',
    	'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    	"sec-ch-ua-mobile": "?0",
    	"sec-ch-ua-platform": "Windows",
    	"sec-fetch-dest": "document",
    	"sec-fetch-mode": "navigate",
    	"sec-fetch-site": "none",
    	"sec-fetch-user": "?1",
    	"upgrade-insecure-requests": "1",
    	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    	"viewport-width": "1366"}
    	res = requests.get(url,headers=headers).json()
    	user_list = []
    	full_list = []
    	try:
    		se = 0
    		while True:
    			try:
    				se += 1
    				user = str(res['users'][se]['user']['username'])
    				name = str(res['users'][se]['user']['full_name'])
    				user_list.append(user)
    				full_list.append(name)
    			except IndexError:break
    		return {'status':'Success','users':user_list,'names':full_list}
    	except:
    		return {'status':'error','users':[],'names':[]}
    			
    			
    def get_proxy():
        pro = requests.get('https://gimmeproxy.com/api/getProxy')
        if '"protocol"' in pro.text or '"ip"' in pro.text or '"port"' in pro.text:
            if str(pro.json()['protocol']) == 'socks5':
                proxy = str(pro.json()['curl'])
                return {'proxy' :proxy ,'status' :True}
            else:
                return {'message' :'Bad proxy' ,'status' :'error'}
        else:
            return  {'message' :'Bad Protocol' ,'status' :'error'}


    def get_user_agent():
        message = str(os.system('ua'))
        return message


    def csrf_token():
        headers = {"User-Agent": str(generate_user_agent())}
        with requests.Session() as azoz:
            url_tok = "https://www.instagram.com/"
            data = azoz.get(url_tok, headers=headers).content
            token = re.findall('{"config":{"csrf_token":"(.*)","viewer"', str(data))[0]
            return {'csrf_token' :str(token)}



    def id_post(url: str) -> str:
        url = str(url)
        igshid = url.split("?igshid=")[1].split("%")[0]
        data = {"igshid": igshid ,}
        res = requests.get(url ,data=data).text
        id = res.split('"media_id":"')[1].split('",')[0]
        return id


    def get_info_ip(ip: str) -> str:
        url = "https://ipinfo.io/widget/demo/ " +ip
        headers = {
            'Host': 'ipinfo.io',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?1',
            'save-data': 'on',
            'user-agent': str(generate_user_agent()),
            'sec-ch-ua-platform': '"Android"',
            'content-type': 'application/json',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://ipinfo.io/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'flash=',
            'cookie': 'bento_visitor_id=d0224ad9-b83a-4103-a8e6-aa794b0fc1da',
            'cookie': 'bento_visit_id=b70e5bfe-8341-43e5-a46c-84a3c14cf2e5',
            'cookie': 'bento_events=%5B%7B%22id%22%3A%22a1203021-2f6a-4d31-b42d-06718983bd77%22%2C%22site%22%3A%220d66e7448ad29ad69828d1d4201299a2%22%2C%22visitor%22%3A%22d0224ad9-b83a-4103-a8e6-aa794b0fc1da%22%2C%22visit%22%3A%22b70e5bfe-8341-43e5-a46c-84a3c14cf2e5%22%2C%22type%22%3A%22%24view%22%2C%22date%22%3A%22Wed%2C%2022%20Jun%202022%2015%3A46%3A15%20GMT%22%2C%22browser%22%3A%7B%22user_agent%22%3A%22Mozilla/5.0%20%28Linux%3B%20Android%208.0.0%3B%20SM-G930V%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/96.0.4664.92%20Mobile%20Safari/537.36%22%7D%2C%22page%22%3A%7B%22url%22%3A%22https%3A//ipinfo.io/%22%2C%22queryString%22%3A%22%22%2C%22anchor%22%3A%22%22%2C%22host%22%3A%22ipinfo.io%22%2C%22path%22%3A%22/%22%2C%22protocol%22%3A%22https%3A%22%2C%22title%22%3A%22Comprehensive%20IP%20address%20data%2C%20IP%20geolocation%20API%20and%20database%20-%20IPinfo.io%22%2C%22referrer%22%3A%22%22%7D%2C%22identity%22%3A%7B%7D%7D%5D' ,}
        res = json.loads(requests.get(url ,headers=headers).text)
        try:
            try:ip = res["data"]["ip"]
            except KeyError:ip = False
            try:name = res["data"]["name"]
            except KeyError:name = False
            try:city = res["data"]["city"]
            except KeyError:city= False
            try:country = res["data"]["country"]
            except KeyError:country = False
            try:isp = res["data"]["region"]
            except KeyError:isp = False
            try:region = res["data"]["org"]
            except KeyError:region = False
            try:timezone = res["data"]["timezone"]
            except KeyError: timezone = False
            try:postal = res["data"]["postal"]
            except KeyError:postal = False
            try:asn = res["data"]["asn"]["asn"]
            except KeyError: asn = False
            try:asn_name = res["data"]["asn"]["name"]
            except KeyError:asn_name = False
            try:domain = res["data"]["asn"]["domain"]
            except KeyError:domain = False
            try:route = res["data"]["asn"]["route"]
            except KeyError: route = False
            try:company_name = res["data"]["company"]["name"]
            except KeyError:company_name = False
            try:vpn = res["data"]["privacy"]["vpn"]
            except KeyError:vpn = False
            try:proxy = res["data"]["privacy"]["proxy"]
            except KeyError: proxy = False
            try:service = res["data"]["privacy"]["service"]
            except KeyError: service = False
            try:hosting = res["data"]["privacy"]["hosting"]
            except KeyError: hosting = False
            try:address = res["data"]["abuse"]["address"]
            except KeyError: address = False
            try:email = res["data"]["abuse"]["email"]
            except KeyError: email = False
            try:phone = res["data"]["abuse"]["phone"]
            except KeyError: phone = False

            message ={}
            message["ip"] = ip
            message["name"] = name
            message["city"] = city
            message["country"] = country
            message["isp"] = isp
            message["region"] = region
            message["timezone"] = timezone
            message["postal"] = postal
            message["asn"] = asn
            message["asn_name"] = asn_name
            message["domain"] = domain
            message["route"] = route
            message["company_name"] = company_name
            message["vpn"] = vpn
            message["proxy"] = proxy
            message["service"] = service
            message["hosting"] = hosting
            message["address"] = address
            message["email"] = email
            message["phone"] = phone

            return message
        except:
            return False

# -------------------------[CoDe BY GDØ]------------------------
# -------------------------[CoDe BY GDØ]------------------------
# -------------------------[CoDe BY GDØ]------------------------

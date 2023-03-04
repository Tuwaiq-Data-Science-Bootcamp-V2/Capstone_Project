import ipaddress
import app as app
import whois as whois
import numpy as np
from django.shortcuts import render
import datetime
import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences
import warnings
import pickle
warnings.filterwarnings('ignore')
import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
from urllib.parse import urlparse


def FeatureExtractionDef(url):
    fe = []
    domain = ""
    whois_response = ""
    urlparse = ""
    response = ""
    soup = ""
    try:
        urlparse = urlparse(url)
        domain = urlparse.netloc
    except:
        domain = ""
        urlparse = ""

    try:
        whois_response = whois.whois(domain)
    except:
        whois_response = ""

    ip = 0
    try:
        ipaddress.ip_address(url)
        ip = -1
    except:
        ip = 1
    fe.append(ip)

    leng = 0
    if len(url) < 54:
        leng = 1
    if len(url) >= 54 and len(url) <= 75:
        leng = 0
    else:
        leng = -1
    fe.append(leng)

    short = 0
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                      url)
    if match:
        short = -1
    else:
        short = 1
    fe.append(short)

    symbol = 0
    if re.findall("@", url):
        symbol = -1
    else:
        symbol = 1
    fe.append(symbol)

    redirecting = 0
    if url.rfind('//') > 6:
        redirecting = -1
    else:
        redirecting = 1
    fe.append(redirecting)

    prefixSuffix = 0
    try:
        match = re.findall('\-', domain)
        if match:
            prefixSuffix = -1
        else:
            prefixSuffix = 1
    except:
        prefixSuffix = -1
    fe.append(prefixSuffix)

    SubDomains = 0

    dot_count = len(re.findall("\.", url))
    if dot_count == 1:
        SubDomains = 1
    elif dot_count == 2:
        SubDomains = 0
    else:
        SubDomains = -1
    fe.append(SubDomains)

    Hppts = 0
    try:
        https = urlparse.scheme
        if 'https' in https:
            Hppts = 1
        else:
            Hppts = -1
    except:
        Hppts = 1
    fe.append(Hppts)

    DomainRegLen = 0
    try:
        expiration_date = whois_response.expiration_date
        creation_date = whois_response.creation_date
        try:
            if (len(expiration_date)):
                expiration_date = expiration_date[0]
        except:
            pass
        try:
            if (len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass

        age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
        if age >= 12:
            DomainRegLen = 1
        else:
            DomainRegLen = -1
    except:
        DomainRegLen = -1
    fe.append(DomainRegLen)

    Favicon = 0
    try:
        for head in soup.find_all('head'):
            for head.link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                    Favicon = 1
        if (Favicon == 0):
            Favicon = -1
    except:
        Favicon = -1
    fe.append(Favicon)

    NonStdPort = 0
    try:
        port = domain.split(":")
        if len(port) > 1:
            NonStdPort = -1
        else:
            NonStdPort = 1
    except:
        NonStdPort = -1
    fe.append(NonStdPort)

    HTTPSDomainURL = 0
    try:
        if 'https' in domain:
            HTTPSDomainURL = -1
        else:
            HTTPSDomainURL = 1
    except:
        HTTPSDomainURL = -1
    fe.append(HTTPSDomainURL)

    RequestURL = 0
    try:
        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        try:
            percentage = success / float(i) * 100
            if percentage < 22.0:
                RequestURL = 1
            elif ((percentage >= 22.0) and (percentage < 61.0)):
                RequestURL = 0
            else:
                RequestURL = -1
        except:
            RequestURL = 0
    except:
        RequestURL = -1

    fe.append(RequestURL)

    AnchorURL = 0
    try:
        i, unsafe = 0, 0
        for a in soup.find_all('a', href=True):
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                    url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
            if percentage < 31.0:
                AnchorURL = 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                AnchorURL = 0
            else:
                AnchorURL = -1
        except:
            AnchorURL = -1

    except:
        AnchorURL = -1
    fe.append(AnchorURL)

    LinksInScriptTags = 0
    try:
        i, success = 0, 0

        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        try:
            percentage = success / float(i) * 100
            if percentage < 17.0:
                LinksInScriptTags = 1
            elif ((percentage >= 17.0) and (percentage < 81.0)):
                LinksInScriptTags = 0
            else:
                LinksInScriptTags = -1
        except:
            LinksInScriptTags = 0
    except:
        LinksInScriptTags = -1

    fe.append(LinksInScriptTags)

    ServerFormHandler = 0
    try:
        if len(soup.find_all('form', action=True)) == 0:
            ServerFormHandler = 1
        else:
            for form in soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    ServerFormHandler = -1
                elif url not in form['action'] and domain not in form['action']:
                    ServerFormHandle = 0
                else:
                    ServerFormHandler = 1
    except:
        ServerFormHandler = -1
    fe.append(ServerFormHandler)

    InfoEmail = 0
    try:
        if re.findall(r"[mail\(\)|mailto:?]", soup):
            InfoEmail = -1
        else:
            InfoEmail = 1
    except:
        InfoEmail = -1
    fe.append(InfoEmail)

    AbnormalURL = 0
    try:
        if response.text == whois_response:
            AbnormalURL = 1
        else:
            AbnormalURL = -1
    except:
        AbnormalURL = -1
    fe.append(AbnormalURL)

    WebsiteForwarding = 0

    try:
        if len(response.history) <= 1:
            WebsiteForwarding = 1
        elif len(response.history) <= 4:
            WebsiteForwarding = 0
        else:
            WebsiteForwarding = -1
    except:
        WebsiteForwarding = -1
    fe.append(WebsiteForwarding)

    StatusBarCust = 0
    try:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            StatusBarCust = 1
        else:
            StatusBarCust = -1
    except:
        StatusBarCust = -1
    fe.append(StatusBarCust)

    DisableRightClick = 0
    try:
        if re.findall(r"event.button ?== ?2", response.text):
            DisableRightClick = 1
        else:
            DisableRightClick = -1
    except:
        DisableRightClick = -1
    fe.append(DisableRightClick)

    UsingPopupWindow = 0
    try:
        if re.findall(r"alert\(", response.text):
            UsingPopupWindow = 1
        else:
            UsingPopupWindow = -1
    except:
        UsingPopupWindow = -1
    fe.append(UsingPopupWindow)

    IframeRedirection = 0
    try:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            IframeRedirection = 1
        else:
            IframeRedirection = -1
    except:
        IframeRedirection = -1
    fe.append(IframeRedirection)

    AgeofDomain = 0
    try:
        creation_date = whois_response.creation_date
        try:
            if (len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass

        today = date.today()
        age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
        if age >= 6:
            AgeofDomain = 1
        else:
            AgeofDomain = -1
    except:
        AgeofDomain = -1
    fe.append(AgeofDomain)

    DNSRecording = 0
    try:
        creation_date = whois_response.creation_date
        try:
            if (len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass

        today = date.today()
        age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
        if age >= 6:
            DNSRecording = 1
        else:
            DNSRecording = -1
    except:
        DNSRecording = -1
    fe.append(DNSRecording)

    WebsiteTraffic = 0
    try:
        rank = \
        BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
            "REACH")['RANK']
        if (int(rank) < 100000):
            WebsiteTraffic = 1
        else:
            WebsiteTraffic = 0
    except:
        WebsiteTraffic = -1
    fe.append(WebsiteTraffic)

    PageRank = 0
    try:
        prank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": domain})
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", prank_checker_response.text)[0])
        if global_rank > 0 and global_rank < 100000:
            PageRank = 1
        else:
            PageRank = -1
    except:
        PageRank = -1
    fe.append(PageRank)

    GoogleIndex = 0
    try:
        site = search(url, 5)
        if site:
            GoogleIndex = 1
        else:
            GoogleIndex = -1
    except:
        GoogleIndex = 1
    fe.append(GoogleIndex)

    LinksPointingToPage = 0
    try:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            LinksPointingToPage = 1
        elif number_of_links <= 2:
            LinksPointingToPage = 0
        else:
            LinksPointingToPage = -1
    except:
        LinksPointingToPage = -1
    fe.append(LinksPointingToPage)

    StatsReport = 0
    try:
        url_match = re.search(
            'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',
            url)
        ip_address = socket.gethostbyname(domain)
        ip_match = re.search(
            '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
            '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
            '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
            '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
            '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
            '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
            ip_address)
        if url_match:
            StatsReport = -1
        elif ip_match:
            StatsReport = -1
        else:
            StatsReport = 1
    except:
        StatsReport = 1
    fe.append(StatsReport)

    return fe

def getPredictions2(result):
    model = pickle.load(open('urlModelNew.pkl', 'rb'))
    prediction = model.predict(result)
    if prediction == 1:
        return 'No'
    elif prediction == -1:
        return 'Yes'
    else:
        return 'error'

# Create your views here.
def home(request):
    return render(request, 'index.html')

def homeAR(request):
    return render(request, 'indexAr.html')

def URL(request):
    return render(request, 'URL.html')

def URLAr(request):
    return render(request, 'URLAr.html')

def AboutUs(request):
    return render(request, 'AboutUs.html')

def AboutUsAr(request):
    return render(request, 'AboutUsAr.html')

def SMSEMAIL(request):
    return render(request, 'SMSEMAIL.html')

def SMSEMAILAr(request):
    return render(request, 'SMSEMAILAr.html')

def featureExtraction(url):
    age = 0
    end = 0
    featuresExtracted = []

    # 1-Charcters number:
    feature = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    for a in feature:
        featuresExtracted.append(url.count(a))

        # 2-Hostname:
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    if match:
        featuresExtracted.append(1)
    else:
        featuresExtracted.append(0)

    # 3-Https
    htp = urlparse(url).scheme
    match = str(htp)
    if match == 'https':
        featuresExtracted.append(1)
    else:
        featuresExtracted.append(0)

    # 4- Number count
    numbers = 0
    for i in url:
        if i.isnumeric():
            numbers = numbers + 1
    featuresExtracted.append(numbers)

    # 5- Alpha count
    alphabets = 0
    for i in url:
        if i.isalpha():
            alphabets = alphabets + 1
    featuresExtracted.append(alphabets)

    # 6- Short URL
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        featuresExtracted.append(1)
    else:
        featuresExtracted.append(0)

    # 7- IP Address
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        featuresExtracted.append(1)
    else:
        featuresExtracted.append(0)

    # 8- Age
    try:
        domain_name = whois.whois(urlparse(url).netloc)
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date
        if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
            try:

                creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except:
                age = 1
                if age != 1:
                    if ((expiration_date is None) or (creation_date is None)):
                        age = 1
                        if age != 1:
                            ageofdomain = abs((expiration_date - creation_date).days)
                            if ((ageofdomain / 30) < 12):
                                age = 1
                            else:
                                age = 0
    except:
        age = 1
    featuresExtracted.append(age)

    # 9- End Age
    try:
        domain_name = whois.whois(urlparse(url).netloc)
        expiration_date = domain_name.expiration_date
        if isinstance(expiration_date, str):
            try:
                expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
            except:
                end = 1
                if end != 1:
                    if (expiration_date is None):
                        end = 1
                        if end != 1:
                            today = datetime.now()
                            end = abs((expiration_date - today).days)
                            if ((end / 30) < 6):
                                end = 1
                            else:
                                end = 0
    except:
        end = 1
    featuresExtracted.append(end)

    # 10-IFRAME
    response = requests.get(url)
    try:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            featuresExtracted.append(0)
        else:
            featuresExtracted.append(1)
    except:
        featuresExtracted.append(1)

    # 11-MouseOver
    try:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            featuresExtracted.append(1)
        else:
            featuresExtracted.append(0)
    except:
        featuresExtracted.append(1)

    # 12-RightClick
    try:
        if re.findall(r"event.button ?== ?2", response.text):
            featuresExtracted.append(0)
        else:
            featuresExtracted.append(1)
    except:
        featuresExtracted.append(1)

    # 13-MultiDirect
    try:
        if len(response.history) <= 2:
            featuresExtracted.append(0)
        else:
            featuresExtracted.append(1)
    except:
        featuresExtracted.append(1)

    return featuresExtracted


def getPredictions(result):
    model = pickle.load(open('urlModellass.pkl', 'rb'))
    scaled = pickle.load(open('urlScalerlass.pkl', 'rb'))
    dataScaled=scaled.transform([result])
    prediction = model.predict(dataScaled)
    if prediction == 0:
        return 'No'
    elif prediction == 1:
        return 'Yes'
    else:
        return 'error'

def resultURL(request):
    url2 = request.GET['linke']
    if not (url2.startswith("http")):
        url2='http://'+url2
    result = FeatureExtractionDef(url2)
    result = np.reshape(result, (1, 30))
    Predict_text = getPredictions2(result)
    return render(request, 'resultURL.html',{'Predict_text':Predict_text})

def reseltURLAr(request):
    url2 = request.GET['linke']
    if not (url2.startswith("http")):
        url2='http://'+url2
    result = FeatureExtractionDef(url2)
    result = np.reshape(result, (1, 30))
    Predict_text = getPredictions2(result)
    return render(request, 'reseltURLAr.html',{'Predict_text':Predict_text})

def cleanText(text):
    # Create a regular experssion pattern for whitespaces '\s', + means there is one or more charater after the whitespace
    # ==> as result this pattern remove the whitespace at the begining of string
    whitespace = re.compile(r"\s+")


    # Create a regular experssion pattern for web addresses
    # (?i) ==> for case insinstive
    # (s) ==> means either http or https
    # \/\/ ==> means douple slash
    #[a-z0-9.~_\-\/]+ ==> means set of characters between a-z and 0-9, . except newlines , ~_ include underscore and \, + one or more characters
    web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")

    # Create a regular experssion pattern for users ids
    # (?i) ==> for case insinstive
    # @ ==> means contains @ character
    # [a-z0-9_]+ ==> means contains characters a to z and digits 0 to 9 and underscore
    user = re.compile(r"(?i)@[a-z0-9_]+")

    # to replace the . in text with empty string
    text = text.replace('.', '')

    # Apply the whitespace pattern into the text using sub
    text = whitespace.sub(' ', text)

    # Apply web addreses pattern into the text using sub
    text = web_address.sub('', text)

    # Apply user pattern into the text using pattern
    text = user.sub('', text)
    text = re.sub(r"\[[^()]*\]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r'[^\w\s]','',text)
    text = re.sub(r"(?:@\S*|#\S*|http(?=.*://)\S*)", "", text)
    return text.lower()

def getPredictionsMasage(result):

    loadedModel = tf.keras.models.load_model('messagesModele')
    tokeize = pickle.load(open('messagesTokenizer.pkl', 'rb'))
    finalText = pad_sequences(tokeize.texts_to_sequences([result]), padding='pre', maxlen=171)
    prediction = loadedModel.predict(finalText)
    if prediction > 0.5:
        return 'Spam'
    else:
        return 'Ham'


def resultMasage(request):
    masage2 = request.GET['masage']
    finalmasage = cleanText(masage2)
    Predict_Mesage=getPredictionsMasage(finalmasage)
    return render(request, 'resultSMSEMAIL.html',{'Predict_Mesage':Predict_Mesage})

def resultSMSEMAIAr(request):
    masage2 = request.GET['masage']
    finalmasage = cleanText(masage2)
    Predict_Mesage=getPredictionsMasage(finalmasage)
    return render(request, 'resultSMSEMAIAr.html',{'Predict_Mesage':Predict_Mesage})
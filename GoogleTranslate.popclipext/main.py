# coding: utf-8
import urllib
import urllib.request
import json
import os
import re
from urllib.parse import quote

def translate(tl,q):
    base_url = "https://translate.googleapis.com/translate_a/single?"
    params =  ("client=gtx&sl=auto&model=nmt&tl=%s&dt=t&q=%s" % (tl,quote(q)))
    content = urllib.request.urlopen(base_url + params).read().decode('utf-8')
    data = json.loads(content)
    return data

def display_text(tl,q):
    text = []
    for trans in translate(tl,q)[0]:
        text.append(trans[0])
    return "".join(text)

if __name__ == '__main__':

    tl = re.findall(r'[(](.*?)[)]', (os.getenv("POPCLIP_OPTION_TL")))[0] 
    tl_alt= re.findall(r'[(](.*?)[)]', (os.getenv("POPCLIP_OPTION_TL_ALT"))) [0]
    text = os.getenv("POPCLIP_TEXT")
    flag = os.getenv("POPCLIP_MODIFIER_FLAGS")
    key = tl
    if flag == "1048576":
        key = tl_alt
    
    result = display_text(key,text)
    script =  '\'display dialog "%s" buttons {"Copy and Close"} default button 1 with title "Google Translate"\''  % result
    os.system('echo "%s" | /usr/bin/pbcopy' % result)
    os.system("/usr/bin/osascript -e %s" % script)

from flask import Flask
from subprocess import Popen, PIPE
import cgi

import os, re

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/print/<path:message>')
def lol(message):
    return message

@app.route('/show/<file>')
def show(file):
    return file

@app.route('/blame/<path:path>')
def blame(path):
    try:
        f = open(path + '.blame')
        blamedata = f.read()
    except IOError as (errno, strerror):
        blamedata = Popen(["svn", "blame", path], stdout=PIPE).stdout.read()
    
    dataz = blamedata.split('\n')
    
    filelisting = ''
    
    for root, dirs, files in os.walk("hbase/"):
		for name in files:
		    thelink = os.path.join(root, name)
		    url = os.path.join(root, name)
		    listentry = '<li><a href="/blame/' + url + '">'+ thelink +'</a>'
		    if '/.' not in listentry and '.blame' not in listentry:
			filelisting += listentry

		    

    toreturn = """
    
    
    <head>
    <link href='http://fonts.googleapis.com/css?family=UnifrakturMaguntia|Meddon|IM+Fell+English+SC|Rokkitt|Josefin+Sans|Sniglet:800|VT323|Varela+Round&v2' rel='stylesheet' type='text/css'>
    </head>
    <body>
    <div style="position:fixed;top:0;left:0;border:1px solid black;width:300px; overflow-y:scroll; height:100%">
    <ul>""" + filelisting + """
    </ul>
    </div>
    <div style="padding-left: 300px; white-space:pre;">
    """

    
    for d in dataz:
        
        m = re.match('(^[0-9]+)\s+([a-zA-Z]+)(.*)$',d)
        if m:
            #toreturn += "<span style='"+ get_style(m.group(1)) + "'>" + m.group(1) + ": "+ cgi.escape(m.group(3)) + "</span><br/>"
	    toreturn += "<span style='"+ get_style(m.group(1)) + "; COLOR: "+ get_color(m.group(2)) + "'>" + cgi.escape(m.group(3)) + "</span><br/>"

    toreturn += "</div></body>"
                                                                                
    return toreturn

def get_color(committer):
    if 'stack' in committer:
	return 'red'
    if 'jimk' in committer:
	return 'black'
    if 'apurtell' in committer:
	return 'green'
    if 'jdcryans ' in committer:
	return 'purple'
    if 'jgray' in committer:
	return 'gray'
    if 'rawson' in committer:
	return 'orange'
    if 'todd' in committer:
	return 'blue'
    if 'bryanduxbury' in committer:
	return 'pink'
    if 'cutting' in committer:
	return 'orange'
    if 'nspiegelberg' in committer:
	return 'red'
    if 'nitay' in committer:
	return 'blue'
    if 'lars' in committer:
	return 'green'
    if 'gary' in committer:
	return 'yellow'
    if 'tom' in committer:
	return 'black'
    if 'malley' in committer:
	return 'black'
    if 'nigel' in committer:
	return 'black'
    if 'joes' in committer:
	return 'black'
    return 'black'
    

def get_style(rev, lower_bound=600000, upper_bound=1300000):
    rev = int(rev)
    
    font_list = ["UnifrakturMaguntia","Meddon","IM Fell English SC","rokkitt","Josefin Sans","sniglet","vt323","Varela Round"]
    font_list = ["UnifrakturMaguntia","UnifrakturMaguntia","IM Fell English SC","rokkitt","Josefin Sans","sniglet","vt323","Varela Round"]
    
    fonts = len(font_list)

    upper_bound -= lower_bound
    real_rev = rev
    rev -= lower_bound
    
    era_size = upper_bound/fonts
    era = 1
    
    #print "REAL_REV=",real_rev
    #print "rev=",rev
    #print "fonts = ", fonts
    for i in range(1,8):
        #print "if " + str(rev) + " > ",era_size*i
        if rev < era_size*i:
            #print "yes! setting era=",i
            era = i
            break
    
    return 'font-family: ' + font_list[era]


if __name__ == '__main__':
    test = get_style(750333)
    app.run(debug = True)
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://www.mancavemedia.nl'
ADDON=xbmcaddon.Addon(id='plugin.video.MCMBWizard')
dialog = xbmcgui.Dialog()
VERSION = "1.0.1"
PATH = "MCMBWizard"

    
def CATEGORIES():
    link = OPEN_URL('http://mancavemedia.nl/wizard/MCMB_Updates.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ackageroot="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,packageroot in match:
        addDir(name,url,1,iconimage,fanart,description,packageroot)
    setView('movies', 'MAIN')
        
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description,packageroot):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))    
# MCMB: ask pin and replace 'xxxx' with pin in download url
    versionpin = xbmcgui.Dialog().input('Pssst... Wat is de pincode?', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
    url = url.replace('xxxx', versionpin)
# END
    dp = xbmcgui.DialogProgress()
    dp.create("[B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR] Wizard[/B]","[B][COLOR FF593C24]Stap 1.[/COLOR] [COLOR FF4379A5]Eentjes en nulletjes binnenhalen.[/COLOR][/B]","Stap 2. Alles uitpakken en op de juiste plek zetten.", "Pak gerust wat te drinken. Dit kan even duren...")
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
#    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    addonfolder = xbmc.translatePath(packageroot)
    time.sleep(2)
    dp.update(0,"Stap 1. Eentjes en nulletjes binnenhalen. [B][COLOR FF4379A5](Klaar!)[/COLOR][/B]","[B][COLOR FF593C24]Stap 2.[/COLOR] [COLOR FF4379A5]Alles uitpakken en op de juiste plek zetten.[/COLOR][/B]","Zit je nog goed? Nog een paar minuten...")
    print '======================================='
    print addonfolder
    print '======================================='
    try:
        extract.all(lib,addonfolder,dp)
    except Exception, e:
        xbmcgui.Dialog().ok("[B][COLOR red]Oeps![/COLOR][/B]","Het lijkt er op dat je de verkeerde pincode hebt ingetoetst.","Probeer het gerust nog een keer.","")
        print str(e)
        sys.exit()
    dialog = xbmcgui.Dialog()
    dialog.ok("Klaar!", "Wij zijn er klaar voor om je [B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR][/B] te herstarten.",'','')
    killxbmc() 
      
        
def killxbmc():
    choice = xbmcgui.Dialog().yesno('[B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR][/B] herstarten', 'We trekken even virtueel de stekker uit je [B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR][/B]. (Bij netjes afsluiten blijven de nieuwe instellingen niet hangen.)', 'Ben je er klaar voor?', nolabel='Nee, niet doen!',yeslabel='Ja, prima!')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'linux': #Linux
#        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]Oeps![/COLOR][/B]", "Het is blijkbaar niet gelukt om je [B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR][/B] te herstarten. ", "Je zult het dus zelf moeten doen: even de stroom eraf en er weer op.","Dus NIET netjes uitschakelen via het menu!")
    else: #ATV
#        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]Oeps![/COLOR][/B]", "Het is blijkbaar niet gelukt om je [B][COLOR FF593C24]ManCave[/COLOR][COLOR FF4379A5]MediaBox[/COLOR][/B] te herstarten. ", "Je zult het dus zelf moeten doen: even de stroom eraf en er weer op.","Dus NIET netjes uitschakelen via het menu!")

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description,packageroot):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&packageroot="+urllib.quote_plus(packageroot)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
       
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
packageroot=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        packageroot=urllib.unquote_plus(params["packageroot"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description,packageroot)
        

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))


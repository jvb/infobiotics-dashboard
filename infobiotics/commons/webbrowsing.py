from infobiotics.commons.api import which
import subprocess, webbrowser

def dedicated_window(url):             
    chrome = which('google-chrome') 
    if chrome:
        subprocess.Popen(
            [chrome,'--app=%s' % url], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
        )    
    else:    
        webbrowser.open(url, new=1, autoraise=True)
        # may not open a new browser window depending on users setup
        
from infobiotics.thirdparty.which import which, WhichError
import subprocess, webbrowser

def dedicated_window(url, browser_executable='google-chrome', correct_missing_http=True):
    if correct_missing_http and not '://' in url:
        url = 'http://' + url
    try:
        browser_executable_path = which(browser_executable)
        arg1 = '--app=%s' % url if browser_executable == 'google-chrome' else url
        if browser_executable_path:
            subprocess.Popen(
                [browser_executable_path, arg1], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT
            )
    except WhichError:
        webbrowser.open(url, new=1, autoraise=True)
        # may not open a new browser window depending on users setup


if __name__ == '__main__':
    
    url = 'www.google.com'
    
    # Chrome
#    dedicated_window(url)

    # Firefox
#    dedicated_window(url, 'firefox')

    # default
    dedicated_window(url, 'bogus_browser_executable')

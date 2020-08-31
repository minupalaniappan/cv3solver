from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from flask import Flask, request

app = Flask(__name__)

app.config['PAGES'] = 0
app.config['DRIVER'] = None


def solve(site_key, action, site):
    options = Options()
    options.headless = True

    PAGES = app.config.get('PAGES', None)
    DRIVER = app.config.get('DRIVER', None)

    if PAGES is 50 and DRIVER is not None:
        app.config['PAGES'] = 0
        app.config['DRIVER'] = None
        DRIVER.quit()

    if DRIVER is None:
        app.config['DRIVER'] = webdriver.Firefox(options=options)

    driver = app.config.get('DRIVER', None)

    if driver is None:
        return ''

    driver.execute_script(
        '''window.open("{site}", "_blank");'''.format(site=site))

    driver.switch_to.window(driver.window_handles[PAGES])

    app.config['PAGES'] = app.config.get('PAGES', 0) + 1

    driver.get(site)
    driver.execute_script(
        "var s = window.document.createElement('script'); \
      s.src='https://www.google.com/recaptcha/api.js?render={site_key}'; \
      window.document.head.appendChild(s); \
      ".format(
            site_key=site_key
        )
    )

    driver.execute_script(
        "grecaptcha.execute('{site_key}', {{'action': 'search' }}).then(t => {{ window.localStorage.setItem('solution', t) }})".format(
            site_key=site_key
        )
    )

    solution = None

    while(solution is None):
        solution = driver.execute_script(
            "return window.localStorage.getItem('solution')"
        )

    return solution

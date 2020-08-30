from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def solve(site_key, action, site):
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

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

    driver.quit()

    return solution

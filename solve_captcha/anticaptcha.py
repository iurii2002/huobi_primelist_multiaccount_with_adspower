from anticaptchaofficial.recaptchav2proxyless import *

def solve_recaptchaV2(key, url, web_site_key):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(0)
    solver.set_key(key)
    solver.set_website_url(url)
    solver.set_website_key(web_site_key)
    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print("g-response: " + g_response)
    else:
        print("task finished with error " + solver.error_code)
    return g_response

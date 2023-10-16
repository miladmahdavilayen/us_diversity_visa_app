from twocaptcha import TwoCaptcha


def translate_captcha(path):  
    config = {
                'server':           'rucaptcha.com',
                'apiKey':           'ea2a130fe32ff8e6bd270d812d2525e7'
            }
    solver = TwoCaptcha(**config)
    result = solver.normal(path)
    
    return result
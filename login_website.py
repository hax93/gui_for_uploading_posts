import requests
import urllib3
urllib3.disable_warnings()

"""Login
to website with
panel adm.
"""

def linki(final_id, rodzaj):
    #   linki na podstawie rodzaj_linku//komunikat_post
    if rodzaj == 'Option1':
        licytacje_kom = 'linkoption1 with {final_id}'
        return licytacje_kom
    if rodzaj == 'Option2':
        pozostale_ogl = 'linkoption2 with {final_id}'
        return pozostale_ogl
    if rodzaj == 'Option3':
        sprawy_upadl = 'linkoption3 with {final_id}'
        return sprawy_upadl

def headers_func(final_id):
    #   function with headers need to requests
    headers_post = {
                    # ...
    }

try:
    def uwaga_post(user, password, lokalizacja, title_ogl, attachment,
                   data_publikacji, data_zakonczenia, date_time_now,
                   date_now, rodzaj_linku):
        
        headers = {
                    # ...
        }

        data = {
                    #data login, password
        }

        
        data_post = { 
                    #data containter in website
        }

        url = 'url website'

        #   session login
        with requests.Session() as session:
            response = session.get(url, verify=False)
            r_post = session.post(url, data=data, headers=headers, verify=False)
            
            #   get id from url
            url_id = r_post.url
            find_id = url_id.find('=')
            final_id = url_id[find_id + 1:]

            add_post = session.post(linki(final_id, rodzaj_linku), verify=False, data=data_post,
                                          headers=headers_func(final_id))
                    
                    
except Exception as exc:
    print(exc)
    

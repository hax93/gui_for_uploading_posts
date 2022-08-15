import logging

import requests
from bs4 import BeautifulSoup
from requests_ntlm3 import HttpNtlmAuth

"""Download
Attachment from SP
"""

#   errors
logging.basicConfig(filename='data/error_message.txt',
                    filemode='a+',
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )


try:
    def download_pdf(link_do_edit, user, password):
        username = ''
        user_download = fr"C:\Users\{user}\Downloads"
        url = 'url sharepoint list'
        
        with requests.Session() as session: 
            response = session.get(
                           url,
                           auth=HttpNtlmAuth(username, password)
                           )

            response = session.get(link_do_edit)
            with open('data/zalacznik.html', 'w', encoding="UTF-8") as f:
                    f.write(response.text)

            attach_html = 'data/zalacznik.html'       
            with open(attach_html, 'r', encoding='UTF-8') as response:
                soup = BeautifulSoup(response, 'html.parser')
                for i in soup.select('tr[id]'):   #wyświetla wszystkie tytuły
                    link = i.find('a', href=True)
                    if link is None:
                        continue
                    link_attach = link.get('href')
                    get_name_attach = link.get_text()
                    full_link = 'serwer SP + link_attach'
                    
                #   download attach 
                local_filename = full_link.split('/')[-1]
                with session.get(full_link, stream=True) as r:

                    r.raise_for_status()
                    with open(fr"{user_download}\{local_filename}", 'wb') as f:
                        for chunk in r.iter_content(chunk_size=None):
                            f.write(chunk)


except Exception as exc:
    logging.error(f"ERROR: {exc}")

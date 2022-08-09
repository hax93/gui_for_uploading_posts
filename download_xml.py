import json
import requests
import logging

from requests_ntlm3 import HttpNtlmAuth


#   errors
logging.basicConfig(filename='data/error_message.txt',
                    filemode='a+',
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )


try:
    def dow_excel(username, password):
        x = json.load(open('data/config.json'))
        url = x.get('URL')
        
        with requests.Session() as session: 
            response = session.get(
                url,
                auth=HttpNtlmAuth(username, password)
                )

            response = session.get(x.get('XML_SH'))
            with open(fr"data/sp_xml.xml", 'wb') as f:
                for chunk in response.iter_content(chunk_size=None):
                    f.write(chunk)

            url = []
            file = fr"data/sp_xml.xml"
            with open(file, mode='r') as file_xml:
                for i, v in enumerate(file_xml):
                    if i == 2:
                        url.append(v)

            #   url get from sp_xml.xml
            response = session.get(url[0])
            with open(fr"data/baza_xml.xml", 'wb') as f:
                for chunk in response.iter_content(chunk_size=None):
                    f.write(chunk)
            
except Exception as exc:
    logging.error(f"ERROR: {exc}")

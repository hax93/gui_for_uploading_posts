import logging
import xml.etree.ElementTree as ET

import pandas as pd

#   errors
logging.basicConfig(filename='data/error_message.txt',
                    filemode='a+',
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )


try:
    def get_data_xml():
        file = fr"data/baza_xml.xml"
        xmlparse = ET.parse(file)
        root = xmlparse.getroot()
        
        sharepoint = []
        number = 0
        for i in root.iter():
            #   only 300 rows get from baza_xml.xml
            if number >= 300:
                break
            if i.attrib.get('xyz') == None:
                continue
            else:
                """
                Data anonimized

                """
                
                sharepoint.append(["xyz"])
                number += 1
                
        columns = ["xyz..."]
        
        df = pd.DataFrame(sharepoint, columns=columns)
        df.to_excel(fr"data/final_excel.xlsx", index=False)

        
except Exception as exc:
    logging.error(f"ERROR: {exc}")

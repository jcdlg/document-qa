
import os
import re

# PI for Orencia has different format, set manually
orencia_indications = '''ORENCIA is a prescription medicine that reduces signs and symptoms in:  
• adults with moderate to severe rheumatoid arthritis (RA), including those who have not been helped enough by 
other medicines for RA. ORENCIA may prevent further damage to your bones and joints and may help your ability 
to perform daily activities. In adults, ORENCIA may be used alone or with other RA treatments other than tumor 
necrosis fact or (TNF) antagonists.  
• people 2 years of age and older with moderate to severe polyarticular juvenile idiopathic arthritis ( pJIA). ORENCIA 
may be used alone or with methotrexate.  
• people 2 years of age and older with active psoriatic arthritis (PsA). In adul ts, ORENCIA can be used alone or with 
other PsA treatments.  In children, ORENCIA can be used alone or with methotrexate.  
 
ORENCIA is also used for the preventative treatment of acute graft versus host disease (aGVHD) , in combination with 
a calcineurin inhi bitor and methotrexate, in:  
• people 2 years of age and older undergoing hematopoietic stem cell transplantation (HSCT) from a matched or 1 
allele -mismatched unrelated- donor .  '''


def get_indication(text):
    indications = ""
    #p = re.search("--+ *INDICATIONS AND USAGE *--+(.+?)--+", text, flags=re.MULTILINE | re.DOTALL)
    p = re.search("--+ *INDICATIONS AND USAGE *-*(.+?)--+", text, flags=re.MULTILINE | re.DOTALL)
    if p:
        indications = p.group(1)
    return indications


def get_indication_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
        
    indication = get_indication(text)
    if not indication: 
        print("Indications missing in ",file_name)
    return indication

def get_all_indications():
    txt_directory = "product_inserts/txt/"
    text = ""
    for file_name in os.listdir(txt_directory):
        #print(txt_directory+file_name)
        #print(get_indication_from_file(txt_directory+file_name))
        text += get_indication_from_file(txt_directory+file_name)
    text += orencia_indications
    return text

text = get_all_indications()


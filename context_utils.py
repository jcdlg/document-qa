import os
import re

# PI for Orencia has different format, set manually
orencia_indications = """
DOC: pi_zeposia.txt
Content: 
ORENCIA is a prescription medicine that reduces signs and symptoms in:  
• adults with moderate to severe rheumatoid arthritis (RA), including those who have not been helped enough by 
other medicines for RA. ORENCIA may prevent further damage to your bones and joints and may help your ability 
to perform daily activities. In adults, ORENCIA may be used alone or with other RA treatments other than tumor 
necrosis fact or (TNF) antagonists.  
• people 2 years of age and older with moderate to severe polyarticular juvenile idiopathic arthritis ( pJIA). ORENCIA 
may be used alone or with methotrexate.  
• people 2 years of age and older with active psoriatic arthritis (PsA). In adul ts, ORENCIA can be used alone or with 
other PsA treatments.  In children, ORENCIA can be used alone or with methotrexate.  
 
ORENCIA is also used for the preventative treatment of acute graft versus host disease (aGVHD) , in combination with 
a calcineurin inhibitor and methotrexate, in:  
• people 2 years of age and older undergoing hematopoietic stem cell transplantation (HSCT) from a matched or 1 
allele -mismatched unrelated-donor .

-----
"""


def get_indications_from_pi(pi):
    indications = ""
    # p = re.search("--+ *INDICATIONS AND USAGE *--+(.+?)--+", text, flags=re.MULTILINE | re.DOTALL)
    p = re.search(
        "--+ *INDICATIONS AND USAGE *-*(.+?)--+", pi, flags=re.MULTILINE | re.DOTALL
    )
    if p:
        indications = p.group(1)
    return indications


def load_pi_from_file(file_name):
    with open(file_name, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()

    indication = get_indications_from_pi(text)
    #if not indication:
    #    print("Indications missing in ", file_name)

    return indication


def get_context():
    """Get context for a GPT chat.  Currently retrieves the indications for PIs for top selling BMS drugs."""

    pi_dir = "product_inserts/txt/"
    context = """
-----
"""
    for file_name in os.listdir(pi_dir):
        # print(pi_dir + file_name)
        # print(load_pi_from_file(pi_dir + file_name))

        document_name = file_name
        document_content = load_pi_from_file(pi_dir + file_name)
        document = f"""

DOC: {document_name}
Content: {document_content}

-----

"""
        context += document
        
    context += orencia_indications
    print(context)
    return context


# text = get_all_indications()
# print(text)

import re
from transliterate import translit

russian_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'

def transliterate_ru_to_en(st):

    st = re.sub(r'(?!['+russian_letters+'0-9 ]+?).*?','',st)
    st = st.lower().replace(' ','_')
    st = translit(st, "ru", reversed=True)
    st = re.sub(r'(?![a-zA-Z0-9_]+?).*?','',st).strip('_')

    return st


def clean_text(text):
    
    status = 0 # text was cleaned successfully
    space = '[ \t\r\f\v]' # \s without \n
    punct1  = '[#$%&\*+/:<=>?@[\\]^_{|}~]' # string.punctuation without ! " ' ( ) , - . ; `
    punct2  = '[#$%&\*+/:<=>?@[\\]^_{|}~-]' # punct1 with -
    chord  = '\W([a-z]{1,2}[0-9]*(?:('+space+'+?)|('+punct1+'+?)))' # string like 'am dm5 c'
    num_punct = '(?:([0-9]*'+space+'*'+punct2+'+\d+'+punct2+'+)|(\d+'+punct2+'+))'
    
    text   = '\n'+text.lower()+'\n'
    
    try:
                
        text = re.sub(r''+num_punct+'+', ' ', text) # remove str like '|-5--7--5--7--5--7--5--7-|'
        text = re.sub(r''+punct1+'+','',text ) # remove some of punct symbols, see definition for details
        text = re.sub(r''+chord+'+', ' ', text) # remove chords
        
        # remove the word from the list if it is the only cyrillic word in a row
        for r_word in ['вступление', 'припев', 'проигрыш', 'соло','запев','соло для припева', ' ']:
            text = re.sub(r'\n'+space+'*?'+r_word+space+'*?\n', '\n', text)
            
            # remove string like 'припев 2 раза'
            text = re.sub(r'\n\W*?('+r_word+punct1+'*'+space+'*[0-9]+'+space+'*раз.{0,2})+\n', '\n', text) 

        
        text = re.sub(r'\n+', '\n', text).strip()
    except Exception as e:
        status = 1 # exception was raised
        print(f'Exception raised: {e}')
        
    return text, status
# %%
import pandas as pd
import numpy as np
import docxpy

def flag_private_urls(doc):
    '''This function takes a word document name as an input, identifies hyperlinks and their urls that do not fit the criteria of being in a newsletter. The function returns a table with columns 'Link_Text','Likely_Personal_URL?', and 'URL' with all the URLs within the document, sorted by the likeliness of being a personal link.'''

    #read in document
    #file = f'{doc}.docx'
    #create DOCReader object
    doc = docxpy.DOCReader(doc)
    #process file
    doc.process() 
    #extract hyperlinks
    hyperlinks = doc.data['links']
    
    # create DataFrame using hyperlinks object 
    df = pd.DataFrame(hyperlinks, columns =['Link_Text', 'URL'])
    #the 'text' column is byte type, convert to string type
    df['Link_Text'] = df['Link_Text'].str.decode("utf-8")
    
    #initiate a list of words to filter the dataframe, and return the result. This list will soon grow once we are able to obtain more examples of private urls.
    words_to_filter = ["personal",':p:/t'] 
    df['Likely_Private_URL?'] = df.iloc[:, 1].str.contains(r'\b(?:{})\b'.format('|'.join(words_to_filter)))
    df = df.sort_values(by='Likely_Private_URL?',ascending=False)
    result =  df[['Link_Text','Likely_Private_URL?','URL']]
    #pandas setting to see the whole url
    #result = result.to_json()
    return result


# %%
from gensim.summarization import summarize
from summarizer import Summarizer
# from TextRankSummarizer import get_summary
import unicodedata
import pandas as pd
import numpy as np
import re
import math

#this is the model for Bert extractor summarization
model = Summarizer()

def gensim_sum(text, ratio=0.2):
    """ 
    text : Text to be summarized
    ratio : Length of summary (value from 0-1.0) relative to original text
    """
    return summarize(text, ratio=ratio)

def bert_sum(text, ratio=0.2, model=model):
    """
    text : Text to be summarized
    ratio : Length of summary (value from 0-1.0) relative to original text
    """
    return model(text, ratio=ratio)

def top_sum(text, ratio=0.3):
    """
    text : Text to be summarized
    ratio : Length of summary (value from 0-1.0) relative to original text 
    """
    sentences = re.split(r'(?<!Ms)(?<!Mr)(?<!vs)\.|\!|\?', text)
    length = len(sentences)
    n = math.ceil(ratio*length)
    return ('.').join(sentences[0:n])

def rob_sum(text, sentence_length=4):
    """
    text : Text to be summarized
    sentence_length : Length of summary in number of sentences
    """
    df = pd.DataFrame([text], columns=['text'])
    return (' ').join(get_summary(df, sentence_length=sentence_length))

def extract_sum(text, ratio, method='bert_sum'):
    text = unicodedata.normalize("NFKD", text)
    text.replace('\n','')
    if method == 'bert_sum':
        return bert_sum(text, ratio)
    elif method == 'gensim_sum':
        return gensim_sum(text, ratio)
    elif method == 'top_sum':
        return top_sum(text, ratio)
    elif method == 'rob_sum':
        return rob_sum(text)
    else:
        return "This method is not supported. Try 'bert_sum', 'gensim_sum', 'rob_sum', or 'top_sum'."
#%%
test = "There is a total of 161 partners in the $1M+ TTM Tranche, which is up from 125 (vs. last year) and 161 (vs. last month) representing 29% YoY growth. This is down from February number of 166. 63 of these partners are coming from the $100K-999K & <$100K tranches. The growth in the $100-999K tranche when it comes to number of partners is 13%, which is mainly driven by CSP (45 growth). With continued efforts to build the Power Apps ecosystem, 56+ AIAD were delivered and Airlifts via Teams since late March. The NEW Partner Playbook and Pitch deck are launching during June. For Power Bi, since March this year, 76 Partners executed a total of Virtual DIAD 162 sessions with ~4,000 attendees, resulting in 1,000+ leads. 150+ more DIAD planned by end of FY20. The first VILT of the Power BI Adoption Framework was finished with 1,945 partner attendees. When it comes to BGI, the targeted partner investments, there have been 10 partners in the top performance category grow 78% YoY and 15 partners in the next tranche category grow 215% YoY as a group. While this represents 50 of the SIs invested in, the year 1 of BGI gives great learnings to apply in FY21 to target investments towards new areas of growth around the new 6 Sales Plays. From the ISV Investments, there have been 23 Business Central applications migrated that are published in AppSource. Lastly, while we learned a lot about our GSI investments and are redesigning how to measure impact, we’re seeing 50%+ YoY in the Business Apps influenced revenue coming from Accenture and KPMG."
test_two = "Last month, the 60th Premium Tier app was approved! By focusing on the BizApps Premium Tier offers, you benefit from the 20% RevShare. Each app has been through a comprehensive evaluation by the Biz Apps BG is recommended for you to prioritize these offers for joint account planning. Click here to see a list of all Premium Tier offers in Co-sell Solution Finder. More information on the ISV Connect Program or Premium Tier benefits can be found on Business Applications Hub on //Learning. Call to action: Include the Premium Tier offers for joint account planning in your area. For questions, contact bizappsISVprogram@microsoft.com."
test_three = "Attend a free Airlift to accelerate your journey to become a Power Apps and Automate partner, seats and events are limited!  Starting to build your Power Apps practice? Get hands on training to quickly grow your capacity and business with Power Apps. If you are a practice lead, ask your technical & customer facing resources to sign up for the Airlift today. Why build a Power Apps and Automate practice? Implement solutions with 3-month ROI. Save on developer time by nearly 70%. Modernize both 1st and 3rd party applications on one single platform. Register for the Power Apps and Automate Partner Airlift."
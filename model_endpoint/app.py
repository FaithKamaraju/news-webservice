from fastapi import FastAPI
from contextlib import asynccontextmanager
import torch
from transformers import AutoConfig,AutoTokenizer,BertForTokenClassification
import math
import json



models = {}
tokenizers = {}
text = "LONDON — Dozens of countries, including Germany, South Africa and Mexico, said Friday that President Donald Trump’s decision to sanction the International Criminal Court would “erode the international rule of law.”\n\nThe joint statement by 79 countries came hours after Trump signed an executive order slapping financial sanctions and visa restrictions against ICC staff and their family members, alleging the court has improperly targeted the United States and Israel.\n\n“Such measures increase the risk of impunity for the most serious crimes and threaten to erode the international rule of law, which is crucial for promoting global order and security,” the 79 countries, including Canada and France, said in a statement publicly released by numerous governments.\n\nThe statement added that “sanctions could jeopardize the confidentiality of sensitive information and the safety of those involved—including victims, witnesses, and court officials, many of whom are our nationals.”\n\nThe International Criminal Court in The Hague, Netherlands. Alex Gottschalk / DeFodi Images via Getty Images\n\nThe signatories said the sanctions may result in the ICC having to close its field offices.\n\n\"We regret any attempts to undermine the court’s independence, integrity and impartiality,\" they said, crediting the \"ICC’s indispensable role in ending impunity, promoting the rule of law, and fostering lasting respect for international law and human rights.\"\n\nThe United States and Israel are among a minority of around 40 countries that never signed up to the ICC, an international court based in the Netherlands that seeks to hold to account the perpetrators of war crimes, like genocide.\n\nBut after some historic cooperation between Washington and the ICC, Trump's executive order Thursday accused the world body of “illegitimate and baseless actions targeting America and our close ally Israel.”\n\nIn November, the ICC issued arrest warrants for Israeli Prime Minister Benjamin Netanyahu and former Israeli Defense Minister Yoav Gallant, as well as for Hamas leaders Yahya Sinwar, Mohammad Deif and Ismail Haniyeh.\n\nThe warrants relate to events on and since Oct. 7, 2023, when Hamas-led terrorist attacks killed 1,200 people and saw around 250 others taken hostage, according to Israeli officials. Since, then Israel has launched a military offensive that has killed more than 47,500 people in the Gaza Strip, according to local health officials.\n\nThe court said there was reason to believe Netanyahu and Gallant used “starvation as a method of warfare” by restricting humanitarian aid and intentionally targeting civilians in Israel’s campaign in Gaza. Israel, which also does not recognize the ICC, dismissed those charges as false and antisemitic.\n\nThe court's \"recent actions against Israel and the United States set a dangerous precedent, directly endangering current and former United States personnel, including active service members of the Armed Forces, by exposing them to harassment, abuse, and possible arrest,\" the executive order said.\n\nIts signing appeared timed to coincide with Netanyahu's visit to Washington, in which Trump made the surprise announcement that he wanted the U.S. to take control of the Gaza Strip, shocking and outraging many officials, activists and experts around the world.\n\nWashington’s historical relationship with the ICC is a complex one.\n\nThe administration of President Bill Clinton was involved in negotiating the 1998 Rome Statute on which the ICC is based. But the U.S. opposed the final draft because of fears it “could subject U.S. soldiers and officials to politicized prosecutions,” according to the Council on Foreign Relations.\n\nClinton later signed the statute but asked it not be sent to the Senate for ratification until these concerns were addressed."




def chunk_text(model,text:str, tokenizer, prob_threshold=0.5)->list[str]:
    # slide context window chunking
    MAX_TOKENS=191
    tokens=tokenizer(text, return_tensors="pt",truncation=False)
    input_ids=tokens['input_ids']
    attention_mask=tokens['attention_mask'][:,0:MAX_TOKENS]
    attention_mask=attention_mask.to(model.device)
    CLS=input_ids[:,0].unsqueeze(0)
    SEP=input_ids[:,-1].unsqueeze(0)
    input_ids=input_ids[:,1:-1]
    model.eval()
    split_str_poses=[]
    
    token_pos = []

    windows_start =0
    windows_end= 0
    logits_threshold = math.log(1/prob_threshold-1)
    
    print(f'Processing {input_ids.shape[1]} tokens...')
    while windows_end <= input_ids.shape[1]:
        windows_end= windows_start + MAX_TOKENS-2

        ids=torch.cat((CLS, input_ids[:,windows_start:windows_end],SEP),1)

        ids=ids.to(model.device)
        
        output=model(input_ids=ids,attention_mask=torch.ones(1, ids.shape[1],device=model.device))
        logits = output['logits'][:, 1:-1,:]
        chunk_decision = (logits[:,:,1]>(logits[:,:,0]-logits_threshold))
        greater_rows_indices = torch.where(chunk_decision)[1].tolist()

        # null or not
        if len(greater_rows_indices)>0 and (not (greater_rows_indices[0] == 0 and len(greater_rows_indices)==1)):

            split_str_pos=[tokens.token_to_chars(sp + windows_start + 1).start for sp in greater_rows_indices]
            token_pos +=[sp + windows_start + 1 for sp in greater_rows_indices]
            split_str_poses += split_str_pos

            windows_start = greater_rows_indices[-1] + windows_start

        else:

            windows_start = windows_end

    substrings = [text[i:j] for i, j in zip([0] + split_str_poses, split_str_poses+[len(text)])]
    token_pos = [0] + token_pos
    return substrings,token_pos



@asynccontextmanager
async def lifespan(app : FastAPI):
    
    model_path="./models/tim1900/bert-chunker-2"
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        padding_side="right",
        model_max_length=255,
        trust_remote_code=True,
    )
    config = AutoConfig.from_pretrained(
        model_path,
        trust_remote_code=True,
    )
    device = 'cuda'# or cuda
    
    model = BertForTokenClassification.from_pretrained(model_path, ).to(device)
    models['bert-chunker'] = model
    tokenizers['bert-chunker'] = tokenizer
    
    yield
    
    # del models
    print("Shutting down")
    
    

    
app = FastAPI(lifespan = lifespan)



@app.get('/chunk')
async def chunk() -> dict[str,list[int]]:

    # chunk the text. The prob_threshold should be between (0, 1). The lower it is, the more chunks will be generated.
    chunks, token_pos = chunk_text(models['bert-chunker'], text, tokenizers['bert-chunker'], prob_threshold=0.5)

    return {'chunk_lengths':[len(chunk) for chunk in chunks ]}


@app.get('/bias')
async def bias():
    return {"bias_score":0.5}



#2022.7.24 pip install mysqlclient
from uvirun import *
myhost,myport,mydb  = os.getenv("myhost", "lab.jukuu.com" if "Windows" in platform.system() else "172.17.0.1"), int(os.getenv("myport", 3307)) ,os.getenv("mydb", "kpsi")

@app.get('/kpsi/rows', tags=["kpsi"])
def rows(sql:str="show tables"):
	import pymysql
	if not hasattr(rows, 'conn') or not rows.conn.ping():
		rows.conn = pymysql.connect(host=myhost,port=myport,user='root',password='cikuutest!',db=mydb) #, defer_connect=True
	with rows.conn.cursor() as cursor: #pymysql.cursors.SSDictCursor
		cursor.execute(sql)
		res = cursor.fetchall()
	return res 

@app.get('/kpsi/snts', tags=["kpsi"], response_class=HTMLResponse)
def kpsi_snts(s:str="open:VERB:dobj:NOUN:door", cp:str='dic', hl_words:str="open,door", topk:int=10): 
	''' return HTML <ol><li> , 2022.7.24 '''
	from dic import lemma_lex
	sids = rows(f"select t from {cp} where s = '{s}' limit 1")
	if sids and len(sids) > 0 :
		sids = ",".join([str(sid) for sid in sids[0][0].split(',')[0:topk] ])
	snts = rows(f"select snt from {cp}_snt where sid in ({sids})")
	words = '|'.join([ '|'.join(list(lemma_lex.lemma_lex[w])) for w in hl_words.strip().split(',') if w in lemma_lex.lemma_lex])
	arr = [re.sub(rf'\b({words})\b', r'<font color="red">\g<0></font>', snt[0]) if words else snt[0] for snt in snts]
	html = "\n".join([f"<li>{snt}</li>" for snt in arr])
	return HTMLResponse(content=f"<ol>{html}</ol>")

@app.get('/kpsi/kndata', tags=["kpsi"])
def kn_data(sumkey='knowledge:NOUN:~dobj', cps:str='clec', cpt:str='dic', slike:str="knowledge:NOUN:~dobj:VERB:%"): 
	''' return (word, srccnt, tgtcnt, srcsum, tgtsum, keyness) '''
	try:
		clause = f"like '{slike}'" if '%' in slike else f" in ('" + "','".join(slike.strip().split(',')) + "')" # in ('consider:VERB:vtov','consider:VERB:vvbg')
		df = pd.DataFrame({cps: dict(rows(f"select s, i from {cps} where s {clause}")),
			cpt: dict(rows(f"select s, i from {cpt} where s {clause}"))}).fillna(0)
		df[f'{cps}_sum'] = rows(f"select i from {cps} where s ='{sumkey}' limit 1")[0][0]
		df[f'{cpt}_sum'] = rows(f"select i from {cpt} where s ='{sumkey}' limit 1")[0][0]
		df = df.sort_values(df.columns[0], ascending=False) #.astype(int)
		return [ {"index": index,cps:int(row[cps]),f'{cps}_sum':int(row[f'{cps}_sum']),cpt:int(row[cpt]),f'{cpt}_sum':int(row[f'{cpt}_sum']), 'keyness':likelihood(row[cps],row[cpt],row[f'{cps}_sum'],row[f'{cpt}_sum'])}  for index, row in df.iterrows()] 
	except Exception as e:
		print("kn_data ex:", e) 
		return []

if __name__ == '__main__':
	print (kn_data(), flush=True)
	uvicorn.run(app, host='0.0.0.0', port=80)

'''
@app.get('/kpsi/si', tags=["kpsi"])
def si(sql,asdic:bool=True): return { s:int(i) for s,i in rows(sql)} if asdic else [ (s,int(i)) for s,i in rows(sql)]

import io
from starlette.responses import StreamingResponse
app = FastAPI()
@app.post("/vector_image")
def image_endpoint(*, vector):
    # Returns a cv2 image array from the document vector
    cv2img = my_function(vector)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
'''
"""Extract exact tested clean fixed-head Work build ZIP; never build or update market data."""
import hashlib,json,re,zipfile
from pathlib import Path
HEAD='6402a46d8d493eef34bd3735341cabc37cd4cf64'
SPECS={'rc':('3981b5968a7a870ef8e7a649dcb21b61f5b44918527afd4747bcc08be9c0e98e','8f111cdbdfd9d662aafe3aa4f5b04e51def145aad1d36c838ea0b119244c3ba6','bd5c0630bc3424e7c20aed05cf1f8801af90e34bd27563a9743615b907b1d7f9')}
sha=lambda b:hashlib.sha256(b).hexdigest()
LANDING='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PR #9 產業名稱 Safari 預覽</title><style>body{font:18px/1.7 system-ui;max-width:700px;margin:40px auto;padding:20px;background:#0b1626;color:#dce7f5}a{color:#96baff}code{overflow-wrap:anywhere}</style><h1>PR #9 產業中文名稱預覽</h1><p>獨立測試環境，非正式網站。固定舊行情日期：2026/10/13，未更新行情。</p><p><a href="rc/">開啟 Safari 驗收候選</a></p><p>候選 <code>6402a46d8d493eef34bd3735341cabc37cd4cf64</code></p><p>請確認產業輪動、族群明細、熱力圖及個股抽屜中文名稱。17 上市為金融保險，上櫃為金融業；合併母體保留兩者名稱。未知分類保留原碼。</p><p>同一 owner 的 GitHub Pages 共用 origin，建議使用 Safari 私密瀏覽避免舊快取與關注清單干擾。新候選尚待 iPhone Safari 真機驗收；VoiceOver 與實體鍵盤未驗證。</p><a href="preview-inventory.json">檔案 SHA256 清單</a></html>'
root=Path('site');root.mkdir(exist_ok=False);inventory={}
for mode,(ziphash,mhash,datahash) in SPECS.items():
 archive=Path('approved-'+mode+'.zip');assert sha(archive.read_bytes())==ziphash
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();assert len(names)==len(set(names))==8
  assert all(n in ['index.html','.nojekyll','market.json','release-manifest.json'] or re.fullmatch(r'assets/[A-Za-z0-9_.-]+\.(js|css)',n) for n in names)
  assert all((i.external_attr>>16)&0o170000!=0o120000 for i in z.infolist());assert sum(i.file_size for i in z.infolist())<12*1024*1024
  files={n:z.read(n) for n in names};assert sha(files['release-manifest.json'])==mhash;assert sha(files['market.json'])==datahash
  m=json.loads(files['release-manifest.json']);assert set(files)==set(m['assets'])|{'release-manifest.json'}
  assert m['asOf']=='2026-10-13' and m['profile']=='observation-only' and m['strategyComplete'] is False and m['deploymentAuthorized'] is False
  if mode=='rc':assert m['candidateCommit']==HEAD and m['localTreeDirty'] is False
  for n,b in files.items():
   if n in m['assets']:assert sha(b)==m['assets'][n]
   path=root/mode/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b);inventory[mode+'/'+n]={'sha256':sha(b),'bytes':len(b)}
for n in ['index.html','.nojekyll']:
 b=LANDING.encode() if n=='index.html' else b'';(root/n).write_bytes(b);inventory[n]={'sha256':sha(b),'bytes':len(b)}
(root/'preview-inventory.json').write_text(json.dumps({'sourceHead':HEAD,'sourceRun':40854910931,'sourceBuild':'clean fixed-head Work build','environment':'ISOLATED TEST PREVIEW ONLY','marketDate':'2026-10-13','productionAuthorized':False,'files':inventory},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'verified':True,'sourceHead':HEAD,'files':len(inventory),'rebuild':False,'productionAuthorized':False}))

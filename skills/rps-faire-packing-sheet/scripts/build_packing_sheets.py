#!/usr/bin/env python3
"""Build offline Faire packing checklists from verified order JSON and local photos."""
import argparse, base64, csv, hashlib, html, io, json, mimetypes, re
from collections import Counter
from pathlib import Path


def build(source, out):
    source=Path(source).resolve(); out=Path(out).resolve()
    data=json.loads(source.read_text()); orders=data['orders']
    if not orders: raise ValueError('No orders supplied')
    template=(Path(__file__).resolve().parents[1]/'assets/packing.html').read_text()
    results=[]; seen_orders=set(); rendered=[]
    for raw in orders:
        order=dict(raw); oid=order['order_id']
        if not re.fullmatch(r'[A-Za-z0-9-]+',oid) or oid in seen_orders: raise ValueError('Invalid or duplicate order ID')
        seen_orders.add(oid)
        for field in ('customer','verified_at','status','ship_date','source_url'):
            if not isinstance(order.get(field),str) or not order[field].strip(): raise ValueError(f'{oid}: missing {field}')
        items=[dict(i) for i in order['items']]
        if not items: raise ValueError(f'{oid}: no items')
        seen_lines=set()
        for i in items:
            for f in ('sku','title','size','photo_path'):
                if not isinstance(i.get(f),str) or not i[f].strip(): raise ValueError(f'{oid}: missing {f}')
            if type(i.get('quantity')) is not int or i['quantity']<1: raise ValueError(f'{oid}: invalid quantity')
            if 'id' not in i: i['id']=hashlib.sha256((i['sku']+'\0'+i['size']).encode()).hexdigest()[:20]
            if i['id'] in seen_lines: raise ValueError(f'{oid}: duplicate line key; provide source line IDs')
            seen_lines.add(i['id'])
            i['title']=html.unescape(i['title'])
            photo=(source.parent/i.pop('photo_path')).resolve(); content=photo.read_bytes()
            if content.startswith(b'\xff\xd8\xff'): mime='image/jpeg'
            elif content.startswith(b'\x89PNG\r\n\x1a\n'): mime='image/png'
            elif content[:4]==b'RIFF' and content[8:12]==b'WEBP': mime='image/webp'
            elif content[:6] in (b'GIF87a',b'GIF89a'): mime='image/gif'
            else: raise ValueError(f'{oid}: unsupported or invalid photo {photo.name}')
            i['photo']='data:'+mime+';base64,'+base64.b64encode(content).decode()
        units=sum(i['quantity'] for i in items)
        if order.get('expected_lines') != len(items): raise ValueError(f'{oid}: source line count mismatch')
        if order.get('expected_units') != units: raise ValueError(f'{oid}: source unit count mismatch')
        order['items']=items
        sizes=Counter()
        for i in items: sizes[i['size']]+=i['quantity']
        page=template
        replacements={'CUSTOMER':order['customer'],'ORDER_ID':oid,'LINES':len(items),'UNITS':units,'SIZE_SUMMARY':'; '.join(f'{s}: {q}' for s,q in sizes.items()),'VERIFIED':order['verified_at'],'STATUS':order['status'],'SHIP_DATE':order['ship_date']}
        for key,value in replacements.items(): page=page.replace('__'+key+'__',html.escape(str(value)))
        page=page.replace('__DATA__',json.dumps(order,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029'))
        slug=re.sub(r'[^a-z0-9]+','-',order['customer'].lower()).strip('-') or 'order'
        filename=f'{slug}-{oid}-packing.html'
        csvout=io.StringIO(); writer=csv.writer(csvout); writer.writerow(['SKU','Title','Size','Quantity'])
        writer.writerows((i['sku'],i['title'],i['size'],i['quantity']) for i in items)
        rendered.append((filename,page,csvout.getvalue()))
        results.append({k:order[k] for k in ('order_id','customer','status','ship_date','verified_at','source_url')}|{'lines':len(items),'units':units,'photos':len(items),'file':filename})
    out.mkdir(parents=True,exist_ok=True)
    for name,page,csvdata in rendered:
        dest=out/name
        if dest.exists(): raise FileExistsError(f'Preserve existing outputs; use a new output folder: {dest}')
    for name,page,csvdata in rendered:
        (out/name).write_text(page); (out/name.replace('.html','.csv')).write_text(csvdata)
    esc=html.escape
    rows=''.join(f'<tr><td><a href="{esc(r["file"])}">{esc(r["customer"])}</a><small>#{esc(r["order_id"])}</small></td><td>{esc(r["ship_date"])}</td><td>{r["lines"]}</td><td>{r["units"]}</td><td><a href="{esc(r["file"])}">Open sheet →</a></td></tr>' for r in results)
    index='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Faire packing desk</title><style>body{font:16px/1.5 system-ui;background:#f6f4ee;color:#25372d;margin:0;padding:40px 24px}main{max-width:1100px;margin:auto}h1{font:44px Georgia;margin:10px 0}a{color:#315b40}small{display:block;color:#657168}table{width:100%;border-collapse:collapse;background:white;margin:26px 0}th,td{text-align:left;padding:18px;border-bottom:1px solid #dedfd5}th{font-size:12px;text-transform:uppercase}p{color:#657168}.scroll{overflow:auto}button,input{font:inherit}input{padding:12px;width:min(100%,500px);box-sizing:border-box;border:1px solid #b7c2b3;border-radius:8px}@media(max-width:600px){body{padding:24px 16px}h1{font-size:34px}th,td{padding:12px}}</style><main><small>ROCK PAPER SCISSORS / PACKING DESK</small><h1>Faire packing sheets</h1>'''
    index+=f'<p>{len(results)} open orders · {sum(r["lines"] for r in results)} line items · {sum(r["units"] for r in results)} prints</p>'
    index+='<input type="search" aria-label="Find an order" placeholder="Find customer or order number…"><div class="scroll"><table><thead><tr><th>Customer / order</th><th>Ship date</th><th>Lines</th><th>Prints</th><th>Packing sheet</th></tr></thead><tbody>'+rows+'</tbody></table></div><p>Each sheet has offline photos, title and SKU search, print sizes, quantities, saved checkmarks, and a print view. Checkmarks save in the same browser and do not update Faire.</p><p>Verified '+esc(data.get('verified_at',results[0]['verified_at']))+'. Open orders include New and Unfulfilled; fulfilled and canceled orders are excluded.</p></main><script>document.querySelector("input").addEventListener("input",e=>document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(e.target.value.toLowerCase())))</script></html>'
    (out/'index.html').write_text(index)
    (out/'manifest.json').write_text(json.dumps({'verified_at':data.get('verified_at'),'orders':results},indent=2,ensure_ascii=False))
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('input'); p.add_argument('--output',required=True); a=p.parse_args()
    for r in build(a.input,a.output): print(f'{r["order_id"]}: {r["lines"]} lines / {r["units"]} prints / {r["photos"]} photos -> {r["file"]}')

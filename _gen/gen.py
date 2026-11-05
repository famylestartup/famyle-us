"""Gera o pacote organico de pre-lancamento Famyle Orlando (LPs familia, LPs de vaga, guias, sitemap, llms.txt).
Fonte unica dos dados: facts.json (cada numero com fonte). Uso: python _gen/gen.py
"""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = json.load(open(os.path.join(ROOT, "_gen", "facts.json"), encoding="utf-8"))
BASE = "https://us.famyle.com"
TODAY = datetime.date.today().isoformat()
GA = "G-8DPML3JJ6F"; AW = "AW-11419257934"; LBL_WAIT = "tPyrCI_drbAdEM6YkMUq"
FORM = "https://formsubmit.co/ajax/adm@famyle.com"
API = "https://api.famyle.com/nps/us/lead/"  # D-444: grava no nosso banco (tabela us_lead). /nps/ e nao /metrics/: o Cloudflare desvia api.famyle.com/metrics/* para o Google
e = html.escape
def pl(w):
    w = w.lower(); return w[:-1] + 'ies' if w.endswith('y') and w[-2:-1] not in 'aeiou' else w + 's'
pages = []  # (path, title) para sitemap/llms

CSS = """:root{--ink:#1d1d2b;--muted:#5d5f73;--brand:#6b3fd6;--brand-2:#f4efff;--line:#e7e5ef;--ok:#1f8a5b}
*{box-sizing:border-box}html,body{margin:0}body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}header{padding:16px 0;border-bottom:1px solid var(--line)}header .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px}
.logo{font-weight:800;font-size:22px;color:var(--brand);text-decoration:none}nav a{color:var(--muted);text-decoration:none;font-size:14px;margin-left:14px}
.crumbs{font-size:13px;color:var(--muted);margin:14px 0 0}.crumbs a{color:var(--muted)}
.hero{background:linear-gradient(180deg,var(--brand-2),#fff);padding:30px 0 26px}
h1{font-size:clamp(28px,5vw,40px);line-height:1.15;margin:10px 0 12px;letter-spacing:-.5px}h2{font-size:23px;margin:34px 0 10px}h3{font-size:18px;margin:18px 0 6px}
.lead{font-size:18px;color:var(--muted);margin:0 0 18px}.badge{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:14px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:15px}th,td{border:1px solid var(--line);padding:8px 10px;text-align:left}th{background:#faf9ff}
.src{font-size:13px;color:var(--muted)}.box{border:1px solid var(--line);border-radius:16px;padding:20px;margin:20px 0}
.btn{display:inline-block;background:var(--brand);color:#fff;border:0;border-radius:12px;padding:14px 22px;font-size:17px;font-weight:700;cursor:pointer;text-decoration:none}
label{display:block;font-size:14px;font-weight:600;margin:10px 0 4px}input,select,textarea{width:100%;font-family:inherit;padding:11px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:#fff}
.row{display:flex;gap:10px}.row>*{flex:1}.ok{display:none;color:var(--ok);font-weight:700}
ul.links{columns:2;padding-left:18px}footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0;color:var(--muted);font-size:14px}
@media(max-width:600px){ul.links{columns:1}.row{flex-direction:column}}"""

def head(title, desc, path, jsonld):
    url = BASE + path
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<link rel="stylesheet" href="/assets/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={AW}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{AW}');gtag('config','{GA}');</script>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script></head><body>
<header><div class="wrap"><a class="logo" href="/">famyle</a><nav><a href="/">Families</a><a href="/jobs/">Jobs</a><a href="/guides/">Guides</a></nav></div></header>"""

FOOT = """<footer><div class="wrap">Famyle is an online platform in Orlando, Florida: families hire professionals directly; Famyle is not an employer or a staffing agency.<br>
<a href="/">For families</a> · <a href="/jobs/">For professionals</a> · <a href="/guides/">Guides</a> · <a href="/pt/guias/">Guias em português</a> · <a href="mailto:suporte@famyle.com">suporte@famyle.com</a><br>Areas: <a href="/orlando/winter-garden-horizon-west/">Winter Garden &amp; Horizon West</a> · <a href="/orlando/windermere/">Windermere</a> · <a href="/orlando/dr-phillips/">Dr. Phillips</a> · <a href="/orlando/metrowest/">MetroWest</a></div></footer>"""

OFFER = "Founding family offer: the first 100 families in Orlando get 12 months free when Famyle starts charging."
CC = "guilherme@famyle.com"
AUTO_FAM = ("Thanks for posting your job on Famyle Orlando!\n\n"
  "You're one of our founding families: the first 100 families in Orlando get 12 months free when Famyle starts charging.\n\n"
  "What happens next:\n"
  "1. We review your job and publish it on Famyle and Google Jobs. We never show your name, email, phone or address, only the area.\n"
  "2. Local professionals apply. As soon as we have good candidates, we email you their profiles.\n"
  "3. You talk to the ones you like and hire directly.\n\n"
  "Need to change something? Just reply to this email.\n\n"
  "Guilherme, Famyle")
CATS_FORM = ["Housekeeper", "House Cleaner", "Nanny", "Babysitter", "Pet Sitter", "Private Cook"]

def form_job(cat_label, city, fid="job"):
    """Formulario 'publique sua vaga gratis' (familia). Mesmo HTML/JS nas LPs e na home (dialog)."""
    opts = "".join(f'<option{" selected" if x == cat_label else ""}>{e(x)}</option>' for x in CATS_FORM)
    mw = F["fl_min_wage"]["now"]
    return f"""<form id="{fid}" onsubmit="return postJob(event,this)">
<div class="row"><div><label>First name</label><input name="fn" required autocomplete="given-name"></div>
<div><label>Email</label><input name="em" type="email" required autocomplete="email"></div></div>
<label>Mobile (optional, faster replies)</label><input name="ph" type="tel" autocomplete="tel" placeholder="(407) 555-0123" pattern="[0-9 ()+.-]{{10,20}}">
<label style="font-weight:400;display:flex;gap:8px;align-items:flex-start"><input type="checkbox" name="wa" style="width:auto;margin-top:5px">I agree that Famyle may contact me by WhatsApp, text or email about my job. Msg &amp; data rates may apply. I can reply STOP anytime.</label>
<div class="row"><div><label>I need a</label><select name="cat">{opts}</select></div>
<div><label>ZIP code</label><input name="zip" inputmode="numeric" pattern="[0-9]{{5}}" required></div></div>
<div class="row"><div><label>Schedule</label><select name="sch"><option>Part-time</option><option>Full-time</option><option>A few days a week</option><option>Once a week</option><option>Every 2 weeks</option><option>One-time</option></select></div>
<div><label>Hours per week</label><input name="hrs" type="number" min="1" max="60" placeholder="e.g. 10"></div></div>
<div class="row"><div><label>Pay you offer (US$/hour)</label><input name="pay" type="number" min="{mw:.0f}" max="80" step="0.5" required placeholder="e.g. 20"></div>
<div><label>Start</label><select name="start"><option>Right now</option><option>Within a month</option><option>In 1–3 months</option></select></div></div>
<label>Describe the job (optional)</label><textarea name="desc" maxlength="400" rows="3" placeholder="e.g. Weekly cleaning of a 3-bedroom house in Windermere, Tuesdays."></textarea>
<label style="font-weight:400;display:flex;gap:8px;align-items:flex-start"><input type="checkbox" name="pub" required style="width:auto;margin-top:5px">Publish my job on Famyle and Google Jobs so local professionals can apply. My name, email and address are never shown.</label>
<p class="src">{e(OFFER)} Florida minimum wage: ${mw:.2f}/hr.</p>
<button class="btn" style="width:100%">Post my job — free</button></form>"""

JOB_JS = """<script>function postJob(ev,f){ev.preventDefault();var g=function(n){return (f.elements[n]||{}).value||'';};
var wa=f.elements['wa'].checked;if(g('ph')&&!wa){alert('Please check the box so we can text you, or leave the mobile number blank.');return false;}
var b={_subject:'Famyle Orlando - VAGA '+g('cat')+' '+g('zip'),_template:'table',_cc:'""" + CC + """',_autoresponse:""" + json.dumps(AUTO_FAM) + """,
tipo:'familia-vaga',nome:g('fn'),email:g('em'),categoria:g('cat'),zip:g('zip'),horario:g('sch'),horas_semana:g('hrs'),pagamento_hora:g('pay'),inicio:g('start'),descricao:g('desc'),publicar:f.elements['pub'].checked?'sim':'nao',telefone:g('ph'),consentimento_contato:wa?'sim (texto: I agree that Famyle may contact me by WhatsApp, text or email about my job. Msg & data rates may apply. I can reply STOP anytime.)':'nao',pagina:location.pathname,origem:(location.search+(document.referrer&&document.referrer.indexOf(location.host)<0?'|ref='+document.referrer.split('/')[2]:'')),ts:new Date().toISOString()};
var a={kind:'family_job',name:b.nome,email:b.email,phone:wa?b.telefone:'',zip:b.zip,category:b.categoria,language:'en',page:b.pagina,origin:b.origem,schedule:b.horario,hours_week:b.horas_semana,pay_hour:b.pagamento_hora,start:b.inicio,description:b.descricao,publish:b.publicar};
try{fetch('""" + API + """',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(a),keepalive:true});}catch(x){}
try{fetch('""" + FORM + """',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(b)});}catch(x){}
try{gtag('event','conversion',{send_to:'""" + AW + "/" + LBL_WAIT + """'});}catch(x){}try{gtag('event','generate_lead',{lead_type:'family_job',category:a.category});}catch(x){}
f.style.display='none';var ok=document.getElementById(f.id+'-ok');if(ok)ok.style.display='block';return false;}</script>"""

def ok_box(fid):
    return f"""<div class="ok" id="{fid}-ok"><p>Your job is in ✓ Check your email: we sent you what happens next.</p>
<p style="color:var(--ink);font-weight:400">You're one of our <b>founding families</b>: the first 100 families in Orlando get <b>12 months free</b> when Famyle starts charging. We'll publish your job (without your name or contact) and email you as soon as local professionals apply.</p>
<a class="btn" href="https://wa.me/?text=I%20just%20posted%20a%20job%20on%20Famyle%20to%20find%20trusted%20help%20in%20Orlando%20%E2%80%94%20it%27s%20free%3A%20https%3A%2F%2Fus.famyle.com%2F" target="_blank" rel="noopener">Share with a friend on WhatsApp</a></div>"""

def form_family(cat_label, city):
    what = f"{e(cat_label.lower())} job" if cat_label in CATS_FORM else "job"
    return f"""<div class="box" id="join"><h2 style="margin-top:0">Post your {what} in {e(city)} — free</h2>
<p>Takes 1 minute. Local professionals apply to you.</p>
{form_job(cat_label, city)}{ok_box("job")}</div>{JOB_JS}"""

def answer_box(txt, label="Quick answer"):
    return f'<div class="box answer"><p style="margin:0"><b>{e(label)}:</b> {e(txt)}</p></div>' if txt else ""

def faq_ld(qas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

WHY_HTML = """<h2>Why families choose Famyle</h2><ul>
<li><b>Free.</b> No subscription to see or contact professionals.</li>
<li><b>Real jobs only.</b> Every job on Famyle is posted by a real family — no filler listings.</li>
<li><b>We talk to them first.</b> We talk to every professional before we introduce them to you.</li>
<li><b>Closest first.</b> The professionals nearest to you show first.</li>
<li><b>English, Spanish and Portuguese.</b> Find a bilingual nanny or cleaner.</li>
<li><b>A small team that listens.</b> Tell us what's missing and we fix it fast — usually the same week.</li></ul>"""
ORG = {"@type": "Organization", "name": "Famyle", "url": BASE + "/", "description": "Online platform connecting families with housekeepers, house cleaners, nannies, babysitters, pet sitters and cooks. Operating in Brazil for over 10 years; now in Orlando, Florida.", "sameAs": ["https://famyle.com/"]}

def write(path, body):
    fp = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(body)

def wage_table(c):
    w = F["wages"][c["bls"]]; m = F["market"].get(c["market"])
    rows = f"<tr><td>Median hourly wage, {e(w['label'])} ({e(w['area'])})</td><td><b>${w['median']:.2f}</b></td><td>BLS OEWS, {w['period']}</td></tr>"
    if w.get("mean"): rows += f"<tr><td>Mean hourly wage</td><td>${w['mean']:.2f}</td><td>BLS OEWS, {w['period']}</td></tr>"
    if w.get("emp"): rows += f"<tr><td>People employed in this occupation</td><td>{w['emp']:,}</td><td>BLS OEWS, {w['period']}</td></tr>"
    if m: rows += f"<tr><td>Typical rate families pay (market average range)</td><td><b>${m['lo']:.2f}–${m['hi']:.2f}/hr</b></td><td>Care.com cost data, {m['asof']}</td></tr>"
    rows += f"<tr><td>Florida minimum wage</td><td>${F['fl_min_wage']['now']:.2f}/hr</td><td>Since {F['fl_min_wage']['since']}</td></tr>"
    return f"""<table><tr><th>What</th><th>Value</th><th>Source</th></tr>{rows}</table>
<p class="src">Sources: <a href="{w['url']}">BLS Occupational Employment and Wage Statistics</a>{' · <a href="'+m['url']+'">Care.com cost of care</a>' if m else ''} · <a href="{F['fl_min_wage']['url']}">Florida minimum wage</a>. Wages are what employers report to the BLS; what a family pays a private professional is usually higher.</p>"""

# ---------- LPs de familia ----------
for c in F["categories"]:
    for city in c["cities"]:
        cs = city["slug"]; cn = city["name"]
        path = f"/{c['slug']}/fl/{cs}/"
        title = f"{c['label']} in {cn}, FL — Find a Trusted {c['label']} | Famyle"
        desc = f"Find a trusted {c['label'].lower()} in {cn}, Florida. Local rates, what to ask and how to hire legally. Post your job for free on Famyle."
        w = F["wages"][c["bls"]]; m = F["market"].get(c["market"])
        qas = [(f"How much does a {c['label'].lower()} cost in {cn}, FL?",
                (f"Families in the Orlando area typically pay ${m['lo']:.2f} to ${m['hi']:.2f} per hour (Care.com, {m['asof']}). " if m else "")
                + f"The BLS median wage for {w['label'].lower()} in the {w['area']} is ${w['median']:.2f}/hour ({w['period']}), and the Florida minimum wage is ${F['fl_min_wage']['now']:.2f}/hour."),
               (f"Is Famyle available in {cn}?", f"Yes. Post your job for free. If we don't have enough {pl(c['label'])} in your area yet, we'll look for them and contact you as soon as we have candidates."),
               ("Is Famyle free?", "Yes. Posting a job, receiving applications and contacting professionals is free. No subscription, no fees."),
               ] + [(q.replace("{city}", cn), a.replace("{city}", cn)) for q, a in c["faq"]]
        ld = {"@context": "https://schema.org", "@graph": [ORG,
              {"@type": "Service", "name": f"{c['label']} services in {cn}, FL", "serviceType": c["label"], "provider": {"@type": "Organization", "name": "Famyle"}, "areaServed": {"@type": "City", "name": f"{cn}, FL"}},
              faq_ld(qas), crumbs_ld([("Famyle", "/"), (c["label"], f"/{c['slug']}/fl/orlando/"), (cn, path)])]}
        others = "".join(f'<li><a href="/{o["slug"]}/fl/orlando/">{e(o["label"])} in Orlando</a></li>' for o in F["categories"] if o["slug"] != c["slug"])
        near = "".join(f'<li><a href="/{c["slug"]}/fl/{x["slug"]}/">{e(c["label"])} in {e(x["name"])}</a></li>' for x in c["cities"] if x["slug"] != cs)
        body = head(title, desc, path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › {e(c['label'])} › {e(cn)}, FL</div>
<h1>{e(c['label'])} in {e(cn)}, FL</h1><p class="lead">{e(c['intro'].replace('{city}', cn))}</p>
<a class="btn" href="#join">Post your job — free</a></div></div>
<div class="wrap">
{answer_box(((f"A {c['label'].lower()} in {cn}, FL typically costs" if cn == "Orlando" else f"In the Orlando area, including {cn}, a {c['label'].lower()} typically costs") + f" ${m['lo']:.2f}–${m['hi']:.2f} per hour in 2026 (Care.com, {m['asof']})" if m else f"Private household cooks in Florida earn a median of ${w['median']:.2f} per hour (BLS, {w['period']})") + f". On Famyle, families post the job for free, local {pl(c['label'])} apply, and we talk to each one before introducing them. You hire directly and agree on pay and schedule.")}
{('<p>' + e(city['note']) + '</p>') if city.get('note') else ''}
<h2>How much does a {e(c['label'].lower())} cost in {e(cn)}?</h2>{wage_table(c)}
<h2>What a {e(c['label'].lower())} does</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['duties'])}</ul>
<h2>What to ask before you hire</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['ask'])}</ul>
<h2>Hiring legally in Florida</h2><p>{e(c['legal'])} See our guide: <a href="/guides/hire-household-employee-florida/">how to hire a household employee in Florida</a>.</p>
<h2>How Famyle works</h2><ol><li>Post your job for free.</li><li>Local professionals apply to you; the closest ones show first.</li><li>We talk to each professional before we introduce them.</li><li>Hire directly: you agree on pay and schedule with the professional.</li><li>It's free: posting, receiving applications and contacting professionals.</li></ol>
<h2>Why families choose Famyle</h2><ul>
<li><b>Free.</b> No subscription to see or contact professionals.</li>
<li><b>Real jobs only.</b> Every job on Famyle is posted by a real family — no filler listings.</li>
<li><b>We talk to them first.</b> We talk to every professional before we introduce them to you.</li>
<li><b>Closest first.</b> The professionals nearest to you show first.</li>
<li><b>English, Spanish and Portuguese.</b> Find a bilingual nanny or cleaner.</li>
<li><b>A small team that listens.</b> Tell us what's missing and we fix it fast — usually the same week.</li></ul>
{form_family(c['label'], cn)}
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in qas)}
{('<h2>Nearby</h2><ul class="links">'+near+'</ul>') if near else ''}
<h2>Other services in Orlando</h2><ul class="links">{others}</ul>
<p class="src">Last updated {TODAY}. Are you a {e(c['label'].lower())}? <a href="/jobs/{c['slug']}/fl/orlando/">See {e(c['label'].lower())} jobs in Orlando</a>.</p>
</div>{FOOT}</body></html>"""
        write(path, body); pages.append((path, title))

# ---------- VAGAS REAIS (JobPosting -> Google Jobs) ----------
# Fonte: _gen/jobs.json (1 item por vaga recebida no formulario, so com publicar=sim).
# Regra D-379 (BR): so emite vaga com validThrough > agora+24h; vencida sai da pagina e do sitemap.
NOW = datetime.datetime.now(datetime.timezone.utc)
CAT_BY_LABEL = {c["label"]: c for c in F["categories"]}
EMP = {"Full-time": "FULL_TIME", "Part-time": "PART_TIME", "A few days a week": "PART_TIME", "Once a week": "PART_TIME", "Every 2 weeks": "PART_TIME", "One-time": "TEMPORARY"}
try:
    JOBS = json.load(open(os.path.join(ROOT, "_gen", "jobs.json"), encoding="utf-8"))
except FileNotFoundError:
    JOBS = []
open_jobs = {}
for j in JOBS:
    c = CAT_BY_LABEL.get(j["cat"])
    if not c or j.get("closed"):
        continue
    posted = datetime.datetime.fromisoformat(j["posted"]).replace(tzinfo=datetime.timezone.utc)
    valid = posted + datetime.timedelta(days=j.get("valid_days", 30))
    if valid <= NOW + datetime.timedelta(hours=24):
        continue
    path = f"/jobs/{c['slug']}/fl/orlando/{j['id']}/"
    area = j.get("area") or "Orlando"
    title = f"{c['label']} — {j['schedule']} in {area}, FL"
    hrs = f", about {j['hours']} hours a week" if j.get("hours") else ""
    desc_txt = (j.get("desc") or "").strip()
    desc_html = (f"<p>{e(desc_txt)}</p>" if desc_txt else "") + f"<p>A family in {e(area)}, Florida (ZIP {e(j['zip'])}) is looking for a {e(c['label'].lower())}: {e(j['schedule'].lower())}{e(hrs)}. Pay: ${float(j['pay']):.2f} per hour. Start: {e(j['start'].lower())}.</p><p>Apply for free on Famyle: create your free profile and we will get in touch. The family will contact you directly. Famyle never charges professionals.</p>"
    jp = {"@context": "https://schema.org", "@type": "JobPosting", "title": f"{c['label']} ({j['schedule']})", "description": desc_html,
          "datePosted": posted.date().isoformat(), "validThrough": valid.isoformat(), "employmentType": EMP.get(j["schedule"], "PART_TIME"),
          "hiringOrganization": {"@type": "Organization", "name": "Private family via Famyle", "sameAs": BASE + "/"},
          "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": area, "addressRegion": "FL", "postalCode": j["zip"], "addressCountry": "US"}},
          "baseSalary": {"@type": "MonetaryAmount", "currency": "USD", "value": {"@type": "QuantitativeValue", "value": float(j["pay"]), "unitText": "HOUR"}},
          "directApply": False, "identifier": {"@type": "PropertyValue", "name": "Famyle", "value": j["id"]}}
    apply = f"/pro.html?cat={c['label'].replace(' ', '%20')}&job={j['id']}"
    body = head(title + " | Famyle", f"{c['label']} job in {area}, FL: {j['schedule'].lower()}, ${float(j['pay']):.2f}/hour. Apply free on Famyle.", path, jp) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/jobs/">Jobs</a> › <a href="/jobs/{c['slug']}/fl/orlando/">{e(c['label'])}</a> › {e(area)}</div>
<h1>{e(title)}</h1><p class="lead">${float(j['pay']):.2f}/hour · {e(j['schedule'])}{e(hrs)} · posted {posted.date().isoformat()}</p>
<a class="btn" href="{apply}">Apply free</a></div></div>
<div class="wrap">{desc_html}<p><a class="btn" href="{apply}">Apply free</a></p>
<p class="src">Posted by a real family on Famyle. Famyle is an online platform, not the employer. <a href="/jobs/{c['slug']}/fl/orlando/">More {e(c['label'].lower())} jobs in Orlando</a>.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, title))
    open_jobs.setdefault(c["slug"], []).append((path, title, j))

def jobs_list(slug=None):
    items = [x for k, v in open_jobs.items() if slug in (None, k) for x in v]
    if not items:
        return ""
    return "<h2>Open jobs now</h2><ul>" + "".join(f'<li><a href="{p}">{e(t)}</a> — ${float(j["pay"]):.2f}/hr</li>' for p, t, j in items) + "</ul>"

# ---------- LPs de vaga (profissional) ----------
for c in F["categories"]:
    path = f"/jobs/{c['slug']}/fl/orlando/"
    title = f"{c['label']} Jobs in Orlando, FL — Join Free | Famyle"
    desc = f"{c['label']} jobs with local families in Orlando, Florida. Free to join. Pay rates, what families look for, and how Famyle works."
    w = F["wages"][c["bls"]]; m = F["market"].get(c["market"])
    qas = [(f"How much do {pl(c['label'])} make in Orlando?", f"The BLS median wage for {w['label'].lower()} in the {w['area']} is ${w['median']:.2f}/hour ({w['period']})." + (f" Families hiring privately typically pay ${m['lo']:.2f} to ${m['hi']:.2f}/hour (Care.com, {m['asof']})." if m else "")),
           ("Do I pay to join Famyle?", "No. Creating your profile and applying to jobs is free."),
           ("Do I need to speak English?", "Many Orlando families look for bilingual professionals. Famyle works in English, Portuguese and Spanish."),
           ("Are there jobs near me right now?", "Sign up and we'll contact you by WhatsApp, text or email as soon as a family near you posts a job. If there are no open jobs in your area yet, you'll be among the first professionals we contact.")]
    ld = {"@context": "https://schema.org", "@graph": [ORG, faq_ld(qas), crumbs_ld([("Famyle", "/"), ("Jobs", "/jobs/"), (c["label"], path)])]}
    body = head(title, desc, path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/jobs/">Jobs</a> › {e(c['label'])} · Orlando, FL</div>
<h1>{e(c['label'])} jobs in Orlando, FL</h1><p class="lead">Work directly with local families. Free to join.</p>
<a class="btn" href="/pro.html?cat={e(c['label'])}">Join free</a> <a class="btn" style="background:#fff;color:var(--brand);border:1px solid var(--brand)" href="/pro.html?lang=pt">Português</a> <a class="btn" style="background:#fff;color:var(--brand);border:1px solid var(--brand)" href="/pro.html?lang=es">Español</a></div></div>
<div class="wrap"><h2>How much {e(pl(c['label']))} make in Orlando</h2>{wage_table(c)}
<h2>What families look for</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['families_want'])}</ul>
{jobs_list(c['slug'])}
<h2>How Famyle works for professionals</h2><ol><li>Create your free profile.</li><li>We get in touch to learn about your experience.</li><li>Apply to jobs near you; families contact you directly.</li><li>You agree on pay and schedule with the family.</li></ol>
<h2>Why professionals choose Famyle</h2><ul><li><b>Free.</b> No membership, and we never take a cut of what families pay you.</li><li><b>Real families only.</b> Every job is posted by a real family near you.</li><li><b>We introduce you to families</b> looking for someone near you.</li><li><b>Work in your language:</b> English, Spanish or Portuguese.</li><li><b>Closest jobs first,</b> so you spend less time driving.</li></ul>
<p><a class="btn" href="/pro.html?cat={e(c['label'])}">Join free</a></p>
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in qas)}
<h2>Other jobs in Orlando</h2><ul class="links">{''.join(f'<li><a href="/jobs/{o["slug"]}/fl/orlando/">{e(o["label"])} jobs</a></li>' for o in F["categories"] if o["slug"]!=c["slug"])}</ul>
<p class="src">Last updated {TODAY}. Looking to hire? <a href="/{c['slug']}/fl/orlando/">Find a {e(c['label'].lower())} in Orlando</a>.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, title))

# ---------- bairros (1 pagina por bairro, todas as categorias) ----------
for nb in F["neighborhoods"]:
    path = f"/orlando/{nb['slug']}/"
    title = f"Nannies, Housekeepers & House Cleaners in {nb['name']}, FL | Famyle"
    desc = f"Find a nanny, babysitter, housekeeper, house cleaner, pet sitter or private cook in {nb['name']} (ZIP {nb['zips']}). Free on Famyle."
    qas = [(f"Does Famyle serve {nb['name']}?", f"Yes. Famyle serves {nb['name']} (ZIP {nb['zips']}) and nearby {', '.join(nb['near'])}. Post your job for free; if we don't have enough professionals near you yet, we'll find them and contact you first."),
           ("Is Famyle free?", "Yes. Posting a job, receiving applications and contacting professionals is free. No subscription, no fees.")]
    ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "Service", "name": f"Household help in {nb['name']}, FL", "provider": {"@type": "Organization", "name": "Famyle"}, "areaServed": {"@type": "Place", "name": f"{nb['name']}, FL"}}, faq_ld(qas), crumbs_ld([("Famyle", "/"), ("Orlando", "/"), (nb["name"], path)])]}
    cats = "".join(f'<li><a href="/{c["slug"]}/fl/orlando/">{e(c["label"])}</a> — typical Orlando rate ' + (f'${F["market"][c["market"]]["lo"]:.0f}–${F["market"][c["market"]]["hi"]:.0f}/hr' if c["market"] else f'BLS median ${F["wages"][c["bls"]]["median"]:.2f}/hr (Florida)') + '</li>' for c in F["categories"])
    nears = "".join(f'<li><a href="/orlando/{x["slug"]}/">{e(x["name"])}</a></li>' for x in F["neighborhoods"] if x["slug"] != nb["slug"])
    body = head(title, desc, path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › Orlando › {e(nb['name'])}</div>
<h1>Household help in {e(nb['name'])}, FL</h1><p class="lead">{e(nb['desc'])}</p><a class="btn" href="#join">Post your job — free</a></div></div>
<div class="wrap">{answer_box(f"Families in {nb['name']}, FL (ZIP {nb['zips']}) can find nannies, babysitters, housekeepers, house cleaners, pet sitters and private cooks on Famyle for free. Typical Orlando rates in 2026: nanny ${F['market']['nanny']['lo']:.2f}–${F['market']['nanny']['hi']:.2f}/hour and house cleaning ${F['market']['cleaning']['lo']:.2f}–${F['market']['cleaning']['hi']:.2f}/hour (Care.com, {F['market']['nanny']['asof']}).")}<p>Famyle serves {e(nb['name'])} (ZIP {e(nb['zips'])}) in {e(nb['area'])}, and nearby {e(', '.join(nb['near']))}. Professionals close to you show first, so they spend less time driving and are more likely to stay.</p>
<h2>What you can find in {e(nb['name'])}</h2><ul>{cats}</ul><p class="src">Rates: <a href="https://www.care.com/cost/nannies/orlando-fl">Care.com Orlando cost data, Nov 2026</a> · BLS OEWS May 2025.</p>
{WHY_HTML}
{form_family("Professional", nb["name"])}
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in qas)}
<h2>Nearby neighborhoods</h2><ul class="links">{nears}</ul>
<p class="src">Last updated {TODAY}. Are you a nanny, housekeeper or pet sitter in {e(nb['name'])}? <a href="/pro.html">Join free</a>.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, title))

# hub de vagas
hub = "".join(f'<li><a href="/jobs/{c["slug"]}/fl/orlando/">{e(c["label"])} jobs in Orlando</a></li>' for c in F["categories"])
write("/jobs/", head("Household Jobs in Orlando, FL — Join Free | Famyle", "Housekeeper, house cleaner, nanny, babysitter, pet sitter and cook jobs with families in Orlando, Florida. Free to join.", "/jobs/", {"@context": "https://schema.org", "@graph": [ORG]})
      + f'<div class="hero"><div class="wrap"><h1>Household jobs in Orlando, FL</h1><p class="lead">Free for professionals.</p><a class="btn" href="/pro.html">Join free</a></div></div><div class="wrap">{jobs_list()}<h2>Jobs by category</h2><ul class="links">{hub}</ul></div>{FOOT}</body></html>')
pages.append(("/jobs/", "Household jobs in Orlando"))

# ---------- guias ----------
for g in F["guides"]:
    path = f"/guides/{g['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "Article", "headline": g["title"], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Famyle"}}, faq_ld(g["faq"])]}
    body = head(g["title"] + " | Famyle", g["desc"], path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/guides/">Guides</a></div><h1>{e(g['title'])}</h1><p class="lead">{e(g['desc'])}</p></div></div>
<div class="wrap">{answer_box(g.get('answer'))}{g['html']}
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in g['faq'])}
<p class="src">Last updated {TODAY}. This guide is general information, not legal or tax advice.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, g["title"]))
glist = "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></li>' for g in F["guides"])
write("/guides/", head("Guides for Orlando Families | Famyle", "Costs, rules and tips for hiring household help in Orlando, Florida.", "/guides/", {"@context": "https://schema.org", "@graph": [ORG]})
      + f'<div class="hero"><div class="wrap"><h1>Guides for Orlando families</h1></div></div><div class="wrap"><ul>{glist}</ul></div>{FOOT}</body></html>')
pages.append(("/guides/", "Guides"))

# ---------- guias em portugues (comunidade brasileira em Orlando) ----------
FOOT_PT = """<footer><div class="wrap">A Famyle é uma plataforma online em Orlando, Flórida: a família contrata a profissional direto; a Famyle não é empregadora nem agência.<br>
<a href="/">Para famílias</a> · <a href="/pro.html?lang=pt">Para profissionais</a> · <a href="/pt/guias/">Guias em português</a> · <a href="mailto:suporte@famyle.com">suporte@famyle.com</a></div></footer>"""
def head_pt(title, desc, path, jsonld):
    h = head(title, desc, path, jsonld).replace('<html lang="en">', '<html lang="pt-BR">', 1)
    return h.replace('<nav><a href="/">Families</a><a href="/jobs/">Jobs</a><a href="/guides/">Guides</a></nav>', '<nav><a href="/">Famílias</a><a href="/pro.html?lang=pt">Profissionais</a><a href="/pt/guias/">Guias</a></nav>', 1)
for g in F.get("guides_pt", []):
    path = f"/pt/guias/{g['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "Article", "headline": g["title"], "inLanguage": "pt-BR", "dateModified": TODAY, "author": {"@type": "Organization", "name": "Famyle"}}, faq_ld(g["faq"])]}
    body = head_pt(g["title"] + " | Famyle", g["desc"], path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/pt/guias/">Guias em português</a></div><h1>{e(g['title'])}</h1><p class="lead">{e(g['desc'])}</p></div></div>
<div class="wrap">{answer_box(g.get('answer'), "Resposta rápida")}{g['html']}
<h2>Perguntas frequentes</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in g['faq'])}
<p class="src">Atualizado em {TODAY}. Este guia é informação geral, não orientação jurídica ou tributária.</p></div>{FOOT_PT}</body></html>"""
    write(path, body); pages.append((path, g["title"]))
if F.get("guides_pt"):
    _gl = "".join(f'<li><a href="/pt/guias/{g["slug"]}/">{e(g["title"])}</a></li>' for g in F["guides_pt"])
    write("/pt/guias/", head_pt("Guias em português para famílias em Orlando | Famyle", "Quanto custa babá e diarista em Orlando, como contratar e o que a lei da Flórida exige, em português.", "/pt/guias/", {"@context": "https://schema.org", "@graph": [ORG]})
          + f'<div class="hero"><div class="wrap"><h1>Guias em português para famílias em Orlando</h1><p class="lead">Babá, diarista e housekeeper em Orlando: valores, como contratar e o que a lei exige.</p></div></div><div class="wrap"><ul>{_gl}</ul></div>{FOOT_PT}</body></html>')
    pages.append(("/pt/guias/", "Guias em português para famílias em Orlando"))

# ---------- sitemap, robots, llms ----------
all_paths = ["/", "/pro.html"] + [p for p, _ in pages]
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in all_paths) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /_gen/\nSitemap: {BASE}/sitemap.xml\n")
llms = ["# Famyle (United States)", "", "> Famyle is an online platform where families find and hire housekeepers, house cleaners, nannies, babysitters, pet sitters and cooks directly. Operating in Brazil for over 10 years; now accepting families and professionals in Orlando, Florida. Families post jobs for free; professionals join for free. Famyle is not an employer or staffing agency.", "",
        "## Key facts", f"- City: Orlando, FL and nearby (Kissimmee, Clermont, Winter Garden). Families pay nothing until there are professionals for them.", "- Free for families and professionals: no subscription, no fees.", "- Professionals: free to join; we talk to every professional before introducing them to a family.", "- Languages: English, Portuguese, Spanish. Guides in Portuguese for Brazilian families: https://us.famyle.com/pt/guias/", "", "## Pages"] + [f"- [{t}]({BASE}{p})" for p, t in pages]
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms) + "\n")
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True); open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8").write(CSS)
print(len(pages), "paginas geradas")

# ---------- home (index.html, escrita a mao): troca o formulario da lista de espera pelo de vaga ----------
import re as _re
_ix = os.path.join(ROOT, "index.html"); _h = open(_ix, encoding="utf-8").read()
_new_f = '<div id="f"><h3>Post your job — free</h3><p>Takes 1 minute. Local professionals apply to you.</p>' + form_job("House Cleaner", "Orlando") + '</div>' + ok_box("job")
_h = _re.sub(r'<div id="f">.*?</div>\s*<div id="t" class="thanks">.*?</div>\n</div></dialog>', lambda m: _new_f + '\n</div></dialog>', _h, count=1, flags=_re.S)
_h = _h.replace("document.querySelector('#cat option[value=\"'+m[k][1]+'\"]')||[].find.call(document.querySelectorAll('#cat option')", "[].find.call(document.querySelectorAll('select[name=cat] option')")
_h = _h.replace('pet:["Find a trusted pet sitter in Orlando.","Pet sitter"]', 'pet:["Find a trusted pet sitter in Orlando.","Pet Sitter"]').replace('cleaning:["Find a trusted housekeeper or house cleaner in Orlando.","Housekeeper"]', 'cleaning:["Find a trusted housekeeper or house cleaner in Orlando.","House Cleaner"]')
_h = _re.sub(r"<script>function postJob\(.*?</script>\n?", "", _h, flags=_re.S)
_h = _h.replace("</body>", JOB_JS + "\n</body>", 1)
open(_ix, "w", encoding="utf-8").write(_h)

"""Gera o pacote organico de pre-lancamento Famyle Orlando (LPs familia, LPs de vaga, guias, sitemap, llms.txt).
Fonte unica dos dados: facts.json (cada numero com fonte). Uso: python _gen/gen.py
"""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = json.load(open(os.path.join(ROOT, "_gen", "facts.json"), encoding="utf-8"))
BASE = "https://us.famyle.com"
TODAY = datetime.date.today().isoformat()
AW = "AW-11419257934"; LBL_WAIT = "tPyrCI_drbAdEM6YkMUq"
FORM = "https://formsubmit.co/ajax/adm@famyle.com"
e = html.escape
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
label{display:block;font-size:14px;font-weight:600;margin:10px 0 4px}input,select{width:100%;padding:11px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:#fff}
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
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{AW}');</script>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script></head><body>
<header><div class="wrap"><a class="logo" href="/">famyle</a><nav><a href="/">Families</a><a href="/jobs/">Jobs</a><a href="/guides/">Guides</a></nav></div></header>"""

FOOT = """<footer><div class="wrap">Famyle is an online platform in Orlando, Florida: families hire professionals directly; Famyle is not an employer or a staffing agency.<br>
<a href="/">For families</a> · <a href="/jobs/">For professionals</a> · <a href="/guides/">Guides</a> · <a href="mailto:suporte@famyle.com">suporte@famyle.com</a></div></footer>"""

def form_family(cat_label, city):
    return f"""<div class="box" id="join"><h2 style="margin-top:0">Find a {e(cat_label.lower())} in {e(city)}</h2>
<p>Tell us where and when. Posting is free.</p>
<form onsubmit="return wl(event)"><label for="em">Email</label><input id="em" type="email" required autocomplete="email">
<div class="row"><div><label for="zip">ZIP code</label><input id="zip" inputmode="numeric" pattern="[0-9]{{5}}" required></div>
<div><label for="when">When do you need help?</label><select id="when"><option>Right now</option><option>In the next 3 months</option><option>Just looking</option></select></div></div><br>
<button class="btn">Find a {e(cat_label.lower())}</button></form><div class="ok" id="ok"><p>Got it! ✓ We don't have enough {e(cat_label.lower())}s in your area yet — we're looking for them now and will email you as soon as we have candidates. You'll be among the first families we contact.</p>
<p style="color:var(--ink);font-weight:400">What you'll get on Famyle: it's <b>free</b>, every professional has a <b>video interview</b> and a <b>verified ID</b>, and every job is posted by a real family. Help us get there faster:</p>
<a class="btn" href="https://wa.me/?text=I%20just%20posted%20on%20Famyle%20to%20find%20trusted%20help%20in%20Orlando%20%E2%80%94%20it%27s%20free%3A%20https%3A%2F%2Fus.famyle.com%2F" target="_blank" rel="noopener">Share with a friend on WhatsApp</a></div></div>
<script>function wl(ev){{ev.preventDefault();var b={{_subject:'Famyle Orlando - lista de espera',_template:'table',tipo:'familia',categoria:'{e(cat_label)}',cidade:'{e(city)}',email:em.value,zip:zip.value,when:when.value,pagina:location.pathname,origem:location.search,ts:new Date().toISOString()}};
try{{fetch('{FORM}',{{method:'POST',headers:{{'Content-Type':'application/json',Accept:'application/json'}},body:JSON.stringify(b)}});}}catch(x){{}}
try{{gtag('event','conversion',{{send_to:'{AW}/{LBL_WAIT}'}});}}catch(x){{}}ev.target.style.display='none';document.getElementById('ok').style.display='block';return false;}}</script>"""

def faq_ld(qas):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

ORG = {"@type": "Organization", "name": "Famyle", "url": BASE + "/", "description": "Online platform connecting families with housekeepers, house cleaners, nannies, babysitters, pet sitters and cooks. Operating in Brazil for over 10 years; now in Orlando, Florida."}

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
               (f"Is Famyle available in {cn}?", f"Yes. Post your job for free. If we don't have enough {c['label'].lower()}s in your area yet, we'll look for them and contact you as soon as we have candidates."),
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
{('<p>' + e(city['note']) + '</p>') if city.get('note') else ''}
<h2>How much does a {e(c['label'].lower())} cost in {e(cn)}?</h2>{wage_table(c)}
<h2>What a {e(c['label'].lower())} does</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['duties'])}</ul>
<h2>What to ask before you hire</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['ask'])}</ul>
<h2>Hiring legally in Florida</h2><p>{e(c['legal'])} See our guide: <a href="/guides/hire-household-employee-florida/">how to hire a household employee in Florida</a>.</p>
<h2>How Famyle works</h2><ol><li>Post your job for free.</li><li>Local professionals apply to you; the closest ones show first.</li><li>Watch each professional's short video interview and see their verified ID.</li><li>Hire directly: you agree on pay and schedule with the professional.</li><li>It's free: posting, receiving applications and contacting professionals.</li></ol>
<h2>Why families choose Famyle</h2><ul>
<li><b>Free.</b> No subscription to see or contact professionals.</li>
<li><b>Real jobs only.</b> Every job on Famyle is posted by a real family — no filler listings.</li>
<li><b>Meet them before you call.</b> Every professional records a short video interview.</li>
<li><b>Verified ID</b> on every profile, and the closest professionals show first.</li>
<li><b>English, Spanish and Portuguese.</b> Find a bilingual nanny or cleaner.</li>
<li><b>A small team that listens.</b> Tell us what's missing and we fix it fast — usually the same week.</li></ul>
{form_family(c['label'], cn)}
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in qas)}
{('<h2>Nearby</h2><ul class="links">'+near+'</ul>') if near else ''}
<h2>Other services in Orlando</h2><ul class="links">{others}</ul>
<p class="src">Last updated {TODAY}. Are you a {e(c['label'].lower())}? <a href="/jobs/{c['slug']}/fl/orlando/">See {e(c['label'].lower())} jobs in Orlando</a>.</p>
</div>{FOOT}</body></html>"""
        write(path, body); pages.append((path, title))

# ---------- LPs de vaga (profissional) ----------
for c in F["categories"]:
    path = f"/jobs/{c['slug']}/fl/orlando/"
    title = f"{c['label']} Jobs in Orlando, FL — Join Free | Famyle"
    desc = f"{c['label']} jobs with local families in Orlando, Florida. Free to join. Pay rates, what families look for, and how Famyle works."
    w = F["wages"][c["bls"]]; m = F["market"].get(c["market"])
    qas = [(f"How much do {c['label'].lower()}s make in Orlando?", f"The BLS median wage for {w['label'].lower()} in the {w['area']} is ${w['median']:.2f}/hour ({w['period']})." + (f" Families hiring privately typically pay ${m['lo']:.2f} to ${m['hi']:.2f}/hour (Care.com, {m['asof']})." if m else "")),
           ("Do I pay to join Famyle?", "No. Creating your profile and applying to jobs is free."),
           ("Do I need to speak English?", "Many Orlando families look for bilingual professionals. Famyle works in English, Portuguese and Spanish."),
           ("Are there jobs near me right now?", "Sign up and we'll contact you by WhatsApp, text or email as soon as a family near you posts a job. If there are no open jobs in your area yet, you'll be among the first professionals we contact.")]
    ld = {"@context": "https://schema.org", "@graph": [ORG, faq_ld(qas), crumbs_ld([("Famyle", "/"), ("Jobs", "/jobs/"), (c["label"], path)])]}
    body = head(title, desc, path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/jobs/">Jobs</a> › {e(c['label'])} · Orlando, FL</div>
<h1>{e(c['label'])} jobs in Orlando, FL</h1><p class="lead">Work directly with local families. Free to join.</p>
<a class="btn" href="/pro.html?cat={e(c['label'])}">Join free</a> <a class="btn" style="background:#fff;color:var(--brand);border:1px solid var(--brand)" href="/pro.html?lang=pt">Português</a> <a class="btn" style="background:#fff;color:var(--brand);border:1px solid var(--brand)" href="/pro.html?lang=es">Español</a></div></div>
<div class="wrap"><h2>How much {e(c['label'].lower())}s make in Orlando</h2>{wage_table(c)}
<h2>What families look for</h2><ul>{''.join('<li>'+e(x)+'</li>' for x in c['families_want'])}</ul>
<h2>How Famyle works for professionals</h2><ol><li>Create your free profile and verify your ID.</li><li>Record a short video interview so families can meet you.</li><li>Apply to jobs near you; families contact you directly.</li><li>You agree on pay and schedule with the family.</li></ol>
<h2>Why professionals choose Famyle</h2><ul><li><b>Free.</b> No membership, and we never take a cut of what families pay you.</li><li><b>Real families only.</b> Every job is posted by a real family near you.</li><li><b>Stand out with your video interview</b> — families meet you before they call.</li><li><b>Work in your language:</b> English, Spanish or Portuguese.</li><li><b>Closest jobs first,</b> so you spend less time driving.</li></ul>
<p><a class="btn" href="/pro.html?cat={e(c['label'])}">Join free</a></p>
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in qas)}
<h2>Other jobs in Orlando</h2><ul class="links">{''.join(f'<li><a href="/jobs/{o["slug"]}/fl/orlando/">{e(o["label"])} jobs</a></li>' for o in F["categories"] if o["slug"]!=c["slug"])}</ul>
<p class="src">Last updated {TODAY}. Looking to hire? <a href="/{c['slug']}/fl/orlando/">Find a {e(c['label'].lower())} in Orlando</a>.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, title))

# hub de vagas
hub = "".join(f'<li><a href="/jobs/{c["slug"]}/fl/orlando/">{e(c["label"])} jobs in Orlando</a></li>' for c in F["categories"])
write("/jobs/", head("Household Jobs in Orlando, FL — Join Free | Famyle", "Housekeeper, house cleaner, nanny, babysitter, pet sitter and cook jobs with families in Orlando, Florida. Free to join.", "/jobs/", {"@context": "https://schema.org", "@graph": [ORG]})
      + f'<div class="hero"><div class="wrap"><h1>Household jobs in Orlando, FL</h1><p class="lead">Free for professionals.</p><a class="btn" href="/pro.html">Join free</a></div></div><div class="wrap"><ul class="links">{hub}</ul></div>{FOOT}</body></html>')
pages.append(("/jobs/", "Household jobs in Orlando"))

# ---------- guias ----------
for g in F["guides"]:
    path = f"/guides/{g['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "Article", "headline": g["title"], "dateModified": TODAY, "author": {"@type": "Organization", "name": "Famyle"}}, faq_ld(g["faq"])]}
    body = head(g["title"] + " | Famyle", g["desc"], path, ld) + f"""
<div class="hero"><div class="wrap"><div class="crumbs"><a href="/">Famyle</a> › <a href="/guides/">Guides</a></div><h1>{e(g['title'])}</h1><p class="lead">{e(g['desc'])}</p></div></div>
<div class="wrap">{g['html']}
<h2>Frequently asked questions</h2>{''.join('<h3>'+e(q)+'</h3><p>'+e(a)+'</p>' for q,a in g['faq'])}
<p class="src">Last updated {TODAY}. This guide is general information, not legal or tax advice.</p></div>{FOOT}</body></html>"""
    write(path, body); pages.append((path, g["title"]))
glist = "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></li>' for g in F["guides"])
write("/guides/", head("Guides for Orlando Families | Famyle", "Costs, rules and tips for hiring household help in Orlando, Florida.", "/guides/", {"@context": "https://schema.org", "@graph": [ORG]})
      + f'<div class="hero"><div class="wrap"><h1>Guides for Orlando families</h1></div></div><div class="wrap"><ul>{glist}</ul></div>{FOOT}</body></html>')
pages.append(("/guides/", "Guides"))

# ---------- sitemap, robots, llms ----------
all_paths = ["/", "/pro.html"] + [p for p, _ in pages]
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in all_paths) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /_gen/\nSitemap: {BASE}/sitemap.xml\n")
llms = ["# Famyle (United States)", "", "> Famyle is an online platform where families find and hire housekeepers, house cleaners, nannies, babysitters, pet sitters and cooks directly. Operating in Brazil for over 10 years; now accepting families and professionals in Orlando, Florida. Families post jobs for free; professionals join for free. Famyle is not an employer or staffing agency.", "",
        "## Key facts", f"- City: Orlando, FL and nearby (Kissimmee, Clermont, Winter Garden). Families pay nothing until there are professionals for them.", "- Free for families and professionals: no subscription, no fees.", "- Professionals: free to join; profiles include a short video interview and ID verification.", "- Languages: English, Portuguese, Spanish.", "", "## Pages"] + [f"- [{t}]({BASE}{p})" for p, t in pages]
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms) + "\n")
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True); open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8").write(CSS)
print(len(pages), "paginas geradas")

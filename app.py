import os, json, re, time, base64
from urllib.parse import quote
import requests
import streamlit as st

st.set_page_config(page_title="RAN-NEETI | Sports × Anime Intelligence", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

SPORTS = {
    "Football / Soccer":"⚽", "Cricket":"🏏", "Basketball":"🏀", "Tennis":"🎾", "Badminton":"🏸", "Baseball":"⚾", "American Football":"🏈", "Rugby Union":"🏉", "Rugby Sevens":"🏉", "Ice Hockey":"🏒", "Field Hockey":"🏑", "Volleyball":"🏐", "Beach Volleyball":"🏐", "Handball":"🤾", "Kabaddi":"🤼", "Table Tennis":"🏓", "Squash":"🎾", "Pickleball":"🏓", "Golf":"⛳", "Boxing":"🥊", "MMA / UFC":"🥊", "Wrestling":"🤼", "Judo":"🥋", "Karate":"🥋", "Taekwondo":"🥋", "Fencing":"🤺", "Motorsport / F1":"🏎️", "MotoGP":"🏍️", "Cycling":"🚴", "Athletics / Track & Field":"🏃", "Marathon":"🏃", "Swimming":"🏊", "Diving":"🤿", "Gymnastics":"🤸", "Weightlifting":"🏋️", "Powerlifting":"🏋️", "Archery":"🏹", "Shooting":"🎯", "Rowing":"🚣", "Canoe / Kayak":"🛶", "Sailing":"⛵", "Surfing":"🏄", "Skateboarding":"🛹", "Snowboarding":"🏂", "Skiing":"⛷️", "Figure Skating":"⛸️", "Badminton Doubles":"🏸", "Chess":"♟️", "Esports":"🎮", "Dota 2":"🎮", "League of Legends":"🎮", "Counter-Strike":"🎯", "Valorant":"🎮", "Rocket League":"🚗", "Overwatch":"🎮", "Water Polo":"🤽", "Lacrosse":"🥍", "Netball":"🏐", "Softball":"🥎", "Bowling":"🎳", "Darts":"🎯", "Snooker":"🎱", "Billiards":"🎱", "Polo":"🐎", "Equestrian":"🐎", "Triathlon":"🏊", "Duathlon":"🚴", "Strongman":"🏋️", "CrossFit":"💪", "Floorball":"🏑", "Sepak Takraw":"⚽", "Kho Kho":"🏃", "Ultimate Frisbee":"🥏", "Competitive Dance":"💃", "Futsal":"⚽", "Beach Soccer":"⚽", "Indoor Cricket":"🏏", "Street Basketball":"🏀"
}

CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');
:root{--cyan:#35d9ff;--violet:#a78bfa;--panel:rgba(7,18,35,.88);--line:rgba(74,170,224,.28)}
.stApp{background:#040914;color:#edf7ff;font-family:Inter,sans-serif}
[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 12% 0%,rgba(0,155,255,.15),transparent 32%),radial-gradient(ellipse at 90% 10%,rgba(130,57,255,.13),transparent 28%),linear-gradient(180deg,#050b17,#071020 58%,#030812)}
[data-testid="stHeader"]{background:rgba(3,8,18,.75)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#06101e,#08182a);border-right:1px solid var(--line)}
.block-container{padding-top:1.1rem;padding-bottom:3rem;max-width:1500px}
.hero{position:relative;overflow:hidden;border:1px solid rgba(53,217,255,.45);border-radius:22px;min-height:260px;padding:30px 34px;margin-bottom:22px;background:linear-gradient(90deg,rgba(3,10,22,.92),rgba(3,10,22,.70) 50%,rgba(6,12,30,.58)),url('/app/static/neon_sports_anime_background.png') center/cover;box-shadow:0 0 42px rgba(0,180,255,.08),inset 0 0 60px rgba(16,112,205,.12)}
.hero:after{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(110deg,transparent 40%,rgba(27,203,255,.07),transparent 70%);animation:scan 8s linear infinite}
@keyframes scan{0%{transform:translateX(-40%)}100%{transform:translateX(40%)}}
.brand{font:800 clamp(36px,5vw,62px) 'Barlow Condensed',sans-serif;letter-spacing:1px;line-height:1;color:#f4fbff;text-shadow:0 0 25px rgba(53,217,255,.55)}
.kicker{color:#5be6ff;text-transform:uppercase;letter-spacing:3px;font-weight:800;font-size:11px}
.hero-sub{color:#c8dbef;max-width:720px;font-size:14px;line-height:1.7;margin-top:10px}
.pill{display:inline-block;border:1px solid rgba(53,217,255,.35);border-radius:999px;padding:6px 11px;margin:10px 6px 0 0;background:rgba(8,35,58,.7);color:#bcefff;font-size:11px}
.section-title{font:700 24px 'Barlow Condensed',sans-serif;letter-spacing:.6px;color:#f0f8ff;margin:8px 0 4px}
.muted{color:#8fa8c5;font-size:12px}
.panel{background:linear-gradient(145deg,rgba(12,29,51,.93),rgba(5,15,29,.92));border:1px solid var(--line);border-radius:17px;padding:18px 19px;box-shadow:0 12px 32px rgba(0,0,0,.16);height:100%}
.panel:hover{border-color:rgba(53,217,255,.52)}
.tile{border:1px solid rgba(72,160,218,.27);border-radius:14px;padding:15px;background:linear-gradient(135deg,rgba(13,40,67,.85),rgba(7,20,38,.9));min-height:105px}
.tile-icon{font-size:25px}.tile-title{font-weight:750;color:#effaff;margin-top:7px}.tile-sub{font-size:11px;color:#8eaac6;margin-top:4px}
div[data-testid="stButton"]>button{border-radius:10px;border:1px solid rgba(53,217,255,.5);background:linear-gradient(110deg,#087db7,#0b4c85);color:white;font-weight:700;min-height:42px;transition:.2s}
div[data-testid="stButton"]>button:hover{border-color:#8cf1ff;box-shadow:0 0 18px rgba(53,217,255,.2);transform:translateY(-1px)}
.stTextInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea{background:#08172a!important;border-color:#234a70!important;border-radius:10px!important;color:#edf7ff!important}
.stTabs [data-baseweb="tab-list"]{gap:7px;background:rgba(7,17,32,.8);border:1px solid var(--line);padding:7px;border-radius:13px}
.stTabs [data-baseweb="tab"]{border-radius:8px;color:#a9c2dd;font-weight:700}
.stTabs [aria-selected="true"]{background:#103d60;color:#7feaff!important}
.metric-card{border:1px solid var(--line);border-radius:12px;background:rgba(7,24,42,.8);padding:14px;text-align:center}
.metric-label{font-size:10px;color:#8eaac6;text-transform:uppercase;letter-spacing:1px}.metric-value{font:700 24px 'Barlow Condensed',sans-serif;color:#58e3ff;margin-top:4px}
.vs{font:800 27px 'Barlow Condensed',sans-serif;color:#64eaff;text-align:center;padding-top:30px;text-shadow:0 0 16px rgba(53,217,255,.35)}
.entity-img{width:100%;height:190px;object-fit:cover;border-radius:13px;border:1px solid rgba(53,217,255,.35);background:#09182a}
.source{font-size:11px;color:#9ab6d1;overflow-wrap:anywhere}
hr{border-color:rgba(77,150,205,.18)}
footer{visibility:hidden}
</style>'''
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(ttl=1800, show_spinner=False)
def anime_search(name):
    try:
        r=requests.get('https://api.jikan.moe/v4/characters',params={'q':name,'limit':5,'order_by':'favorites','sort':'desc'},timeout=9,headers={'User-Agent':'RAN-NEETI demo app'})
        if r.ok: return r.json().get('data',[])
    except Exception: pass
    return []

@st.cache_data(ttl=1800, show_spinner=False)
def wiki_search(name):
    try:
        r=requests.get('https://en.wikipedia.org/w/api.php',params={'action':'query','generator':'search','gsrsearch':name,'gsrlimit':5,'gsrnamespace':0,'prop':'pageimages|extracts|info','pithumbsize':600,'exintro':1,'explaintext':1,'inprop':'url','format':'json'},timeout=9,headers={'User-Agent':'RAN-NEETI/1.0 (educational project)'})
        if r.ok:
            pages=r.json().get('query',{}).get('pages',{})
            return sorted(pages.values(),key=lambda p:p.get('index',999))
    except Exception: pass
    return []

def get_gemini_key():
    try: return st.secrets.get('GEMINI_API_KEY','')
    except Exception: return os.getenv('GEMINI_API_KEY','')

@st.cache_data(ttl=600, show_spinner=False)
def grounded_analysis(prompt, api_key):
    if not api_key: return None, 'No Gemini API key configured. Add GEMINI_API_KEY in Streamlit Secrets to enable live AI research.'
    # Google Search grounding is requested via the Gemini API tool declaration.
    try:
        url=f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}'
        body={'contents':[{'role':'user','parts':[{'text':prompt}]}], 'tools':[{'google_search':{}}], 'generationConfig':{'temperature':0.35,'maxOutputTokens':2200}}
        r=requests.post(url,json=body,timeout=45)
        if not r.ok: return None, f'AI research request failed ({r.status_code}). Check API key, model access and quota.'
        data=r.json(); parts=data.get('candidates',[{}])[0].get('content',{}).get('parts',[])
        text='\n'.join(p.get('text','') for p in parts if p.get('text'))
        grounding=data.get('candidates',[{}])[0].get('groundingMetadata',{})
        sources=[]
        for c in grounding.get('groundingChunks',[]):
            web=c.get('web',{})
            if web.get('uri'): sources.append({'title':web.get('title') or web['uri'],'url':web['uri']})
        return {'text':text,'sources':sources}, None
    except Exception as e: return None, f'Could not reach the AI service: {type(e).__name__}. Try again later.'

def image_for_entity(name, mode):
    if mode=='fiction':
        data=anime_search(name)
        if data:
            ch=data[0]
            imgs=ch.get('images',{}).get('jpg',{})
            return imgs.get('image_url') or imgs.get('small_image_url'), ch.get('name',''), ch.get('url',''), ch.get('about','')
    pages=wiki_search(name)
    if pages:
        p=pages[0]
        return p.get('thumbnail',{}).get('source'), p.get('title',''), p.get('fullurl',''), p.get('extract','')
    return None, name, '', ''

def entity_card(name, mode, side_label):
    img,title,url,desc=image_for_entity(name,mode)
    if img: st.image(img,use_container_width=True)
    else:
        st.markdown(f"<div style='height:150px;border-radius:12px;border:1px dashed #275274;background:linear-gradient(135deg,#102945,#090f1e);display:flex;align-items:center;justify-content:center;font-size:48px'>{'🌌' if mode=='fiction' else '🏆'}</div>",unsafe_allow_html=True)
    st.markdown(f"**{title or name}**")
    st.caption(side_label + (f' · Image/info: {url}' if url else ' · No matching image found; name will still be analysed'))
    if desc: st.caption(desc[:220] + ('…' if len(desc)>220 else ''))
    return {'name':name,'resolved_title':title or name,'image':img,'url':url,'description':desc}

def build_prompt(mode, domain, a, b, context, format_choice, extras):
    if mode=='fiction':
        return f'''You are RAN-NEETI, an evidence-grounded fictional battle/anime sports analyst. Compare {a} versus {b}. User context/rules: {context or 'Use the most widely documented canon versions; explicitly state assumptions.'}. Additional settings: {extras or 'None'}. Use Google Search to research trustworthy official/primary or well-documented sources. Distinguish sourced facts from inference. Never invent feats or citations. Explain: (1) character/version identity and image/source evidence; (2) capabilities shown on-screen/on-page, speed, range, defence, stamina, special abilities, weaknesses; (3) win probability estimates that are clearly subjective and not scientifically calibrated; probabilities must sum to 100%; (4) 3-5 major moves per side, trigger, expected impact, counter, risk and turning point; (5) likely battle sequence in stages; (6) win conditions for each; (7) assumptions and unknowns; (8) source links. If evidence is weak or versions unclear, lower confidence and say so. No graphic detail. Format with headings and a compact probability table.''' 
    return f'''You are RAN-NEETI, a careful real-world sports analyst. Analyse {a} versus {b} in {domain}. Match format/competition: {format_choice}. User context: {context or 'Find the most relevant upcoming or recent matchup if identifiable; state which match/date you selected.'}. Advanced settings: {extras or 'None'}. Use Google Search grounding to retrieve recent, reliable sources (official league/team/stat providers preferred). Identify exact teams/athletes and match if ambiguous; do not silently guess. Report source freshness and date. Include: (1) selected matchup and competition/date; (2) win/draw/loss or sport-appropriate outcome probabilities totaling 100%; (3) distinguish actual historical/model statistics from qualitative AI estimates; (4) recent form, head-to-head only if relevant, roster/injuries/venue/weather when verified, strengths and weaknesses; (5) key matchup edges; (6) 3-5 major tactical moves per side, trigger, impact, opponent counter, risk and turning point; (7) likely scenarios and what could change the prediction; (8) win conditions and an uncertainty note; (9) clickable source links. Never invent scores, injuries, statistics, or model accuracy. If no dependable data/model is available, label percentages as qualitative AI estimates rather than validated ML probabilities. For a sport with no draw, do not include a draw outcome.''' 

# Sidebar navigation
with st.sidebar:
    st.markdown("<div style='padding:8px 2px 20px'><div class='brand' style='font-size:34px'>RAN-NEETI</div><div class='kicker' style='letter-spacing:2px'>SPORTS × ANIME × STRATEGY</div></div>",unsafe_allow_html=True)
    if st.session_state.get('nav_jump'):
        st.session_state['nav_page'] = st.session_state.pop('nav_jump')
    page=st.radio('NAVIGATION',['Home Dashboard','Real Sports Lab','Anime & Fictional Battles','Recent Reports','About RAN-NEETI'],index=0,key='nav_page')
    st.markdown('---')
    st.markdown('**QUICK SPORTS**')
    for n in ['Football / Soccer','Cricket','Basketball','Tennis','Badminton','MMA / UFC','Motorsport / F1','Esports']:
        st.caption(f'{SPORTS[n]}  {n}')
    st.markdown('---')
    st.caption('Different worlds. Same question: who has the edge?')
    st.caption('AI analysis · source-aware · uncertainty shown')

if 'reports' not in st.session_state: st.session_state.reports=[]
if 'selected_sport' not in st.session_state: st.session_state.selected_sport='Football / Soccer'

# Home
if page=='Home Dashboard':
    st.markdown('''<div class="hero"><div class="kicker">THE NEXT-GEN MATCHUP INTELLIGENCE HUB</div><div class="brand">RAN-NEETI</div><div class="hero-sub">Real-world sports analysis. Anime matchups. Fictional battles. Compare two sides, research the evidence, and discover the moves, counters and turning points that could decide the outcome.</div><span class="pill">⚡ AI-powered research</span><span class="pill">⚔️ Head-to-head comparisons</span><span class="pill">📊 Probabilities + reasoning</span><span class="pill">🔎 Sources when available</span></div>''',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.markdown('<div class="panel"><div class="kicker">01 / SPORTS</div><div class="section-title">REAL SPORTS LAB</div><div class="muted">Choose the exact sport, then compare teams or players side by side.</div><br><div style="font-size:32px">⚽ 🏏 🏀 🎾</div><div class="muted">80+ sport categories · tactical matchups · win conditions</div></div>',unsafe_allow_html=True)
    with c2: st.markdown('<div class="panel"><div class="kicker">02 / ANIME</div><div class="section-title">ANIME & FICTION</div><div class="muted">Type two character names. Character images are looked up automatically where available.</div><br><div style="font-size:32px">🥷 ⚔️ 🌌 💥</div><div class="muted">Version-aware comparisons · feats · abilities · counters</div></div>',unsafe_allow_html=True)
    with c3: st.markdown('<div class="panel"><div class="kicker">03 / INTELLIGENCE</div><div class="section-title">MOVES THAT MATTER</div><div class="muted">Not just who wins: see why, how, which counters work and what might flip the result.</div><br><div style="font-size:32px">📈 🎯 🧠</div><div class="muted">Major moves · risks · turning points · win conditions</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Choose your arena</div><div class="muted">Start from a dedicated dashboard. Each comparison has two separate sides — no one-box matchup guessing.</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="tile"><div class="tile-icon">🏆</div><div class="tile-title">Real Sports Dashboard</div><div class="tile-sub">Pick from a large sport list, then search Side A and Side B.</div></div>',unsafe_allow_html=True)
        if st.button('Open Sports Lab →',use_container_width=True): st.session_state['nav_jump']='Real Sports Lab'; st.rerun()
    with b:
        st.markdown('<div class="tile"><div class="tile-icon">⚔️</div><div class="tile-title">Anime & Fictional Battle Dashboard</div><div class="tile-sub">Character-versus-character, anime sports, game fighters and fictional matchups.</div></div>',unsafe_allow_html=True)
        if st.button('Open Anime / Fiction →',use_container_width=True): st.session_state['nav_jump']='Anime & Fictional Battles'; st.rerun()
    st.markdown('<div class="section-title">How to use it</div>',unsafe_allow_html=True)
    steps=st.columns(4)
    for col,num,title,desc in zip(steps,['01','02','03','04'],['Choose a dashboard','Name both sides','Run AI research','Read the matchup report'],['Real sport or fictional universe.','Separate A and B inputs; portraits resolve automatically where possible.','AI searches available web sources when the API key is configured.','Probabilities, key factors, major moves, counters, risks and sources.']):
        with col: st.markdown(f'<div class="tile"><div class="kicker">STEP {num}</div><div class="tile-title">{title}</div><div class="tile-sub">{desc}</div></div>',unsafe_allow_html=True)

# Sports lab
elif page=='Real Sports Lab':
    st.markdown('<div class="kicker">01 / REAL-WORLD COMPETITION</div><div class="brand" style="font-size:42px">SPORTS MATCHUP LAB</div><div class="hero-sub">Choose a sport first. Compare two teams, athletes or competitors with a source-aware AI scouting report.</div>',unsafe_allow_html=True)
    with st.container():
        s1,s2,s3=st.columns([1.2,1,1])
        with s1: sport=st.selectbox('SELECT SPORT',list(SPORTS.keys()),index=list(SPORTS.keys()).index(st.session_state['selected_sport']) if st.session_state['selected_sport'] in SPORTS else 0)
        with s2: fmt=st.selectbox('MATCH FORMAT', ['Auto-detect','Upcoming match','Recent match','League / tournament','Best-of series','T20','ODI','Test','Friendly / exhibition','Custom rules'])
        with s3: venue=st.selectbox('VENUE / CONTEXT',['Auto research','Home advantage matters','Neutral venue','Indoor','Outdoor','Custom'])
    st.markdown('<div class="section-title">Head-to-head comparison</div><div class="muted">Enter both sides independently. The site will try to fetch matching images and summaries; the AI report identifies the most relevant matchup.</div>',unsafe_allow_html=True)
    l,r=st.columns(2,gap='large')
    with l:
        st.markdown('<div class="panel"><div class="kicker">SIDE A / BLUE CORNER</div><div class="section-title">First team or athlete</div>',unsafe_allow_html=True)
        a_name=st.text_input('Side A name',placeholder='e.g. Manchester City, India, Carlos Alcaraz',key='sports_a')
        st.markdown('</div>',unsafe_allow_html=True)
    with r:
        st.markdown('<div class="panel"><div class="kicker">SIDE B / VIOLET CORNER</div><div class="section-title">Opponent</div>',unsafe_allow_html=True)
        b_name=st.text_input('Side B name',placeholder='e.g. Liverpool, Australia, Jannik Sinner',key='sports_b')
        st.markdown('</div>',unsafe_allow_html=True)
    context=st.text_input('Optional match / league / date (leave blank for AI to identify)',placeholder='e.g. Premier League, final, next match')
    extras=st.text_area('Advanced controls (optional)',placeholder='e.g. use T20 only, neutral venue, compare current roster, focus on defensive tactics',height=75)
    go=st.button('⚡  RESEARCH & COMPARE BOTH SIDES',use_container_width=True,key='sports_go')
    if go:
        if not a_name.strip() or not b_name.strip(): st.warning('Enter a name for both Side A and Side B to run the comparison.')
        elif a_name.strip().casefold()==b_name.strip().casefold(): st.warning('Choose two different opponents for a head-to-head comparison.')
        else:
            with st.spinner('Resolving teams and researching current sources…'):
                ca,cb=st.columns(2)
                with ca: aa=entity_card(a_name.strip(),'sports','SIDE A')
                with cb: bb=entity_card(b_name.strip(),'sports','SIDE B')
                prompt=build_prompt('sports',sport,a_name.strip(),b_name.strip(),context,fmt,f'Venue: {venue}. {extras}')
                result,err=grounded_analysis(prompt,get_gemini_key())
            if result:
                st.markdown('<div class="section-title">AI scouting report</div>',unsafe_allow_html=True)
                st.markdown(result['text'])
                if result['sources']:
                    st.markdown('#### Research sources')
                    for src in result['sources'][:10]: st.markdown(f"- [{src['title']}]({src['url']})")
                st.session_state.reports.insert(0,{'type':'Sports','title':f'{a_name} vs {b_name}','sport':sport,'text':result['text'],'sources':result['sources'],'time':time.strftime('%Y-%m-%d %H:%M')})
            else: st.error(err)
            st.caption('Image lookup and AI search are separate: an image match is not proof of current form, roster or performance. Probabilities are not validated ML probabilities unless explicitly backed by a tested model.')

# Fiction lab
elif page=='Anime & Fictional Battles':
    st.markdown('<div class="kicker">02 / FICTIONAL UNIVERSES</div><div class="brand" style="font-size:42px">ANIME & FICTION ARENA</div><div class="hero-sub">Anime fights, anime sports, game fighters, comics and fictional matchups. Type both names; the dashboard attempts to fetch character portraits automatically.</div>',unsafe_allow_html=True)
    typ=st.selectbox('CHOOSE MATCHUP TYPE',['Anime / manga fight','Anime sports match','Video game fighters','Comics / fictional characters','Any fictional matchup'])
    universe=st.text_input('Universe / series (optional)',placeholder='e.g. Naruto, Dragon Ball, Haikyuu, Tekken')
    l,r=st.columns(2,gap='large')
    with l:
        st.markdown('<div class="panel"><div class="kicker">SIDE A / CHALLENGER</div><div class="section-title">Character one</div>',unsafe_allow_html=True)
        a_name=st.text_input('Character A',placeholder='e.g. Naruto Uzumaki',key='fiction_a')
        st.markdown('</div>',unsafe_allow_html=True)
    with r:
        st.markdown('<div class="panel"><div class="kicker">SIDE B / RIVAL</div><div class="section-title">Character two</div>',unsafe_allow_html=True)
        b_name=st.text_input('Character B',placeholder='e.g. Sasuke Uchiha',key='fiction_b')
        st.markdown('</div>',unsafe_allow_html=True)
    versions=st.text_input('Versions / story arc (optional)',placeholder='e.g. Six Paths Naruto vs Rinnegan Sasuke; leave blank for AI to state assumptions')
    rules=st.selectbox('BATTLE RULES',['Standard abilities; no prep time','Both at strongest canon version','Specific arc / version','Tournament rules','Anime sports rules','Custom rules below'])
    extra=st.text_area('Optional rules / scenario',placeholder='e.g. neutral arena, no outside help, win by knockout or surrender; compare team formations and signature plays',height=75)
    go=st.button('⚔️  ANALYSE THE MATCHUP',use_container_width=True,key='fiction_go')
    if go:
        if not a_name.strip() or not b_name.strip(): st.warning('Enter two character / fighter names. You do not need to configure separate anime APIs.')
        elif a_name.strip().casefold()==b_name.strip().casefold(): st.warning('Choose two different characters for this versus matchup.')
        else:
            with st.spinner('Finding character portraits and researching cited feats…'):
                aa=entity_card(a_name.strip(),'fiction','SIDE A')
                bb=entity_card(b_name.strip(),'fiction','SIDE B')
                ctx=f'Type: {typ}. Universe: {universe or "AI identify from names"}. Versions: {versions or "AI must state version assumptions"}. Battle rules: {rules}. {extra}'
                result,err=grounded_analysis(build_prompt('fiction',typ,a_name.strip(),b_name.strip(),ctx,'',extra),get_gemini_key())
            if result:
                st.markdown('<div class="section-title">Versus intelligence report</div>',unsafe_allow_html=True)
                st.markdown(result['text'])
                if result['sources']:
                    st.markdown('#### Evidence & references')
                    for src in result['sources'][:10]: st.markdown(f"- [{src['title']}]({src['url']})")
                st.session_state.reports.insert(0,{'type':'Anime / Fiction','title':f'{a_name} vs {b_name}','sport':typ,'text':result['text'],'sources':result['sources'],'time':time.strftime('%Y-%m-%d %H:%M')})
            else: st.error(err)
            st.caption('Fictional battle percentages are subjective estimates based on cited feats and declared assumptions; they are not objectively measurable real-world probabilities. Portraits may be missing or mismatched if the character database has no exact match.')

elif page=='Recent Reports':
    st.markdown('<div class="kicker">YOUR SESSION</div><div class="brand" style="font-size:42px">RECENT REPORTS</div>',unsafe_allow_html=True)
    if not st.session_state.reports: st.info('No reports in this session yet. Run a comparison in Sports Lab or Anime & Fiction Arena first.')
    else:
        for i,rep in enumerate(st.session_state.reports):
            with st.expander(f"{rep['type']} · {rep['title']} · {rep['time']}",expanded=(i==0)):
                st.markdown(rep['text'])
                for src in rep.get('sources',[])[:10]: st.markdown(f"- [{src['title']}]({src['url']})")
                st.download_button('Download report as Markdown',data=f"# {rep['title']}\n\n{rep['text']}\n\nSources:\n"+'\n'.join(f"- [{s['title']}]({s['url']})" for s in rep.get('sources',[])),file_name=re.sub(r'[^a-zA-Z0-9]+','_',rep['title']).strip('_')+'.md',mime='text/markdown',key=f'dl_{i}')

elif page=='About RAN-NEETI':
    st.markdown('<div class="kicker">PROJECT OVERVIEW</div><div class="brand" style="font-size:42px">WHAT RAN-NEETI DOES</div>',unsafe_allow_html=True)
    st.markdown('''<div class="panel"><div class="section-title">One platform. Two separate arenas.</div><p>RAN-NEETI provides separate dashboards for real sports and fictional/anime matchups. Each comparison asks for two sides and returns an evidence-aware report when the AI service is configured.</p><hr><div class="section-title">Every report aims to include</div><ul><li>Matchup / character identity and relevant context</li><li>Win probabilities with clear labels about their basis</li><li>Strengths, weaknesses and key matchup factors</li><li>Major moves, triggers, impact, counters and risks</li><li>Turning points, likely scenarios and win conditions</li><li>Source links, unknowns and uncertainty</li></ul><hr><div class="section-title">Honest limitations</div><p>Web search does not guarantee complete or accurate data. Public images may be missing or mismatched. A grounded AI explanation is not the same as a separately trained and validated sports prediction model. API access, quotas and licensing can limit automatic research.</p></div>''',unsafe_allow_html=True)
    st.markdown('#### Enable AI search')
    st.write('Create a Gemini API key in Google AI Studio, then add it in Streamlit Cloud → App settings → Secrets:')
    st.code('GEMINI_API_KEY = "paste_your_private_key_here"',language='toml')
    st.caption('Never publish your API key in GitHub or inside the app source code.')

#!/usr/bin/env python3
"""Build index.html for the control center. Usage: python3 tools/build.py [version]
Renders CONTROL.md + CHANGELOG.md into site/template.html."""
import sys,os,re,datetime
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def md_to_html(md, anchor_sections=False):
    def inline(t):
        t=re.sub(r'&','&amp;',t); t=re.sub(r'<','&lt;',t); t=re.sub(r'>','&gt;',t)
        t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2" target="_blank" rel="noreferrer">\1</a>',t)
        t=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',t)
        t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
        return t
    out=[]; ul=False
    def close_ul():
        nonlocal ul
        if ul: out.append('</ul>'); ul=False
    for line in md.splitlines():
        s=line.strip()
        if not s: close_ul(); continue
        m=re.match(r'^(#{1,4})\s+(.*)',s)
        if m:
            close_ul(); lv=len(m.group(1)); txt=m.group(2)
            anchor=''
            if anchor_sections and lv==2:
                sm=re.match(r'^(\d+)\.',txt)
                if sm: anchor=' id="s%s"'%sm.group(1)
            out.append('<h%d%s>%s</h%d>'%(lv,anchor,inline(txt),lv)); continue
        m=re.match(r'^[-*]\s+(.*)',s)
        if m:
            if not ul: out.append('<ul>'); ul=True
            out.append('<li>%s</li>'%inline(m.group(1))); continue
        m=re.match(r'^\d+[.、]\s*(.*)',s)
        if m:
            if not ul: out.append('<ul>'); ul=True
            out.append('<li>%s</li>'%inline(m.group(1))); continue
        if s in ('---','***'):
            close_ul(); out.append('<hr>'); continue
        close_ul(); out.append('<p>%s</p>'%inline(s))
    close_ul()
    return '\n'.join(out)

rd=lambda p:open(os.path.join(R,p),encoding='utf-8').read()
ver=sys.argv[1] if len(sys.argv)>1 else 'dev'
stamp=ver+' '+datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')
html=rd('site/template.html')
html=html.replace('__CSS__',rd('site/style.css'))
html=html.replace('__STAMP__',stamp)
html=html.replace('__CONTROL__',md_to_html(rd('CONTROL.md'),anchor_sections=True))
html=html.replace('__CHANGELOG__',md_to_html(rd('CHANGELOG.md')))
open(os.path.join(R,'index.html'),'w',encoding='utf-8').write(html)
print('built',stamp,len(html))

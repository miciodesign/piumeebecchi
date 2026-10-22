import subprocess, os, sys, html
V,G,A,C,VS="#1f4d3a","#f5c518","#e07a2f","#fbf8f1","#173b2c"
def wrap(t,n):
    w,l,out=t.split(),"",[]
    for x in w:
        if len(l+" "+x)>n and l: out.append(l); l=x
        else: l=(l+" "+x).strip()
    return out+[l]
def slide(i,kicker,text,sub,bg,fg,big=88,n=16):
    L=wrap(text,n); y=760-int(len(L)*big*0.55)
    ts="".join(f'<tspan x="540" dy="{0 if k==0 else int(big*1.15)}">{html.escape(s)}</tspan>' for k,s in enumerate(L))
    sy=y+int((len(L)-1)*big*1.15)+110
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<rect width="1080" height="1920" fill="{bg}"/>
<circle cx="540" cy="330" r="120" fill="{A}"/><circle cx="540" cy="330" r="70" fill="{bg}" opacity=".15"/>
<text x="540" y="560" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" font-weight="700" fill="{G if bg==V else A}" letter-spacing="6">{html.escape(kicker)}</text>
<text x="540" y="{y+330}" text-anchor="middle" font-family="Georgia,serif" font-size="{big}" font-weight="700" fill="{fg}">{ts}</text>
<text x="540" y="{sy+330}" text-anchor="middle" font-family="Arial,sans-serif" font-size="38" fill="{fg}" opacity=".8">{html.escape(sub)}</text>
<text x="540" y="1740" text-anchor="middle" font-family="Georgia,serif" font-size="58" font-weight="700" fill="{fg}">Piume <tspan fill="{G}" font-style="italic" font-weight="400">e</tspan> Becchi</text>
<text x="540" y="1800" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="{fg}" opacity=".8">piumeebecchi.it</text>
</svg>'''
    open(f"s{i}.svg","w").write(svg)
    subprocess.run(["node","-e",f"require('sharp')('s{i}.svg').png().toFile('s{i}.png')"],check=True)
S=[("LO SAPEVI?","5 curiosità sul pettirosso","Una scheda per la scuola primaria",V,C,92,14,4),
("CURIOSITÀ 1","Pesa come 3 o 4 monete da 1 euro","Circa 15-20 grammi",C,VS,84,17,4),
("CURIOSITÀ 2","Il petto è arancione, non rosso!","Maschio e femmina sono uguali",V,C,84,17,4),
("CURIOSITÀ 3","Canta anche d'inverno","È uno dei pochi uccelli a farlo",C,VS,88,16,4),
("CURIOSITÀ 4","Segue chi zappa l'orto","Aspetta i vermetti della terra smossa",V,C,88,16,4),
("CURIOSITÀ 5","Difende il suo giardino da tutti gli altri pettirossi","Anche in pieno inverno",C,VS,76,19,5),
("PER LA RICERCA","Scheda completa per la scuola primaria","Gratis su piumeebecchi.it",V,C,80,18,5)]
for i,(k,t,s,bg,fg,b,n,d) in enumerate(S): slide(i,k,t,s,bg,fg,b,n)
for i,(*_,d) in enumerate(S):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",f"s{i}.png","-t",str(d),"-vf",f"scale=1188:2112,zoompan=z='1+0.0008*on':d={d*30}:s=1080x1920:fps=30,fade=t=in:d=0.4,fade=t=out:st={d-0.4}:d=0.4,format=yuv420p","-r","30",f"c{i}.mp4"],check=True)
open("l.txt","w").write("".join(f"file 'c{i}.mp4'\n" for i in range(len(S))))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-i","l.txt","-c","copy","pettirosso-short.mp4"],check=True)

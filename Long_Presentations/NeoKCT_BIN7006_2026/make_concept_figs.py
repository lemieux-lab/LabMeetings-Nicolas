# Hand-built conceptual figures for the IRIC talk: tsa_therapy, tsa_sources, two_workflows, peptide_query,
# posting_lists, delta_metaphor, packing_crates, tcell_questions.
# Same dark palette as every other figure in this repo. Counts in peptide_query are
# illustrative, k-mer sequences are real translations (see NeoKCT/Figures/kct_overview.svg).
# Run: python3 make_concept_figs.py
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G='#3ecfa2';R='#e58468';K='#f0b429';D='#9db3ab';I='#e8efec';CARD='#151f1b';PAN='#1c2822';BR='#2a3a33';B='#6f8fd8'
F="font-family=\"'Archivo', sans-serif\""
M=" font-family=\"'JetBrains Mono', monospace\""
BOLD=' font-weight="700"'

def head(W,H):
    mk=''.join(f'<marker id="{n}" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="{c}"/></marker>'
               for n,c in (('a',D),('ag',G),('ar',R),('ak',K)))
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {F}>',
            f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{CARD}"/>', f'<defs>{mk}</defs>']
def box(o,x,y,w,h,stroke=BR,fill=PAN,sw=1.5):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def t(o,x,y,s,col=I,fs=16,anchor='start',mono=False,bold=False):
    s=s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    o.append(f'<text x="{x}" y="{y}" fill="{col}" font-size="{fs}" text-anchor="{anchor}"{BOLD if bold else ""}{M if mono else ""}>{s}</text>')
def line(o,d,col=D,m='a',sw=2):
    o.append(f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="none" marker-end="url(#{m})"/>')

# ---------------- tsa_therapy.svg ----------------
# Why TSAs are worth finding: a T cell kills the tumor cell that shows one and leaves healthy cells alone.
# Purely conceptual, no numbers.
def mhc(o,x,y,pep):
    # MHC-I groove sitting on the membrane at (x,y), opening to the right, peptide inside
    o.append(f'<path d="M{x},{y} L{x+22},{y}" stroke="{B}" stroke-width="5"/>')
    o.append(f'<path d="M{x+44},{y-20} L{x+22},{y-20} L{x+22},{y+20} L{x+44},{y+20}" stroke="{B}" stroke-width="6" fill="none"/>')
    o.append(f'<rect x="{x+26}" y="{y-9}" width="16" height="18" rx="3" fill="{pep}"/>')
# The talk's mascot, a CD8 T cell that shows up in corners looking at figures. Round body, a ring
# of Y-shaped TCRs on the membrane (none on the bottom so it can sit on things), a nucleus hint,
# two small eyes that slide toward `look`, and a small CD8 label. `look` is a direction, (0,0) means
# straight at the audience.
import math
MASCOT_BODY='#1f3a31'
def mascot(o,cx,cy,look=(0,0),r=60,mood='neutral',sweat=False):
    for ang in (-150,-115,-80,-45,-10,25,155,190):
        a=math.radians(ang); ux,uy=math.cos(a),math.sin(a); px,py=-uy,ux
        x0,y0=cx+r*ux,cy+r*uy; x1,y1=cx+(r+11)*ux,cy+(r+11)*uy
        o.append(f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f} M{x1:.1f},{y1:.1f} L{x1+7*ux+5*px:.1f},{y1+7*uy+5*py:.1f} M{x1:.1f},{y1:.1f} L{x1+7*ux-5*px:.1f},{y1+7*uy-5*py:.1f}" stroke="{G}" stroke-width="3.2" stroke-linecap="round" fill="none"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MASCOT_BODY}" stroke="{G}" stroke-width="3"/>')
    o.append(f'<circle cx="{cx+r*0.28:.1f}" cy="{cy+r*0.35:.1f}" r="{r*0.3:.1f}" fill="#25463b"/>')
    # face: two small solid eyes, no whites, no mouth. Gaze is the whole pair sliding toward `look`,
    # like a head turning, which reads at slide-corner size without going cartoonish.
    # Moods only touch the brows and the eye shape: angry (brows down to the middle), worried
    # (brows up in the middle), surprised (round eyes, high brows), perplexed (one brow up, one
    # flat), satisfied (eyes closed into arcs), squint (right eye shut, for the telescope).
    lx,ly=look; n=math.hypot(lx,ly)
    lx,ly=(lx/n*13,ly/n*10) if n else (0,0)
    ey=cy-10+ly
    brow=lambda d: o.append(f'<path d="{d}" stroke="{G}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    for side,ex in ((-1,cx-13+lx),(1,cx+13+lx)):
        outer,inner=ex+7*side,ex-7*side
        if mood=='squint' and side==1:
            # one eye shut, as if the other one is at an eyepiece
            o.append(f'<path d="M{ex-6:.1f},{ey+1:.1f} Q{ex:.1f},{ey-3:.1f} {ex+6:.1f},{ey+1:.1f}" stroke="{I}" stroke-width="3" fill="none" stroke-linecap="round"/>')
            brow(f'M{ex-7:.1f},{ey-9:.1f} L{ex+7:.1f},{ey-12:.1f}')
        elif mood=='satisfied':
            o.append(f'<path d="M{ex-6:.1f},{ey+2:.1f} Q{ex:.1f},{ey-7:.1f} {ex+6:.1f},{ey+2:.1f}" stroke="{I}" stroke-width="3" fill="none" stroke-linecap="round"/>')
        else:
            rx,ry={'surprised':(5.5,7.5),'angry':(4.5,5)}.get(mood,(4.5,6.5))
            o.append(f'<ellipse cx="{ex:.1f}" cy="{ey:.1f}" rx="{rx}" ry="{ry}" fill="{I}"/>')
        if mood=='angry': brow(f'M{outer:.1f},{ey-16:.1f} L{inner:.1f},{ey-9:.1f}')
        elif mood=='worried': brow(f'M{outer:.1f},{ey-11:.1f} L{inner:.1f},{ey-17:.1f}')
        elif mood=='surprised' or (mood=='perplexed' and side==-1): brow(f'M{ex-7:.1f},{ey-15:.1f} Q{ex:.1f},{ey-23:.1f} {ex+7:.1f},{ey-15:.1f}')
        elif mood=='perplexed': brow(f'M{ex-7:.1f},{ey-11:.1f} L{ex+7:.1f},{ey-13:.1f}')
    if sweat:
        sx,sy=cx+40,cy-30
        o.append(f'<path d="M{sx},{sy-10} Q{sx+8},{sy+2} {sx},{sy+6} Q{sx-8},{sy+2} {sx},{sy-10} Z" fill="#8fd3ff"/>')
    t(o,cx-r*0.35,cy+r*0.62,'CD8',D,15,'middle',bold=True)
def tcell(o,cx,cy,stroke,mood='neutral'):
    # the mascot plus one TCR reaching out to the MHC on its left
    o.append(f'<path d="M{cx-62},{cy} L{cx-84},{cy} M{cx-84},{cy-14} L{cx-84},{cy+14}" stroke="{G}" stroke-width="5" fill="none"/>')
    mascot(o,cx,cy,look=(-1,0),mood=mood)
o=head(1090,500)
for x0,title,cellcol,fill,pep,tc,res,rescol in ((30,'Tumor cell','#e58468','#2a1d19',R,G,['non-self antigen on MHC-I is recognized,','the tumor cell is killed'],G),
                                                (560,'Healthy cell',D,'#1a2420',D,BR,['only self peptides, nothing','to recognize, tissue is spared'],D)):
    box(o,x0,30,500,440)
    cx=x0+140
    o.append(f'<circle cx="{cx}" cy="230" r="105" fill="{fill}" stroke="{cellcol}" stroke-width="2.5"/>')
    t(o,cx,236,title,cellcol,19,'middle',bold=True)
    mhc(o,cx+105,230,pep)
    tcell(o,x0+400,230,tc if tc!=BR else D,mood='angry' if pep==R else 'neutral')
    if pep==R:
        t(o,cx+148,276,'non-self',R,15,'middle',bold=True)
        o.append(f'<path d="M{x0+300},175 Q{x0+250},150 {cx+70},160" stroke="{G}" stroke-width="2.5" fill="none" stroke-dasharray="6 5" marker-end="url(#ag)"/>')
        t(o,x0+300,150,'kill',G,15,'middle',bold=True)
    else:
        t(o,cx+148,276,'self',D,15,'middle')
    for i,s in enumerate(res): t(o,x0+250,400+i*26,s,rescol,17,'middle')
    # knife for the killer (mirrored left-right so the blade faces the tumor), ok hand for the bystander,
    # both perched on the T cell's top-left
    ex=x0+345
    if pep==R: o.append(f'<text x="{ex}" y="182" font-size="40" text-anchor="middle" transform="matrix(-1,0,0,1,{2*ex},0)">\U0001F52A</text>')
    else: t(o,ex,182,'\U0001F44C',I,40,'middle')
o.append('</svg>'); open('tsa_therapy.svg','w').write('\n'.join(o))

# ---------------- tsa_sources.svg ----------------
# Where MHC-I peptides come from and why non-canonical ones are hard to trace back to RNA.
# ~90% figure from Laumont et al. 2018. Everything else is a conceptual diagram.
o=head(1600,600)
box(o,30,30,330,500)
t(o,195,64,'Tumor cell',I,20,'middle',bold=True)
box(o,50,82,290,46,stroke=G); t(o,195,111,'annotated proteins',G,16,'middle')
t(o,195,156,'non-canonical sources:',D,15,'middle')
for i,s in enumerate(['transposable elements (ERVs)','gene fusions, viral integration','out-of-frame translation','intron retention, non-coding RNA','unannotated splice junctions']):
    y=172+i*68; box(o,50,y,290,52,stroke=R); t(o,195,y+32,s,R,15,'middle')
line(o,'M360,280 L408,280')
box(o,410,200,250,160,stroke=B); t(o,535,238,'MHC-I peptides',I,19,'middle',bold=True)
for i,s in enumerate(['8 to 11 residues,','presented at the','cell surface']): t(o,535,268+i*22,s,D,15,'middle')
line(o,'M660,280 L708,280')
box(o,710,200,280,160); t(o,850,238,'Mass spectrometry',I,19,'middle',bold=True)
for i,s in enumerate(['spectra matched against','a protein database built','from the tumor\'s RNA-seq']): t(o,850,268+i*22,s,D,15,'middle')
line(o,'M990,250 L1058,150',G,'ag'); line(o,'M990,310 L1058,400',R,'ar')
box(o,1060,60,510,170,stroke=G); t(o,1080,94,'Canonical peptides',G,19,bold=True)
for i,s in enumerate(['come from an annotated protein,','so a gene model says where their RNA is.','A minority of tumor-specific antigens.']): t(o,1080,124+i*24,s,D,15)
box(o,1060,300,510,200,stroke=R); t(o,1080,334,'Non-canonical peptides',R,19,bold=True)
for i,s in enumerate(['no annotated protein, no gene model.','About 90% of the tumor-specific antigens','in Laumont et al. (2018), the most promising','candidates and the hardest to trace back to RNA.']): t(o,1080,364+i*24,s,D,15)
box(o,30,545,1540,40,stroke=K,fill='#2a2414')
t(o,50,571,'Next question for every candidate: where is this peptide\'s RNA, in the tumor and in healthy tissue?',I,17)
o.append('</svg>'); open('tsa_sources.svg','w').write('\n'.join(o))

# ---------------- two_workflows.svg ----------------
# Top lane: BamQuery back-translates each peptide into every coding DNA sequence, keeps the ones
# found in GRCh38, then reads every BAM at those loci (Ruiz Cuevas et al. 2023). The explosion
# strip is exact for AGLKVTSAP (codon degeneracy per residue). The per-length averages use
# 3.6 codons per residue, the degeneracy averaged over approximate human proteome amino-acid
# frequencies (UniProt), so they are expected values, not exact. 199/550 and ~730 CPU-h are
# from C5 and the BamQuery paper. Bottom lane: NeoKCT translates reads forward instead.
import math
DEG=dict(L=6,S=6,R=6,A=4,G=4,P=4,V=4,T=4,I=3,E=2,K=2,Q=2,D=2,F=2,N=2,Y=2,H=2,C=2,M=1,W=1)
o=head(1600,534)
t(o,30,40,'Alignment-based validation (BamQuery): each peptide is translated backward, then filtered by the genome',R,20,bold=True)
pep='AGLKVTSAP'; tot=math.prod(DEG[c] for c in pep)
steps=[(230,'Peptide',[pep,'from mass spec'],BR),
       (290,'Back-translate',[f'{tot:,} DNA sequences','could code for it'],R),
       (290,'Keep those in GRCh38',['the reference genome','filters them to a few loci'],R),
       (290,'Read every BAM',['at those loci,','2,489 GTEx samples'],BR),
       (230,'Counts',['per peptide,','per sample'],BR)]
x=30
for i,(w,a,ls,col) in enumerate(steps):
    box(o,x,58,w,110,stroke=col,sw=2 if col==R else 1.5)
    t(o,x+18,92,a,I,19,bold=True)
    for j,s in enumerate(ls): t(o,x+18,120+j*22,s,K if (i==1 and j==0) else D,15 if not (i==1 and j==0) else 17,mono=(i==0 and j==0),bold=(i==1 and j==0))
    if i<4: line(o,f'M{x+w},113 L{x+w+40},113')
    x+=w+42
# explosion, one compact strip: the exact product for the example, then the per-length average
DY=-248  # bottom lane moves up into the space the old bar chart and genome-filter strip used
box(o,30,186,1540,70,stroke=R,fill='#2e201b')
prod=' × '.join(str(DEG[c]) for c in pep)
t(o,50,215,f'{pep}: {prod} = {tot:,} possible coding sequences.',I,17,bold=True)
t(o,50,241,f'At 3.6 codons per residue on average, a 9-mer has about 100,000 and an 11-mer about 1.3 million.',D,15)
o.append(f'<g transform="translate(0,{DY})">')
# bottom lane: NeoKCT
t(o,30,548,'NeoKCT: translate the reads forward instead, count once, then look up',G,20,bold=True)
lane=[(270,'RNA-seq reads',['all reads, no alignment,','no reference'],BR),
      (270,'Translate forward',['each 30-nt window gives','exactly one 10-mer'],K),
      (270,'The table',['2,486 GTEx samples,','62.6 billion fragments'],K),
      (270,'Look up',['any peptide list,','any sequence'],G),
      (268,'Counts',['per peptide,','per sample'],G)]
x=30
for i,(w,a,ls,col) in enumerate(lane):
    box(o,x,566,w,110,stroke=col,sw=2 if col==K else 1.5)
    t(o,x+18,600,a,K if a=='The table' else I,19,bold=True)
    for j,s in enumerate(ls): t(o,x+18,628+j*22,s,D,15)
    if i<4: line(o,f'M{x+w},621 L{x+w+46},621',G if i>=2 else D,'ag' if i>=2 else 'a')
    x+=w+48
t(o,483,700,'one-time cost, about 10 days on one server',K,15,'middle')
t(o,1143,700,'1,245 peptides x 2,486 samples: 0.5 s of lookup, ~46 min with loading',G,15,'middle')
box(o,30,716,1540,44,stroke=G,fill='#17281f')
t(o,50,744,'Going forward, translation has exactly one answer: no explosion, no genome filter, every peptide can be queried.',I,17)
o.append('</g>')
o.append('</svg>'); open('two_workflows.svg','w').write('\n'.join(o))

# ---------------- peptide_query.svg ----------------
o=head(1600,600)
t(o,30,44,'The table stores 10-amino-acid fragments. MHC-I peptides are 8 to 11 long, so a query has three cases.',I,20,bold=True)
cols=['s1','s2','s3','s4']
def panel(x,title,sub,rows,res,reslabel,col):
    box(o,x,70,500,500)
    t(o,x+20,104,title,col,19,bold=True)
    for i,s in enumerate(sub): t(o,x+20,132+i*22,s,D,15)
    y0=210
    for j,c in enumerate(cols): t(o,x+300+j*48,y0,c,'#8fb0e8',15,'middle',bold=True)
    y=y0+36
    for (km,hl,vals) in rows:
        if hl:
            t(o,x+20,y,km[:hl],K,16,mono=True); t(o,x+20+hl*9.6,y,km[hl:],I,16,mono=True)
        else: t(o,x+20,y,km,I,16,mono=True)
        for j,v in enumerate(vals): t(o,x+300+j*48,y,'·' if v==0 else str(v),D if v==0 else I,16,'middle',mono=True)
        y+=34
    o.append(f'<path d="M{x+20},{y-14} L{x+480},{y-14}" stroke="{BR}" stroke-width="1.5"/>')
    t(o,x+20,y+16,reslabel,col,16)
    for j,v in enumerate(res): t(o,x+300+j*48,y+16,str(v),col,17,'middle',mono=True,bold=True)
    return y+16
# Shorter-than-10 panel is drawn by hand: two anchor groups (fragments starting with the peptide,
# fragments ending with it), each summed, then the per-sample max. Matches peptide_counts'
# default anchor=:both since 2026-11-20. The end-anchored group is what rescues a peptide whose
# next codon is a stop, the old C-terminal blind spot.
x=30
box(o,x,70,500,500)
t(o,x+20,104,'Shorter than 10 (e.g. a 9-mer)',G,19,bold=True)
t(o,x+20,132,'fragments that start with it, and fragments',D,15); t(o,x+20,154,'that end with it: add each group, keep the larger',D,15)
for j,c in enumerate(cols): t(o,x+300+j*48,200,c,'#8fb0e8',15,'middle',bold=True)
def qrow(y,km,pre,vals):
    if pre: t(o,x+20,y,km[:9],K,16,mono=True); t(o,x+20+9*9.6,y,km[9:],I,16,mono=True)
    else: t(o,x+20,y,km[:1],I,16,mono=True); t(o,x+20+9.6,y,km[1:],K,16,mono=True)
    for j,v in enumerate(vals): t(o,x+300+j*48,y,'·' if v==0 else str(v),D if v==0 else I,16,'middle',mono=True)
def subtotal(y,label,vals,col=D,bold=False):
    o.append(f'<path d="M{x+20},{y-20} L{x+480},{y-20}" stroke="{BR}" stroke-width="1.5"/>')
    t(o,x+20,y,label,col,15 if not bold else 16,bold=bold)
    for j,v in enumerate(vals): t(o,x+300+j*48,y,str(v),col,16 if not bold else 17,'middle',mono=True,bold=bold)
for i,(km,v) in enumerate((('AGLKVTSAPA',[3,0,1,0]),('AGLKVTSAPQ',[3,0,0,6]),('AGLKVTSAPS',[0,2,0,1]))): qrow(232+i*30,km,True,v)
subtotal(326,'starts with it',[6,2,1,7])
for i,(km,v) in enumerate((('MAGLKVTSAP',[5,0,8,0]),('KAGLKVTSAP',[0,3,0,0]))): qrow(354+i*28,km,False,v)
subtotal(414,'ends with it',[5,3,8,0])
subtotal(452,'AGLKVTSAP',[6,3,8,7],G,True)
t(o,x+20,500,'if the next codon is a stop, nothing starts with',D,14); t(o,x+20,520,'the peptide, but fragments still end with it',D,14)
y=panel(550,'Exactly 10',['one fragment, one row:','read it directly'],
        [('MAGLKVTSAP',0,[5,0,8,0])],[5,0,8,0],'MAGLKVTSAP',G)
y=panel(1070,'Longer than 10 (e.g. an 11-mer)',['two overlapping fragments:','keep the smaller count per sample'],
        [('MAGLKVTSAP',0,[5,0,8,0]),('AGLKVTSAPQ',0,[3,0,0,6])],[3,0,0,0],'MAGLKVTSAPQ',G)
t(o,1090,y+60,'a read covering the whole 11-mer must',D,14); t(o,1090,y+80,'carry both fragments: an upper bound',D,14)
t(o,1570,590,'Counts illustrative. · = absent, not stored. I/L ambiguity can be summed over on request (isobaric in MS).',D,13,'end')
o.append('</svg>'); open('peptide_query.svg','w').write('\n'.join(o))

# ---------------- posting_lists.svg ----------------
# Search-engine metaphor for posting lists. Words and page numbers illustrative, table numbers
# real: 62.6 B k-mers x 2,486 samples = 155.5 trillion cells, 909.7 B filled (0.58%).
o=head(1600,640)
t(o,30,44,'How a search engine finds pages: it never stores the full word × page grid',I,20,bold=True)
# left: the grid nobody stores
box(o,30,70,560,400)
t(o,50,104,'The grid nobody stores',R,18,bold=True)
words=['antigen','thymus','tolerance','kinase','…']
pages=['p1','p2','p3','p4','p5','p6','…']
hits={(0,1),(0,4),(1,4),(2,2),(2,4),(3,0)}
for j,pg in enumerate(pages): t(o,200+j*52,146,pg,'#8fb0e8',15,'middle')
for i,w in enumerate(words):
    y=184+i*46
    t(o,50,y,w,I,16,mono=True)
    for j in range(len(pages)):
        if w=='…' or pages[j]=='…': t(o,200+j*52,y,'…',D,15,'middle'); continue
        on=(i,j) in hits
        o.append(f'<rect x="{200+j*52-18}" y="{y-20}" width="36" height="30" rx="4" fill="{G if on else "#24302b"}" fill-opacity="{1 if on else 1}"/>')
t(o,50,440,'billions of words × billions of pages, almost all empty',D,15)
# middle: what it stores
box(o,620,70,460,400,stroke=G)
t(o,640,104,'What it stores: one list per word',G,18,bold=True)
for i,(w,l) in enumerate([('antigen','→ p2, p5'),('thymus','→ p5'),('tolerance','→ p3, p5'),('kinase','→ p1')]):
    y=160+i*50; t(o,640,y,w,I,17,mono=True); t(o,800,y,l,G,17,mono=True)
t(o,640,390,'a search for "antigen" reads one short list,',D,15)
t(o,640,412,'never the grid',D,15)
# right: same for fragments
box(o,1110,70,460,400,stroke=K,sw=2)
t(o,1130,104,'NeoKCT: one list per fragment',K,18,bold=True)
for i,(w,l) in enumerate([('MAGLKVTSAP','→ (s1, 5) (s3, 8)'),('','   (s2486, 2)'),('AGLKVTSAPQ','→ (s1, 3) (s4, 6)'),('KTVAEQLSMG','→ (s2, 12) (s3, 7)')]):
    y=160+i*50; t(o,1130,y,w,I,16,mono=True); t(o,1260,y,l,G,16,mono=True)
t(o,1130,390,'fragment → (sample, count) pairs,',D,15)
t(o,1130,412,'only for samples where it was seen',D,15)
box(o,30,495,1540,120,stroke=K,fill='#2a2414')
t(o,50,530,'GTEx: 62.6 billion fragments × 2,486 samples = 155 trillion values. Only 909.7 billion are non-zero: 0.58%.',I,18)
t(o,50,562,'Stored as a grid, that is 622 TB. Stored as lists, the counts are a small fraction of that (next slide).',I,18)
t(o,50,594,'Words, pages and counts above are illustrative. Table sizes are from the GTEx build.',D,13)
o.append('</svg>'); open('posting_lists.svg','w').write('\n'.join(o))

# ---------------- delta_metaphor.svg ----------------
# Finish-line metaphor for delta encoding: a race clock only moves forward, and sorted fragment
# codes only increase, so both can be stored as one full value plus small positive gaps. The
# runner times are chosen so their gaps match the real fragment deltas (+5, +10, +27). K-mer
# codes are the real AAAlphabet encodings (5 bits per residue, first residue in the high bits).
AA='ARNDCQEGHILKMFPSTWYV'
def code(p):
    v=0
    for c in p: v=(v<<5)|AA.index(c)
    return v
o=head(1600,640)
t(o,30,44,'Sorted fragments only ever go up, so store the first one and then the gaps',I,20,bold=True)
# left: the finish line
box(o,30,70,560,420)
t(o,50,104,'Times at a finish line',G,18,bold=True)
t(o,50,134,'runner',D,15,bold=True); t(o,190,134,'clock',D,15,bold=True); t(o,380,134,'written down',D,15,bold=True)
times=['2:31:04','2:31:09','2:31:19','2:31:46']; gaps=['full time','+5 s','+10 s','+27 s']
for i,(tm,g) in enumerate(zip(times,gaps)):
    y=186+i*56
    t(o,50,y,f'#{i+1}',D,17,mono=True); t(o,190,y,tm,I,18,mono=True); t(o,380,y,g,K if i==0 else G,18,mono=True)
t(o,50,436,'The clock never runs backward, so every gap',D,15)
t(o,50,460,'is positive, and short when runners are close.',D,15)
# right: fragments are numbers
kms=['AGLKVTSAPA','AGLKVTSAPQ','AGLKVTSAPS','AGLKVTSASL']
vals=[code(k) for k in kms]
box(o,620,70,950,420,stroke=K,sw=2)
t(o,640,104,'Fragments are numbers too',K,18,bold=True)
t(o,640,134,'Each residue is written as 5 bits (A=0, R=1, N=2 … V=19), so a 10-mer becomes one 50-bit number.',D,15)
t(o,640,156,'Sorting fragments alphabetically is the same as sorting those numbers, and the numbers only go up.',D,15)
t(o,640,194,'fragment',  '#8fb0e8',15,bold=True); t(o,840,194,'as a number','#8fb0e8',15,bold=True); t(o,1180,194,'written down','#8fb0e8',15,bold=True)
for i,(k,v) in enumerate(zip(kms,vals)):
    y=236+i*56
    t(o,640,y,k,I,17,mono=True); t(o,840,y,f'{v:,}',D,16,mono=True)
    t(o,1180,y,'full number' if i==0 else f'+{v-vals[i-1]}',K if i==0 else G,17,mono=True)
t(o,640,460,'A full number takes 8 bytes, a gap fits in 4.',D,15)
box(o,30,512,1540,104,stroke=G,fill='#17281f')
t(o,50,546,'Like a clock time posted at every checkpoint, the full number is written again every 256 fragments,',I,17)
t(o,50,574,'so reaching any fragment takes at most 255 small additions. Halves the storage for 62.6 billion sorted fragments.',I,17)
t(o,50,602,'Fragment numbers and gaps are the real encodings of these four 10-mers, the runner times are made to match.',D,13)
o.append('</svg>'); open('delta_metaphor.svg','w').write('\n'.join(o))

# ---------------- packing_crates.svg ----------------
# Bit packing of counts within one 64-fragment block, from _pack_block! in NeoKCT's
# KCTLayers.jl: cbits is the bit length of the block's largest count. Only the standard case
# is drawn. The all-ones (cbits = 0) and 16-bit-cap-plus-exception-list cases exist but are
# rare or beside the point for this audience. Box widths drawn to scale (3.5 px per bit).
# Trimmed for BIN7006 to one line per row, one line on why the width is per block, and the result. Result bars to scale: 909.7 B entries as plain lists (4-byte sample, 4-byte
# count, 8-byte fragment per row) is 7.78 TB = 7.08 TiB, against the real 2.15 TiB table, so
# gaps + packing together cut 70%. Same numbers as the old 8.5 vs 2.6 bytes per entry.
o=head(1600,450)
PX=3.5; X0=330
counts=[1,3,1,2,6,1,2,1]
def boxes(y,bits,col,labels,fs=15):
    x=X0
    for v,lab in zip(counts,labels):
        w=bits*PX
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="50" rx="3" fill="#24302b" stroke="{col}" stroke-width="1.5"/>')
        if w>=40: t(o,x+w/2,y+31,lab,col,fs,'middle',mono=True)
        else: t(o,x+w/2,y-8,lab,I,fs,'middle',mono=True)  # too narrow to the scale, label goes on top
        x+=w+12
    return x
def row(y,title,sub,col):
    t(o,30,y+22,title,col,18,bold=True); t(o,30,y+46,sub,D,15)
y=40; row(y,'As plain numbers','32 bits, room for 4.3 billion',R)
boxes(y,32,R,[f'{c:010d}' for c in counts],14)
y=150; row(y,'Packed','3 bits, enough for this block',G)
xe=boxes(y,3,G,[str(c) for c in counts],15)
t(o,xe+12,y+32,'largest count is 6 = 110 in binary',G,17)
t(o,30,250,'Each block of 64 fragments picks the width of its largest count. One width per block keeps every count findable at position × width.',D,16)
# result: the whole GTEx table, plain lists vs gaps + packing, bars to scale
plain=7.08; real=2.15; BW=1000/plain
y=290; t(o,30,y+22,'GTEx, as plain lists',R,17,bold=True)
o.append(f'<rect x="{X0}" y="{y}" width="{plain*BW:.0f}" height="36" rx="4" fill="#2e201b" stroke="{R}" stroke-width="1.5"/>')
t(o,X0+plain*BW+14,y+25,f'{plain} TiB',R,18)
y=346; t(o,30,y+16,'with gaps + packing',G,17,bold=True)
o.append(f'<rect x="{X0}" y="{y}" width="{real*BW:.0f}" height="36" rx="4" fill="#17281f" stroke="{G}" stroke-width="1.5"/>')
t(o,X0+real*BW+14,y+25,f'{real} TiB',G,18)
t(o,X0+real*BW+150,y+28,f'{round(100*(1-real/plain))}% smaller',G,34,bold=True)
t(o,30,425,'Box widths drawn to scale. Counts illustrative, 8 of a block\'s 64 shown.',D,13)
o.append('</svg>'); open('packing_crates.svg','w').write('\n'.join(o))

# ---------------- tcell_questions.svg ----------------
# Callback to tsa_therapy for the Questions slide: same CD8 T cell, off duty with a coffee and a
# question mark where the kill arrow used to be. No background card so it sits on the slide
# itself, cropped tight because it's placed small in the top-right corner.
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="140 30 300 265" width="300" height="265" {F}>']
cx,cy=310,215
mascot(o,cx,cy)
t(o,cx+88,cy+10,'\u2615',I,40,'middle')
o.append(f'<path d="M170,40 h110 a14,14 0 0 1 14,14 v46 a14,14 0 0 1 -14,14 h-30 l24,30 l-56,-30 h-48 a14,14 0 0 1 -14,-14 v-46 a14,14 0 0 1 14,-14 z" fill="{PAN}" stroke="{D}" stroke-width="2"/>')
t(o,225,98,'?',K,52,'middle',bold=True)
o.append('</svg>'); open('tcell_questions.svg','w').write('\n'.join(o))

# ---------------- mascot_*.svg ----------------
# Standalone mascots for slide corners, transparent, one per slide mood. Same 240 x 220 canvas for
# all of them with the cell at (120,130), so the cell is the same size on every slide when placed
# at width 250 with {.absolute} in presentation.qmd. Props are emoji glyphs held at the side
# (there's no tape-measure emoji, the ruler stands in for it).
def bubble(o,x,y,w,h,tx,ty,s,col=K,fs=34):
    # rounded speech bubble with its tail pointing to (tx,ty)
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PAN}" stroke="{D}" stroke-width="2"/>')
    o.append(f'<path d="M{x+w*0.55:.0f},{y+h-1} L{tx},{ty} L{x+w*0.8:.0f},{y+h-1}" fill="{PAN}" stroke="{D}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(f'<path d="M{x+w*0.55+2:.0f},{y+h-1} L{x+w*0.8-2:.0f},{y+h-1}" stroke="{PAN}" stroke-width="3"/>')
    t(o,x+w/2,y+h/2+fs*0.36,s,col,fs,'middle',bold=True)
def prop(o,x,y,glyph,fs=46,rot=0):
    o.append(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="middle" transform="rotate({rot} {x} {y-fs*0.35:.0f})">{glyph}</text>')
MASCOTS={
    'worried':   dict(look=(-1,-1),mood='worried',sweat=True),
    'surprised': dict(look=(-1,-0.6),mood='surprised'),
    'perplexed': dict(look=(-1,-1),mood='perplexed'),
    'satisfied': dict(look=(-1,-1),mood='satisfied'),
    'stopwatch': dict(look=(-0.4,-1),mood='neutral'),
    'telescope': dict(look=(-1,-1),mood='squint'),
}
for name,kw in MASCOTS.items():
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 220" width="240" height="220" {F}>']
    mascot(o,120,130,**kw)
    if name=='surprised': bubble(o,14,8,52,46,60,78,'!')
    if name=='perplexed': prop(o,196,196,'\U0001F4CF',44,-20)
    if name=='stopwatch': prop(o,200,200,'\u23F1\uFE0F',42)
    if name=='telescope': prop(o,76,136,'\U0001F52D',46)  # eyepiece (lower right of the glyph) at the open left eye
    o.append('</svg>'); open(f'mascot_{name}.svg','w').write('\n'.join(o))

# ---------------- mascot_computer.svg ----------------
# Slide 10 (BamQuery): the mascot stuck waiting on a smoking laptop, angry brows, a scribbled storm
# cloud over its head. The cloud is black ink as asked, drawn over a slightly wider grey copy of
# the same path, or it vanishes on the near-black slide. Wider canvas (300 x 250) for the laptop
# and the smoke, cell still at r=60 so it matches the other mascots at width 312.
import random
def scribble(o,cx,cy,rx,ry,seed=7):
    # a pen going round and round an ellipse with fast wobbles on top, plus a little jitter, reads
    # as an angry scribbled cloud instead of a blob
    rnd=random.Random(seed); pts=[]
    N=420
    for i in range(N):
        u=i/(N-1)*14*math.pi
        f=0.25+0.75*(0.5+0.5*math.cos(u/3.3))  # spiral in and out so the inside fills up
        pts.append((cx+f*rx*math.cos(u)+8*math.cos(4.7*u)+rnd.uniform(-2,2),
                    cy+f*ry*math.sin(u)+6*math.sin(3.9*u)+rnd.uniform(-2,2)))
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f} '+' '.join(f'L{x:.1f},{y:.1f}' for x,y in pts[1:])
    o.append(f'<path d="{d}" stroke="#6a6a6a" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="{d}" stroke="#000" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 250" width="300" height="250" {F}>']
scribble(o,112,40,62,22)
mascot(o,112,164,look=(1,0.7),mood='angry')
prop(o,242,244,'\U0001F4BB',58)
# smoke rising off the laptop lid
for i,x0 in enumerate((226,244,262)):
    o.append(f'<path d="M{x0},{196-i*4} q-7,-11 0,-20 q7,-9 0,-19 q-7,-9 0,-18" stroke="#9a9a9a" stroke-width="{4-i*0.6:.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
o.append('</svg>'); open('mascot_computer.svg','w').write('\n'.join(o))

# ---------------- mascot_books.svg ----------------
# Slide 7 (why it has to fit in memory): the mascot hauling a wobbly pile of books up from the
# basement, strained brows and a sweat drop. Taller canvas (240 x 320), cell at (120,250) so the
# body matches the other mascots at width 250.
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 320" width="240" height="320" {F}>']
mascot(o,120,250,look=(0,-1),mood='worried',sweat=True)
# pile, bottom to top, each book a little off-axis so it reads as unstable
# pile, bottom to top: the stacked-books glyph, then single books turned on their side so they lie
# flat, each a little off-axis so it reads as unstable
prop(o,120,190,'\U0001F4DA',62,-4)
for x,y,g,rot in ((112,150,'\U0001F4D5',84),(128,118,'\U0001F4D8',97),(114,86,'\U0001F4D7',80),(126,54,'\U0001F4D9',101)):
    prop(o,x,y,g,48,rot)
# wobble marks either side of the top of the pile
for sx in (-1,1):
    o.append(f'<path d="M{120+sx*56},30 q{sx*8},10 0,20 M{120+sx*64},24 q{sx*9},14 0,30" stroke="{D}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
o.append('</svg>'); open('mascot_books.svg','w').write('\n'.join(o))

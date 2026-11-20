# Hand-built conceptual figures for the IRIC talk: tsa_therapy, tsa_sources, two_workflows, peptide_query,
# posting_lists, delta_metaphor, packing_crates.
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
def tcell(o,cx,cy,stroke):
    o.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="{PAN}" stroke="{stroke}" stroke-width="2.5"/>')
    o.append(f'<path d="M{cx-62},{cy} L{cx-84},{cy} M{cx-84},{cy-14} L{cx-84},{cy+14}" stroke="{stroke}" stroke-width="5" fill="none"/>')
    t(o,cx,cy+6,'CD8 T cell',I,16,'middle',bold=True)
o=head(1090,500)
for x0,title,cellcol,fill,pep,tc,res,rescol in ((30,'Tumor cell','#e58468','#2a1d19',R,G,['TSA on MHC-I is recognized,','the tumor cell is killed'],G),
                                                (560,'Healthy cell',D,'#1a2420',D,BR,['only self peptides, nothing','to recognize, tissue is spared'],D)):
    box(o,x0,30,500,440)
    cx=x0+140
    o.append(f'<circle cx="{cx}" cy="230" r="105" fill="{fill}" stroke="{cellcol}" stroke-width="2.5"/>')
    t(o,cx,236,title,cellcol,19,'middle',bold=True)
    mhc(o,cx+105,230,pep)
    tcell(o,x0+400,230,tc if tc!=BR else D)
    if pep==R:
        t(o,cx+138,200,'TSA',R,15,'middle',bold=True)
        o.append(f'<path d="M{x0+300},175 Q{x0+250},150 {cx+70},160" stroke="{G}" stroke-width="2.5" fill="none" stroke-dasharray="6 5" marker-end="url(#ag)"/>')
        t(o,x0+300,150,'kill',G,15,'middle',bold=True)
    else:
        t(o,cx+138,200,'self',D,15,'middle')
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
o=head(1600,602)
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
DY=-198  # bottom lane moves up into the space the old bar chart used
box(o,30,186,1540,70,stroke=R,fill='#2e201b')
prod=' × '.join(str(DEG[c]) for c in pep)
t(o,50,215,f'{pep}: {prod} = {tot:,} possible coding sequences.',I,17,bold=True)
t(o,50,241,f'At 3.6 codons per residue on average, a 9-mer has about 100,000 and an 11-mer about 1.3 million.',D,15)
box(o,30,268,1540,44,stroke=R,fill='#2e201b')
t(o,50,296,'Too many to search in raw reads, so the genome filters them first: peptides it can\'t place are never counted (199 of 550 in our test), and every new list costs ~730 CPU-hours.',I,16)
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
box(o,30,716,1540,66,stroke=G,fill='#17281f')
t(o,50,744,'Translation has hundreds of thousands of answers going backward, and exactly one going forward. Translating the reads instead of the peptides',I,16)
t(o,50,768,'removes the explosion, and the genome filter with it: fusions, ERVs and unannotated junctions are queried exactly like canonical peptides.',I,16)
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
y=panel(30,'Shorter than 10 (e.g. a 9-mer)',['every fragment that starts with it,','neighbors in the sorted table: add them up'],
        [('AGLKVTSAPA',9,[3,0,1,0]),('AGLKVTSAPQ',9,[3,0,0,6]),('AGLKVTSAPS',9,[0,2,0,1])],[6,2,1,7],'AGLKVTSAP',G)
t(o,50,y+60,'each read window that starts with the',D,14); t(o,50,y+80,'peptide counts once, whatever follows',D,14)
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
o=head(1600,600)
PX=3.5; X0=330
t(o,30,44,'Drop the leading zeros: each block of 64 fragments uses the width of its largest count',I,20,bold=True)
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
y=90; row(y,'As plain numbers','room for 4.3 billion, every time',R)
xe=boxes(y,32,R,[f'{c:010d}' for c in counts],14); t(o,xe+12,y+31,'32 bits each',R,16)
y=200; row(y,'Packed','largest count here is 6',G)
xe=boxes(y,3,G,[str(c) for c in counts],15)
t(o,xe+12,y+31,'3 bits each, because 6 is 110 in binary',G,16)
t(o,X0,y+84,'in bits:  '+' '.join(format(c,'03b') for c in counts),D,16,mono=True)
box(o,30,320,1540,170,stroke=BR)
t(o,50,354,'Why one width per block instead of one per count',I,18,bold=True)
t(o,50,386,'With every count the same width, the 30th one sits exactly 30 × 3 bits in, so it can be read without decoding the 29 before it.',I,16)
t(o,50,414,'The next block picks its own width: a block holding a count of 900 uses 10 bits, one holding only small counts uses 2.',I,16)
t(o,50,442,'Sample numbers are packed the same way, written as gaps between samples, which stay small because samples are ordered by tissue.',I,16)
t(o,50,470,'Box widths drawn to scale. Counts illustrative, 8 of the block\'s 64 shown.',D,13)
box(o,30,512,1540,60,stroke=G,fill='#17281f')
t(o,50,549,'Result on GTEx: about 2.6 bytes per (sample, count) entry, the fragment itself included. Plain lists would need about 8.5.',I,17)
o.append('</svg>'); open('packing_crates.svg','w').write('\n'.join(o))

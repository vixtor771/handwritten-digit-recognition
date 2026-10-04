import numpy as np, gzip, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent      # skill demonstration 文件夹
DATA, RESULTS, FIGS = BASE / 'Data' / 'MNIST', BASE / 'Results', BASE / 'Figures'
BLUE='#2a78d6'; INK2='#52514e'
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.titleweight':'bold'})
with gzip.open(DATA / 'train-images-idx3-ubyte.gz') as f: X=np.frombuffer(f.read(),np.uint8,offset=16).reshape(-1,28,28)/255
with gzip.open(DATA / 'train-labels-idx1-ubyte.gz') as f: Y=np.frombuffer(f.read(),np.uint8,offset=8)
k=0; img=X[k]; lab=Y[k]
fig,ax=plt.subplots(1,4,figsize=(16,4.3),gridspec_kw={'width_ratios':[1,1,1.4,1.1],'wspace':0.35})
ax[0].imshow(img,cmap='gray_r'); ax[0].set_title(f'1. One training image\n(label = {lab})',loc='left')
r0,c0=8,10; ax[0].add_patch(Rectangle((c0-0.5,r0-0.5),6,6,fill=False,ec='#eb6834',lw=2)); ax[0].set_xticks([]); ax[0].set_yticks([])
patch=img[r0:r0+6,c0:c0+6]
ax[1].imshow(patch,cmap='gray_r',vmin=0,vmax=1)
for i in range(6):
    for j in range(6): ax[1].text(j,i,f'{patch[i,j]:.1f}',ha='center',va='center',fontsize=8,color='white' if patch[i,j]>0.5 else INK2)
ax[1].set_title('2. Zoom in: each pixel\nis a number from 0 to 1',loc='left'); ax[1].set_xticks([]); ax[1].set_yticks([])
for s in ax[1].spines.values(): s.set_color('#eb6834'); s.set_linewidth(2)
flat=img.reshape(-1)
ax[2].bar(np.arange(784),flat,width=1,color=BLUE); ax[2].set_xlim(0,784)
ax[2].set_xlabel('pixel index (row by row)'); ax[2].set_ylabel('value')
ax[2].set_title('3. Unrolled into 784 numbers\n= the input s0',loc='left'); ax[2].spines[['top','right']].set_visible(False)
t=np.zeros(10); t[lab]=1
ax[3].bar(np.arange(10),t,color=[BLUE if i==lab else '#d9d8d3' for i in range(10)],width=0.7)
ax[3].set_xticks(range(10)); ax[3].set_xlabel('output neuron (digit)'); ax[3].set_ylim(0,1.15)
ax[3].set_title(f'4. Target: 10 numbers,\na 1 at position {lab}',loc='left'); ax[3].spines[['top','right']].set_visible(False)
for ext in ('png','pdf'): fig.savefig(FIGS / f'fig1_what_the_network_sees.{ext}',dpi=300,bbox_inches='tight')

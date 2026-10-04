import numpy as np, gzip, matplotlib.pyplot as plt
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent      # skill demonstration 文件夹
DATA, RESULTS, FIGS = BASE / 'Data' / 'MNIST', BASE / 'Results', BASE / 'Figures'
BLUE,ORANGE,AQUA,GRAY,INK2='#2a78d6','#eb6834','#1baf7a','#9b9a95','#52514e'
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False})
sig=lambda z:1/(1+np.exp(-z))
with gzip.open(DATA / 't10k-images-idx3-ubyte.gz') as f: Xt=np.frombuffer(f.read(),np.uint8,offset=16).reshape(-1,784)/255
with gzip.open(DATA / 't10k-labels-idx1-ubyte.gz') as f: Yt=np.frombuffer(f.read(),np.uint8,offset=8)
R={m:np.load(RESULTS / f'result_{m}.npz') for m in ('bp','fa','shallow')}
name={'bp':'backprop','fa':'feedback alignment','shallow':'last layer only'}
col={'bp':BLUE,'fa':ORANGE,'shallow':GRAY}

# Figure 3: error curves + angle
fig,ax=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={'wspace':0.28})
for m in ('shallow','bp','fa'):
    e=100*R[m]['err']; ep=np.arange(len(e))
    ax[0].plot(ep[1:],e[1:],'o-',ms=4,lw=2,color=col[m],label=f'{name[m]}  (final {e[-1]:.2f}%)')
ax[0].set_yscale('log'); ax[0].set_yticks([1,2,3,5,10,20]); ax[0].set_yticklabels(['1','2','3','5','10','20'])
ax[0].set_xlabel('epoch (1 epoch = all 60,000 training images once)'); ax[0].set_ylabel('test error (%)  on 10,000 unseen images')
ax[0].set_xticks([1,5,10,15,20]); ax[0].set_title('Test error during training',loc='left'); ax[0].legend(frameon=False); ax[0].grid(axis='y',color='#eeeeee')
a=R['fa']['ang']
ax[1].plot(a[:,0]/60000,a[:,1],'o-',ms=3,lw=2,color=ORANGE)
ax[1].axhline(90,color=INK2,ls=':',lw=1); ax[1].text(ax[1].get_xlim()[1]*0.98,91.5,'90° = unrelated directions',ha='right',fontsize=9,color=INK2)
ax[1].set_ylim(0,100); ax[1].set_xticks([0,5,10,15,20]); ax[1].set_xlabel('epoch'); ax[1].set_ylabel('angle (degrees)')
ax[1].set_title('Angle between FA error signal and backprop error signal',loc='left')
for ext in ('png','pdf'): fig.savefig(FIGS / f'fig3_error_and_angle.{ext}',dpi=300,bbox_inches='tight')

# Figure 3a: test error only (for slides)
fig,ax=plt.subplots(figsize=(7,4.6))
for m in ('shallow','bp','fa'):
    e=100*R[m]['err']; ep=np.arange(len(e))
    ax.plot(ep[1:],e[1:],'o-',ms=4,lw=2,color=col[m],label=f'{name[m]}  (final {e[-1]:.2f}%)')
ax.set_yscale('log'); ax.set_yticks([1,2,3,5,10,20]); ax.set_yticklabels(['1','2','3','5','10','20'])
ax.set_xlabel('epoch (1 epoch = all 60,000 training images once)'); ax.set_ylabel('test error (%)  on 10,000 unseen images')
ax.set_xticks([1,5,10,15,20]); ax.set_title('Test error during training',loc='left'); ax.legend(frameon=False); ax.grid(axis='y',color='#eeeeee')
for ext in ('png','pdf'): fig.savefig(FIGS / f'fig3a_test_error.{ext}',dpi=300,bbox_inches='tight')

# Figure 4: example predictions
fig,axs=plt.subplots(2,8,figsize=(13,3.1),gridspec_kw={'height_ratios':[3,1],'hspace':0.05})
pred={m:sig(R[m]['W1']@sig(R[m]['W0']@Xt.T)).argmax(0) for m in ('bp','fa')}
wrong=np.where(pred['fa']!=Yt)[0][:3]; right=np.arange(13)[:13][:5]
idx=list(right)+list(wrong)
for c,i in enumerate(idx):
    axs[0,c].imshow(Xt[i].reshape(28,28),cmap='gray_r'); axs[0,c].set_xticks([]); axs[0,c].set_yticks([])
    axs[0,c].set_title(f'true {Yt[i]}',fontsize=10)
    for s in axs[0,c].spines.values(): s.set_visible(True); s.set_color('#d9d8d3')
    axs[1,c].axis('off')
    for r,(m,lab) in enumerate([('bp','BP'),('fa','FA')]):
        ok=pred[m][i]==Yt[i]
        axs[1,c].text(0.5,0.75-0.55*r,f"{lab}: {pred[m][i]}"+('' if ok else '  ✗'),ha='center',va='center',fontsize=12,
            color='#0b0b0b' if ok else '#e34948',fontweight='normal' if ok else 'bold',transform=axs[1,c].transAxes)
fig.suptitle('Network guesses on test images (last 3 = images feedback alignment got wrong; ✗ = wrong)',x=0.12,ha='left',fontweight='bold',fontsize=11)
for ext in ('png','pdf'): fig.savefig(FIGS / f'fig4_example_guesses.{ext}',dpi=300,bbox_inches='tight')
print({m:round(100*R[m]['err'][-1],2) for m in R}, 'angle start %.1f end %.1f'%(a[0,1],a[-1,1]))

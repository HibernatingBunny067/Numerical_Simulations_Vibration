import warnings
warnings.filterwarnings('ignore')
from core import rk45
from model import Parameters,resolver_nd,system,univIndex
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter

IN = perf_counter()

base = Parameters()
index = univIndex().idx
sampled_params = base.sample(mode='paper')

params_array,tau_total = resolver_nd(base,sampled_params)

t_span = [0,tau_total] ## non dimensional time
t_eval = np.linspace(0,t_span[-1],2000)
y0 = [0.01,0,0,0]


solution = rk45(
    system,
    y0,
    t_span,
    t_eval=t_eval,
    sys_params=params_array,
    rtol=1e-7
)

print(solution)

t = solution.t
x = solution.y[:,0]
y = solution.y[:,1]
xdot = solution.y[:,2]
ydot = solution.y[:,-1]
r = np.sqrt(x**2 + y**2)
contact = r > 1.0
theta = np.linspace(0,2*np.pi,1000)
xc = np.cos(theta)
yc = np.sin(theta)

contact_ration = np.mean(r > 1)
mean_r = np.mean(r)
print(contact_ration)

fig,ax = plt.subplots(1,2)
fig.suptitle(f"""F_shaft: {sampled_params.get('f_shaft'):.3f}, E_bar: {params_array[index["E_BAR"]]:.3f}, OMEGA_BAR: {params_array[index['OMEGA_BAR']]:.3f}, KC_BAR: {params_array[index['KC_BAR']]:.3f}, MU: {params_array[index["MU"]]}, R_DISK_BAR: {params_array[index["R_DISK_BAR"]]:.3f}, Contact_Ratio: {contact_ration:.3f}, Mean_orbit:{mean_r:.3f}""")
ax[0].plot(t,r,linestyle = "--",color='black')
ax[0].grid()
ax[0].set_title('q v/s t')

ax[1].plot(x,y,color='red')
ax[1].grid()
ax[1].set_title('Phase Portrait')
ax[1].set_xlabel('x')
ax[1].set_ylabel('y')
ax[1].plot(xc,yc,color='black',linestyle='--',label='clearance circle')
ax[1].scatter(x[contact],y[contact],color='blue',s=5)
ax[1].legend()
ax[1].axis('equal')

OUT = perf_counter()
print(F"Exit in {OUT-IN} seconds")

plt.show()
# <div align = "center"> Decoupled 2-DOF Jefcott Rotor based Rubbing informed System Formulation </div> 

- from #14 Jie HONG et al. the equation of motion for complete geometrical constraint rubbing system can be written as: <br>

$m\ddot{q} + c\dot{q} + kq = me\omega^2e^{i \omega t} \text{ ; } |q| ≤ r_0$ <br>
$m\ddot{q} + c\dot{q} + kq + (kc(1+i\text{sign}(v_{rel})\mu)(1-\frac{r_0}{|q|}))q = me\omega^2e^{i \omega t} \text{  ;  } |q| > r_0$ <br>
$\text{where q = x + iy}$<br>

- where the rubbing is modelled as a sign dependent frictionional force having force dependence on rubbing penetration.
- Forcing has been modelled as a Jefcott system for ease of simulation
---

- We decoupled the equation by decomposing the complex notation to cartesion coordinates resulting in the aformentioned equations: 

$m\ddot{x}+c\dot{x}+kx+S(x - \mu \text{sign}(V_{rel})y) = me\omega^2\cos(\omega t)$<br>
$m\ddot{y}+c\dot{y}+ky+S(y + \mu \text{sign}(V_{rel})x) = me\omega^2\sin(\omega t)$ <br> 
$\text{where }S=\begin{bmatrix} 0\text{ , }  |\sqrt{x^2+y^2}| < r_0 \\ 
k_c(1-\frac{r_0}{\sqrt{x^2+y^2}}) \text{ , }|\sqrt{x^2+y^2}| > r_0 \end{bmatrix}$

- following this we used transforms (mentioned in #14 Jie HONG et al.) to further convert this eqaution to a non-dimensional form 
- we assumed $X = \frac{x}{r_0}, \, Y = \frac{y}{r_0},\, \tau = \omega_nt ,\, \bar{k_c} = \frac{k_c}{k},\,V_{rel} = \frac{v_{rel}}{\omega_n r_0},\, \bar{\Omega} = \frac{\Omega}{\omega_n},\,\bar{\omega} = \frac{\omega}{\omega_n},\,{R_{disk}} = \frac{r_disk}{r_0}$.
- The transformed non-dimensional equation assumes the following form: 

$X''(\tau) + 2\zeta X'(\tau) + X(\tau)+\bar{k_c}(1-\frac{1}{\sqrt{X^2 + Y^2}})(X-\mu \text{sign}(V_{rel})Y) = \bar{e} \Omega^2 \cos(\Omega \tau)$<br>

$Y''(\tau) + 2\zeta Y'(\tau) + Y(\tau)+\bar{k_c}(1-\frac{1}{\sqrt{X^2 + Y^2}})(Y+\mu \text{sign}(V_{rel})X) = \bar{e} \Omega^2 \sin(\Omega \tau)$
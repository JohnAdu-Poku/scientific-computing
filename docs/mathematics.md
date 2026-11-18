# Mathematics behind the computation

## 1. From a differential equation to a time-stepping rule

For $y'=f(t,y)$, Taylor expansion around $t_n$ gives

$$y(t_n+h)=y(t_n)+h f(t_n,y(t_n))+O(h^2).$$

Dropping the remainder and replacing the unknown exact value by $y_n$ gives forward Euler:

$$y_{n+1}=y_n+h f(t_n,y_n).$$

Its one-step error is $O(h^2)$ when started from the exact value. Under the usual smoothness and Lipschitz assumptions on a fixed interval, the accumulated global error is $O(h)$.

## 2. Classical fourth-order Runge–Kutta

Sample the slope at four positions:

$$k_1=f(t_n,y_n),$$
$$k_2=f(t_n+h/2,y_n+hk_1/2),$$
$$k_3=f(t_n+h/2,y_n+hk_2/2),$$
$$k_4=f(t_n+h,y_n+hk_3),$$
$$y_{n+1}=y_n+\frac{h}{6}(k_1+2k_2+2k_3+k_4).$$

For sufficiently smooth problems the one-step error is $O(h^5)$ and global error is $O(h^4)$. RK4 uses four right-hand-side evaluations per step; Euler uses one. Comparing at equal step sizes is not the same as comparing at equal computational cost.

## 3. An exact benchmark

For $y'=-y$, separation gives $\ln y=-t+C$ for the positive solution; $y(0)=1$ yields $y(t)=e^{-t}$. The exact solution is positive and tends to zero. It provides a reference independent of either implementation.

Euler becomes $y_{n+1}=(1-h)y_n$, hence $y_n=(1-h)^n$. RK4 gives $y_{n+1}=R(-h)y_n$, where

$$R(z)=1+z+z^2/2+z^3/6+z^4/24.$$

These amplification formulas provide independent implementation checks.

## 4. Error and observed order

At grid points $t_n=nh$, measure

$$E(h)=\max_n |y_n-e^{-t_n}|.$$

This is a maximum over the sampled nodes, not a continuous-time supremum. If $E(h)\approx Ch^p$, then

$$p_{\mathrm{obs}}=\log_2\!\left(\frac{E(h)}{E(h/2)}\right)\approx p.$$

We use $N=10,20,40,80,160$ steps with $h=2/N$. The first row has no order because there is no coarser comparison. A convergence experiment supports expected behavior on this problem; it does not prove convergence for every ODE.

## 5. Stability and positivity are different

For $y'=-a y$ with $a>0$, Euler's amplification factor is $1-ah$. Decay in magnitude requires $|1-ah|<1$, equivalently $0<ah<2$. Nonnegative iterates from a nonnegative initial value require $0\le ah\le1$. Thus a stable discretization can still oscillate in sign. All default steps satisfy both conditions for $a=1$.

RK4 requires $|R(-ah)|<1$ for decay on this test equation. Higher order does not remove restrictions on explicit methods. Neither implementation is intended as a general stiff ODE solver.

## Exercises

1. Change $a$ to 2 in the right-hand side and use $e^{-2t}$ as the exact solution everywhere.
2. Test Euler with $ah=0.5$, $1.5$, and $2.5$. Explain positivity, oscillation, and growth.
3. Compare Euler with $4N$ steps against RK4 with $N$ steps to approximate an equal evaluation budget.
4. Try $y'=2t$, $y(0)=0$ and compare against $t^2$.
5. Explain why reducing $h$ indefinitely eventually encounters floating-point limitations.

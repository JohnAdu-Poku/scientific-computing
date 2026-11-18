function [t, y] = solve_ivp_fixed(rhs, y0, t0, t_end, n_steps, method)
%SOLVE_IVP_FIXED Scalar Euler or classical RK4 on a uniform time grid.
validateattributes(n_steps, {'numeric'}, {'scalar','integer','positive','finite'});
validateattributes(y0, {'numeric'}, {'scalar','real','finite'});
validateattributes(t0, {'numeric'}, {'scalar','real','finite'});
validateattributes(t_end, {'numeric'}, {'scalar','real','finite','>',t0});
if ~any(strcmp(method, {'euler','rk4'}))
    error('method must be euler or rk4');
end
t = linspace(t0, t_end, n_steps + 1)';
h = (t_end - t0) / n_steps;
y = zeros(n_steps + 1, 1); y(1) = y0;
for j = 1:n_steps
    k1 = rhs(t(j), y(j));
    if strcmp(method, 'euler')
        y(j+1) = y(j) + h*k1;
    else
        k2 = rhs(t(j)+h/2, y(j)+h*k1/2);
        k3 = rhs(t(j)+h/2, y(j)+h*k2/2);
        k4 = rhs(t(j)+h, y(j)+h*k3);
        y(j+1) = y(j) + h*(k1+2*k2+2*k3+k4)/6;
    end
end
end

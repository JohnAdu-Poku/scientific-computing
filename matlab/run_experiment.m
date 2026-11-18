% Run from any working directory. Uses only base MATLAB.
project = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(project, 'matlab'));
out = fullfile(project, 'results');
if ~exist(out, 'dir'), mkdir(out); end
methods = {'euler','rk4'}; steps = [10 20 40 80 160];
fid = fopen(fullfile(out,'matlab_convergence.csv'),'w');
assert(fid >= 0, 'Cannot open result file');
fprintf(fid,'method,n_steps,h,max_error,observed_order\n');
errors = zeros(2,5);
for m = 1:2
    for k = 1:5
        n = steps(k);
        [t,y] = solve_ivp_fixed(@(t,y) -y,1,0,2,n,methods{m});
        errors(m,k) = max(abs(y-exp(-t)));
        if k == 1
            fprintf(fid,'%s,%d,%.17g,%.17g,\n',methods{m},n,2/n,errors(m,k));
        else
            order = log2(errors(m,k-1)/errors(m,k));
            fprintf(fid,'%s,%d,%.17g,%.17g,%.17g\n',methods{m},n,2/n,errors(m,k),order);
        end
    end
end
fclose(fid);
[t,ye] = solve_ivp_fixed(@(t,y) -y,1,0,2,20,'euler');
[~,yr] = solve_ivp_fixed(@(t,y) -y,1,0,2,20,'rk4');
writetable(table(t,exp(-t),ye,yr,'VariableNames',{'t','exact','euler','rk4'}),fullfile(out,'matlab_trajectory.csv'));
f = figure('Color','w');
plot(t,exp(-t),'k-',t,ye,'o--',t,yr,'s:');
xlabel('Time t'); ylabel('y(t)'); title('Exponential decay; h = 0.1');
legend('Exact','Euler','RK4'); grid off; set(gca,'Color','w');
print(f,fullfile(out,'matlab_solution.svg'),'-dsvg');
f = figure('Color','w');
loglog(2./steps,errors(1,:),'o-',2./steps,errors(2,:),'s--');
xlabel('Step size h'); ylabel('Maximum nodal absolute error');
legend('Euler','RK4'); grid off; set(gca,'Color','w');
print(f,fullfile(out,'matlab_convergence.svg'),'-dsvg');
% Analytic error and convergence checks, independent of the Python output.
assert(max(abs(ye - (1-0.1).^(0:20)')) < 1e-12);
assert(abs(log2(errors(1,4)/errors(1,5))-1) < 0.1);
assert(abs(log2(errors(2,4)/errors(2,5))-4) < 0.1);
disp('MATLAB checks passed. Results saved in results/.');

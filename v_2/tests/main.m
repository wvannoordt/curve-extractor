clear
clc
close all

generate_graphs = 0;
run_comparison = 1;

if generate_graphs
   t = linspace(-3, 3, 1500);
   plot(t, f_1(t))
   saveas(gcf, 't1_profile.png')
   figure
   plot(t, f_2(t))
   saveas(gcf, 't2_profile.png')
   figure
   plot(t, f_3(t))
   saveas(gcf, 't3_profile.png')
end

if run_comparison
    listing = dir('./*.csv');
    for i = 1:length(listing)
       figure
       curfilename =  listing(i).name;
       fstring = ['f_', num2str(i)];
       f = str2func(fstring);
       data = csvread(curfilename);
       t_cur = data(:, 1);
       x_cur_prof = data(:,2);
       x_cur_real = f(t_cur);
       subplot(2, 1, 1)
       plot(t_cur, x_cur_prof)
       hold on
       plot(t_cur, x_cur_real)
       ylabel(['Profile (' fstring ')'])
       legend('extracted', 'real')
       subplot(2, 1, 2)
       plot(t_cur, (x_cur_prof - x_cur_real) / max(1e-50+abs(x_cur_real)))
       ylabel('Relative error')
    end
end
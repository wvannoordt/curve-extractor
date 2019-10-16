function [xout] = f_1(t)
    xout = 3*sin(2*t) + 0.1*t.^2 + 4 * t - exp(0.3*t);
end
function [xout] = f_2(t)
    xout = 3*cos(2*t) - 0.2*t.^3 + log(1 + t.^2);
end
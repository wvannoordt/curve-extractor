function [xout] = f_3(t)
    xout = (1./(1+t.^2)) + atan(3*t);
end
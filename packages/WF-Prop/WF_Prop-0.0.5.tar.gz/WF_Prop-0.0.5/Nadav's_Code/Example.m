n = 1024;
x = linspace(-10,10,n)*1e-9;
dx = x(2)-x(1);

k = -1/(2*dx):1/(n*dx):1/(2*dx);
k = 2*pi*ifftshift(k(2:end));

m = 9.1e-31;
hbar = 6.626e-34 / (2*pi);
w = 5e15;
V = 1/2*m*w^2*x.^2;
x0 = 1e-9;
wavefun = exp(-w*m*(x-x0).^2 / (2*hbar));
wavefun = wavefun / sqrt(wavefun*wavefun'*dx);
timestep = 0.1/w;
figure;
% k = 0;
for i = 1:3000
   tempwavefun = exp(-1i*timestep*V/(2*hbar)).*wavefun;
   tempwavefun = fft(tempwavefun);
   tempwavefun = exp(-1i*timestep*hbar*k.^2 / (2*m)).*tempwavefun;
   tempwavefun = ifft(tempwavefun);
   wavefun = exp(-1i*timestep*V/(2*hbar)).*tempwavefun;
   plot(x,abs(wavefun).^2/max(abs(wavefun).^2),x,V/max(V));
   ylim([0, 4])
   getframe;
end
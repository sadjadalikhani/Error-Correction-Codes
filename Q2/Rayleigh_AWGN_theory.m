
M = 2;  % Modulation order  
Ebno = 8:2:20;    %SNR range to simulate
berRayleigh_1 = berfading(Ebno,'psk',M,1);
berRayleigh_10 = berfading(Ebno,'psk',M,10);
berRayleigh_20 = berfading(Ebno,'psk',M,20);
berAWGN = berawgn(Ebno,'psk',M,'nondiff');
semilogy(Ebno,berRayleigh_1,'r',Ebno,berRayleigh_10,'g',Ebno,berRayleigh_20,'b',Ebno,berAWGN,'c-') %blue:RS(31,27)  %red:RS(31,15)   %green:uncoded
ylabel('BER')
xlabel('Eb/No(dB)')
legend('Rayleigh(diversity=1) Theory','Rayleigh(diversity=10) Theory','Rayleigh(diversity=20) Theory','AWGN Theory')
grid
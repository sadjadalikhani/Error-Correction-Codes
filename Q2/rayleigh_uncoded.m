EbNo = 8:2:20;   %SNR range
ber = zeros(length(EbNo),20);
for L = 1:20 
    ber(:,L) = berfading(EbNo,'psk',2,L);    %computing theorical rayleigh channel BER with BPSK modulation for different diversity orders
end
semilogy(EbNo,ber,'r')
text(18.5, 0.02, sprintf('L=%d',1))
text(18.5, 1e-11, sprintf('L=%d',20))
title('Uncoded BPSK over fading channel with diversity order 1 to 20')
xlabel('E_b/N_0(dB)')
ylabel('BER')
grid on
ebnoVec = (-5:1:8)';  %SNR range
ber = berawgn(ebnoVec,'psk',2,'nodiff');  %BER for BPSK over AWGN Channel
trellis = poly2trellis(3,[6 5 7]);    %defines corresponding trellis diagram
spect = distspec(trellis);   %mii=nimum distance
berub = bercoding(ebnoVec,'conv','hard',1/3,spect); % BER bound
semilogy(ebnoVec,ber,'g',ebnoVec,berub,'r')   %plots uncoded BER and corresponding project convolutional code
ylabel('BER')
xlabel('Eb/No (dB)')
title('BER for Uncoded and Convolutional BPSK over AWGN Channel in Theory')
legend('Uncoded BPSK Theory','Convolutional(3,1,2) BPSK Theory')
grid
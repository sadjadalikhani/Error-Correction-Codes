n = 15;             % Codeword length
EbNo = -3:14;        % Eb/No range (dB)
berHamming = bercoding(EbNo,'Hamming','hard',n);   %BER:hard decision hamming theory-awgn-bpsk
berUncoded = berawgn(EbNo,'psk',2,'nodiff');		%BER:uncoded theory-awgn-bpsk
semilogy(EbNo,berHamming,'r',EbNo,berUncoded,'g')		%plot
title('BER for Hamming(15,11) and Uncoded over AWGN Channel')
ylabel('BER')
xlabel('Eb/No (dB)')
legend('Hamming(15,11) BPSK Theory','Uncoded BPSK Theory')
grid


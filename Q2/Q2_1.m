N =31; % RS codeword length
K = 27; % RS message length
S = 15;
M = 2;  % Modulation order  
bps = log2(M); % Bits per symbol

pskModulator = comm.PSKModulator('ModulationOrder',M,'BitInput',true);      %creating BPSK modulator
pskDemodulator = comm.PSKDemodulator('ModulationOrder',M,'BitOutput',true); %creating BPSK demodulator
awgnChannel = comm.AWGNChannel('BitsPerSymbol',bps);  %creating AWGN channel

rsEncoder = comm.RSEncoder('BitInput',true,'CodewordLength',N,'MessageLength',K);   %creating Reed Solomon encoder for RS(31,27)
rsDecoder = comm.RSDecoder('BitInput',true,'CodewordLength',N,'MessageLength',K);   %creating Reed Solomon decoder for RS(31,27)

rsEncoder3 = comm.RSEncoder('BitInput',true,'CodewordLength',N,'MessageLength',S);  %creating Reed Solomon encoder for RS(31,15)
rsDecoder3 = comm.RSDecoder('BitInput',true,'CodewordLength',N,'MessageLength',S);  %creating Reed Solomon encoder for RS(31,15)

ebnoVec = (-3:1:8)';    %SNR range to simulate
ber1 = zeros(length(ebnoVec));  %bit error rate for RS(31,27)
ber2 = zeros(length(ebnoVec));  %bit error rate for Uncoded
ber3 = zeros(length(ebnoVec));  %bit error rate for RS(31,25)

codedBER15 = bercoding(ebnoVec,'RS','hard',31,15);
codedBER27 = bercoding(ebnoVec,'RS','hard',31,27);
codedBER106 = bercoding(ebnoVec,'RS','hard',127,106);
uncodedBER = berawgn(ebnoVec,'psk',M,'nondiff');
for i = 1:length(ebnoVec)   %compute BER for all defined SNR's
    eps1 = 0;  %error per symbol
    eps2 = 0;
    eps3 = 0;
    awgnChannel.EbNo = ebnoVec(i);      %generate AWGN channel depending on SNR
    data = randi([0 1],27*300,1); %generate binary data for RS(31,27) coding
    data2 = randi([0 1],15*300,1);%generate binary data for RS(31,15) coding
    encData = rsEncoder(data); % RS(31,27) encode
    reset(rsEncoder)  %reset previous encoder to be used for the next encoding
    release(rsEncoder)
    encData2 = rsEncoder3(data2);% RS(31,15) encode
    reset(rsEncoder)
    release(rsEncoder)
    modData = pskModulator(encData); %RS(31,27) modulate
    modData2 = pskModulator(encData2);%RS(31,27) modulate
    modUncoded = pskModulator(data);%uncode message modulate
    rxSig = awgnChannel(modData); %pass signal through AWGN
    rxSig2 = awgnChannel(modData2);
    rxUncoded = awgnChannel(modUncoded);
    rxData = pskDemodulator(rxSig); % Demodulate RS(31,27)
    rxData2 = pskDemodulator(rxSig2);% Demodulate RS(31,15)
    rxUncoded = pskDemodulator(rxUncoded); % Demodulate uncoded message
    decData = rsDecoder(rxData); % RS(31,27) decode
    reset(rsDecoder)
    release(rsDecoder)
    decData2 = rsDecoder3(rxData2);% RS(31,15) decode
    reset(rsEncoder)
    release(rsEncoder)
    for q = 1:length(data)      
        if xor(decData(q),data(q))==1  %counting number of bit errors
            eps1 = eps1 + 1;
        end
        if xor(rxUncoded(q),data(q))==1 %counting number of bit errors
            eps2 = eps2 + 1;
        end    
    end
    for w = 1:length(data2)  %counting number of bit errors
        if xor(decData2(w),data2(w))==1 
            eps3 = eps3 + 1;
        end
    end    
    ber1(i) = eps1 / length(data);   %computing BER for RS(31,27)
    ber3(i) = eps3 / length(data2);  %computing BER for RS(31,15)
    ber2(i) = eps2 / length(data);     %computing BER for uncoded message
end

% semilogy(ebnoVec,ber1,'b',ebnoVec,ber2,'g',ebnoVec,ber3,'r') %blue:RS(31,27)  %red:RS(31,15)   %green:uncoded
% ylabel('BER')
% xlabel('Eb/No (dB)')
% legend('RS(31,27) BPSK','RS(31,15) BPSK','Uncoded BPSK')
% grid


semilogy(ebnoVec,codedBER15,'r',ebnoVec,codedBER27,'b',ebnoVec,codedBER106,'c-',ebnoVec,uncodedBER,'g') %blue:RS(31,27)  %red:RS(31,15)   %green:uncoded
ylabel('BER')
xlabel('Eb/No (dB)')
legend('RS(31,15) BPSK Theory','RS(31,27) BPSK Theory','RS(127,106)','Uncoded BPSK Theory')
grid
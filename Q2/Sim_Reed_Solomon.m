N =31; % RS codeword length
K = 27; % RS message length
S = 15;
M = 2;  % Modulation order  
bps = log2(M); % Bits per symbol

pskModulator = comm.PSKModulator('ModulationOrder',M,'BitInput',true);   %BPSK modulator
pskDemodulator = comm.PSKDemodulator('ModulationOrder',M,'BitOutput',true);    %BPSK demodulator
awgnChannel = comm.AWGNChannel('BitsPerSymbol',bps);   %awgn channel generating
errorRate = comm.ErrorRate;  

rsEncoder = comm.RSEncoder('BitInput',true,'CodewordLength',N,'MessageLength',K);   %reed solomon encoder
rsDecoder = comm.RSDecoder('BitInput',true,'CodewordLength',N,'MessageLength',K);   %reed solomon decoder 

ebnoVec = (-3:1:8)';
ber1 = zeros(length(ebnoVec));   %BER RS
ber2 = zeros(length(ebnoVec));   %BER uncoded


for i = 1:length(ebnoVec)
    eps1 = 0;
    eps2 = 0;
    awgnChannel.EbNo = ebnoVec(i);
    reset(errorRate)
    data = randi([0 1],27*300,1); % Generate binary data
    encData = rsEncoder(data); % RS encode
    modData = pskModulator(encData); % Modulate
    modUncoded = pskModulator(data);
    rxSig = awgnChannel(modData); % Pass signal through AWGN
    rxUncoded = awgnChannel(modUncoded);
    rxData = pskDemodulator(rxSig); % Demodulate
    rxUncoded = pskDemodulator(rxUncoded); 
    decData = rsDecoder(rxData); % RS decode
    for q = 1:length(data)
        if xor(decData(q),data(q))==1 % Collect error statistics
            eps1 = eps1 + 1;
        end 
        if xor(rxUncoded(q),data(q))==1
            eps2 = eps2 + 1;
        end    
    end    
    ber1(i) = eps1 / length(data);        
    ber2(i) = eps2 / length(data);   
end
% length(ber2)
% ber2
% berCurveFit1 = berfit(ebnoVec,ber1);
% berCurveFit2 = berfit(ebnoVec,ber2);

semilogy(ebnoVec,ber1,'c-',ebnoVec,ber2,'r')
ylabel('BER')
xlabel('Eb/No (dB)')
legend('RS','Uncoded')
grid
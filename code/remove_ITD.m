File1 = 'HRIR_HUTUBS_subject2_numerical.sofa';
Sofa1 = SOFAload(File1);

THRESHOLD = 0.5;
N = 4;
LENGTH = 30;
fade_window=[ones(1,LENGTH-10) [0.9:-0.1:0]];
newIR = zeros(size(Sofa1.Data.IR,1),2,LENGTH);


for j = 1:2
    for i = 1:size(Sofa1.Data.IR,1)
        normalized_hrir = (1/max(abs(Sofa1.Data.IR(i,j,:)))) * Sofa1.Data.IR(i,j,:);
        normalized_hrir = squeeze(normalized_hrir);
        smoothed_hrir=(abs(0.5*[normalized_hrir',0])+abs(0.5*[0,normalized_hrir']));
        smoothed_hrir(1)=0;
        sample_index_above = find(smoothed_hrir > THRESHOLD);
        t = squeeze(Sofa1.Data.IR(i,j,sample_index_above(1)-N:sample_index_above(1)-N+LENGTH-1));
        trimed_HRIR= t'.*fade_window;
        newIR(i,j,:) =  trimed_HRIR;
        Sofa1.Data.Delay(i,j)=sample_index_above(1)-N;
    end
end

Sofa1.Data.IR = newIR;

SOFAsave('HRIR_HUTUBS_subject2_numerical_remove_ITD.sofa',Sofa1)


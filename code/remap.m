scale = (0.0639+0.0578)/(2.4454+2.1125);

myDir = 'D:\fyp\pinnar\test_htrf\GAN_PINNA_DATA\HRIR'; %gets directory
myFiles = dir(fullfile(myDir,'*.sofa')); %gets all wav files in struct
outputDir = 'D:\fyp\HRTF_DATA\ARI\sofa_remap';
for k = 1:length(myFiles)
  baseFileName = myFiles(k).name;
  fullFileName = fullfile(myDir, baseFileName);
  Sofa1 = SOFAload(fullFileName);
  Sofa1.Data.IR = Sofa1.Data.IR * scale;
  ari_min = min(Sofa1.Data.IR,[],'all');
  ari_max = max(Sofa1.Data.IR,[],'all');
  fullFileName = fullfile(outputDir, baseFileName);
  SOFAsave(fullFileName,Sofa1);
end


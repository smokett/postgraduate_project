myDir = 'D:\fyp\HRTFcomparison\barycentric_interpolated_data_80_1280_valid'; %gets directory
rawDir = 'D:\fyp\HRTFcomparison\raw_1280';
myFiles = dir(fullfile(myDir,'*.sofa')); %gets all wav files in struct

curdir = cd; amt_start(); cd(curdir); % start AMT
pol_acc1_avg = 0.0;
pol_rms1_avg = 0.0;
querr1_avg = 0.0;
pol_acc1_array = zeros(length(myFiles),1);
pol_rms1_array = zeros(length(myFiles),1);
querr1_array = zeros(length(myFiles),1);



for k = 1:length(myFiles)
  baseFileName = myFiles(k).name;
  fullFileName = fullfile(myDir, baseFileName);
  Sofa1 = SOFAload(fullFileName);
  fullFileName = fullfile(rawDir, baseFileName);
  Sofa2 = SOFAload(fullFileName);
  [h1,fs,az,el] = sofa2hrtf(Sofa1);
  [h2,fs2,az2,el2] = sofa2hrtf(Sofa2);
  fs = 48000;
  fs2 = 48000;
  num_exp = 10;


  % Run barumerli2021 for h1
  disp('Running barumerli2021 for first HRTF...'), tic

  dtf = getDTF(h1,fs);
  SOFA_obj1 = hrtf2sofa(dtf,fs,az,el);
  % Preprocessing source information
  [~, target1] = barumerli2021_featureextraction(SOFA_obj1);

  dtf = getDTF(h2,fs2);
  SOFA_obj2 = hrtf2sofa(dtf,fs2,az2,el2);
  % Preprocessing source information
  [template2, target2] = barumerli2021_featureextraction(SOFA_obj2);

  % Run virtual experiments
  [m1,doa1] = barumerli2021('template',template2,'target',target2,'num_exp',num_exp);
  % Calculate performance measures
  sim1 = barumerli2021_metrics(m1, 'middle_metrics');
  lat_acc1 = sim1.accL; % mean lateral error
  lat_rms1 = sim1.rmsL; % lateral RMS error
  pol_acc1 = sim1.accP; % mean polar error
  pol_rms1 = sim1.rmsP; % polar RMS error
  querr1 = sim1.querr; % quadrant error percentage
  pol_acc1_avg = pol_acc1_avg + pol_acc1;
  pol_rms1_avg = pol_rms1_avg + pol_rms1;
  querr1_avg = querr1_avg + querr1;
  pol_acc1_array(k) = pol_acc1;
  pol_rms1_array(k) = pol_rms1;
  querr1_array(k) = querr1;
  fprintf('Finished running barumerli2021 for %d HRTF. Took %0.2f s\n', k, toc)
end

disp(length(myFiles));
pol_acc1_abs_avg = mean(abs(pol_acc1_array));
pol_acc1_avg = mean(pol_acc1_array);
pol_rms1_avg = mean(pol_rms1_array);
querr1_avg = mean(querr1_array);
pol_acc1_std = std(pol_acc1_array);
pol_rms1_std = std(pol_rms1_array);
querr1_avg_std = std(querr1_array);
pol_acc1_min = min(pol_acc1_array);
pol_rms1_min = min(pol_rms1_array);
querr1_avg_min = min(querr1_array);
pol_acc1_max = max(pol_acc1_array);
pol_rms1_max = max(pol_rms1_array);
querr1_avg_max = max(querr1_array);
pol_acc1_median = median(pol_acc1_array);
pol_rms1_median = median(pol_rms1_array);
querr1_median = median(querr1_array);
save("C:\Users\smoketw\Desktop\Mads\polar_accuracy.mat","pol_acc1_array");
save("C:\Users\smoketw\Desktop\Mads\polar_rms.mat","pol_rms1_array");
save("C:\Users\smoketw\Desktop\Mads\quadrant.mat","querr1_array");





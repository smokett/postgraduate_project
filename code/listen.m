File1 = 'HRIR_HUTUBS_subject1_empirical_remove_ITD.sofa';
Sofa1 = SOFAload(File1);
hrtfData = Sofa1.Data.IR;
sourcePosition = Sofa1.SourcePosition;

sourcePosition = sourcePosition(:,[1,2]);

desiredAz = [-120;-60;0;60;120;0;-120;120];
desiredEl = [-90;90;45;0;-45;0;45;45];
desiredAz = [0;45;90;135;180;225;270;315];
desiredEl = [0;0;0;0;0;0;0;0];
% desiredAz(1:360) = (0:359);
% desiredEl(1:360) = 0;
desiredPosition = [desiredAz desiredEl];

interpolatedIR  = interpolateHRTF(hrtfData,sourcePosition,desiredPosition);

leftIR = squeeze(interpolatedIR(:,1,:));
rightIR = squeeze(interpolatedIR(:,2,:));

desiredFs = 44100;
[audio,fs] = audioread('5_Audio_Track.aiff');
audio = 0.8*resample(audio,desiredFs,fs);
audiowrite('5_Audio_Track_32000.wav',audio,desiredFs);

fileReader = dsp.AudioFileReader('5_Audio_Track_32000.wav');
deviceWriter = audioDeviceWriter('SampleRate',fileReader.SampleRate);

leftFilter = dsp.FIRFilter('NumeratorSource','Input port');
rightFilter = dsp.FIRFilter('NumeratorSource','Input port');

durationPerPosition = 2;
samplesPerPosition = durationPerPosition*fileReader.SampleRate;
samplesPerPosition = samplesPerPosition - rem(samplesPerPosition,fileReader.SamplesPerFrame);

sourcePositionIndex = 1;
samplesRead = 0;

fileWriter = dsp.AudioFileWriter('test.wav','SampleRate',desiredFs);
while ~isDone(fileReader)
    audioIn = fileReader();
    samplesRead = samplesRead + fileReader.SamplesPerFrame;
    
    leftChannel = leftFilter(audioIn,leftIR(sourcePositionIndex,:));
    rightChannel = rightFilter(audioIn,rightIR(sourcePositionIndex,:));
    
    %deviceWriter([leftChannel(:,1),rightChannel(:,2)]);
    fileWriter([leftChannel(:,1),rightChannel(:,2)]);
    
    if mod(samplesRead,samplesPerPosition) == 0
        sourcePositionIndex = sourcePositionIndex + 1;
    end
    sourcePositionNumber = size(leftIR,1);
    if sourcePositionIndex > sourcePositionNumber
        sourcePositionIndex = 1;
    end
end

release(deviceWriter)
release(fileReader)
release(fileWriter)
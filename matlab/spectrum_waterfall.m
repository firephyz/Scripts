image = imread("~/Downloads/pan.jpg");
##image = image';

factor=128.0;
image = image(cast(linspace(1,size(image,1),cast(size(image,1)/factor, 'int32')),'int32'),
              cast(linspace(1,size(image,2),cast(size(image,2)/factor, 'int32')),'int32'));

image(1,:) = image(2,:);
image(:,1) = image(:,2);
image(size(image,1)-1,:) = image(size(image,1),:);
image(:,size(image,2)-1) = image(:,size(image,2));

der_x = zeros(size(image,1)-2, size(image,2)-2);
der_y = zeros(size(image,1)-2, size(image,2)-2);
for i = 2 : size(image,1) - 1
  for j = 2 : size(image,2) - 1
    der_x(i-1,j-1) = (image(i+1,j) - image(i-1,j)) / 2;
    der_y(i-1,j-1) = (image(i,j+1) - image(i,j-1)) / 2;
  end
  if (mod(i,100) == 0)
    printf("%f\n", 100 * i / size(image,1));
  endif
end
    
der = (der_x .^ 2 + der_y .^ 2) .^ 0.5;
##der = image;
der = cast(der / max(max(der)) * 255,'int32');

fvals = linspace(1200, 17000, size(der,1));
%fvals = e .^ fvals;

sfreq = 44100;
time_width = 19*4.5;
dtime_width = time_width / size(der,2);
nsamples_per_f = cast(dtime_width * sfreq, 'int32');

audio = zeros(1,nsamples_per_f * size(der,2));
xvals = linspace(0,time_width,nsamples_per_f * size(der,2));
for tbi = 1:size(der,2)
  block = zeros(1,nsamples_per_f);
  fxvals = xvals(1,(tbi-1)*nsamples_per_f+1:tbi*nsamples_per_f);
  for fqi = 1 : size(fvals,2)
    freq = fvals(fqi);
    sinwave = sin(2 * pi * freq * fxvals);
    block = block + cast(der(fqi,tbi),'double') / 255 * sinwave;
  end
  audio(1,(tbi-1)*nsamples_per_f+1:tbi*nsamples_per_f) = block;
  
  if mod(tbi,50) == 0
    printf("%f\n", 100.0 * tbi / size(der,2));
  endif
end

audio = audio / max(audio);

fftaudio = fft(audio);
for i = 1 : size(fftaudio)
  if (abs(fftaudio(i)) > 500)
    fftaudio(i) = 0;
  endif
end

audio_filtered = real(ifft(fftaudio));

audiowrite("audioout3.wav", audio_filtered, sfreq);

# test = sin(440*2*pi*linspace(0,44100*5));
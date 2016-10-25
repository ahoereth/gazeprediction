% Plot eye fixation coordinates on the image file
%
% Gaze Prediction Seminar 2016/2017
%
% SYNOPSIS: outImage = plotGaze(imagefile, coordinates, ...)
%
%
% INPUT
%
%   imagefile[in] image file
%
%   coordXY[in]   eye-fixation coordinates
%
%
%
% OUTPUT
%
%   outImage
%
% AUTHOR: ahoereth
% DATE:   2016/10/24
%
%
% -------------------------------------------------------------------------

function outImage = plotGaze(imagefile, coordXY)
  coordXY = squeeze(coordXY);
  imshow(imread(imagefile))
  hold on
  scatter(coordXY(:,1), coordXY(:,2), '*')
  hold off
end

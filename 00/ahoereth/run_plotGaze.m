% Main run to plot images and coordinates from files.
%
% Gaze Prediction Seminar 2016/2017
%
% SYNOPSIS:
%
%
% INPUT Requirement:
%     image files:      input image
%     mat file:         eye fixation coordinates
%
% OUTPUT
%     image files with plot of eye fixation coordinates
%
% AUTHOR: ahoereth
% DATE:   2016/10/24
%
% -------------------------------------------------------------------------

load 'coordinates.mat'
for i = 1:length(coordXYs)
  subplot(2,4,i)
  plotGaze(coordXYs(i).filename, coordXYs(i).coordXY)
end

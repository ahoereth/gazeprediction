% Gaussian Mixture Models
% Alexander Höreth and Sebastian Höffner
% December 03, 2016

---
navigation: empty
theme: CambridgeUS 
colortheme: beaver
---

# Background Subtraction
## Background Subtraction
* surveillance monitoring
* motion detection
* image segmentation

Primarily used for preprocessing! 

e.g.

1. remove background
2. detect moving objects
3. identify individual humans


## Mixture of Gaussians
* consider an image as a distribution over its pixel's values
* estimate it using a mixture of three to five Gaussians
* use expectation maximization (expensive) or k-means to make the Gaussians mixture model better fit the image

* sort by weights by variance ($\omega/\sigma$) 
* first few distributions are declared as background
* pixels belonging to these can be declared as background pixels, others are foreground

[@stauffer99, specifically page 4]


# Improving Background Subtraction
## Improving Background Subtraction
* *Improved Adaptive Background Mixture Model* (MOG) by @ktkp01
* *Improved Adaptive Gaussian Mixture Model* (MOG2) by @zivkovic04 and @zivkovic06


## Improved Adaptive Background Mixture Model (MOG)
* add more Gaussians if pixels are $2.5$ standard deviations away from all current distributions
    - allows the model to adapt to changes quicker
    - predict fore/background affiliation faster
* use *expectation maximization* instead of k-means
    - k-means was basically an approximation of EM
    - EM got computational feasible
* detect shadows (FIXME: how?)
    - combination of background and foreground features
* more precise than original algorithm

[@ktkp01]


## Improved Adaptive Gaussian Mixture Model (MOG2)
* dynamically add and remove Gaussians:
    - pixels are considered to be not represented by model if more than $3$ standard deviations away from all Gaussians
    - if useful, remove Gaussian with lowers probability and add a new one for the not represented pixels
    - cap Gaussian count at 5
* introduce *balloon estimator* as alternative to k-means
    - again approximates EM
* also detects shadows
* faster than original algorithm

[@zivkovic06]




# Thank you for listening
## References

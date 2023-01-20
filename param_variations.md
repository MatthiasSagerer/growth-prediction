# Overview over the parameters to be varied

## Dataset parameters
- Dataset size
- Image resolution
- Image "Format"
- Temporal video length / Frame rate

## Hyper parameters of the FutureGAN network

<span style="color:red">
These parameters first need to be determined
</span>
<br/>
<br/>

## Growth_prediction dataset1/2

### Metadata:
- Dataset size          : each 90 videos => 180 videos
- Frame resolution      : 660 x 660
- DPI (dots per inch)   : 96
- Image depth           : 24 bit
- Additional info	    : binary image (b/w)

<br/>

## Group variation of parameters by two
### Dataset size and frame resolution
- Dataset size:         18/45/90/180 videos <br/>
  (corresponding to 10/25/50/100% of the available data)
- Frame resolutions:    128x128/256x256/512x512
<br>
<br>
<br>

### Time span between frame / Image type
- Time span between frames:     1/2/3/4h
- (corresponding to 6/12/18/24h prediction)
- Image type:               raw/segmented(/something in between)

#### Possible splitting of the raw data
##### Raw data metadata: (12FrVi := 12Frame-Video)
Two wells:
- left well
  - Original resolution: 7446x7440 (19359.62x19344.02 microns)
  - Frames: 78 with 1h difference (useable: 77)
  - Usable resolution: about (14x512)x(13x512) = 7168x6656
- right well
  - Original resolution: 7445x7438 (19357.02x19338.82 microns)
  - Frames: 78 with 1h difference (usable: 74)
  - Usable resolution: about (14x512)x(13x512) = 7168x6656

#### (14x512)x(13x512) = 6656x7168, 72 1h frames, 2 wells [with data augmentation (rotation)]
- 1h: 14 columns x 13 rows x 2 wells x 6 (12FrVi/video) = 2184 12FrVi [2: 4368]
- 2h: 14 columns x 13 rows x 2 wells x 3 (12FrVi/video) = 1092 12FrVi [2: 2184]
- 3h: 14 columns x 13 rows x 2 wells x 2 (12FrVi/video) = 728 12FrVi [2: 1456]
- 4h: 14 columns x 13 rows x 2 wells x 1 (12FrVi/video) = 364  12FrVi [2: 728]
<br>
<span style="color:red">
Use 364 12FrVi with 2 different rotations for every time interval between frames => 182 per well
</span>

### Plan to get 182 12FrVi per well for all time intervals
- 1h: 6 (12FrVi/video) x 4 cols x 8 rows = 192 => remove 10
- 2h: 3 (12FrVi/video) x 7 cols x 9 rows = 189 => remove 7
- 3h: 2 (12FrVi/video) x 7 cols x 13 rows = 182 
- 4h: 1 (12FrVi/video) x 14 cols x 13 rows = 182
<br>
<span style="color:red">
switch between first/last 48 frames !!
</span>

### Splitting into train/test set: approx 90/10 => 84/644
<span style="color:red">
#### IMPORTANT NOTE: the columns and rows are switched for 1/2/3!!
</span>
- 1h (left/right well): x_offset, y_offset = 512 px
  - omitted
    - column 3 row 5
    - column 3 row 7 time series 0, 1, 4, 5 <br>
      => 20 videos (40 for both wells)
  - test set
    - column 0 row 0
    - column 1 row 2
    - column 2 row 4
    - column 3 row 6 only rotated <br>
      => 42 videos (84 for both wells)
  - train set
    - column 0 rows 1, 2, 3, 4, 5, 6, 7
    - column 1 rows 0, 1, 3, 4, 5, 6, 7
    - column 2 rows 0, 1, 2, 3, 5, 6, 7
    - column 3 rows 0, 1, 2, 3, 4
    - column 3 row 6 without rotation
    - column 3 row 7 time series 2, 3 <br>
      => 322 videos (644 for both wells)
- 2h (left/right well): x_offset, y_offset = 512 px
  - omitted
    - column 5 row 8
    - column 6 row 7
    - column 6 row 8 time series 1<br>
      => 14 videos (28 for both wells)
  - test set
    - column 0 row 0
    - column 1 row 1
    - column 2 row 2
    - column 3 row 3
    - column 4 row 4
    - column 5 row 5
    - column 6 row 6 <br>
      => 42 videos (84 for both wells)
  - train set
    - column 0 rows 1, 2, 3, 4, 5, 6, 7, 8
    - column 1 rows 0, 2, 3, 4, 5, 6, 7, 8
    - column 2 rows 0, 1, 3, 4, 5, 6, 7, 8
    - column 3 rows 0, 1, 2, 4, 5, 6, 7, 8
    - column 4 rows 0, 1, 2, 3, 5, 6, 7, 8
    - column 5 rows 0, 1, 2, 3, 4, 6, 7 
    - column 6 rows 0, 1, 2, 3, 4, 5
    - column 6 row 8 time series 2, 3
      => 322 videos (644 for both wells)
- 3h: 
  - omitted: not necessary
  - test set
    - column 0 rows 0, 7
    - column 1 row 1
    - column 2 rows 2, 9
    - column 3 row 3
    - column 4 rows 4, 11
    - column 5 row 5
    - column 6 row 6
    - column 6 row 12 only rotated <br>
      => 42 videos (84 for both wells)
  - train set
    - column 0 rows 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12
    - column 1 rows 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 2 rows 0, 1, 3, 4, 5, 6, 7, 8, 10, 11, 12
    - column 3 rows 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 4 rows 0, 1, 2, 3, 5, 6 , 7, 8, 9, 10, 12
    - column 5 rows 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12
    - column 6 rows 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11
    - column 6 row 12 only original
      => 322 videos (644 for both wells)
- 4h: 
  - omitted: not necessary
- test set
    - column 0 rows 0, 5
    - column 1 rows 1, 6
    - column 2 rows 2, 7
    - column 3 rows 3, 8
    - column 4 rows 4, 9
    - column 5 rows 5, 10
    - column 6 rows 6, 11
    - column 7 rows 7, 12
    - column 8 row 8
    - column 9 row 9
    - column 10 row 10
    - column 11 row 11
    - column 12 row 12
      => 42 videos (84 for both wells)
  - train set
    - column 0 rows 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12
    - column 1 rows 0, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12
    - column 2 rows 0, 1, 3, 4, 5, 6, 8, 9, 10, 11, 12
    - column 3 rows 0, 1, 2, 4, 5, 6, 7, 9, 10, 11, 12 
    - column 4 rows 0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12
    - column 5 rows 0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12
    - column 6 rows 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 12
    - column 7 rows 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11
    - column 8 rows 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12
    - column 9 rows 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12
    - column 10 rows 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12
    - column 11 rows 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12
    - column 12 rows 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 
    - column 13 rows 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
      => 322 videos (644 for both wells)

Thresholding:
- process > find edges
- process > filters > gaussian blur (radius = 10)
- image > adjust > threshold (0 - about 21)

### Data augmentation
basic properties:
- 3h => 2 12 FrVi per cutout
- 14 columns, 13 rows => 182 cutouts per well
- segmented, two wells
- 182 cutouts x 2 12 FrVi per cutout x 2 wells = 728 vids
- splitting into 84 test vids & 644 training vids

Three datasets: 
- control (crl):all 728 vids as control (14 cols, 13 rows)
- rotated (rot): 364 vids + rotated 90° counterclockwise (7 cols, 13 rows)
- mirrored (mir): 364 vids + mirrored on the vertical axis (7 cols, 13 rows)
- not augmented (noa): 364 vids (7 cols, 13 rows)
- NOTE: use the same test set for all data augmentation models

#### train/test splitting for data augmentation
- ctrl: cols 0-13, rows 0-12
  - test
    - column 0 row 0 
    - column 1 row 1
    - column 2 row 2
    - column 3 row 3
    - column 4 row 4
    - column 5 row 5
    - column 6 rows 6, 0
    - column 7 rows 7, 1
    - column 8 rows 8, 2
    - column 9 rows 9, 3
    - column 10 rows 10, 4
    - column 11 rows 11, 5
    - column 12 rows 12, 6
    - column 13 row 7 <br>
      => 21 cutouts for the test set (1 well: 42 vids, 2 wells: 84 vids)
  - train
    - column 0 rows 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 1 rows 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 2 rows 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 3 rows 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 4 rows 0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12
    - column 5 rows 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12
    - column 6 rows 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12
    - column 7 rows 0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12
    - column 8 rows 0, 1, 3, 4, 5, 6, 7, 9, 10, 11, 12
    - column 9 rows 0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12
    - column 10 rows 0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12
    - column 11 rows 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12
    - column 12 rows 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11
    - column 13 rows 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12
- mir/rot (noa: without augmentation): cols 0-6, rows 0-12
  - test
    - column 0 row 0
    - column 1 row 1
    - column 2 row 2
    - column 3 rows 3, 9
    - column 4 rows 4, 10
    - column 5 rows 5, 11
    - column 6 row 6
    - column 6 row 12 first 36 frames <br>
      => 10,5 cutouts for test set with ori and mir (1 well: 42 vids, 2 wells: 84 vids)
  - train
    - column 0 rows 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 1 rows 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 2 rows 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    - column 3 rows 0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12
    - column 4 rows 0, 1, 2, 3, 5, 6, 7, 8, 9, 11, 12
    - column 5 rows 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12
    - column 6 rows 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11
    - column 6 row 12 last 36 frames
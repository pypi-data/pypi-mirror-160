# exifmgr

## installation

```
git clone https://github.com/bluszcz/exifmgr.git
cd exifmgr
pip -i requirements.txt
```

## usage

Launch the script with directory parameter, pointing to your folder with photos. After that it will organize your photos depends on used lenses.

```
./script.py directory
```

### Example

```
(p3-bluszcz) bluszcz@raspberrypi-02:~/Dev/exifmgr $ ./script.py /storage/Photos/2022-05-01-Canon-90D/
  2% (15 of 516) |###
  5% (28 of 516) |###                                                            | Elapsed Time: 0:00:22 ETA:   0:05:40
(p3-bluszcz) bluszcz@raspberrypi-02:~/Dev/exifmgr $ ls -1 /storage/Photos/2022-05-01-Canon-90D/ 
Canon_EF_50mm_f_1.8_STM
Canon_EF-S_24mm_f_2.8_STM
(p3-bluszcz) bluszcz@raspberrypi-02:~/Dev/exifmgr $
```

## TODO:

* Allow split per various parameters (fov, iso? ss?)
* Prepare a proper package's structure https://packaging.python.org/en/latest/tutorials/packaging-projects/

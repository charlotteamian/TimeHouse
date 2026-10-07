# Third-party notices

## Exercises Dataset

This app bundles a normalized Chinese text snapshot of
[`hasaneyldrm/exercises-dataset`](https://github.com/hasaneyldrm/exercises-dataset)
at commit `7455efae41b330c265e7cd4b78dfa848e7ce5ebd`.

Included fields: exercise identifiers and names, body categories, equipment,
target and secondary muscle metadata, and Chinese instruction steps. These
code/data portions are provided under the MIT License. The complete upstream
license is packaged at `app/src/main/assets/licenses/exercises-dataset-LICENSE.txt`.

The upstream images and GIFs are copyrighted by Gym visual and are explicitly
excluded from this app because cloning the repository does not grant a reuse
license for that media.

## Free Exercise DB

For exercises with an exact English-name match, this app uses both public-domain
start/end frames from
[`yuhonas/free-exercise-db`](https://github.com/yuhonas/free-exercise-db) at
commit `b0eed061e1c832b3ed815fbaa4b45b3cdc14df49`. That project releases its
dataset and images into the public domain under the Unlicense. The full license
is packaged at `app/src/main/assets/licenses/free-exercise-db-UNLICENSE.txt`.

The app's import script converts those public-domain frame pairs into 113
original looping previews. The remaining imported exercises use the app's own
anatomical motion frames: start/end illustration pairs generated for this app,
then interpolated into a smooth loop with dense optical flow (a single source
frame is warped per step, never a blend of two, to avoid ghosting). Frames are
normalized onto a fixed white canvas with the target muscle group tinted red.
Every imported exercise therefore has an offline animation.

All media is 480x480 animated WebP that loops infinitely (decoded natively by
Android's `ImageDecoder`, hence `minSdkVersion` 28). No upstream Gym visual
pixels are included in the imported dataset media; the anatomical illustrations
are generated assets owned by this app, not copied from the excluded upstream
media.

The animations are movement aids, not a claim that the pictured pose is a
substitute for professional technique review.

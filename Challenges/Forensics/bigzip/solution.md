Intended solve:
Most of the zip files are stored in STORE algo, which makes things very easy as you can just blast away the layers. I did it 10000 STOREs for each DEFLATE. Script in `solve`. Script runs in <1 min on my (quite potato) machine.

Funny solve:
Write script to actually unzip each later with `7z` in a loop. I actually calculated this will take minimum 40h when making the chal, making it unusable.

Flag: `blahaj{z1p5_AlL_tH3_W4Y}`
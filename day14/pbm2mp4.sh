ffmpeg -framerate 5 -pattern_type glob -i '*.pbm' -vf "scale=3*iw:3*ih" -c:v libx264 -pix_fmt yuv420p out.mp4

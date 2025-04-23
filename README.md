# allsky_calan

Compatible with every ASI ZWO camera. Just install "requirements.py" and ensure you have the ZWO drivers.

Just run "allsky.py" and the script will:

1. Connect the Camera
2. Take exposures every minute, controlling gain and exptime
3. Show the image in a .html file
4. Save the exposure in the "imagenes" directory
5. Sleep during daytime

You can also run "checkspace.py" to control the size of the "imagenes" directory, removing the oldest directory once the total size is above 10gb.


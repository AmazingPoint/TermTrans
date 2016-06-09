echo 'copy trans.py to /usr/local/share'
sudo cp trans.py /usr/local/share
echo 'add execute permission '
sudo chmod +x trans.py
echo 'lin to path /usr/bin'
sudo ln -s /usr/local/share/trans.py /usr/bin/trans
echo 'SUCCESSFUL'
echo 'You can use trans'

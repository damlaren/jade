python setup.py sdist
sudo pip install dist/adiencealign-0.1.tar.gz --upgrade
cd ./adiencealign/tests/
sudo ./clear_test.sh
python test_pipeline.py

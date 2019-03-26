cd app
pip install -r requirements.txt

vim ~/.bash_profile

# paste the following
export TAMKEEN_EMAIL=youremail@tamkee.us
export TAMKEEN_PASSWORD=anypassword
export ACCESS_KEY=access_key
export SECRET_KEY=secret_key
export TAMKEEN_DB_HOST=52.27.126.98
export TAMKEEN_DB_USER=postgres
export TAMKEEN_DB_PASSWORD=passw0rd
export TAMKEEN_S3_ACCESS_KEY=key
export TAMKEEN_S3_SECRET_KEY=secret
export GA_TRACKING_ID=id
source ~/.bash_profile


python3 manage.py make migrations
python3 manege.py runserver 0.0.0.0:8080

# Instance setup instructions
    1. Create an VM instance - 
        open firewall with 5000 port

    2. clone the code from wget:
        wget https://github.com/sasidhar-danturti/text-summarization/archive/master.zip

    3. sudo apt-get install zip

    4. Install pip
        wget https://bootstrap.pypa.io/get-pip.py
        sudo python get-pip.py

    5. sudo pip install flask

    6. sudo pip install tensorflow

    7. gcloud config set project text-summarization-webapp

    8. create a service account file 
        gcloud auth activate-service-account --key-file /home/sasidhar_danturti/text-summarization-webapp-3514772eff5d.json 


# Enable https routing for trainer on Compute Engine Instance

    1. Install pyopenssl 
        pip install pyopenssl
    
    2. Download Certifiactes and key and keep under dir trainer/
        openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Resolve Cross Origin problem with Flask
    
    1. Install flask-cors
    pip install -U flask-cors

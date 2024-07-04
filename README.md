#**get_redis_info**

Get info from multiple Redis instances.

This code allows you to collect info from multiple Redis databases in one pass. It works for both Redis Enterprise and Redis OSS/source available.

Usage:

1- Clone the repository create a virtual environment

% python3 -m venv .env && source .env/bin/activate 

2- Install the requirements

(venv)% pip install -r requirements.txt

3- Edit the input file (input_file.txt) to include all instances. Follow the format directive in the file.

4- Run the code

(venv)% python get_redis_info.py

5- Check the output file (redis_info_output.csv)

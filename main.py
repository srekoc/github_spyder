import os 
import re
import sys
import json
import yaml
import shlex
import ujson
import signal
import subprocess
from os import path

def signal_handler(signal, frame):
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    os.system("stty -echo")
    print ("--------\n")
    github_password = input('Github password: ')
    print ("\n")
    print ("--------")
    os.system("stty echo")
    print("")
    print("\n")
    print ("please wait while processing, this would take sometime...")
    with open("input.yml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        # print(data_loaded)
    github_username = data_loaded['github_username']
    github_username.strip()
    language = data_loaded['language']
    language.strip()
    keyword = data_loaded['keyword']
    keyword.strip()
    github_password.strip()
    key = data_loaded['github_apikey']
    key.strip()
    cmd = f'scrapy runspider ./github-scraper.py \
            -s LOG_ENABLED=False \
            -a github_user={github_username} \
            -a github_pass={github_password} \
            -a language_type={language} \
            -a search_string={keyword} \
            -o z.json'
    if path.exists("z.json"):
        os.unlink("z.json")
    command = subprocess.Popen(shlex.split(cmd))
    command.communicate()
    pattern = data_loaded['regex']
    re.escape(pattern)
    api_url = "https://github.com/api/v3"
    api_key = f'{github_username}:{key}'
    init_cmd = f'curl -s -u {api_key} -X GET "{api_url}/repos'
    with open('z.json', encoding="utf8") as f:
        jsonObject = json.load(f)
    fo = open("result", "w", encoding="utf8")
    for key in jsonObject:
        repo_name = key['repo_name']
        filename = key['filename']
        # This can be made so much faster with just picking up the first commit. Not now though.
        cmd = f'{init_cmd}/{repo_name}/commits?path={filename}"'
        
        # don't like the subprocess. Perl does matter job than this. 
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        var = proc.stdout.read()

        # because pytjon json module sucks, picked up ujson
        resp = ujson.loads(var)

        # print ("var " + resp)
        author_details = resp[0]['commit']['author']
        codestr = key['code']
        lines = codestr.split('\n')
        final_line = ""
        
        for line in lines:
            result = re.search(pattern, line)
            if result:
                final_line += "\n" + line
        if final_line != "":
            print (repo_name)
            print (filename)
            print (final_line)
            print (author_details)
            print ("--------------")
            
            # write/writelines method sucks. no time to make it better
            fo.write(repo_name)
            fo.write(filename)
            author_details = str(author_details)
            fo.write(author_details)
            fo.write(final_line)
    
    f.close()            
    fo.close()

if __name__ == '__main__':
    main()

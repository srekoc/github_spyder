# github spyder

> Crawler script that scans github repositories for clear text passwords

## Background
This tool was developed because 
- no similar tools available that can scan github code base 
- github has no regular expression search
- cannot export paginated github search results
- can't use regex/wildcard characters search on github

### Preperation

- App is built in quick time, if you see a feature missing, fork it & implement it
- Ensure docker for windows is available on the system & daemon is running
- Ensure access to github, github.com
- Unless admin, spyder just scans github repos user has access to
- Better to be on vpn if you are trying on laptop & not in office network
- If at all you wish to generate a clean docker image (on your personal space)
  Note: Avoid these steps if you are on shared tenets
  #### Delete existing Docker containers
  #### Must be run first because images are attached to containers
  docker rm -f $(docker ps -a -q)
  #### Delete existing Docker images
  docker rmi -f $(docker images -q)

### Build & Run
Update ***input.yml*** file with relevant details

**Windows:**
- open git bash / command prompt on windows OS.
- ensure docker daemon is up and running (verify tray items)
- `winpty docker build . -t <docker_image_name>`
- `winpty docker run -u 0 -it <docker_image_name>` (runs it as 'root' user)
- provide the relevant github password

**Linux**
- open bash shell.
- ensure docker is installed on the box
- validate proxy information if any
- `docker build . -t <docker_image_name>`
- `docker run -u 0 -it <docker_image_name>` (runs it as 'root' user)
- provide the relevant github password

### Limitations

- There is no full blown error catching or logging, if it fails, figure it out
- Sanity of search string or input is not validated. User input is trusted as-is
- Ensure the yaml file is accurate
- Usernames and passwords are not validated against Active directory. 
- Punch in the right password or brace up for errors on screen
- Rough on edges. App needs more testing.

### Author
Sreekanth Kocharlakota

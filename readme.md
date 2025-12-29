Code Execution in shell:


Configuring REDIS-WSL(terminal 1-WSL)

    cmds: 
        1) wsl --install
        2)sudo apt update && sudo apt upgrade -y
        3)sudo apt install redis-server -y
        4)sudo service redis-server start
        5)redis-cli ping  (output : PONG)

(Terminal 2)
1)Python venv creation

    cmd: python -m venv venv

    activate: venv/Scripts/activate

2) Upgrade Pip
    python -m pip install --upgrade pip
    pip cache purge

3) Download requirements
        pip install -r requirements.txt

4) Create .env and add GOOGLE_API_KEY

5)Change Working directory to Veritas\veritas

6) Run veritas_crew.py 

Checking Redis(Terminal 1 -WSL)

cmds:
    1)redis-cli
    2) KEYS agent1:*
    3)HGETALL agent1:claim:001
# Description: Install the project dependencies
#!/bin/bash

$(which python3) -m pip install --upgrade pip
$(which python3) -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt

---


#!/bin/bash

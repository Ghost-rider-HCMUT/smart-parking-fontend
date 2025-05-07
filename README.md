python -m venv .venv

.venv\Scripts\activate

pip install python-dotenv
pip install requests
pip install PyQt5
pip install QT-PyQt-PySide-Custom-Widgets

## CLI
### qrc => py
'''
pyrcc5 assets/icons/resource.qrc -o resource_rc.py  
'''

### ui => py
'''
pyuic5 -x admin.ui -o admin.py
'''

## SETUP ENV
### Create env
'''
python -m venv myenv
'''

### Active env
'''
myenv\Scripts\activate
'''

###  Deactive env
'''
deactivate
'''

### Save list lib
'''
pip freeze > requirements.txt
'''                                                                                         
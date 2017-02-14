#  /***********************************************************
#  * Author       : M_Kepler
#  * EMail        : m_kepler@foxmail.com
#  * Last modified: 2017-01-05 16:51:31
#  * Filename     : flask_app.py
#  * Description  : 用于pythonanywhere的部署
#  **********************************************************/

from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run()

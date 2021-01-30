Quickstart
===========

This pages explains on how to install and setup your PyMine server.

.. important:: 
    It is recommend to use `PyPy3 <https://www.pypy.org/>`_ as it faster and more efficent than the regular python 

=======================
Installing from Source
======================= 

You can get PyMine from the git repository: ::

    git clone https://github.com/py-mine/PyMine.git

Next, move into the directory and install the required Python packages. ::
    
    cd PyMine
    pip install -r requirements.txt

.. note::
    If you are using PyPy3 run ``pypy3 -m pip install -r requirements.txt``
    

====================
Starting the Server
====================

To start the server run ::

    python3 pymine

.. note::

    If you are using PyPy3 run ``pypy3 pymine``
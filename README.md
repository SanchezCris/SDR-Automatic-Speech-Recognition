# SDR-Automatic-Speech-Recognition

FM signal capturing system and voice recognition for the assistance of individuals with hearing impairments.

### Clone for GNU Radio 3.8

    $ git clone https://github.com/SanchezCris/SDR-Automatic-Speech-Recognition.git

## Features

* Supports LimeSDR through GNU Radio.
* Supports 2 MHz as sample rate and demodulates a signal at 48 KHz
* FM demodulation of an RF signal.
* Wav to Text
* Threading
* Printing in terminal and web graphical interface

## Usage

There is an example GNU Radio Companion ``(.grc)`` flowgraph located at ``SDR-Automatic-Speech-Recognition/app/gnuradio/fm_receive_tcp.grc``. To use it, double click on this file and run it.

[![gnu.png](https://i.postimg.cc/7hRyhSCg/gnu.png)](https://postimg.cc/ctfz5gBH)

Example of GUI GNU Radio.

[![block5.png](https://i.postimg.cc/4x2wMZKF/block5.png)](https://postimg.cc/21v4bs74)

Example of printing on terminal.

[![terminal.png](https://i.postimg.cc/QCwRhsPm/terminal.png)](https://postimg.cc/kRNjyr7R)

### Webserver

To view the real-time transcription of the audio signal, a webserver is included. The webserver should be started after the GRC flowgraph. Before running the webserver, be sure to install its [dependences](https://github.com/SanchezCris/SDR-Automatic-Speech-Recognition/blob/main/README.md#installation).

   1. Open a terminal at ``SDR-Automatic-Speech-Recognition/app/``.
   2. ``$ conda activate sdr``
   3. ``$ streamlit run webserver_tcp.py [ARGUMENTS]``
   4. Open a web browser
   5. Browse to ``localhost:8501``
    
[![sl.png](https://i.postimg.cc/4xxsPNG7/sl.png)](https://postimg.cc/56ThNJ6b)

## Installation

GNU Radio is a dependence for ``fm_receive_tcp.grc``. I recommend installing it with this [Ubuntu image](https://drive.google.com/file/d/1_R5C6GQj89v0KfQvk3u3zDcED1a0o-Mh/view).

### Webserver Dependencies

If using ``webserver_tcp.py``, you'll need to install the following Python packages.

    $ conda activate sdr
    $ pip install numpy 
    $ pip install scipy
    $ pip install speechrecognition
    $ pip install streamlit

## Recommendations

Perform the tests in an open space, preferably without nearby appliances, with the antenna placed vertically.

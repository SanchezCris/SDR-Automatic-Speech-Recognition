#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: popuser
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class fm_example(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_example")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000*10
        self.tap_up = tap_up = firdes.low_pass(1.0, samp_rate, 30000,500, firdes.WIN_HAMMING, 6.76)
        self.level = level = 0.3

        ##################################################
        # Blocks
        ##################################################
        self._level_range = Range(0, 1, 0.1, 0.3, 200)
        self._level_win = RangeWidget(self._level_range, self.set_level, 'level', "counter_slider", float)
        self.top_grid_layout.addWidget(self._level_win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccf(
                interpolation=1,
                decimation=2,
                taps=tap_up,
                fractional_bw=None)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=10,
                decimation=1,
                taps=tap_up,
                fractional_bw=None)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/popuser/Desktop/SDR-ASR/app/audios/locutor.wav', True)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, 753.952e3, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_tcp_server_sink_0 = blocks.tcp_server_sink(gr.sizeof_gr_complex*1, '127.0.0.1', 40868, True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(5*level)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(1, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1)
        self.band_pass_filter_0 = filter.fir_filter_fcc(
            1,
            firdes.complex_band_pass(
                1,
                samp_rate,
                90000,
                150000,
                100,
                firdes.WIN_HAMMING,
                6.76))
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=120000,
        	audio_decim=5,
        	deviation=75000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=75e-6,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_tcp_server_sink_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_fm_demod_cf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_example")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, 90000, 150000, 100, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_tap_up(self):
        return self.tap_up

    def set_tap_up(self, tap_up):
        self.tap_up = tap_up
        self.rational_resampler_xxx_0.set_taps(self.tap_up)
        self.rational_resampler_xxx_0_0.set_taps(self.tap_up)

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level
        self.blocks_multiply_const_vxx_0.set_k(5*self.level)





def main(top_block_cls=fm_example, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()

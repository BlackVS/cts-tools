#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RX to FILE
# Author: VVS
# GNU Radio version: 3.8.2.0

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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from rf_over_ip_source import rf_over_ip_source  # grc-generated hier_block
import epy_mkfifo  # embedded python module
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from gnuradio import qtgui

class rx_to_file(gr.top_block, Qt.QWidget):

    def __init__(self, config_file_path="./config.cfg", rx_frequency=900000000, server_ip="127.0.0.1", throttle=1, zmq_rx_timeout=1000):
        gr.top_block.__init__(self, "RX to FILE")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RX to FILE")
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

        self.settings = Qt.QSettings("GNU Radio", "rx_to_file")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.config_file_path = config_file_path
        self.rx_frequency = rx_frequency
        self.server_ip = server_ip
        self.throttle = throttle
        self.zmq_rx_timeout = zmq_rx_timeout

        ##################################################
        # Variables
        ##################################################
        self.config_file = config_file = config_file_path
        self._server_port_base_config = configparser.ConfigParser()
        self._server_port_base_config.read(config_file)
        try: server_port_base = self._server_port_base_config.getint('main', "server_port_base")
        except: server_port_base = 10000
        self.server_port_base = server_port_base
        self._server_bw_per_port_config = configparser.ConfigParser()
        self._server_bw_per_port_config.read(config_file)
        try: server_bw_per_port = self._server_bw_per_port_config.getint('main', "server_bw_per_port")
        except: server_bw_per_port = 1000000
        self.server_bw_per_port = server_bw_per_port
        self.server_port = server_port = int(server_port_base + (rx_frequency / server_bw_per_port))
        self._server_address_format_config = configparser.ConfigParser()
        self._server_address_format_config.read(config_file)
        try: server_address_format = self._server_address_format_config.get("main", "server_address_format")
        except: server_address_format = "tcp://%s:%d"
        self.server_address_format = server_address_format
        self.server_address = server_address = server_address_format % (server_ip, server_port) if server_address_format != "" else ""
        self.samp_rate = samp_rate = 500000

        ##################################################
        # Blocks
        ##################################################
        self.rf_over_ip_source_0 = rf_over_ip_source(
            parent=self if 'self' in locals() else None,
            rx_frequency=rx_frequency,
            samp_rate=samp_rate,
            server_address_format=server_address_format,
            server_bw_per_port=server_bw_per_port,
            server_ip=server_ip,
            server_port_base=server_port_base,
            throttle=throttle,
            zmq_rx_timeout=zmq_rx_timeout,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', "")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, os.path.join(os.path.expanduser('~'), "cts.raw"), False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.rf_over_ip_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rf_over_ip_source_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.rf_over_ip_source_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.rf_over_ip_source_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rx_to_file")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_config_file_path(self):
        return self.config_file_path

    def set_config_file_path(self, config_file_path):
        self.config_file_path = config_file_path
        self.set_config_file(self.config_file_path)

    def get_rx_frequency(self):
        return self.rx_frequency

    def set_rx_frequency(self, rx_frequency):
        self.rx_frequency = rx_frequency
        self.set_server_port(int(self.server_port_base + (self.rx_frequency / self.server_bw_per_port)))
        self.rf_over_ip_source_0.set_rx_frequency(self.rx_frequency)

    def get_server_ip(self):
        return self.server_ip

    def set_server_ip(self, server_ip):
        self.server_ip = server_ip
        self.set_server_address(self.server_address_format % (self.server_ip, self.server_port) if self.server_address_format != "" else "")
        self.rf_over_ip_source_0.set_server_ip(self.server_ip)

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, throttle):
        self.throttle = throttle
        self.rf_over_ip_source_0.set_throttle(self.throttle)

    def get_zmq_rx_timeout(self):
        return self.zmq_rx_timeout

    def set_zmq_rx_timeout(self, zmq_rx_timeout):
        self.zmq_rx_timeout = zmq_rx_timeout
        self.rf_over_ip_source_0.set_zmq_rx_timeout(self.zmq_rx_timeout)

    def get_config_file(self):
        return self.config_file

    def set_config_file(self, config_file):
        self.config_file = config_file
        self._server_address_format_config = configparser.ConfigParser()
        self._server_address_format_config.read(self.config_file)
        if not self._server_address_format_config.has_section("main"):
        	self._server_address_format_config.add_section("main")
        self._server_address_format_config.set("main", "server_address_format", str(None))
        self._server_address_format_config.write(open(self.config_file, 'w'))
        self._server_bw_per_port_config = configparser.ConfigParser()
        self._server_bw_per_port_config.read(self.config_file)
        if not self._server_bw_per_port_config.has_section('main'):
        	self._server_bw_per_port_config.add_section('main')
        self._server_bw_per_port_config.set('main', "server_bw_per_port", str(None))
        self._server_bw_per_port_config.write(open(self.config_file, 'w'))
        self._server_port_base_config = configparser.ConfigParser()
        self._server_port_base_config.read(self.config_file)
        if not self._server_port_base_config.has_section('main'):
        	self._server_port_base_config.add_section('main')
        self._server_port_base_config.set('main', "server_port_base", str(None))
        self._server_port_base_config.write(open(self.config_file, 'w'))

    def get_server_port_base(self):
        return self.server_port_base

    def set_server_port_base(self, server_port_base):
        self.server_port_base = server_port_base
        self.set_server_port(int(self.server_port_base + (self.rx_frequency / self.server_bw_per_port)))
        self.rf_over_ip_source_0.set_server_port_base(self.server_port_base)

    def get_server_bw_per_port(self):
        return self.server_bw_per_port

    def set_server_bw_per_port(self, server_bw_per_port):
        self.server_bw_per_port = server_bw_per_port
        self.set_server_port(int(self.server_port_base + (self.rx_frequency / self.server_bw_per_port)))
        self.rf_over_ip_source_0.set_server_bw_per_port(self.server_bw_per_port)

    def get_server_port(self):
        return self.server_port

    def set_server_port(self, server_port):
        self.server_port = server_port
        self.set_server_address(self.server_address_format % (self.server_ip, self.server_port) if self.server_address_format != "" else "")

    def get_server_address_format(self):
        return self.server_address_format

    def set_server_address_format(self, server_address_format):
        self.server_address_format = server_address_format
        self.set_server_address(self.server_address_format % (self.server_ip, self.server_port) if self.server_address_format != "" else "")
        self.rf_over_ip_source_0.set_server_address_format(self.server_address_format)

    def get_server_address(self):
        return self.server_address

    def set_server_address(self, server_address):
        self.server_address = server_address

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.rf_over_ip_source_0.set_samp_rate(self.samp_rate)




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--rx-frequency", dest="rx_frequency", type=intx, default=900000000,
        help="Set RX Frequency [default=%(default)r]")
    parser.add_argument(
        "--server-ip", dest="server_ip", type=str, default="127.0.0.1",
        help="Set Server IP [default=%(default)r]")
    parser.add_argument(
        "--throttle", dest="throttle", type=intx, default=1,
        help="Set Throttle [default=%(default)r]")
    parser.add_argument(
        "--zmq-rx-timeout", dest="zmq_rx_timeout", type=intx, default=1000,
        help="Set ZMQ RX Timeout [default=%(default)r]")
    return parser


def main(top_block_cls=rx_to_file, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(rx_frequency=options.rx_frequency, server_ip=options.server_ip, throttle=options.throttle, zmq_rx_timeout=options.zmq_rx_timeout)

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

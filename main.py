#!/usr/bin/env python3.5
__author__ = 'jnejati'

import json
import shutil
import os
from urllib.parse import urlparse
import time
import subprocess
import logging
import timeit
import sys


def main(out_path, sites_file, iterations):
    start = timeit.default_timer()
    with open(sites_file) as _sites:
        for _site in _sites:
            time.sleep(5)
            _site = _site.strip()
            logging.info('Navigating to: ' + _site)
            s1 = urlparse(_site)
            _site_data_folder = os.path.join(out_path, s1.netloc)
            if not os.path.isdir(_site_data_folder):
                os.mkdir(_site_data_folder)
            for run_no in range(iterations):
                _run_data_folder = os.path.join(_site_data_folder, 'run_' + str(run_no))
                if not os.path.isdir(_run_data_folder):
                    os.mkdir(_run_data_folder)
                    _subfolders = ['trace', 'screenshot', 'analysis', 'summary']
                    for folder in _subfolders:
                        os.mkdir(os.path.join(_run_data_folder, folder))
                logging.info('Current site: ' + _site + ' - run_no: ' + str(run_no))
                _trace_folder = os.path.join(_run_data_folder, 'trace')
                _screenshot_folder = os.path.join(_run_data_folder, 'screenshot')
                _summary_folder = os.path.join(_run_data_folder, 'summary')
                _trace_file = os.path.join(_trace_folder, str(run_no) + '_' + s1.netloc)
                _screenshot_file = os.path.join(_screenshot_folder, str(run_no) + '_' + s1.netloc)
                _summary_file = os.path.join(_summary_folder, str(run_no) + '_' + s1.netloc)
                logging.info(_trace_file, _screenshot_file, _summary_file)
                time.sleep(5)
                try:
                    _node_cmd = ['node', 'chrome_launcher.js', _site,  _trace_file, _summary_file, _screenshot_file]
                    _cmd =  _node_cmd
                    subprocess.call(_cmd, timeout = 60)
                except subprocess.TimeoutExpired:
                    logging.error("Timeout:  " +  _site + ' - ' + run_no)
                time.sleep(5)
    stop = timeit.default_timer()
    logging.info(100*'-' + '\nTotal time: ' + str(stop -start))

# Use config files for command line
if __name__ == '__main__':
    websites_file = sys.argv[1]
    iterations = sys.argv[2]
    config_file = 'confs/netProfiles.json'
    if sys.argv[3]:
        config_file = sys.argv[3]
    with open(config_file, 'r') as f:
        # Todo: Loop through these
        net_profiles = json.load(f)
        net_profile = net_profiles[0]
        output_path = net_profile['device_type'] + '_' + net_profile['name']
        main(output_path, websites_file, iterations)

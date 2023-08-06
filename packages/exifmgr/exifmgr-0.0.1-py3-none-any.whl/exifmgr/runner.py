#!/usr/bin/env python

EXIFTOOL="/opt/Image-ExifTool-12.41/exiftool"

import argparse
import logging
import os

import progressbar

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', action='store_true', help='action help')
    parser.add_argument('-d', '--debug', action='store_true', help='debug help')
    parser.add_argument('directory')
    args = parser.parse_args()

    if args.debug==True:
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

    logging.debug(args)

    def get_kv_for_result_line(line):
        corrected = line.split(":")
        corrected[0] = corrected[0].strip()
        corrected[0] = corrected[0].lstrip()
        corrected[1] = corrected[1].strip()
        corrected[1] = corrected[1].lstrip()
        logging.debug(corrected)
        return corrected

    def process_file(directory, filename):
        full_filename = os.path.join(directory, filename)
        if not os.path.isfile(full_filename):
            logging.error("ISSUE WITH %s" % full_filename)
            return None
        command = "%s %s" % (EXIFTOOL, full_filename)
        _result = []
        result = {}
        with os.popen(command) as f:
            _result = (f.readlines())
        for line in _result:
            corrected_line = get_kv_for_result_line(line)
            logging.debug(corrected_line)
            result[corrected_line[0]] = corrected_line[1]
        result['full_filename_path'] = full_filename
        logging.debug(result)
        return result

    def process(directory, real_run=False):
        file_list = os.listdir(directory)
        logging.debug(file_list)

        lens_info = {}
        all_results = []

        for filename in progressbar.progressbar(file_list):
            try:
                result = process_file(directory, filename)
                all_results.append(result)
                try:
                    logging.debug(result["Lens ID"])
                    result["lens_id_path"] = result["Lens ID"].replace(" ", "_").replace("..", "_").replace("/", "_").replace("|", "_")
                    full_directory = os.path.join(directory, result["lens_id_path"])
                    logging.debug(full_directory)

                    if real_run:
                        logging.debug("Making directory")
                        if not os.path.isfile(full_directory) and not os.path.exists(full_directory):
                            os.makedirs(full_directory)
                        new_full_filename = os.path.join(full_directory, filename)
                        logging.debug(result["full_filename_path"])
                        logging.debug(new_full_filename)
                        os.replace(result["full_filename_path"], new_full_filename)

                    try:
                        lens_info[result["Lens ID"]] = lens_info[result["Lens ID"]] + 1
                    except:
                        lens_info[result["Lens ID"]] = 1
                    logging.debug(lens_info[result["Lens ID"]])
                except Exception as e:
                    logging.debug(e)
                    logging.debug("NO LENS ID")
            except Exception(e):
                logging.debug(e)
        logging.info(all_results)
        logging.info(len(all_results))

    def real_run(directory):
        logging.debug("=== Real Run ===")
        process(directory, True)
    def dry_run(directory):
        logging.debug("=== Dry Run ===")
        process(directory)

    if args.action==True:
        real_run(args.directory)
    else:
        dry_run(args.directory)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    # main(sys.argv[1:])
    main()

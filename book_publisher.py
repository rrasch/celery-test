import cmdlib
import glob
import logging
import os
import tempfile
import uuid

class BookPublisher:

#   bin_dir = "/usr/local/dlib/book-publisher/bin"
    bin_dir = f"{os.environ['HOME']}/work/book-publisher"

    tmp_rootdir = "/content/prod/rstar/tmp"

    def __init__(self, args):
        self.args = args
        self.cmd = cmdlib.Cmd(args)

    def create_derivatives(self):
        return self._exec_cmd("create-deriv-images.pl")

    def stitch_pages(self):
        return self._exec_cmd("stitch-pages.pl")

    def create_pdf(self):
        return self._exec_cmd("create-pdf.pl")

    def create_ocr(self):
        return self._exec_cmd("create-ocr.pl")

    def create_map(self):
        return self._exec_cmd("gen-kml.pl")

    def gen_all(self):
        return self._exec_cmd("create-deriv-images.pl",
                      "stitch-pages.pl",
                      "create-pdf.pl")

    def shrink_pdf(self):
        shrink_cmd = (f"{self.bin_dir}/shrink-aco-pdf.py"
                      f" {self.args.input_path}"
                      f" {self.args.output_path}")
        return self.cmd.do_cmd(shrink_cmd)

    def _exec_cmd(self, *script_names):
        if self.args.rstar_dir:
            return self.cmd.do_cmd(*script_names)
        else:
            return self._rstar_wrap(*script_names)

    def _rstar_wrap(self, *script_names):
        mets_file = next(
            iter(glob.glob(f"{self.args.input_path}/*_mets.xml")),
            None)
        if mets_file:
            logging.debug(f"METS file: {mets_file}")
            id = os.path.basename(mets_file).replace("_mets.xml", "")
        else:
            logging.warn("Can't find METS file. Generating random id ...")
            id = uuid.uuid1()
        logging.debug(f"wip id: {id}")
        with tempfile.TemporaryDirectory('task-queue') as dir:
            rstar_dir = f"{dir}/wip/se/{id}"
            data_dir  = f"{rstar_dir}/data"
            aux_dir   = f"{rstar_dir}/aux"
            os.makedirs(rstar_dir)
            os.symlink(self.args.input_path, data_dir)
            os.symlink(self.args.output_path, aux_dir)
            cmds = []
            for script_name in script_names:
                rstar_cmd = (f"{BookPublisher.bin_dir}/{script_name} "
                             f"-t {BookPublisher.tmp_rootdir} "
                             f"-q -r {dir} {self.args.extra_args} {id}")
                logging.debug(f"rstar_wrap cmd: {rstar_cmd}")
                cmds.append(rstar_cmd)
            return self.cmd.do_cmd(*cmds)


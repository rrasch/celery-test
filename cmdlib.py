import logging
import subprocess

class Cmd:

    def __init__(self, args):
        self.args = args

    def do_cmd(self, *script_names):
        total_output = ""
        success = True
        for script_name in script_names:
            if self.args.rstar_dir and " -r " not in script_name:
                cmd = (f"{script_name} -q -r {self.args.rstar_dir} "
                       f"{self.args.extra_args} "
                       f"{' '.join(self.args.identifiers)}")
            else:
                cmd = f"{script_name}"
            logging.debug(f"Executing '{cmd}'")
            try:
                process = subprocess.run(cmd,
                                         check=True,
                                         shell=True,
                                         errors="replace",
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
                total_output += process.stdout
                logging.debug("Output: %s", process.stdout)
            except subprocess.CalledProcessError as cpe:
                logging.exception(cpe)
                logging.error("Output: %s", cpe.output)
                total_output += cpe.output
                success = False
                break
        logging.debug("Exiting Cmd.do_cmd()")
        return { "success":success, "output": total_output }


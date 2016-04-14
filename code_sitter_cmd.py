#!/usr/bin/env python
import sys, os, threading, json
from subprocess import Popen, PIPE

class RunCmd(threading.Thread):
    def __init__(self, cmd, outpipe, cwd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.stdout = outpipe
        self.cwd = cwd
        self.timeout = timeout

    def run(self):
        self.p = Popen(self.cmd, stdout=self.stdout, cwd=self.cwd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            print "RunCmd output:\n%s\n"%self.p.stdout.read()
            self.join()

def subcommand(cmd, cmdlist, path, prefix):
    proc = Popen(cmdlist, stdout=PIPE, cwd=path)
    cmd_output = ""
    while proc.poll() is None:
       cmd_output += proc.stdout.readline()
    cmd_output += proc.stdout.read()
    if proc.returncode != 0:
        print "%sCommand failure: %s"%(prefix, cmd)
        print "%sFull log:\n%s\n"%(prefix, cmd_output)
        print "%sCommand '%s' failed with error code %d"%(prefix, cmd, proc.returncode)
        sys.exit(-1)
    print "%sCommand completed successfully: %s"%(prefix, cmd)


def build_recipe(path, name, target, config, run_qemu, prefix):
    full_path = os.path.join(path, name)
    try:
        qemu_path = config['qemu-path']
        qemu_bin = os.path.join(qemu_path, config['qemu-bin'])
        qemu_cmd = [qemu_bin] + config['qemu-args'].split(' ')
    except Exception as e:
        print "Configuration issue: can't create qemu command: %s"%str(e)
        sys.exit(-1)
    print "%sBuilding %s:%s:"%(prefix, name,target)
    subcommand("make mrproper", ['make', 'mrproper'], full_path, "%s  "%prefix)
    subcommand("make distclean", ['make', 'distclean'], full_path, "%s  "%prefix)
    subcommand("make %s"%target, ['make', target], full_path, "%s  "%prefix)
    subcommand("make config", ['make', 'config'], full_path, "%s  "%prefix)
    subcommand("make programs", ['make', 'programs'], full_path, "%s  "%prefix)
    subcommand("make", ['make', 'all'], full_path, "%s  "%prefix)
    if run_qemu:
        RunCmd(qemu_cmd, PIPE, full_path, 5).Run()
    print "%sBuilding %s:%s is a success.\n"%(prefix, name,target)

def setup_recipe(path, name, prefix):
    full_path = os.path.join(path, name)
    print "%sPreparing %s/IMP."%(prefix, name)
    subcommand("sh setup_kernel.sh", ['sh', 'setup_kernel.sh'], full_path, "%s  "%prefix)

def build_recipe_C(path, name, target, config, run_qemu, prefix):
    build_recipe(path, name, target, config, run_qemu, prefix)

def build_recipe_SM(path, name, target, config, run_qemu, prefix):
    setup_recipe(path, name, prefix)
    build_recipe(os.path.join(path, name), "IMP", target, config, run_qemu, prefix)

import os
import shutil


def snowglobes(snowglobes):
    """Copies snowglobes installation into working directory
    Couldn't find a way around this without going into the snowglobes code
    and altering directory paths
    Input: snowglobes: directory path to snowglobes installation"""

    path1 = "./"
    if not os.path.isdir(path1):
        os.makedirs(path1)
    fullpath = os.path.join(path1, "output")
    if not os.path.isdir(fullpath):
       os.makedirs(fullpath)
    fullpath = os.path.join(path1, "fluxes")
    if not os.path.isdir(fullpath):
       os.makedirs(fullpath)
    fullpath = os.path.join(path1, "out")
    if not os.path.isdir(fullpath):
       os.makedirs(fullpath)
    src = os.path.join(snowglobes,"channels")
    dest = os.path.join(path1,"channels")
    if os.path.isdir(dest):
       shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"backgrounds")
    dest = os.path.join(path1,"backgrounds")
    if os.path.isdir(dest):
       shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"bin")
    dest = os.path.join(path1,"bin")
    if os.path.isdir(dest):
      shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"smear")
    dest = os.path.join(path1,"smear")
    if os.path.isdir(dest):
         shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"xscns")
    dest = os.path.join(path1,"xscns")
    if os.path.isdir(dest):
         shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"effic")
    dest = os.path.join(path1,"effic")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"glb")
    dest = os.path.join(path1,"glb")
    if os.path.isdir(dest):
       shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"src")
    dest = os.path.join(path1,"src")
    if os.path.isdir(dest):
       shutil.rmtree(dest)
    shutil.copytree(src,dest)
    src = os.path.join(snowglobes,"supernova.pl")
    dest = os.path.join(path1,"supernova.pl")
    if os.path.isfile(dest):
       os.remove(dest)
    os.symlink(src, dest)
    src =os.path.join(snowglobes,"detector_configurations.dat")
    dest = os.path.join(path1,"detector_configurations.dat")
    if os.path.isfile(dest):
       os.remove(dest)
    shutil.copyfile(src,dest)
    src = os.path.join(snowglobes,"make_event_table.pl")
    dest = os.path.join(path1,"make_event_table.pl")
    if os.path.isfile(dest):
        os.remove(dest)
    os.symlink(src,dest)

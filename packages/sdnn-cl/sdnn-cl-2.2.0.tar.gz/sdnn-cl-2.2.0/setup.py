# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=invalid-name, exec-used
"""Setup TVM package."""
import os
import shutil
import sys
import sysconfig
import platform

from setuptools import find_packages
from setuptools.dist import Distribution

# need to use distutils.core for correct placement of cython dll
if "--inplace" in sys.argv:
    from distutils.core import setup
    from distutils.extension import Extension
else:
    from setuptools import setup
    from setuptools.extension import Extension

CURRENT_DIR = os.path.dirname(__file__)
FFI_MODE = os.environ.get("TVM_FFI", "auto")
CONDA_BUILD = os.getenv("CONDA_BUILD") is not None

#*BEGIN*#
## function:add this function for clear workspace
## data: 22-7-6
def clear_wheel_space():
    # Wheel cleanup
    if os.path.exists("MANIFEST.in"):
        os.remove("MANIFEST.in")

    ## remove pkg
    pkg_path = get_pkgconfig_path()
    _, pkg_name = os.path.split(pkg_path)
    path_to_be_removed = f"tvm/{pkg_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove xrp
    xrp_name = "src"
    path_to_be_removed = f"tvm/{xrp_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove tophub
    tophub_name = "vendor/tophub"
    path_to_be_removed = f"tvm/{tophub_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove sdrv
    sdrv_name = "vendor/sdrv"
    path_to_be_removed = f"tvm/{sdrv_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove include
    folder_name = "include"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove 3rdparty
    folder_name = "3rdparty"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove customer op
    folder_name = "customer_op"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove backend_plugins
    folder_name = "backend_plugins"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove x86-64 linux runtime lib
    folder_name = "build"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove linux runtime lib
    folder_name = "build_aarch64-linux"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove android runtime lib
    folder_name = "build_aarch64-android"
    path_to_be_removed = f"tvm/{folder_name}"
    if os.path.isdir(path_to_be_removed):
        shutil.rmtree(path_to_be_removed)

    ## remove tvm lib
    for path in LIB_LIST:
        _, libname = os.path.split(path)
        path_to_be_removed = f"tvm/{libname}"

        if os.path.isfile(path_to_be_removed):
            os.remove(path_to_be_removed)

        if os.path.isdir(path_to_be_removed):
            shutil.rmtree(path_to_be_removed)
#*END*#


def get_lib_path():
    """Get library path, name and version"""
    # We can not import `libinfo.py` in setup.py directly since __init__.py
    # Will be invoked which introduces dependencies
    libinfo_py = os.path.join(CURRENT_DIR, "./tvm/_ffi/libinfo.py")
    libinfo = {"__file__": libinfo_py}
    exec(compile(open(libinfo_py, "rb").read(), libinfo_py, "exec"), libinfo, libinfo)
    version = libinfo["__version__"]
    if not CONDA_BUILD:
        lib_path = libinfo["find_lib_path"]()
        libs = [lib_path[0]]
        if "runtime" not in libs[0]:
            for name in lib_path[1:]:
                if "runtime" in name:
                    libs.append(name)
                    break

        # Add standalone_crt, if present
        for name in lib_path:
            candidate_path = os.path.join(os.path.dirname(name), "standalone_crt")
            if os.path.isdir(candidate_path):
                libs.append(candidate_path)
                break

        # Add microTVM template projects
        for name in lib_path:
            candidate_path = os.path.join(os.path.dirname(name), "microtvm_template_projects")
            if os.path.isdir(candidate_path):
                libs.append(candidate_path)
                break

    else:
        libs = None

    return libs, version

def get_pkgconfig_path():
    pkg = os.path.join(CURRENT_DIR, "../pkgconfig")
    return pkg

def get_xrplib_path():
    xrp_path = os.path.join(CURRENT_DIR, "..", "src", "runtime", "contrib", "slimai")
    return xrp_path

def git_describe_version(original_version):
    """Get git describe version."""
    ver_py = os.path.join(CURRENT_DIR, "..", "version.py")
    libver = {"__file__": ver_py}
    exec(compile(open(ver_py, "rb").read(), ver_py, "exec"), libver, libver)
    _, gd_version = libver["git_describe_version"]()
    if gd_version != original_version and "--inplace" not in sys.argv:
        print("Use git describe based version %s" % gd_version)
    return gd_version


LIB_LIST, __version__ = get_lib_path()
__version__ = git_describe_version(__version__)

def config_cython():
    """Try to configure cython and return cython configuration"""
    if FFI_MODE not in ("cython"):
        if os.name == "nt" and not CONDA_BUILD:
            print("WARNING: Cython is not supported on Windows, will compile without cython module")
            return []
        sys_cflags = sysconfig.get_config_var("CFLAGS")
        if sys_cflags and "i386" in sys_cflags and "x86_64" in sys_cflags:
            print("WARNING: Cython library may not be compiled correctly with both i386 and x64")
            return []
    try:
        from Cython.Build import cythonize

        # from setuptools.extension import Extension
        if sys.version_info >= (3, 0):
            subdir = "_cy3"
        else:
            subdir = "_cy2"
        ret = []
        path = "tvm/_ffi/_cython"
        extra_compile_args = ["-std=c++14", "-DDMLC_USE_LOGGING_LIBRARY=<tvm/runtime/logging.h>"]
        if os.name == "nt":
            library_dirs = ["tvm", "../build/Release", "../build"]
            libraries = ["tvm"]
            extra_compile_args = None
            # library is available via conda env.
            if CONDA_BUILD:
                library_dirs = [os.environ["LIBRARY_LIB"]]
        else:
            library_dirs = None
            libraries = None

        for fn in os.listdir(path):
            if not fn.endswith(".pyx"):
                continue
            ret.append(
                Extension(
                    "tvm._ffi.%s.%s" % (subdir, fn[:-4]),
                    ["tvm/_ffi/_cython/%s" % fn],
                    include_dirs=[
                        "../include/",
                        "../3rdparty/dmlc-core/include",
                        "../3rdparty/dlpack/include",
                    ],
                    extra_compile_args=extra_compile_args,
                    library_dirs=library_dirs,
                    libraries=libraries,
                    language="c++",
                )
            )
        return cythonize(ret, compiler_directives={"language_level": 3})
    except ImportError as error:
        if FFI_MODE == "cython":
            raise error
        print("WARNING: Cython is not installed, will compile without cython module")
        return []


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False


include_libs = False
wheel_include_libs = False
if not CONDA_BUILD:
    if "bdist_wheel" in sys.argv:
        wheel_include_libs = True
    else:
        include_libs = True

setup_kwargs = {}

clear_wheel_space()

# For bdist_wheel only
if wheel_include_libs:
    with open("MANIFEST.in", "w") as fo:
        for path in LIB_LIST:
            if os.path.isfile(path):
                shutil.copy(path, os.path.join(CURRENT_DIR, "tvm"))
                _, libname = os.path.split(path)
                fo.write(f"include tvm/{libname}\n")

            if os.path.isdir(path):
                _, libname = os.path.split(path)
                shutil.copytree(path, os.path.join(CURRENT_DIR, "tvm", libname))
                fo.write(f"recursive-include tvm/{libname} *\n")

        #*BEGIN*#
        ## package source file and library to whl
        ## data: 22-7-6
        ## sdnn-build
        fo.write(f"include tvm/sdrv/bin/sdnn_build\n")

        ## pkg
        pkg_path = get_pkgconfig_path()
        _, pkg_name = os.path.split(pkg_path)
        shutil.copytree(pkg_path, os.path.join(CURRENT_DIR, "tvm", pkg_name))
        fo.write(f"recursive-include tvm/{pkg_name} *\n")

        ## xrp lib
        xrp_path = get_xrplib_path()
        xrp_name = "src/runtime/contrib/slimai"
        shutil.copytree(xrp_path, os.path.join(CURRENT_DIR, "tvm", xrp_name))
        fo.write(f"recursive-include tvm/{xrp_name} *\n")

        ## tophub
        tophub_path = os.path.join(CURRENT_DIR, "..", "vendor", "tophub")
        tophub_name = "vendor/tophub"
        shutil.copytree(tophub_path, os.path.join(CURRENT_DIR, "tvm", tophub_name))
        fo.write(f"recursive-include tvm/{tophub_name} *\n")

        ## sdrv
        sdrv_path = os.path.join(CURRENT_DIR, "..", "vendor", "sdrv")
        sdrv_name = "vendor/sdrv"
        shutil.copytree(sdrv_path, os.path.join(CURRENT_DIR, "tvm", sdrv_name))
        fo.write(f"recursive-include tvm/{sdrv_name} *\n")

        ## include
        include_path = os.path.join(CURRENT_DIR, "..", "include")
        include_name = "include"
        shutil.copytree(include_path, os.path.join(CURRENT_DIR, "tvm", include_name))
        fo.write(f"recursive-include tvm/{include_name} *\n")

        ## 3rdparty/dlpack
        dlpack_path = os.path.join(CURRENT_DIR, "..", "3rdparty/dlpack")
        dlpack_name = "3rdparty/dlpack"
        shutil.copytree(dlpack_path, os.path.join(CURRENT_DIR, "tvm", dlpack_name))
        fo.write(f"recursive-include tvm/{dlpack_name} *\n")

        ## 3rdparty/dmlc-core
        dmlc_path = os.path.join(CURRENT_DIR, "..", "3rdparty/dmlc-core")
        dmlc_name = "3rdparty/dmlc-core"
        shutil.copytree(dmlc_path, os.path.join(CURRENT_DIR, "tvm", dmlc_name))
        fo.write(f"recursive-include tvm/{dmlc_name} *\n")

        ## customer_op
        customer_op_path = os.path.join(CURRENT_DIR, "..", "customer_op")
        customer_op_name = "customer_op"
        shutil.copytree(customer_op_path,  os.path.join(CURRENT_DIR, "tvm", customer_op_name))
        fo.write(f"recursive-include tvm/{customer_op_name} *\n")

        ## backend_plugins
        metric_plugins_path = os.path.join(CURRENT_DIR, "..", "backend_plugins")
        metric_plugins_name = "backend_plugins"
        shutil.copytree(metric_plugins_path,  os.path.join(CURRENT_DIR, "tvm", metric_plugins_name))
        fo.write(f"recursive-include tvm/{metric_plugins_name} *\n")

        ## x86-64 linux runtime lib
        linux_runtime_path = os.path.join(CURRENT_DIR, "..", "build/libtvm_runtime.so")
        linux_runtime_name = "build"
        if not os.path.exists(os.path.join(CURRENT_DIR, "tvm", linux_runtime_name)):
            os.makedirs(os.path.join(CURRENT_DIR, "tvm", linux_runtime_name))
        shutil.copy(linux_runtime_path,  os.path.join(CURRENT_DIR, "tvm", linux_runtime_name))
        fo.write(f"include tvm/build/libtvm_runtime.so\n")

        ## linux runtime lib
        linux_runtime_path = os.path.join(CURRENT_DIR, "..", "build_aarch64-linux/libtvm_runtime.so")
        linux_runtime_name = "build_aarch64-linux"
        if not os.path.exists(os.path.join(CURRENT_DIR, "tvm", linux_runtime_name)):
            os.makedirs(os.path.join(CURRENT_DIR, "tvm", linux_runtime_name))
        shutil.copy(linux_runtime_path,  os.path.join(CURRENT_DIR, "tvm", linux_runtime_name))
        fo.write(f"include tvm/build_aarch64-linux/libtvm_runtime.so\n")

        ## android runtime lib
        android_runtime_path = os.path.join(CURRENT_DIR, "..", "build_aarch64-android/libtvm_runtime.so")
        android_runtime_name = "build_aarch64-android"
        if not os.path.exists(os.path.join(CURRENT_DIR, "tvm", android_runtime_name)):
            os.makedirs(os.path.join(CURRENT_DIR, "tvm", android_runtime_name))
        shutil.copy(android_runtime_path,  os.path.join(CURRENT_DIR, "tvm", android_runtime_name))
        fo.write(f"include tvm/build_aarch64-android/libtvm_runtime.so\n")
        #*END*#

    setup_kwargs = {"include_package_data": True}

if include_libs:
    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    for i, path in enumerate(LIB_LIST):
        LIB_LIST[i] = os.path.relpath(path, curr_path)
    setup_kwargs = {"include_package_data": True, "data_files": [("tvm", LIB_LIST)]}


def get_package_data_files():
    # Relay standard libraries
    return ["relay/std/prelude.rly", "relay/std/core.rly"]


# Temporarily add this directory to the path so we can import the requirements generator
# tool.
sys.path.insert(0, os.path.dirname(__file__))
import gen_requirements

sys.path.pop(0)

requirements = gen_requirements.join_requirements()
extras_require = {
    piece: deps for piece, (_, deps) in requirements.items() if piece not in ("all", "core")
}

setup(
    #*BEGIN*#
    ## change the name of  whl
    ## data: 22-7-6
    name="sdnn-cl",
    version=__version__,
    description="SDNN: An End to End Tensor IR/DSL Stack for Deep Learning Systems",
    #*END*#
    zip_safe=False,
    entry_points={"console_scripts": ["tvmc = tvm.driver.tvmc.main:main"]},
    install_requires=requirements["core"][1],
    extras_require=extras_require,
    packages=find_packages(),
    package_dir={"tvm": "tvm"},
    package_data={"tvm": get_package_data_files()},
    distclass=BinaryDistribution,
    url="https://github.com/apache/tvm",
    ext_modules=config_cython(),
    **setup_kwargs,
)

if wheel_include_libs:
    #*BEGIN*#
    ## using function to clear workspace
    ## data: 22-7-6
    clear_wheel_space()
    #*END*#


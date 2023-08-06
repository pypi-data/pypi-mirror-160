#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import sys
import os
import re
import tvm
import json
import shutil
import pkgconfig
import numpy as np
from tvm import relay
from tvm.contrib import cc, ndk
from tvm.relay.op.contrib.slimai import partition_for_slimai, partition_for_slimai_iss
from tvm.relay.op.contrib.slimai import slimai_build_init
from . import ModelLoad

class ModelBuild:
    def __init__(self, host, device, os, opt_level=3,
                    emulation=False, debug=False,
                    elf_mode='merge', elf_build_off=False):
        ## Init Parameters
        self.host = host
        self.device = device
        self.os = os
        self.opt_level = opt_level
        self.emulation = emulation
        self.debug = debug
        self.elf_mode = elf_mode
        self.elf_build_off = elf_build_off

        ## === Model Parameter ===
        # the attribute of model
        self.path = []  # the modle file
        self.dir = ''   # the directory of model
        self.type = '' # the type of model
        self.name = ''
        self.layout = ''
        # shape and type of input
        self.shape_dict = {}
        self.dtype_dict = {}
        self.domain = None
        self.channel_order = None
        self.mean = None
        self.std = None
        ## === Quant Parameter === ##
        # judge model whether is quant
        self.is_quant_model = False
        self.cfg = None   # the cfg file for NPU quant needed
        self.quant_bit = None
        ## === Generate Build Variable ===
        # Target Device Type Object
        self.target = ''
        # Model IR and Params Object
        self.ir = ''
        self.param = ''
        # Output Model Library
        self.runtime_module = ''

        # If slimai device need to init build environment
        if self.device == "slimai":
            slimai_build_init()
    ##=== Utils functions ===##
    def get_model_type(self, path):
        """
        get type of model from path
        """
        assert isinstance(path, list), "function get_model_type input parameter [path] must be list type"
        file_ext = []
        for f in path:
            _,ext = os.path.splitext(f)
            file_ext.append(ext)

        if len(file_ext) == 1:
            if file_ext[0] == '.onnx':
                self.type = 'onnx'
            elif file_ext[0] == '.pb':
                self.type = 'tf'
            elif file_ext[0] == '.tflite':
                self.type = 'tflite'
            else:
                raise SystemExit("Model Type Unknow: [%s]" % file_ext[0])
        elif len(file_ext) == 2:
            if (file_ext[0] == '.prototxt' and file_ext[1] == '.caffemodel') \
            or (file_ext[1] == '.prototxt' and file_ext[0] == '.caffemodel'):
                self.type = 'caffe'
            else:
                raise SystemExit("Model Type Unknow: [%s] [%s]" % (file_ext[0], file_ext[1]))
        else:
            raise SystemExit("The number of model file more than two")

    def get_model_name(self, path):
        """
        get name of model from path
        """
        assert isinstance(path, list), "function get_model_name input parameter [path] must be list type"
        file_name = []
        for f in path:
            _,name = os.path.split(f)
            file_name.append(name)
        if len(file_name) == 1:
            self.name,_ = os.path.splitext(file_name[0])
        elif len(file_name) == 2:
            if '.caffemodel' in file_name[0]:
                self.name,_ = os.path.splitext(file_name[0])
            elif '.caffemodel' in file_name[1]:
                self.name,_ = os.path.splitext(file_name[1])
            else:
                raise SystemExit("Model ERROR: [%s][%s]" % (file_name[0], file_name[1]))
        else:
            raise SystemExit("The number of model file more than two")
        self.name = re.sub(r'-', '_', self.name)

    ##=== Model Parameter Dict ===##
    def create_model_dict(self, args, model_files):
        """
        from command line params args to json dict
        args ---> json dict
        + Param args: the command line parameter
        + Param model_files: the list of files
        """
        assert isinstance(model_files, list), "function create_model_dict input parameter [model_files] must be list type"
        ## create model dict
        model_dict = {}
        model_node = {}
        self.dir,_ = os.path.split(model_files[0])
        model_node['path'] = model_files
        ## Name
        if args.net_name != 'null':
            model_node['name'] = args.net_name
        else:
            self.get_model_name(model_files)
            model_node['name'] = self.name
        ## Type
        if args.net_type != 'null':
            model_node['type'] = args.net_type
        else:
            self.get_model_type(model_files)
            model_node['type'] = self.type
        ## Domain
        if args.domain != 'null':
            model_node['domain'] = args.domain
        else:
            model_node['domain'] = 'Classification'
        ## Channel Order
        if args.channel_order != 'null':
            model_node['channel_order'] = args.channel_order
        else:
            model_node['channel_order'] = 'RGB'
        ## Mean
        if args.mean != 'null':
            assert isinstance(args.mean, str), "mean must be string type"
            model_node['mean'] = [float(i) for i in args.mean.split(',')]
        ## std
        if args.std != 'null':
            assert isinstance(args.std, str), "std must be string type"
            model_node['std'] = [float(i) for i in args.std.split(',')]
        model_dict['model'] = model_node

        ##=== Quant Parameter ===##
        quant_node = {}
        if args.quant_bit != 'null':
            quant_node['bit'] = args.quant_bit

        if quant_node:
            model_dict['quant'] = quant_node
        ##=== configure file ===##
        if args.cfg_file != 'null':
            model_dict['cfg'] = args.cfg_file
        return model_dict

    def revise_model_dict(self, args, model_dict, relative_json_path):
        """
        ##= args + model_dict --> new model_dict
        """
        assert isinstance(model_dict, dict), "function[revise_model_dict] input parameter [model_dict] must be dict"
        model_node = model_dict['model']
        ## Name
        if args.net_name != 'null':
            model_node['name'] = args.net_name
        ## Type
        if args.net_type != 'null':
            model_node['type'] = args.net_type
        ## Domain
        if args.domain != 'null':
            model_node['domain'] = args.domain
        ## Channel Order
        if args.channel_order != 'null':
            model_node['channel_order'] = args.channel_order
        ## Mean
        if args.mean != 'null':
            assert isinstance(args.mean, str), "mean must be string type"
            model_node['mean'] = [float(i) for i in args.mean.split(',')]
        ## std
        if args.std != 'null':
            assert isinstance(args.std, str), "std must be string type"
            model_node['std'] = [float(i) for i in args.std.split(',')]

        ##=== Quant Parameter ===##
        if model_dict.get('quant') == None:
            quant_node = {}
            if args.quant_bit != 'null':
                quant_node['bit'] = args.quant_bit
                model_dict['quant'] = quant_node
        else:
            quant_node = model_dict.get('quant')
            if args.quant_bit != 'null':
                quant_node['bit'] = args.quant_bit

        ##=== configure file ===##
        if args.cfg_file != 'null':
            model_dict['cfg'] = args.cfg_file
        ##===Save JSON File ===##
        json_file_path = os.path.join(relative_json_path, "%s.json" % model_node['name'])
        with open(json_file_path, 'w') as f:
            json.dump(model_dict, f, sort_keys=False, indent=4, separators=(',', ':'))
        return model_dict

    def model_dict_parse(self, model_dict, relative_json_path):
        """
        from json dict to self params
        json dict ---> self params
        """
        assert isinstance(model_dict, dict), "function[model_dict_parse] input parameter [model_dict] must be dict"
        assert isinstance(relative_json_path, str), "function[model_dict_parse] input parameter [relative_json_path] must be string"
        ## Model Path
        if model_dict.get('model') == None:
            raise SystemExit("Model Dict ERROR:", model_dict)
        else:
            model_node = model_dict.get('model')
            ## [1]Path
            if model_node.get('path') == None:
                raise SystemExit("Model Path Must be set!")
            else:
                model_relat_path = []
                for mod_path in model_node.get('path'):
                    model_relat_path.append(os.path.join(relative_json_path, mod_path))
                self.path = model_relat_path
                self.dir,_ = os.path.split(model_relat_path[0])
            ## [2]Type
            if model_node.get('type') == None:
                # auto get model type
                self.get_model_type(self.path)
            else:
                self.type = model_node.get('type')
            ## [3]Name
            if model_node.get('name') == None:
                # if no setup name, then using the model file's name
                self.get_model_name(self.path)
            else:
                self.name = model_node.get('name')
            ## [4]Channel Order
            self.channel_order = model_node.get('channel_order')
            ## [5]Domain
            self.domain = model_node.get('domain')
            ## [6] Mean
            self.mean = model_node.get('mean')
            ## [7] Std
            self.std = model_node.get('std')

        ##--- Quant Parameter ---##
        if model_dict.get('quant') != None:
            quant_node = model_dict.get('quant')
            ## [1]Quant bit
            self.quant_bit = quant_node.get('bit')

        ##=== configure file ===##
        ## [1]CFG File
        self.cfg = model_dict.get('cfg')

    def create_cfg_json(self):
        """
        from self parameter to cfg json file
        """
        model_dict = {}
        model_node = {}
        f_name = []
        for f in self.path:
            _,fn = os.path.split(f)
            f_name.append(fn)
        model_node['path'] = f_name
        if self.channel_order == None:
            model_node['channel_order'] = 'RGB'
        else:
            model_node['channel_order'] = self.channel_order
        if self.domain != None:
            model_node['domain'] = 'Classification'
        else:
            model_node['domain'] = self.domain
        if self.mean != None:
            model_node['mean'] = self.mean
        if self.std != None:
            model_node['std'] = self.std
        model_dict['model'] = model_node

        quant_node = {}
        if self.quant_bit != None:
            quant_node['bit'] = self.quant_bit
        if quant_node != None:
            model_dict['quant'] = quant_node

        if self.cfg != None:
            model_dict['cfg'] = self.cfg
        ##===Save JSON File ===##
        json_file_path = os.path.join(self.dir, "%s.json" % self.name)
        with open(json_file_path, 'w') as f:
            json.dump(model_dict, f, sort_keys=False, indent=4, separators=(',', ':'))

    def create_deploy_json(self, path):
        """
        self params ---> deploy json dict
        """
        model_dict = {}
        model_node = {}
        model_node['name'] = self.name
        model_node['accelerator'] = self.device
        model_node['path'] = "%s.so" % self.name
        if self.domain == None:
            model_node['domain'] = 'Classification'
        else:
            model_node['domain'] = self.domain

        ##=== inputs node ===##
        inputs_array = []
        input_node = {}
        for name, shape in self.shape_dict.items():
            if len(shape) == 4:
                if shape[1] < shape[2] and shape[1] < shape[3]:
                    self.layout = "NCHW"
                    channel = shape[1]
                elif shape[3] < shape[1] and shape[3] < shape[2]:
                    self.layout = "NHWC"
                    channel = shape[3]
                else:
                    raise SystemExit("Layout Unsupport")
            input_node['name'] = name
            if self.layout == None:
                input_node['layout'] = 'NCHW'
            else:
                input_node['layout'] = self.layout
            if self.channel_order == None:
                input_node['channel_order'] = 'RGB'
            else:
                input_node['channel_order'] = self.channel_order
            if self.mean == None:
                input_node['mean'] = [0.0 for i in range(channel)]
            else:
                input_node['mean'] = self.mean
            if self.std == None:
                input_node['std'] = [1.0 for i in range(channel)]
            else:
                input_node['std'] = self.std
            inputs_array.append(input_node)

        model_node['inputs'] = inputs_array
        model_dict['model'] = model_node
        json_file_path = os.path.join(path, '%s.deploy.json' % self.name)
        with open(json_file_path, 'w') as f:
            json.dump(model_dict, f, sort_keys=False, indent=4, separators=(',', ':'))
        print("\033[0;36m****** Generate File: %s.deploy.json\033[0m" % self.name)

    def parse_cfg_file(self, cfg_file):
        """
        This function will parse some information to self
        """
        with open(cfg_file, 'r') as fr:
            for line in fr:
                if re.match(r'^input_data_layout\s*=\s*', line):
                    self.layout = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                elif re.match(r'^channel_order\s*=\s*', line):
                    self.channel_order = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                elif re.match(r'^class\s*=\s*', line):
                    self.domain = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                elif re.match(r'^mean\s*=\s*', line):
                    mean_str = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                    mean_arr = mean_str.split(',')
                    mean_flt = []
                    for m in mean_arr:
                        mean_flt.append(float(m))
                    self.mean = mean_flt
                elif re.match(r'^stddev\s*=\s*', line):
                    std_str = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                    std_arr = std_str.split(',')
                    std_flt = []
                    for s in std_arr:
                        std_flt.append(float(s))
                    self.std = std_flt
                elif re.match(r'^accuracy_level\s*=\s*', line):
                    acc_str = re.split(r'\s*\=\s*', line)[1].rstrip('\n')
                    acc_arr = acc_str.split(',')
                    if len(acc_arr) > 1:
                         self.quant_bit = "auto"
                    else:
                        acc_int = int(acc_arr[0])
                        if acc_int > 3:
                            self.quant_bit = "16bit"
                        else:
                            self.quant_bit = "8bit"

    ##=== generate slimai cfg relative files ===##
    def generate_slimai_cfg_file(self):
        """
        auto generte slimai file
        """
        cfg_path = os.path.abspath(self.dir)
        cfg_file = os.path.join(cfg_path, "%s.autogen.cfg" % self.name)
        os.environ["SLIMAI_CFG_FILE"] = cfg_file
        ## create folder for output
        output_dir = os.path.join(self.dir, "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        ## create foldcfg_pather for imagelist
        imagelist_dir = os.path.join(self.dir, "imagelist")
        if not os.path.exists(imagelist_dir):
            os.makedirs(imagelist_dir)
        with open(cfg_file, "w") as cfg:
            ## PATH
            cfg.writelines("[path]\n")
            cfg.writelines("output_dir = %s/output\n" % cfg_path)
            cfg.writelines("image_dir = %s/imagelist\n" % cfg_path)
            ## NETWORK
            cfg.writelines("[network]\n")
            if self.domain == None:
                cfg.writelines("class = Classification\n")
            else:
                cfg.writelines("class = %s\n" % self.domain)
            if self.is_quant_model:
                cfg.writelines("model_type = quantized\n")
            else:
                cfg.writelines("model_type = float\n")

            if self.channel_order == None:
                cfg.writelines("channel_order = RGB\n")
            else:
                cfg.writelines("channel_order = %s\n" % self.channel_order)

            for name, shape in self.shape_dict.items():
                if len(shape) != 4:
                    cfg.writelines("input_data_layout = NonImage")
                    cfg.writelines("mean = 0.0\n")
                    cfg.writelines("stddev = 1.0\n")
                else:
                    if shape[1] < shape[2] and shape[1] < shape[3]:
                        self.layout = "NCHW"
                        channel = shape[1]
                    elif shape[3] < shape[1] and shape[3] < shape[2]:
                        self.layout = "NHWC"
                        channel = shape[3]
                    else:
                        raise SystemExit("Layout Unsupport")

                    if self.mean == None:
                        m = ",".join([str(0.0) for v in range(channel)])
                    else:
                        m = ",".join([str(v) for v in self.mean])

                    if self.std == None:
                        s = ",".join([str(255.0) for v in range(channel)])
                    else:
                        s = ",".join([str(v) for v in self.std])

                    cfg.writelines("input_data_layout = %s\n" % self.layout)
                    cfg.writelines("mean = %s\n" % m)
                    cfg.writelines("stddev = %s\n" % s)
            ## DATASET
            cfg.writelines("[dataset]\n")
            cfg.writelines("calibration_set = imagelist.txt\n")
            cfg.writelines("calibration_count = 1\n")
            cfg.writelines("validation_set = imagelist.txt\n")
            cfg.writelines("validation_count = 1\n")
            ## QUANTIZATION
            cfg.writelines("[quantization]\n")
            cfg.writelines("range = 98:98\n")
            if self.quant_bit == '8bit' or self.quant_bit == None:
                cfg.writelines("accuracy_level = 3\n")
            elif self.quant_bit == '16bit':
                cfg.writelines("accuracy_level = 4\n")
            else:
                raise AssertionError("quant bit unkown")
            ## PERFORMANCE
            cfg.writelines("[performance]\n")
            cfg.writelines("optimization = level2\n")
        print("\033[0;36m****** Generate File: %s.autogen.cfg\033[0m" % self.name)
        return cfg_file

    def generate_calibration_data(self):
        image_list_file = os.path.join(self.dir, "imagelist/imagelist.txt")
        with open(image_list_file, 'w') as txt:
            for name, shape in self.shape_dict.items():
                cal_data = np.random.randint(0,255, size= shape)
                file_name = "%s.npy" % name
                file_path = os.path.join(self.dir, "imagelist/%s" % file_name)
                np.save(file_path, cal_data)
                txt.writelines("1\n")
                txt.writelines("%s\n" % file_name)

    ##=== Model Build Group ===##
    def ir_layout_convert(self):
        if self.device == "slimai":
            desired_layouts = { 'nn.conv2d': ['NCHW', 'OIHW'],
                                'nn.conv3d': ['NCHW', 'OIHW'],
                                'nn.deformable_conv2d': ['NCHW', 'OIHW'],
                                'nn.conv2d_transpose': ['NCHW', 'OIHW'],
                                'nn.avg_pool2d': ['NCHW', 'OIHW'],
                                'nn.max_pool2d': ['NCHW', 'OIHW'],
                                'nn.global_max_pool2d': ['NCHW', 'OIHW'],
                                'nn.global_avg_pool2d': ['NCHW', 'OIHW']}
            # Convert the layout to NCHW
            # RemoveUnunsedFunctions is used to clean up the graph.
            seq = tvm.transform.Sequential([relay.transform.RemoveUnusedFunctions(),
                                            relay.transform.ConvertLayout(desired_layouts)])
            with tvm.transform.PassContext(opt_level=3):
                self.ir = seq(self.ir)
            #self.ir = relay.transform.DynamicToStatic()(self.ir)

    def get_ir(self):
        """
        get relay ir of models
        """
        ## Step1: SlimAI configure for whether freeze params
        if self.device == "slimai":
            freeze_params=True
        else:
            freeze_params=False
        ## Step2: Create model load object
        ml = ModelLoad(self.path, self.device)
        ## Step3: Convert the model to ir module
        if self.type == "onnx":
            onnx_model, self.shape_dict, self.dtype_dict = ml.onnx()
            print("onnx:", self.shape_dict, self.dtype_dict)
            self.ir, self.param = relay.frontend.from_onnx(onnx_model, self.shape_dict, self.dtype_dict, freeze_params=freeze_params)
        elif self.type == "caffe":
            init_net, predict_net, self.shape_dict, self.dtype_dict = ml.caffe()
            print("caffe:", self.shape_dict, self.dtype_dict)
            #self.ir, self.param = relay.frontend.from_caffe(init_net, predict_net, shape_dict, dtype_dict, freeze_params)
            self.ir, self.param = relay.frontend.from_caffe(init_net, predict_net, self.shape_dict, self.dtype_dict)
        elif self.type == "tf":
            graph, self.shape_dict, self.dtype_dict = ml.tf()
            print("tensorflow:", self.shape_dict, self.dtype_dict)
            self.ir, self.param = relay.frontend.from_tensorflow(graph, self.shape_dict)
            ## convert NHWC To NCHW Layout for onnx
            self.ir_layout_convert()
        elif self.type == "tflite":
            ## delete the env variable
            if os.getenv('SLIMAI_MODEL_PATH') != None:
                del os.environ["SLIMAI_MODEL_PATH"]
            # tflite_model, shape_dict, dtype_dict = ml.tflite()
            tflite_model, self.shape_dict, self.dtype_dict= ml.tflite()
            self.ir, self.param = relay.frontend.from_tflite(tflite_model)
            ## judge model type, float or quant
            assert tflite_model.SubgraphsLength() == 1, "only support one subgraph (main subgraph)"
            subgraph = tflite_model.Subgraphs(0)
            model_inputs = subgraph.InputsAsNumpy()
            for model_input in model_inputs:
                if isinstance(subgraph.Tensors(model_input).Quantization().Scale(0), float) and \
                isinstance(subgraph.Tensors(model_input).Quantization().ZeroPoint(0), int):
                    print("TFLITE Quantization Model")
                    if self.device == "slimai":
                        ## if using slimai device, bypass to_onnx
                        print("Bypass To ONNX")
                        self.is_quant_model = True
                        assert len(self.path) == 1, "TFlite model file more than one"
                        os.environ["SLIMAI_MODEL_PATH"] = self.path[0]
                else:
                    print("TFLITE Float Model")
                    self.is_quant_model = False
                    self.ir_layout_convert()
        else:
            raise SystemExit("[ModelBuild]: Unknow Network Type:", net_type)
        # debug information for model ir save
        if self.debug:
            print(self.ir)
            with open("%s.ir" % self.name, 'w') as f:
                f.write(tvm.ir.save_json(self.ir))
                print("\033[0;36m****** Generate File: %s.ir\033[0m" % self.name)

    def get_target(self):
        """
        get the device target for build params
        """
        if self.emulation:
            if self.device == 'slimai':
                host='llvm'
                device="llvm"
            else:
                raise SystemExit("[ERROR]: emulation mode only support slimai device")
        else:
            if self.host == 'x86_64':
                host='llvm'
                if self.device == 'cpu':
                    device="llvm"
                elif self.device == 'gpu':
                    device = "opencl"
                elif self.device == 'slimai':
                    print("[ModelBuild]: x86_64 do not surport slimai device!!!")
                    sys.exit(1)
                else:
                    print("[ModelBuild]: Unknow device type:", self.device)
                    sys.exit(1)
            elif self.host == 'aarch64':
                if self.os == 'linux':
                    #+dotpro
                    host = "llvm -device=arm_cpu -mtriple=aarch64-linux-gnu -mcpu=cortex-a55 -mattr=+neon,+v8.2a"
                elif self.os == 'android':
                    host = "llvm -device=arm_cpu -mtriple=arm64-linux-android -mcpu=cortex-a55 -mattr=+neon,+v8.2a"
                elif self.os == 'qnx':
                    host = "llvm -device=arm_cpu -mtriple=aarch64-linux-gnu -mcpu=cortex-a55 -mattr=+neon,+v8.2a"
                else:
                    raise SystemExit("[ModelBuild]: Unknow os type:", self.os)

                if self.device == 'cpu':
                    device = host
                elif self.device == 'gpu':
                    device = "opencl -max_num_threads=512"
                elif self.device == 'slimai':
                    device = host
                else:
                    raise SystemExit("[ModelBuild]: Unknow device type:", self.device)
            else:
                raise SystemExit("[ModelBuild]: Unsurported Host Type:", self.host)
        self.target = tvm.target.Target(device, host)

    def run_build(self):
        """
        model build relative opration
        """
        print("[ModelBuild]: Compile Without Auto Scheduler File")
        # step 1: SlimAI device  configure
        if self.device == "slimai":
            ## judge whether enable elf file generate
            if self.elf_build_off:
                os.environ["SLIMAI_COMPILE_DISABLE"]="YES"
            else:
                #if slimai compile step needed to be disable to short the compile time
                # comment consequent two lines, uncomment the third line below
                if os.getenv('SLIMAI_COMPILE_DISABLE') != None:
                    del os.environ["SLIMAI_COMPILE_DISABLE"]

            # configure the slimai cfg file environment
            if self.cfg == None:
                abs_path_cfg = self.generate_slimai_cfg_file()
                self.generate_calibration_data()
            else: ## user setup the cfg file
                if os.path.isfile(self.cfg):
                    ## revise cfg file relation path to be abs path
                    abs_path_cfg = self.slimai_cfg_revise_path(self.cfg)
                    ## parse cfg file to global variable
                    self.parse_cfg_file(abs_path_cfg)
                    ## setup the cfg file for compiler
                    os.environ["SLIMAI_CFG_FILE"] = abs_path_cfg
                else:
                    raise SystemExit("[ModelBuild]: Setup SlimAI cfg file is Invalid:", self.cfg)
            # pattition the graph and offload some operations to slimai device
            if self.emulation:
                self.ir = partition_for_slimai_iss(self.ir, self.name)
            else:
                self.ir = partition_for_slimai(self.ir, self.name)

        ## base on self parameter create cfg json file
        self.create_cfg_json()
        # step2: configure elf file combine mode:merge or separate
        if os.getenv('ELF_FILE') != None:
            del os.environ["ELF_FILE"]
        if self.elf_mode == "merge":
            os.environ["ELF_FILE"]="merge"
        elif self.elf_mode == "separate":
            os.environ["ELF_FILE"]="separate"
        else:
            raise SystemExit("[ModelBuild]: Invalid ELF File Mode:", elf_mode)
        # step 3: Build Model
        with tvm.transform.PassContext(self.opt_level):
            self.runtime_module = relay.build(self.ir, target=self.target, params=self.param)
        # if exist temp cfg file, then remove it
        if self.device == "slimai":
            if os.path.isfile(abs_path_cfg) and abs_path_cfg.endswith(".tmp.cfg"):
                os.remove(abs_path_cfg)
            print("[ModelBuild]: Modules Trees:", self.runtime_module.lib.imported_modules)

    def build(self, model_dict, relative_json_path):
        """
        full build stream
        """
        # parse the dict of model
        self.model_dict_parse(model_dict, relative_json_path)
        print("\033[7;32m====== [%s] Model Build ======\033[0m" % (self.name))
        # get device target
        self.get_target()
        # get the network base on the name
        self.get_ir()
        # build model
        self.run_build()
        # emulation
        if self.emulation:
            log_file = os.path.join(self.dir, "quant_eval.log")
            os.system("cd /root/.tvm/slimai_workspace/iss/ && xt-run \
                    --mem_model --mlatency=150 ./test_random | tee %s" % log_file)

    def slimai_cfg_revise_path(self, cfg_file_path):
        """
        Brief
        ---------
        revise the slimai config file to complete the absolute path of the
        slimai config file.

        Parameters
        ----------
        cfg_file_path : str
            The path of slimai config file to be modified.

        Returns
        -------
        temp_cfg : str
            The path of temporary slimai cfg file
        """
        cfg_abs_file_path = os.path.abspath(cfg_file_path)
        cfg_abs_path,cfg_file_name = os.path.split(cfg_abs_file_path)
        cfg_name,_ = os.path.splitext(cfg_file_name)
        temp_cfg = os.path.join(cfg_abs_path, "%s.tmp.cfg" % cfg_name)
        def abs_path_replace(line):
            pattern_path = re.split(r'\s*\=\s*', line)[1]
            if not os.path.isabs(pattern_path):
                abs_path = os.path.normpath(os.path.join(cfg_abs_path, pattern_path))
                modified_line = re.sub(r'\s*'+pattern_path, " "+abs_path, line)
            else:
                modified_line = line
            return modified_line

        with open(temp_cfg, 'w') as fw:
            with open(cfg_file_path, 'r') as fr:
                for line in fr:
                    if re.match(r'^output_dir\s*=\s*', line):
                        modified_line = abs_path_replace(line)
                    elif re.match(r'^image_dir\s*=\s*', line):
                        modified_line = abs_path_replace(line)
                    elif re.match(r'^metric_input\s*=\s*', line):
                        modified_line = abs_path_replace(line)
                    else:
                        modified_line = line
                    fw.writelines(modified_line)
        return temp_cfg

    def get_options(self):
        """
        Brief
        -----
        Composite the options for tvm's model export_library based on
        the platform type and device type. The options including the compiling
        and linking options. In the AI_compiler.pc file, some based options already
        been defined as variables, which need to be parsed using pkgconfig module.

        Parameters
        ----------
        platform_type : Str
            "linux" and "android" is supported for now.

        device_type : Str
            "slimai" and others.

        Returns
        -------
        opts : List
            return the composited build options for tvm's model export_library.
        """

        parsed_sys_config = pkgconfig.variables('AI_compiler')
        tvm_home_path = os.getenv('TVM_HOME')
        contrib_path = os.path.join(tvm_home_path, "src", "runtime", "contrib")
        #xrp_host_path = os.getenv('XRP_HOST_PATH')
        #xrp_host_inc = os.path.join(xrp_host_path, "include")
        opts = []

        if self.os == "linux":
            linux_opts_str = parsed_sys_config['TVM_EXP_LINUX_LIB_OPTS']
            opts += linux_opts_str.split(',')
            if self.device == "slimai":
                opts += ["-I" + contrib_path]
        elif self.os == "android" :
            android_opts_str = parsed_sys_config['TVM_EXP_ANDROID_LIB_OPTS']
            opts += android_opts_str.split(',')
            if self.device == "slimai":
                opts += ["-I" + contrib_path]
                tvm_runtime_lib_path = os.path.join(tvm_home_path, "build_aarch64-android")
                tvm_runtime_lib = os.path.join(tvm_runtime_lib_path, "libtvm_runtime.so")
                opts += ["-L " + tvm_runtime_lib_path, tvm_runtime_lib]
        elif self.os == "qnx":
            qnx_opts_str = parsed_sys_config['TVM_EXP_QNX_LIB_OPTS']
            opts += qnx_opts_str.split(',')
            opts += ["-DDMLC_CMAKE_LITTLE_ENDIAN=1", "-DDMLC_LOG_STACK_TRACE=0", "-D_QNX_SOURCE"]
            opts += qnx_opts_str.split(',')
            if self.device == "slimai":
                opts += ["-I" + contrib_path]
        else:
            print("[ModelBuild]: Invalid OS Type:", self.os)
            sys.exit(1)
        return opts

    def save_library(self, lib_path):
        ## lib_path: the path of library file
        lib_file = os.path.join(lib_path, "%s.so" % self.name)
        if self.host == 'x86_64' or self.emulation:
            self.runtime_module.export_library(lib_file)
        elif self.host == 'aarch64':
            kwargs = {}
            kwargs["options"] = self.get_options()
            if self.os == "linux":
                self.runtime_module.export_library(lib_file, cc.cross_compiler('aarch64-linux-gnu-g++'), **kwargs)
            elif self.os == "android":
                self.runtime_module.export_library(lib_file, ndk.create_shared, **kwargs)
            elif self.os == "qnx":
                self.runtime_module.export_library(lib_file, cc.cross_compiler("q++"), **kwargs)
            else:
                raise SystemExit("[ModelBuild]: Invalid OS Type:", self.os)
        else:
            raise SystemExit("[ModelBuild]: The host type not surported:", self.host)
        print("\033[0;36m****** Generate File: %s.so\033[0m" % self.name)

    def save_params(self, params_path):
        ## params_path: the path of paramter file
        params_file = os.path.join(params_path, "%s.params" % self.name)
        with open(params_file, 'wb') as fo:
            fo.write(relay.save_param_dict(self.param))
        print("\033[0;36m****** Generate File: %s.params\033[0m" % self.name)

    def save_elf_binary(self, elf_path):
        network_name = self.name
        elf_file = os.path.join(elf_path, "xtensa.elf")
        if len(network_name) > 15:
            network_name=network_name[:15]
            print("network name subject:", network_name)
        os.system("cp /root/.tvm/slimai_workspace/elf/tvmgen_" + network_name + "*.elf" + " " + elf_file)
        print("\033[0;36m****** Generate File: xtensa.elf\033[0m")
        if re.search("aarch64-qnx", elf_path):
            tvm_home=os.getenv("TVM_HOME")
            os.system("cp " + tvm_home + "/vendor/sdrv/script/qnx_slimai_deploy.sh " + elf_path)

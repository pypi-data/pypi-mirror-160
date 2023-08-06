
import re
import sys
import os
import numpy
import math

output_level = 0
use_compiled_code = False

def clean_build():
    if os.path.exists("/root/.tvm/slimai_workspace/output/build_dir"):
        f_list = os.listdir("/root/.tvm/slimai_workspace/output/")
        for f in f_list:
            if os.path.splitext(f)[1]  == '.xws':
                os.system("rm /root/.tvm/slimai_workspace/output/*_opt.xws")
                break
        os.system("rm -rf /root/.tvm/slimai_workspace/output/build_dir/*")

def create_clsid_file(onnx_model):
    from onnx import load
    md = load(onnx_model)
    onnx_dim = md.graph.output[0].type.tensor_type.shape.dim
    k = 1
    for d in onnx_dim:
        k = k * d.dim_value
    with open("/root/.tvm/slimai_workspace/labels.txt","w") as f:
        for i in range(k):
            f.writelines(str(i)+"\n")

def rewrite_metric(is_custom_metric, metric_name):
    metric_file = "/opt/xnnc/"+ os.getenv("XNNC_VERSION") + "/Scripts/metric.py"
    WriteFile = False
    with open(metric_file,"r") as f:
        org_lines = f.readlines()
    if "metric_semidrive_customized" in org_lines[0]:
        for i,line in enumerate(org_lines):
            if "backend_plugins/slimai_custom_metric/metric_plugin" in line:
                if not is_custom_metric and re.match("from\s.* import .*",org_lines[i+1]):
                    org_lines[i+1] = "#custom metric placeholder\n"
                    WriteFile = True
                elif is_custom_metric:
                    org_lines[i+1] = "from " + metric_name + " import *\n"
                    WriteFile = True

    else:
        if is_custom_metric:
            raise SystemExit('xnnc component version does not support custom metric!')
    if WriteFile:
        with open(metric_file,"w") as f:
            for i,line in enumerate(org_lines):
                f.writelines(line)


def rewrite_cfg(cfg_path, model, input, output):
    """read user configure file, rewrite the configure file for auto xnnc codegen

    Parameters
    ----------
    cfg_path : str
        user input config file path
    model    : str
        created onnx model name
    input    : str list
        created onnx model input node names
    output   : str list
        created onnx model output node names

    Returns
    -------
    name     : str
        network name
    nettype  : str
        network type
    cout     : str
        xnnc codegen output path
    """
    slimai_odebug = os.getenv('SLIMAI_OUTPUT_DEBUG')
    tvm_home_path = os.getenv('TVM_HOME')
    if slimai_odebug != None:
        if os.path.exists("/root/.tvm/slimai_workspace/net.cfg"):
            os.remove("/root/.tvm/slimai_workspace/net.cfg")
    if not os.path.exists("/root/.tvm/slimai_workspace/elf"):
       os.system("mkdir -p /root/.tvm/slimai_workspace/elf")
    if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir"):
        os.system("mkdir -p /root/.tvm/slimai_workspace/output/build_dir")
    fw = open("/root/.tvm/slimai_workspace/net.cfg", "w")
    os.system("rm -rf /root/.tvm/slimai_workspace/temp/")
    slimai_sys_cfg = os.getenv('SLIMAI_COMPILE_SYS_CFG')
    model_ext = (model.split('.')[-1]).strip()
    has_metric = False
    metric_cls = "NoMetric"
    metric_input = ""
    custom_metric = False
    global output_level
    global use_compiled_code
    output_level = 0
    need_replace_output = False
    with open(cfg_path, "r") as fr:
        org_lines = fr.readlines()
    for line in org_lines:
        if "[metric]" in line:
            has_metric = True
        elif has_metric and re.match("metric_cls\s*=*",line):
            metric_cls = re.split("etric_cls\s*=", line.strip())[1].strip()
            for filename in os.listdir(os.getenv('TVM_HOME')+"/backend_plugins/slimai_custom_metric/metric_plugin/"):
                if metric_cls+'.py' == filename:
                    custom_metric = True

        elif has_metric and re.match("metric_input\s*=*",line):
            metric_input = re.split("etric_input\s*=", line.strip())[1].strip()
        elif has_metric and re.match("output_debug\s*=*", line):
            output_level = int(re.split("utput_debug\s*=", line.strip())[1].strip())
        elif has_metric and re.match("replace_output\s*=*", line):
            replace_output = re.split("eplace_output\s*=", line.strip())[1].strip()
            need_replace_output = True
        elif re.match("code_cache\s*=\s*1",line):
            use_compiled_code = True
    rewrite_metric(custom_metric, metric_cls)
    need_add_path = True
    need_add_network = True
    need_add_out = True
    need_add_sys = True
    need_add_dataset = True
    need_add_quant = True
    need_add_perf = True

    pre_path_replace = False
    pre_network_replace = False
    pre_outcnt_replace = False
    pre_system_replace = False
    pre_dataset_replace = False
    pre_quant_replace = False
    pre_perf_replace = False

    path_replace = False
    path_input_provided = False
    path_tmp_provided = False
    path_out_provided = False
    path_image_provided = False

    network_replace = False
    network_model_provided = False
    network_input_provided = False
    network_type_provided = False
    network_graph_provided = False
    network_name_provided = False
    network_class_provided = False
    network_ilayout_provided = False
    #network_olayout_provided = False
    network_mean_provided = False
    network_std_provided = False

    outcnt_replace = False
    outcnt_provided = False

    system_replace = False
    system_sys_provided = False
    system_core_provided = False
    system_tcml_provided = False
    system_tcmh_provided = False

    dataset_replace = False
    dataset_caliset_provided = False
    dataset_calicnt_provided = False
    dataset_valiset_provided = False
    dataset_valicnt_provided = False

    quant_replace = False
    quant_aq_provided = False
    quant_rg_provided = False

    perf_replace = False
    perf_optim_provided = False
    with open(cfg_path, "r") as fr:
        for line in fr:
            if not re.match(".*\n",line):
                line = line+"\n"
            if  re.match("[\[][_,a-z]+[\]]\s*",line):
                #finish last section cfg info if items are not provided
                if path_replace or network_replace or outcnt_replace or system_replace \
                    or pre_dataset_replace or pre_quant_replace or pre_perf_replace:
                    pre_path_replace = path_replace
                    pre_network_replace = network_replace
                    pre_outcnt_replace = outcnt_replace
                    pre_system_replace = system_replace
                    pre_dataset_replace = dataset_replace
                    pre_quant_replace = quant_replace
                    pre_perf_replace = perf_replace
                path_replace = False
                network_replace = False
                outcnt_replace = False
                system_replace = False
                dataset_replace = False
                quant_replace = False
                perf_replace = False
                if pre_path_replace:
                    if not path_input_provided:
                        fw.writelines("input_dir = ./\n")
                        path_input_provided = True
                    if not path_tmp_provided:
                        fw.writelines("tmp_dir = temp\n")
                        path_tmp_provided = True
                    if not path_out_provided:
                        raise SystemExit('output_dir is not provided in cfg file')
                    if not path_image_provided:
                        raise SystemExit('image_dir is not provided in cfg file')

                elif pre_network_replace:
                    if not network_model_provided:
                        modified_line = "input_model = " + model + "\n"
                        fw.writelines(modified_line)
                        network_model_provided = True
                    if not network_input_provided:
                        modified_line = "input_node_name = " + input[0] + "\n"
                        fw.writelines(modified_line)
                        network_input_provided = True
                    if not network_type_provided:
                        if model_ext != "tflite":
                            fw.writelines("type = ONNX\n")
                        else:
                            fw.writelines("type = Tensorflow\n")
                        network_type_provided = True
                    if not network_graph_provided:
                        fw.writelines("input_graph =\n")
                        network_graph_provided = True
                    if not network_name_provided:
                        name = cfg_path.split("/")[-1].split(".")[0]
                        fw.writelines("name = " + name + "\n")
                        network_name_provided = True
                    if not network_class_provided:
                        raise SystemExit('class is not provided in cfg file')
                    if not network_ilayout_provided:
                        raise SystemExit('input_data_layout is not provided in cfg file')
                    # if not network_olayout_provided:
                    #     raise ValueError('output_data_layout is not provided in cfg file')
                    if not network_mean_provided:
                        raise SystemExit('mean is not provided in cfg file')
                    if not network_std_provided:
                        raise SystemExit('stddev is not provided in cfg file')

                elif pre_outcnt_replace:
                    if not outcnt_provided:
                        out_str = ""
                        if need_replace_output:
                            out_str = replace_output[1:-1]
                        else:
                            for item in output:
                                out_str = out_str + " " + item
                        fw.writelines("description = \"\n")
                        if nettype == "Classification" and len(output) == 1 and model_ext != "tflite":
                            create_clsid_file("/root/.tvm/slimai_workspace/"+model)
                            fw.writelines("\t["+ out_str.strip() +"] save top1_5 /root/.tvm/slimai_workspace/labels.txt\n")
                        else:
                            if has_metric and metric_cls != "NoMetric":
                                fw.writelines("\t["+ out_str.strip() +"] save "+ metric_cls + " "+ metric_input + "\n")
                            else:
                                fw.writelines("\t["+ out_str.strip() +"] save \n")
                        fw.writelines("\t\"\n")
                        outcnt_provided = True
                        need_add_out = False
                elif pre_system_replace:
                    if not system_sys_provided:
                        fw.writelines("xtensa_system  = " + slimai_sys_cfg + "\n")
                        system_sys_provided = True
                        if system_core_provided and system_tcml_provided and system_tcmh_provided:
                            need_add_sys = False
                    if not system_core_provided:
                        fw.writelines("xtensa_core = vision_dsp\n")
                        system_core_provided = True
                        if system_sys_provided and system_tcml_provided and system_tcmh_provided:
                            need_add_sys = False
                    if not system_tcml_provided:
                        fw.writelines("xtensa_system  = " + slimai_sys_cfg + "\n")
                        system_tcml_provided = True
                        if system_core_provided and system_sys_provided and system_tcmh_provided:
                            need_add_sys = False
                    if not system_tcmh_provided:
                        fw.writelines("xtensa_core = vision_dsp\n")
                        system_tcmh_provided = True
                        if system_core_provided and system_sys_provided and system_tcml_provided:
                            need_add_sys = False
                elif pre_dataset_replace:
                    if not dataset_caliset_provided:
                        raise SystemExit('calibration_set is not provided in cfg file')
                    if not dataset_calicnt_provided:
                        raise SystemExit('calibration_count is not provided in cfg file')
                    if not dataset_valiset_provided:
                        raise SystemExit('validation_set is not provided in cfg file')
                    if not dataset_valicnt_provided:
                        raise SystemExit('validation_count is not provided in cfg file')
                elif pre_quant_replace:
                    if not quant_aq_provided:
                        raise SystemExit('accuracy_level is not provided in cfg file')
                    if not quant_rg_provided:
                        raise SystemExit('range is not provided in cfg file')
                elif pre_perf_replace:
                    if not perf_optim_provided:
                        raise SystemExit('optimization is not provided in cfg file')

                #prepare new section process config
                if re.match("[\[]path[\]]\s*",line):
                    path_replace = True
                    need_add_path = False
                elif re.match("[\[]network[\]]\s*",line):
                    network_replace = True
                    need_add_network = False
                elif re.match("[\[]out_cntrl[\]]\s*",line):
                    outcnt_replace = True
                elif re.match("[\[]system[\]]\s*",line):
                    system_replace = True
                elif re.match("[\[]dataset[\]]\s*",line):
                    dataset_replace = True
                    need_add_dataset = False
                elif re.match("[\[]quantization[\]]\s*",line):
                    quant_replace = True
                    need_add_quant = False
                elif re.match("[\[]performance[\]]\s*",line):
                    perf_replace = True
                    need_add_perf = False

                fw.writelines(line)
            #path section process
            elif path_replace and re.match("\s*input_dir\s*=*",line):
                fw.writelines("input_dir = ./\n")
                path_input_provided = True
            elif path_replace and re.match("\s*output_dir\s*=*",line):
                cout = line.split("=")[1].strip()
                #replace output_dir with subdir of net.cfg's dir,
                #and mv output to user defined output dir later
                fw.writelines("output_dir = output\n")
                path_out_provided = True
            elif path_replace and re.match("\s*tmp_dir\s*=*",line):
                fw.writelines("tmp_dir = temp\n")
                path_tmp_provided = True
            elif path_replace and re.match("\s*image_dir\s*=*",line):
                fw.writelines(line)
                custom_info = "custom_op_lib_path = " + tvm_home_path + "/customer_op/slimai/workstation/lib\n"
                fw.writelines(custom_info)
                path_image_provided = True

            #network section process
            elif network_replace and re.match("\s*input_model\s*=*",line):
                modified_line = "input_model = " + model
                fw.writelines(modified_line)
                fw.write('\n')
                network_model_provided = True
            elif network_replace and re.match("\s*input_node_name\s*=*",line):
                modified_line = "input_node_name = " + input[0]
                fw.writelines(modified_line)
                fw.write('\n')
                network_input_provided = True
            elif network_replace and re.match("\s*type\s*=*",line):
                if model_ext != "tflite":
                    fw.writelines("type = ONNX\n")
                else:
                    fw.writelines("type = Tensorflow\n")
                network_type_provided = True
            elif network_replace and re.match("\s*input_graph\s*=*",line):
                fw.writelines("input_graph =")
                fw.write('\n')
                network_graph_provided = True
            elif network_replace and re.match("\s*output_data_layout\s*=*",line):
                #     network_olayout_provided = True
                fw.write('\n')

            #out control section process
            elif outcnt_replace and re.match("\s+[\[]",line):
                out_str = ""
                if need_replace_output:
                    out_str = replace_output[1:-1]
                else:
                    for item in output:
                        out_str = out_str + " " + item
                lp = line.split(']')
                hlp = lp[0].split('[')
                modified_line = hlp[0]+'[' + out_str.strip() + ']'+ lp[1]
                fw.writelines(modified_line)
                outcnt_provided = True
                need_add_out = False

            #system section process
            elif system_replace and re.match("\s*xtensa_system\s*=*",line):
                fw.writelines("xtensa_system  = " + slimai_sys_cfg + "\n")
                system_sys_provided = True
                if system_core_provided and system_tcml_provided and system_tcmh_provided:
                    need_add_sys = False
            elif system_replace and re.match("\s*xtensa_core\s*=*",line):
                fw.writelines("xtensa_core = vision_dsp\n")
                system_core_provided = True
                if system_sys_provided and system_tcml_provided and system_tcmh_provided:
                    need_add_sys = False
            elif system_replace and re.match("\s*tcm_reserve_low\s*=*",line):
                fw.writelines("tcm_reserve_low = 0x280\n")
                system_tcml_provided = True
                if system_core_provided and system_sys_provided and system_tcmh_provided:
                    need_add_sys = False
            elif system_replace and re.match("\s*tcm_reserve_high\s*=*",line):
                fw.writelines("tcm_reserve_high = 0x3000\n")
                system_tcmh_provided = True
                if system_core_provided and system_sys_provided and system_tcml_provided:
                    need_add_sys = False

            else:
                fw.writelines(line)
                if path_replace and re.match("\s*image_dir\s*=*",line):
                    custom_info = "custom_op_lib_path = " + tvm_home_path + "/customer_op/slimai/workstation/lib\n"
                    fw.writelines(custom_info)
                    path_image_provided = True
                elif network_replace and re.match("\s*name\s*=*",line):
                    name = line.split("=")[1].strip()
                    network_name_provided = True
                elif network_replace and re.match("\s*class\s*=*",line):
                    nettype = line.split("=")[1].strip()
                    network_class_provided = True
                elif network_replace and re.match("\s*mean\s*=*",line):
                    network_mean_provided = True
                elif network_replace and re.match("\s*stddev\s*=*",line):
                    network_std_provided = True
                elif network_replace and re.match("\s*input_data_layout\s*=*",line):
                    network_ilayout_provided = True
                    ilt = line.strip().split('=')[-1].strip()
                    fw.writelines("output_data_layout = NHWC\n")
                # elif network_replace and re.match("\s*output_data_layout\s*=*",line):
                #     network_olayout_provided = True
                elif dataset_replace and re.match("\s*calibration_set\s*=*",line):
                    dataset_caliset_provided = True
                elif dataset_replace and re.match("\s*calibration_count\s*=*",line):
                    dataset_calicnt_provided = True
                elif dataset_replace and re.match("\s*validation_set\s*=*",line):
                    dataset_valiset_provided = True
                elif dataset_replace and re.match("\s*validation_count\s*=*",line):
                    dataset_valicnt_provided = True
                elif quant_replace and re.match("\s*accuracy_level\s*=*",line):
                    quant_aq_provided = True
                elif quant_replace and re.match("\s*range\s*=*",line):
                    quant_rg_provided = True
                elif perf_replace and re.match("\s*optimization\s*=*",line):
                    perf_optim_provided = True
                    fw.writelines("dsp_frequency = 748\n")
                    fw.writelines("read_delay = 150\n")
                    fw.writelines("write_delay = 150\n")

    #last section need additionary process
    if (not need_add_path) and (not path_input_provided):
        fw.writelines("input_dir = ./")
        fw.write('\n')
        path_input_provided = True
    if (not need_add_path) and (not path_tmp_provided):
        modified_line = "tmp_dir = temp"
        fw.writelines(modified_line)
        fw.write('\n')
        path_tmp_provided = True
    elif (not need_add_path) and (not path_out_provided):
        raise SystemExit('output_dir is not provided in cfg file')
    elif (not need_add_path) and (not path_image_provided):
        raise SystemExit('image_dir is not provided in cfg file')

    if (not need_add_network) and (not network_model_provided):
        modified_line = "input_model = " + model
        fw.writelines(modified_line)
        fw.write('\n')
        network_model_provided = True
    if (not need_add_network) and (not network_input_provided):
        modified_line = "input_node_name = " + input[0]
        fw.writelines(modified_line)
        fw.write('\n')
        network_input_provided = True
    if (not need_add_network) and (not network_type_provided):
        if model_ext != "tflite":
            fw.writelines("type = ONNX\n")
        else:
            fw.writelines("type = Tensorflow\n")
        network_type_provided = True
    if (not need_add_network) and (not network_graph_provided):
        fw.writelines("input_graph =")
        fw.write('\n')
        network_graph_provided = True
    elif (not need_add_network) and (not network_name_provided):
        name = cfg_path.split("/")[-1].split(".")[0]
        fw.writelines("name = " + name + "\n")
        network_name_provided = True
    elif (not need_add_network) and (not network_class_provided):
        raise SystemExit('class is not provided in cfg file')
    elif (not need_add_network) and (not network_ilayout_provided):
        raise SystemExit('input_data_layout is not provided in cfg file')
    # elif (not need_add_network) and (not network_olayout_provided):
    #     raise SystemExit('output_data_layout is not provided in cfg file')
    elif (not need_add_network) and (not network_mean_provided):
        raise SystemExit('mean is not provided in cfg file')
    elif (not need_add_network) and (not network_std_provided):
        raise SystemExit('stddev is not provided in cfg file')

    if (not need_add_out) and (not outcnt_provided):
        out_str = ""
        if need_replace_output:
            out_str = replace_output[1:-1]
        else:
            for item in output:
                out_str = out_str + " " + item
        fw.writelines("description = \"\n")
        if nettype == "Classification" and len(output) == 1 and model_ext != "tflite":
            create_clsid_file("/root/.tvm/slimai_workspace/"+model)
            fw.writelines("\t["+ out_str.strip() +"] save top1_5 /root/.tvm/slimai_workspace/labels.txt\n")
        else:
            if has_metric and metric_cls != "NoMetric":
                fw.writelines("\t["+ out_str.strip() +"] save "+ metric_cls + " "+ metric_input + "\n")
            else:
                fw.writelines("\t["+ out_str.strip() +"] save \n")
        fw.writelines("\t\"\n")
        outcnt_provided = True

    if (not need_add_sys) and (not system_sys_provided):
        fw.writelines("xtensa_system  = " + slimai_sys_cfg + "\n")
        system_sys_provided = True
    if (not need_add_sys) and (not system_core_provided):
        fw.writelines("xtensa_core = vision_dsp\n")
        system_core_provided = True
    if (not need_add_sys) and (not system_tcml_provided):
        fw.writelines("tcm_reserve_low = 0x280\n")
        system_tcml_provided = True
    if (not need_add_sys) and (not system_tcmh_provided):
        fw.writelines("tcm_reserve_high = 0x3000\n")
        system_tcmh_provided = True

    if (not need_add_dataset) and (not dataset_caliset_provided):
        raise SystemExit('calibration_set is not provided in cfg file')
    elif (not need_add_dataset) and (not dataset_calicnt_provided):
        raise SystemExit('calibration_count is not provided in cfg file')
    elif (not need_add_dataset) and (not dataset_valiset_provided):
        raise SystemExit('validation_set is not provided in cfg file')
    elif (not need_add_dataset) and (not dataset_valicnt_provided):
        raise SystemExit('validation_count is not provided in cfg file')

    if (not need_add_quant) and (not quant_aq_provided):
        raise SystemExit('accuracy_level is not provided in cfg file')
    elif (not need_add_quant) and (not quant_rg_provided):
        raise SystemExit('range is not provided in cfg file')

    if (not need_add_perf) and (not perf_optim_provided):
        raise SystemExit('optimization is not provided in cfg file')


    #exiting traverse of cfg file
    if need_add_path:
        raise SystemExit('[path] section value is not provided in cfg file')
    if need_add_network:
        raise SystemExit('[network] section value is not provided in cfg file')
    if need_add_out:
        out_str = ""
        if need_replace_output:
            out_str = replace_output[1:-1]
        else:
            for item in output:
                out_str = out_str + " " + item
        fw.writelines("[out_cntrl]\n")
        fw.writelines("description = \"\n")
        if nettype == "Classification" and len(output) == 1 and model_ext != "tflite":
            create_clsid_file("/root/.tvm/slimai_workspace/"+model)
            fw.writelines("\t["+ out_str.strip() +"] save top1_5 /root/.tvm/slimai_workspace/labels.txt\n")
        else:
            if has_metric and metric_cls != "NoMetric":
                fw.writelines("\t["+ out_str.strip() +"] save "+ metric_cls + " "+ metric_input + "\n")
            else:
                fw.writelines("\t["+ out_str.strip() +"] save \n")
        fw.writelines("\t\"\n")
        outcnt_provided = True
        need_add_out = False
    if need_add_sys:
        fw.writelines("[system]\n")
        fw.writelines("tcm_reserve_low = 0x280\n")
        fw.writelines("tcm_reserve_high = 0x3000\n")
        fw.writelines("xtensa_system  = " + slimai_sys_cfg + "\n")
        fw.writelines("xtensa_params  =\n")
        fw.writelines("xtensa_core = vision_dsp\n")
        system_sys_provided = True
        system_core_provided = True
        need_add_sys = False
    if need_add_dataset:
        raise SystemExit('[dataset] section value is not provided in cfg file')
    if need_add_quant:
        raise SystemExit('[quantization] section value is not provided in cfg file')
    if need_add_perf:
        raise SystemExit('[performance] section value is not provided in cfg file')
    fw.writelines("[yolo_parameters]\n")
    fw.writelines("enable_yolo_pp = False\n")
    fw.writelines("[graph]\n")
    if network_ilayout_provided and (ilt ==  "NCHW" or ilt ==  "NHWC"):
        if ilt ==  "NHWC":
            fw.writelines("tensor = " + input[0] +", DWH\n")
        else:
            fw.writelines("tensor = " + input[0] +", WHD\n")
    for item in output:
        on = ''.join([c if c.isalnum() else '_' for c in item])
        fw.writelines("tensor = " + on +", DWH\n")

    fw.close()
    return name, nettype, cout

#####################################################################################
# codegen_stages used to freely control the slimai quantization and code generation
#####################################################################################
def xnnc_codegen(netname, out_dir, codegen_stages = ["default"]):
    """wrapper to run xnnc codegen

    Parameters
    ----------

    Returns
    -------
    cpath     : str
        recorded current work directory for recovery after xnnc compilation
    """
    global output_level
    global use_compiled_code
    default_stages = ['gen_quant_profile', 'flt_inference', 'use_quant_profile -m $(nproc)', 'gen_code']
    if len(codegen_stages) == 1 and codegen_stages[0] == "default":
        stages = default_stages
        #if it is not debug case and use_compiled_code is set, try to use cached compiled slimai code
        if output_level == 0 and use_compiled_code and os.path.exists("/root/.tvm/slimai_workspace/code_store/"+netname+"_opt" ):
            if os.path.exists("/root/.tvm/slimai_workspace/output/"+netname+"_opt"):
                os.system("rm -rf /root/.tvm/slimai_workspace/output/"+netname+"_opt")
            if os.path.exists("/root/.tvm/slimai_workspace/temp"):
                os.system("rm -rf /root/.tvm/slimai_workspace/temp")
            os.system("cp -r /root/.tvm/slimai_workspace/code_store/"+netname+"_opt /root/.tvm/slimai_workspace/output/")
            os.system("cp -r /root/.tvm/slimai_workspace/code_store/"+netname+"_temp /root/.tvm/slimai_workspace/temp")
            cpath = os.getcwd()
            os.chdir("/root/.tvm/slimai_workspace")
            return cpath
    else:
        stages = codegen_stages
    xrp_code_dir = "/root/xnnc/"
    xnnc_xrp_path = os.getenv('XNNC_XRP_CODE_PATH')
    if xnnc_xrp_path is not None:
        xrp_code_dir = xnnc_xrp_path+"/"
    cpath = os.getcwd()
    os.chdir("/root/.tvm/slimai_workspace")
    cmd_str = "python3 " + xrp_code_dir + os.getenv("XNNC_VERSION") + "/Scripts/xnnc.py --keep -c net.cfg"
    rs = 0
    for stage in stages:
        rv = os.system(cmd_str + " --stage "+ stage)
        rs = rs + rv
        if output_level > 0:
            if output_level == 1 and 'flt_inference' in stage:
                os.system("cp /root/.tvm/slimai_workspace/temp/output_control.octrl "+ out_dir)
                os.system("cp -r /root/.tvm/slimai_workspace/temp/*_ref "+ out_dir)
                os.system("chmod a+w -R "+ out_dir)
                sys.exit(0)
            elif output_level == 2 and 'use_quant_profile' in stage:
                os.system("cp -r /root/.tvm/slimai_workspace/temp/* "+ out_dir)
                os.system("chmod a+w -R "+ out_dir)
                sys.exit(0)
    #cache complied code
    if not os.path.exists("/root/.tvm/slimai_workspace/code_store/"):
        os.system("mkdir -p /root/.tvm/slimai_workspace/code_store/")
    if os.path.exists("/root/.tvm/slimai_workspace/code_store/"+netname+"_opt" ):
        os.system("rm -rf /root/.tvm/slimai_workspace/code_store/"+netname+"_opt")
    if os.path.exists("/root/.tvm/slimai_workspace/code_store/"+netname+"_temp" ):
        os.system("rm -rf /root/.tvm/slimai_workspace/code_store/"+netname+"_temp")
    if rs == 0:
        os.system("cp -r /root/.tvm/slimai_workspace/output/"+netname+"_opt /root/.tvm/slimai_workspace/code_store/"+netname+"_opt")
        os.system("cp -r /root/.tvm/slimai_workspace/temp /root/.tvm/slimai_workspace/code_store/"+netname+"_temp")

    return cpath
def rewrite_custom_layers(path, folder, out_path, model_name, is_internal = False):
    """maintain custom layers as a shared component:
       if not created

    Parameters
    ----------
    path      : str
        the path of target codegen working directory
    folder   : str
        the custom layer lib folder name
    out_path   : str
        the common custom layer lib directory
    model_name   : str
        model name

    Returns
    -------
    """
    lib_dir = path + folder
    src_dir = lib_dir + "/src"
    include_dir = lib_dir + "/include"
    out_src_dir = out_path + "/src"
    out_include_dir = out_path + "/include"
    #if component is not created, create it first
    if not os.path.exists(out_src_dir + "/custom_layers_common.c"):
        fo = open(out_path + "/CMakeLists.tmp", "w")
        with open(out_path + "/CMakeLists.txt", "r") as fi:
            for line in fi:
                if model_name + "_opt" in line:
                    newline = line.replace(model_name + "_opt", "common")
                    fo.writelines(newline)
                else:
                    fo.writelines(line)
        fo.close()
        os.system("mv " + out_path + "/CMakeLists.tmp " + out_path + "/CMakeLists.txt")
        tvm_home_path = os.getenv('TVM_HOME')
        os.system("cp " + tvm_home_path + "/customer_op/slimai/chip/src/custom_layers_common.c " +  out_src_dir + "/custom_layers_common.c")
        os.system("cp " + tvm_home_path + "/customer_op/slimai/chip/src/custom_layers_common.h " +  out_include_dir + "/custom_layers_common.h")
    if is_internal:
        h_lines = []
        # c_lines = []
        fim = open(out_include_dir + "/custom_layers_common.h", "r")
        fcm = open(out_src_dir + "/custom_layers_common.c", "r")
        main_h_lines = fim.readlines()
        main_c_lines = fcm.readlines()
        h_size = len(main_h_lines)
        c_size = len(main_c_lines)
        fim.close()
        fcm.close()
        with open(include_dir + "/custom_layers_" + model_name + "_opt.h", "r") as fi:
            for line in fi:
                if re.search("LAYER_API\s+XI_ERR_TYPE\s+",line):
                    h_lines.append(line)
        #only use h_lines, assume c_lines are the same as h_lines
        foc = open(out_src_dir + "/custom_layers_common.c.tmp","w")
        foh = open(out_include_dir + "/custom_layers_common.h.tmp","w")
        h_declare_flag = False
        for i in range(h_size):
            insert_h = i
            foh.writelines(main_h_lines[i])
            if re.search("extern\s+\"C\"\s+" ,main_h_lines[i]):
                h_declare_flag = True
            if h_declare_flag and "#endif" in main_h_lines[i]:
                break

        c_declare_flag = False
        for i in range(c_size):
            insert_c = i
            foc.writelines(main_c_lines[i])
            if re.search("#define\s+IGNORE_DUMMY_IMPLEMENTATION", main_c_lines[i]):
                c_declare_flag = True
            if c_declare_flag and "#endif" in main_c_lines[i]:
                break

        for line in h_lines:
            func_name = line.strip().split('(')[0]
            is_impl = False
            for ll in main_h_lines:
                if func_name in ll:
                    is_impl = True
                    break
            if not is_impl:
                foh.writelines(line)
                foc.writelines(line)
        for i in range(insert_c+1 ,c_size):
            foc.writelines(main_c_lines[i])
        for i in range(insert_h+1 ,h_size):
            foh.writelines(main_h_lines[i])

        foc.close()
        foh.close()

        os.system("mv " + out_src_dir + "/custom_layers_common.c.tmp " + out_src_dir + "/custom_layers_common.c")
        os.system("mv " + out_include_dir + "/custom_layers_common.h.tmp " + out_include_dir + "/custom_layers_common.h")

    #remove unnecessary code
    if os.path.exists(out_src_dir + "/custom_layers_" + model_name + "_opt.c"):
        os.system("rm -f " + out_src_dir + "/custom_layers_" + model_name + "_opt.c")
        os.system("rm -f " + out_include_dir + "/custom_layers_" + model_name + "_opt.h")

def rewrite_custom_layers_include(path, model_name):

    """modify custom layers include

    Parameters
    ----------
    path      : str
        the path to be modified
    model_name   : str
        model name

    Returns
    -------
    """
    src_dir = path + "/src"
    fo = open(path + "/CMakeLists.tmp", "w")
    with open(path + "/CMakeLists.txt", "r") as fi:
        for line in fi:
            if "_opt_custom_layers" in line:
                newline = line.replace(model_name + "_opt", "common")
                fo.writelines(newline)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv " + path + "/CMakeLists.tmp " + path + "/CMakeLists.txt")

    fo = open(src_dir + "/layers_" + model_name + "_opt.tmp", "w")
    with open(src_dir + "/layers_" + model_name + "_opt.c", "r") as fi:
        for line in fi:
            if "custom_layers_" + model_name + "_opt.h" in line:
                newline = line.replace(model_name + "_opt", "common")
                fo.writelines(newline)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv " + src_dir + "/layers_" + model_name + "_opt.tmp " + src_dir + "/layers_" + model_name + "_opt.c")

    fo = open(src_dir + "/layers_" + model_name + "_opt_ref.tmp", "w")
    with open(src_dir + "/layers_" + model_name + "_opt_ref.c", "r") as fi:
        for line in fi:
            if "custom_layers_" + model_name + "_opt.h" in line:
                newline = line.replace(model_name + "_opt", "common")
                fo.writelines(newline)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv " + src_dir + "/layers_" + model_name + "_opt_ref.tmp " + src_dir + "/layers_" + model_name + "_opt_ref.c")


def build_for_iss(name, nettype, retpath):
    """target codegen

    Parameters
    ----------
    name      : str
        network name, used by xnnc compiler to define directory name
    nettype   : str
        network type
    retpath   : str
        the path to be returned to after the xnnc compilation

    Returns
    -------
    """

    #check custom layer
    has_custom_layer = False
    if os.path.exists("/root/.tvm/slimai_workspace/output/" + name + "_opt/libsupported_custom_layers"):
        has_internal_custom_layer = True
        has_custom_layer = True
    else:
        has_internal_custom_layer = False
    list = os.listdir("/root/.tvm/slimai_workspace/output/" + name + "_opt/")
    for forp in list:
        if "opt_custom_layers" in forp:
            has_custom_layer = True
            if not os.path.exists( \
                      "/root/.tvm/slimai_workspace/output/" + name + "_opt/libcommon_custom_layers"):
                os.system("mv -f /root/.tvm/slimai_workspace/output/" + name + "_opt/" + forp + \
                          " /root/.tvm/slimai_workspace/output/" + name + "_opt/libcommon_custom_layers")
                rewrite_custom_layers("/root/.tvm/slimai_workspace/output/" + name + "_opt/", \
                          "libcommon_custom_layers", "/root/.tvm/slimai_workspace/output/" + name + "_opt/libcommon_custom_layers", \
                          name, has_internal_custom_layer)
            else:
                if has_internal_custom_layer:
                    rewrite_custom_layers("/root/.tvm/slimai_workspace/output/" + name + "_opt/", \
                        forp,"/root/.tvm/slimai_workspace/output/build_dir/libcommon_custom_layers", \
                            name, has_internal_custom_layer)
            break
    if has_custom_layer:
        rewrite_custom_layers_include("/root/.tvm/slimai_workspace/output/" + name + "_opt/lib" + name + "_opt/", \
          name)
    fo = open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_random_"+name+"_opt/CMakeLists.tmp", "w")
    with open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_random_"+name+"_opt/CMakeLists.txt", "r") as fi:
        for line in fi:
            if name + "_opt_custom_layers" in line:
                newline  = line.replace(name + "_opt", "common")
                fo.writelines(newline)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv /root/.tvm/slimai_workspace/output/" + name + "_opt/test_random_"+name+"_opt/CMakeLists.tmp /root/.tvm/slimai_workspace/output/" + name + "_opt/test_random_"+name+"_opt/CMakeLists.txt")
    fo = open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_"+name+"_opt/CMakeLists.tmp", "w")
    with open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_"+name+"_opt/CMakeLists.txt", "r") as fi:
        for line in fi:
            if name + "_opt_custom_layers" in line:
                newline  = line.replace(name + "_opt", "common")
                fo.writelines(newline)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv /root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_"+name+"_opt/CMakeLists.tmp /root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_"+name+"_opt/CMakeLists.txt")
    os.chdir("./output/" + name + "_opt/")
    fo = open("Makefile_inf.linux", "w")
    with open("Makefile.linux", "r") as fi:
        for line in fi:
            if "TESTS := $(addprefix do-build/,$(wildcard test_*))" in line:
                fo.writelines("TESTS := $(addprefix do-build/,$(filter $(wildcard test_inference_*) $(wildcard test_random_*), $(wildcard test_*)))\n")
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv Makefile Makefile_bak")
    os.system("mv Makefile_inf.linux Makefile")
    os.system("cp Makefile Makefile.linux")

    if os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt"):
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt", "r") as fp:
            out_scales = fp.readlines()
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_zps.txt", "r") as fp:
            out_zps = fp.readlines()
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_names.txt", "r") as fp:
            out_names = fp.readlines()
        with open("/root/.tvm/slimai_workspace/output/build_dir/output_dtypes.txt", "r") as fp:
            out_dtypes = fp.readlines()
        with open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_" + name + "_opt/test_inference.c",'r') as finf:
            test_inf_lines = finf.readlines()
        for k, inf_line in enumerate(test_inf_lines):
            if "DataDump3D(&(tile_" in inf_line:
                segs = re.split(r',',inf_line)
                outname = '_'.join(segs[0].split('_')[1:-1])
                fscale = float(segs[1].strip())
                for j, on in enumerate(out_names):
                    final_oname = ''.join([c if c.isalnum() else '_' for c in on.strip()])
                    if final_oname in outname:
                        id = j
                        break
                oscale = float(out_scales[id].strip())
                ozp = int(out_zps[id].strip())

                if math.fabs(oscale) > 1e-6:
                    scale = fscale*oscale
                    zp = int(-1 * ozp * fscale * oscale)
                    segs[1] = str(scale)
                    segs[2] = str(zp)
                    test_inf_lines[k] = ','.join(segs)
        with open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_" + name + "_opt/test_inference.c",'w') as finf:
            for k, inf_line in enumerate(test_inf_lines):
                finf.writelines(inf_line)
    os.system("make -f Makefile.linux build-xtensa  BUILD_TYPE=Release \
        ENABLE_VERIFY=0 NO_REF_TABLES=1 CNNRT_PERF_CONTROL_ISS=0 CNNRT_PERF_LEVEL=2 \
        -j$(nproc)" )
    if os.path.exists("/root/.tvm/slimai_workspace/iss"):
        os.system("rm -rf /root/.tvm/slimai_workspace/iss" )
    os.system("mkdir -p /root/.tvm/slimai_workspace/iss")
    os.system("mv -f build/bin/test_inference /root/.tvm/slimai_workspace/iss/")
    os.system("mv -f build/bin/test_random /root/.tvm/slimai_workspace/iss/")
    os.system("mv -f data_"+ name + "_opt/network_coeff.bin /root/.tvm/slimai_workspace/iss/")
    os.system("mv -f data_"+ name + "_opt/network_coeff_ref.bin /root/.tvm/slimai_workspace/iss/")
    fo = open("/root/.tvm/slimai_workspace/iss/imagelist.txt", "w")
    fo.writelines("1\n")
    fo.writelines("\n")
    fo.writelines("data.ppm\n")
    fo.close()
    fo = open("/root/.tvm/slimai_workspace/iss/clean_blob.sh", "w")
    fo.writelines("if ls /root/.tvm/slimai_workspace/iss/*.blob 1> /dev/null 2>&1; then\n")
    fo.writelines("    rm /root/.tvm/slimai_workspace/iss/*.blob\n")
    fo.writelines("fi\n")
    fo.close()
    os.system("rm -rf /root/.tvm/slimai_workspace/output/" + name + "_opt/")
    f_list = os.listdir("/root/.tvm/slimai_workspace/output/")
    for f in f_list:
        if os.path.splitext(f)[1]  == '.xws':
            os.system("rm /root/.tvm/slimai_workspace/output/*_opt.xws")
            break

    os.chdir(retpath)

def find_scale_shift(div, maxbits):
    shifts = []
    scales = []
    rems = []

    for i in range(maxbits):
        shifts.append(i)
        scales.append(0)
        rems.append(65535.0)

    for i, shift in enumerate(shifts):
        scales[i] = int((1 << shift) / div)

    for i, scale in enumerate(scales):
        if scale > 0 and scale < 65536:
            rems[i] = abs(((1 << shifts[i])) / scale - div)

    a = numpy.array(rems)
    idx = numpy.argmin(a)
    return scales[idx], shifts[idx]

def rewrite_code(name, nettype, retpath):
    """target codegen

    Parameters
    ----------
    name      : str
        network name, used by xnnc compiler to define directory name
    nettype   : str
        network type
    retpath   : str
        the path to be returned to after the xnnc compilation

    Returns
    -------
    """

    if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/elf_proj"):
        os.system("mkdir -p /root/.tvm/slimai_workspace/output/build_dir/elf_proj")

    os.chdir("./output/" + name + "_opt/")
    if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.txt"):
        module_cnt = 1
        os.system("cp ./test_random_" + name + "_opt/CMakeLists.txt /root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.txt")
        fo = open("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.tmp", "w")
        with open("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.txt", "r") as fi:
            for line in fi:
                if name + "_opt_custom_layers" in line:
                    newline  = line.replace(name + "_opt", "common")
                    fo.writelines(newline)
                else:
                    fo.writelines(line)
        fo.close()
    else:
        fo = open("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.tmp", "w")
        fim = open("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.txt", "r")
        fi = open("./test_random_" + name + "_opt/CMakeLists.txt", "r")
        main_lines = fim.readlines()
        lines = fi.readlines()
        main_size = len(main_lines)
        c_size = len(lines)

        merge_point0 = -1
        merge_point1 = -1
        merge_point2 = -1
        for i in range(0, c_size):
            if "include_directories(${CMAKE_CURRENT_SOURCE_DIR}" in lines[i] and merge_point0 == -1:
                merge_point0 = i
            elif "find_library(LIB_cnnrt NAMES cnnrt)" in lines[i] and merge_point1 == -1:
                merge_point1 = i + 1
            elif "set(OPTIONAL_LIBS" in lines[i] and merge_point2 == -1:
                merge_point2 = i + 1
            elif "if (LIB_supported_custom_layers)" in lines[i]:
                merge_end = i
                break
        merge_include = False
        merge_findlib = False
        merge_custom = False
        for i in range(0, main_size):
            if "include_directories(${CMAKE_CURRENT_SOURCE_DIR}" in main_lines[i] and not merge_include:
                merge_include = True
                model_name = lines[merge_point0].strip().split("../lib")[1].split("_opt/")[0]
                fo.writelines(lines[merge_point0])
                fo.writelines(main_lines[i])
            elif "find_library(LIB_cnnrt NAMES cnnrt)" in main_lines[i] and not merge_findlib:
                fo.writelines(main_lines[i])
                merge_findlib = True
                for m in range(merge_point1, merge_point2):
                    if model_name in lines[m] and (not "custom_layers" in lines[m]):
                        fo.writelines(lines[m])
            elif "set(OPTIONAL_LIBS" in main_lines[i] and not merge_custom:
                fo.writelines(main_lines[i])
                merge_custom = True
                # for m in range(merge_point2, merge_end):
                #     fo.writelines(lines[m])
            elif "add_executable" in main_lines[i]:
                module_cnt = len(main_lines[i].split(" "))
                fo.writelines(main_lines[i].split(")")[0] + " " + model_name + ".c)\n")
            elif "target_link_libraries" in main_lines[i]:
                split_segs = main_lines[i].split("test_random")
                fo.writelines(split_segs[0] + "test_random ${LIB_" + model_name + "_opt}" + split_segs[1])
            else:
                fo.writelines(main_lines[i])
        fo.close()
        fi.close()
        fim.close()
        os.system("rm ./test_random_" + name + "_opt/CMakeLists.txt")
    os.system("mv /root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.tmp /root/.tvm/slimai_workspace/output/build_dir/elf_proj/CMakeLists.txt")


    replace_input_start = False
    replace_input_finished = False
    replace_output_start = False
    replace_output_finished = False
    replace_parse_args_start = False
    replace_parse_args_end = False
    replace_main_start = False
    replace_main_end = False
    replace_tilein_end = False
    replace_tileout_start = False
    replace_tileout_end = False
    tile_cvt_reg_start = False
    tile_cvt_reg_end = False
    tile_cvt_ready = False
    replace_rm_start = False
    replace_rm_end = False
    replace_return = False

    replace_tileout_cnt = 0

    inputnames = []
    inputsizes = []
    inputtypes = []
    outputnames = []
    outputtypes = []
    outputdtypes = []
    outputquan = []
    outputsizes = []
    output4D = []
    #read output name list of semidrive ir
    with open("/root/.tvm/slimai_workspace/output/build_dir/output_names.txt", "r") as fp:
        out_names = fp.readlines()
    with open("/root/.tvm/slimai_workspace/output/build_dir/output_dtypes.txt", "r") as fp:
        out_dtypes = fp.readlines()
    if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/xtensa.c"):
        crt_file_name = "xtensa"
    else:
        crt_file_name = name
    tstr = "short"
    fo = open("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/" + crt_file_name + ".c", "w")
    with open("./test_random_" + name + "_opt/test_random.c", "r") as fi:
        for line in fi:
            if (not replace_input_start) and "#endif // __XTENSA__" in line:
                fo.writelines(line)
                fo.writelines("void XI_TILE4D_DEQUANTIZE(const xi_pTile4D in, xi_pTile4D out, const float ratio);\n")
                replace_input_start = True
            elif replace_input_start and (not replace_input_finished):
                if re.search("\[[0-9]+\];",line):
                    ls = re.split(r'\s+', line.strip())
                    inputnames.append(ls[-1].split('[')[0])
                    inputsizes.append(ls[-1].split('[')[1].split(']')[0])
                    inputtypes.append(' '.join(ls[:-1]) + '*')
                    #only support single input
                    replace_input_finished = True
                    replace_output_start = True
                    # add static to avoid same name conflict
                    fo.writelines("static " + ' '.join(ls[:-1]) + ' *' + ls[-1].split('[')[0] + " = NULL;\n")
                    #fo.writelines(line)
                    #fo.writelines("float *" + ls[-1].split('[')[0] + "_sp = NULL;\n")
                else:
                    fo.writelines(line) #blank line
            elif replace_output_start and (not replace_output_finished):
                if re.search("\[[0-9]+\];",line):
                    ls = re.split(r'\s+', line.strip())
                    cur_output = ls[-1].split('[')[0]
                    outputnames.append(cur_output)
                    outputtypes.append(' '.join(ls[:-1]))
                    outputsizes.append(ls[-1].split('[')[1].split(']')[0])
                    outputquan.append('65535.0') #placeholder 65535
                    #find corresponding sequence number in outputs of semidrive ir
                    for j, on in enumerate(out_names):
                        if on.strip().split(".")[-1] in cur_output:
                            id = j
                            break
                    #find corresponding type,  id is sequence number in outputs of semidrive ir
                    dt = out_dtypes[id].strip()
                    if dt == 'float32':
                        out_ct = "float"
                    elif dt == 'uint32':
                        out_ct = "uint32_t"
                    elif dt == 'int32':
                        out_ct = "int32_t"
                    elif dt == 'uint8':
                        out_ct = "uint8_t"
                    elif dt == 'int8':
                        out_ct = "int8_t"
                    elif dt == 'uint16':
                        out_ct = "uint16_t"
                    elif dt == 'int16':
                        out_ct = "int16_t"
                    else:
                        out_ct = "float"
                    outputdtypes.append(out_ct)
                    fo.writelines("static " + line)
                    fo.writelines("static " + out_ct + " *" + cur_output + "_sp = NULL;\n")
                else:
                    fo.writelines(line) #blank line
                    replace_output_finished = True
                    if os.path.exists("/root/.tvm/slimai_workspace/temp/BestProfile.txt"):
                        with open("/root/.tvm/slimai_workspace/temp/BestProfile.txt", "r") as fp:
                            first_line = fp.readline()
                            dir_name = first_line.strip().split(".")[0]
                        #get dequantize param from blob file in temp dir
                        blob_files = os.listdir("/root/.tvm/slimai_workspace/temp/" + dir_name)
                        for blob in blob_files:
                            #traverse output names used in .cc file, break when iterative item match blob file name
                            for i, outname in enumerate(outputnames):
                                #traverse graph output names, break when iterative item match output name in .cc file
                                for j, on in enumerate(out_names):
                                    final_oname = ''.join([c if c.isalnum() else '_' for c in on.strip()])
                                    if final_oname in outname:
                                        break
                                if final_oname + ".blob" in blob:
                                    with open("/root/.tvm/slimai_workspace/temp/" + dir_name + "/" + blob, "r") as fp:
                                        first_line = fp.readline()
                                        #find output id "i" used in .cc file, use "outputquan[i]" to save the dequantized param
                                        outputquan[i] = first_line.strip().split(" ")[0]
                                    break
            elif (not replace_main_start) and "#endif" in line and "ENABLE_VERIFY" in line:
                replace_parse_args_start = True
                fo.writelines(line)
            elif replace_parse_args_start and (not replace_parse_args_end):
                if "int main(int argc, char* argv[])" in line:
                    replace_parse_args_end = True
                    replace_main_start = True
                    fo.writelines("#include \"xrp_xnnc_ns.h\"\n")
                    fo.writelines("XI_ERR_TYPE flk_start_inf"+ str(module_cnt - 1) +"(const uint8_t *params,\n")
                    fo.writelines("            struct XtensaOperationArgs *input, struct XtensaOperationArgs *output)\n")
                    fo.writelines("{\n")
                    # fo.writelines("    printf(\"inf start\\n\");\n")
                    # fo.writelines("    XI_ERROR_CHECKS(){\n")
                    # fo.writelines("        XI_RUN_TIME_CHECK(params != NULL, \"Params can be NULL\", XI_ERR_BADARG);\n")
                    # fo.writelines("        XI_RUN_TIME_CHECK(input != NULL && ((input->numArgs == 1)),\n")
                    # fo.writelines("                          \"Invalid number of input args\", XI_ERR_BADARG);\n")
                    # fo.writelines("        XI_RUN_TIME_CHECK(input->args[0] != NULL && input->argsSize[0] > 0,\n")
                    # fo.writelines("                          \"Invalid input args\", XI_ERR_BADARG);\n")
                    # fo.writelines("        XI_RUN_TIME_CHECK(output != NULL && output->numArgs == 1\n")
                    # fo.writelines("                          && output->args[0] != NULL && output->argsSize[0] > 0,\n")
                    # fo.writelines("                          \"Invalid output args\", XI_ERR_BADARG);\n")
                    # fo.writelines("    };\n")
                    for i, iname in enumerate(inputnames):
                        fo.writelines("    " + iname + " = (" + inputtypes[i] + ")(input->args[" + str(i) +"]);\n")
                    for i, oname in enumerate(outputnames):
                        for j, on in enumerate(out_names):
                            if on.strip().split(".")[-1] in oname:
                                id = j
                                break
                        fo.writelines("    " + oname + "_sp = (" + outputdtypes[i] + "*)(output->args[" + str(id) +"]);\n")
                # else:
                #     replace_parse_args_start = True
            elif replace_main_start and (not replace_main_end):
                replace_main_end = True
                replace_tilein_end = True
                #fo.writelines(line) #drop one line to skip '{'
            elif replace_tilein_end and (not replace_tileout_start) \
                 and re.search("xi_tile[0-9]D tile_" + outputnames[0],line):
                output4D.append("xi_tile4D" in line)
                replace_tileout_start = True
                fo.writelines(line)
                tile_type = line.strip().split(' ')[0]
                fo.writelines("    " + tile_type + " tile_" + outputnames[0] + "_sp;\n")
                replace_tileout_cnt += 1
                if len(outputnames) < 2:
                    replace_tileout_end = True
            elif replace_tileout_start and (not replace_tileout_end):
                fo.writelines(line)
                output4D.append("xi_tile4D" in line)
                tile_type = line.strip().split(' ')[0]
                fo.writelines("    " + tile_type + " tile_" + outputnames[replace_tileout_cnt] + "_sp;\n")
                replace_tileout_cnt += 1
                if replace_tileout_cnt == len(outputnames):
                    # fo.writelines("    printf(\"inf init finish\\n\");\n")
                    replace_tileout_end = True
            #support multi output
            elif (not tile_cvt_reg_start) and re.search("XI_TILE[0-9]D_SET_BUFF_PTR",line) \
                 and outputnames[0] in line:
                tile_cvt_reg_start = True
                fo.writelines(line)
                tstr = re.findall("[\s,a-z,0-9,'_','-']+", \
                    re.findall("\([\s,a-z,0-9,'_','-']*\*\s*\)", line)[0])[0]
                tmp = re.sub(outputnames[0], outputnames[0] + "_sp", line)
                newline = re.sub("\([\s,a-z,0-9,'_','-']*\*\s*\)","(" + outputdtypes[0] + " *)",tmp)
                fo.writelines(newline)
            elif tile_cvt_reg_start and (not tile_cvt_reg_end):
                if ';' in line:
                    fo.writelines(line)
                    if re.search("XI_TILE[0-9]D_SET_",line):
                        for i, outname in enumerate(outputnames):
                            if outname in line:
                                break
                        tmp = re.sub(outname, outname + "_sp", line)
                        if re.search("XI_TILE[0-9]D_SET_BUFF_SIZE",line):
                            lens = re.findall("[0-9]+", re.findall(",\s*[0-9]+", line)[0])[0]
                            newline = re.sub(",\s*[0-9]+", ", " +
                                lens + " / sizeof(" + tstr + ") * sizeof(" + outputdtypes[i] + ") ", tmp)
                        elif re.search("XI_TILE[0-9]D_SET_TYPE",line):
                            tile_type = re.findall("XI_TILE[0-9]D", \
                                re.findall(",\s+XI_TILE[0-9]D_[A-Z,0-9]*", line)[0])[0]
                            if outputdtypes[i] == "float":
                                str_post = "_F32"
                            elif outputdtypes[i] == "uint8_t":
                                str_post = "_U8"
                            elif outputdtypes[i] == "int8_t":
                                str_post = "_S8"
                            elif outputdtypes[i] == "uint16_t":
                                str_post = "_U16"
                            elif outputdtypes[i] == "int16_t":
                                str_post = "_S16"
                            elif outputdtypes[i] == "uint32_t":
                                str_post = "_U32"
                            elif outputdtypes[i] == "int32_t":
                                str_post = "_S32"
                            else:
                                str_post = "_F32"
                            newline = re.sub(",\s+XI_TILE[0-9]D_[A-Z,0-9]*", ", "+ tile_type + str_post, tmp)
                        elif len(re.findall("\([\s,a-z,0-9,'_','-']*\*\s*\)", line)) > 0:
                            tstr = re.findall("[\s,a-z,0-9,'_','-']+", \
                                re.findall("\([\s,a-z,0-9,'_','-']*\*\s*\)", line)[0])[0]
                            newline = re.sub("\([\s,a-z,0-9,'_','-']*\*\s*\)","(" + outputdtypes[i] +" *)",tmp)
                        else:
                            newline = tmp
                        fo.writelines(newline)
                    else:
                       tile_cvt_reg_end = True
                else:
                    fo.writelines(line)
            elif tile_cvt_ready and "#if ENABLE_VERIFY" in line:
                # fo.writelines("    printf(\"cvt out start\\n\");\n")
                for i, outname in enumerate(outputnames):
                    #print(outputtypes[i], outputdtypes[i])
                    if outputdtypes[i] == "float":
                        if output4D[i]:
                            fo.writelines("    XI_TILE4D_DEQUANTIZE(&(tile_" + outname + \
                                "), &(tile_" + outname + "_sp), 1.0f/"+ outputquan[i] + "f);\n")
                        else:
                            fo.writelines("    xiDataConversion3D_IXFLOAT(&(tile_" + outname + \
                                "), &(tile_" + outname + "_sp), 1.0f/"+ outputquan[i] + "f);\n")
                    elif outputtypes[i] != "float":
                        if os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt"):
                            with open("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt", "r") as fp:
                                out_scales = fp.readlines()
                            with open("/root/.tvm/slimai_workspace/output/build_dir/output_zps.txt", "r") as fp:
                                out_zps = fp.readlines()
                        with open("/root/.tvm/slimai_workspace/output/" + name + "_opt/test_inference_" + name + "_opt/test_inference.c",'r') as finf:
                            for inf_line in finf:
                                if "DataDump3D" in inf_line and "tile_" + outname in inf_line:
                                    segs = re.split(r',',inf_line)
                                    fscale = float(segs[1].strip())
                        if os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/output_scales.txt"):
                            for j, on in enumerate(out_names):
                                final_oname = ''.join([c if c.isalnum() else '_' for c in on.strip()])
                                if final_oname in outname:
                                    id = j
                                    break
                            oscale = float(out_scales[id].strip())
                            ozp = int(out_zps[id].strip())
                        else:
                            oscale = 0.0
                            ozp = 0
                        if math.fabs(oscale) > 1e-6:
                            scale, shift = find_scale_shift(fscale*oscale, 24)
                            zp = int(-1 * ozp * fscale * oscale)
                            print("scale shift zeropoint from quntization parameter:", scale, shift, zp)
                            if zp == 0:
                                fo.writelines("    xiDataConversion3D(&(tile_" + outname + \
                                    "), &(tile_" + outname + "_sp), " + str(scale) + ", " + str(shift) + ");\n")
                            else:
                                fo.writelines("    xiDataConversion3D_asym(&(tile_" + outname + \
                                    "), &(tile_" + outname + "_sp), " + str(zp) + ", " + str(scale) + ", " + str(shift) + ");\n")
                        else:
                            print("no quntization parameter, do conversion only")
                            fo.writelines("    xiDataConversion3D(&(tile_" + outname + \
                                "), &(tile_" + outname + "_sp), 1, 0);\n")
                fo.writelines(line)
                tile_cvt_ready = False
            elif (not replace_rm_start) and "parse_args(argc" in line:
                replace_rm_start = True
            elif replace_rm_start and (not replace_rm_end):
                if "size_t scratch_size = SCRATCH_BUFFER_SIZE" in line or "allocate_aligned_buffer" in line:
                    replace_rm_end = True
                    fo.writelines(line)
            elif (not replace_return) :
                if "cnnrt_deinit()" in line:
                    # fo.writelines("    printf(\"return\\n\");\n")
                    replace_return = True
                    fo.writelines("   return status;\n")
                    fo.writelines("}\n")
                elif "load_bin" not in line and "initialize_" + name + "_opt_io" not in line:
                    if "execute_" + name + "_opt(" in line:
                        tile_cvt_ready = True
                    fo.writelines(line)
    fo.close()
    os.system("rm ./test_random_" + name + "_opt/test_random.c")

    os.system("rm -rf test_inference_" + name + "_opt/")
    if os.path.exists("./test_classification_" + name + "_opt/"):
        os.system("rm -rf test_classification_" + name + "_opt/")

    #move files all to build_dir
    has_custom_layer = False
    if os.path.exists("/root/.tvm/slimai_workspace/output/" + name + "_opt/libsupported_custom_layers"):
        has_internal_custom_layer = True
        has_custom_layer = True
    else:
        has_internal_custom_layer = False
    list = os.listdir("/root/.tvm/slimai_workspace/output/" + name + "_opt/")
    for forp in list:
        if os.path.isfile("/root/.tvm/slimai_workspace/output/" + name + "_opt/" + forp) :
            if "Makefile" in forp :
                os.system("mv /root/.tvm/slimai_workspace/output/" + name + "_opt/" + forp + \
                  " /root/.tvm/slimai_workspace/output/build_dir/")
        else:
            if "build" in forp or "test_random" in forp or "info" in forp:
                if "test_random" in forp and not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/elf_proj/.settings"):
                    os.system("mv -f /root/.tvm/slimai_workspace/output/" + name + "_opt/test_random_" + name + \
                      "_opt/.settings /root/.tvm/slimai_workspace/output/build_dir/elf_proj/.settings")
            else:
                if "opt_custom_layers" in forp:
                    has_custom_layer = True
                    if not os.path.exists( \
                      "/root/.tvm/slimai_workspace/output/build_dir/libcommon_custom_layers"):
                        os.system("mv -f /root/.tvm/slimai_workspace/output/" + name + "_opt/" + forp + \
                          " /root/.tvm/slimai_workspace/output/" + name + "_opt/libcommon_custom_layers")
                        rewrite_custom_layers("/root/.tvm/slimai_workspace/output/" + name + "_opt/", \
                          "libcommon_custom_layers", "/root/.tvm/slimai_workspace/output/" + name + "_opt/libcommon_custom_layers", \
                          name, has_internal_custom_layer)
                        forp = "libcommon_custom_layers"
                    else:
                        if has_internal_custom_layer:
                            rewrite_custom_layers("/root/.tvm/slimai_workspace/output/" + name + "_opt/", \
                                forp,"/root/.tvm/slimai_workspace/output/build_dir/libcommon_custom_layers", \
                                 name, has_internal_custom_layer)
                        continue
                if not os.path.exists("/root/.tvm/slimai_workspace/output/build_dir/" + forp):
                    os.system("mv -f /root/.tvm/slimai_workspace/output/" + name + "_opt/" + forp + \
                    " /root/.tvm/slimai_workspace/output/build_dir/" + forp)
    if has_custom_layer:
        rewrite_custom_layers_include("/root/.tvm/slimai_workspace/output/build_dir/lib" + name + "_opt/", \
          name)
    os.system("rm -rf /root/.tvm/slimai_workspace/output/" + name + "_opt/")

    os.chdir(retpath)

def build_firmware(elfname, retpath, uout):
    """compile the code

    Parameters
    ----------
    elfname   : str
        output elf name
    retpath   : str
        the path to be returned to after the xnnc compilation
    uout      : str
        the path to output to user

    Returns
    -------
    """
    xrp_code_dir = "/root/xnnc/"
    xnnc_xrp_path = os.getenv('XNNC_XRP_CODE_PATH')
    if xnnc_xrp_path is not None:
        xrp_code_dir = xnnc_xrp_path
    with open("%s/libxrp-dsp/xrp_dsp.c"%(xrp_code_dir), "r") as fi:
        contents = fi.readlines()
    need_update1 = True
    for l, line in enumerate(contents):
        if "do_handshake(device->dsp_cmd)" in line:
            update_p0 = l
        elif "UPEATE_DISPATCH_ABNORMAL_FLAG3" in line:
            need_update1 = False
    if need_update1:
        #add backward & last line added first
        contents.insert(update_p0+2, "                status = XRP_STATUS_SUCCESS;\n")
        contents.insert(update_p0+2, '                pr_debug("%s: skip %d;",__func__, __LINE__);\n')
        contents.insert(update_p0+2, '	}else if (flags == 3) {//UPEATE_DISPATCH_ABNORMAL_FLAG3\n')

        fo = open("%s/libxrp-dsp/xrp_dsp.c"%(xrp_code_dir),"w")
        contents = "".join(contents)
        fo.write(contents)
        fo.close()

    with open("%s/libxrp-dsp/include/xrp_xnnc_ns.h"%(xrp_code_dir), "r") as fi:
        contents = fi.readlines()
    need_add_uni2d = True
    for l, line in enumerate(contents):
        if "XFL_XNNC_NAME = XFL_NUM_OPS" in line:
            h_p0 = l
        elif "UNI2D_NUM_OPS = " in line:
            # line = re.sub("[0-9]+","80",line)
            need_add_uni2d = False
    if need_add_uni2d:
        contents.insert(h_p0+1, "    UNI2D_XNNC_NAME = UNI2D_NUM_OPS,\n")
        contents.insert(h_p0+1, '    UNI2D_NUM_OPS = 64,\n')

        fo = open("%s/libxrp-dsp/include/xrp_xnnc_ns.h"%(xrp_code_dir),"w")
        contents = "".join(contents)
        fo.write(contents)
        fo.close()

    with open("%s/target_template.h"%(xrp_code_dir), "r") as fi:
        contents = fi.readlines()
    need_add_uni2d = True
    for l, line in enumerate(contents):
        if '#include "xrp_dsp_hw.h"' in line:
            h_p0 = l
        elif 'unsigned char XRP_XNNC_NSID[] = XRP_XNNC_NSID_INITIALIZER;' in line:
            h_p1 = l
        elif 'arena_static_alloc((void **)&local_cmd_bufs' in line:
            h_p2 = l
        elif '#include "uni2d_cv.h"' in line:
            need_add_uni2d = False
    if need_add_uni2d:
        #add backward & last line added firs
        contents.insert(h_p2+1, '    set_cmd_bufs(local_cmd_bufs);\n')
        contents.insert(h_p1-1, '    register_uni2d_ns(device);\n')
        contents.insert(h_p1-1, '    unset_cmd_bufs();\n')
        contents.insert(h_p0+1, '#include "uni2d_cv.h"\n')

        fo = open("%s/target_template.h"%(xrp_code_dir),"w")
        contents = "".join(contents)
        fo.write(contents)
        fo.close()

    need_add_uni2d = True
    tvm_home_path = os.getenv('TVM_HOME')
    if os.path.exists("%s/libuni2d_cv"%(xrp_code_dir)):
        with open("%s/libuni2d_cv/src/uni2d_op_list.c"%(xrp_code_dir), "r") as fi:
            for line in fi:
                if "uni2d_cv_V" in line:
                    build_system_ver = int(line.strip().split(' ')[0].split('uni2d_cv_V')[1])
                    break
        with open("%s/vendor/sdrv/source/slimai/libuni2d_cv/src/uni2d_op_list.c"%(tvm_home_path), "r") as fi:
            for line in fi:
                if "uni2d_cv_V" in line:
                    source_ver = int(line.strip().split(' ')[0].split('uni2d_cv_V')[1])
                    break
        if source_ver > build_system_ver:
            os.system("rm -rf %s/libuni2d_cv"%(xrp_code_dir))
            os.system("cp -r %s/vendor/sdrv/source/slimai/libuni2d_cv %s/" %(tvm_home_path, xrp_code_dir) )

    else:
        os.system("cp -r %s/vendor/sdrv/source/slimai/libuni2d_cv %s/" %(tvm_home_path, xrp_code_dir) )
    os.system("cp -r %s/libuni2d_cv/ /root/.tvm/slimai_workspace/output/build_dir/"%(xrp_code_dir))

    os.system("cp -r %s/libxrp-dsp/ /root/.tvm/slimai_workspace/output/build_dir/"%(xrp_code_dir))
    os.chdir("/root/.tvm/slimai_workspace/output/build_dir")

    # patch libxi cnn files
    if os.path.exists("%s/vendor/sdrv/source/slimai/libxi/cnn/src/datatransform.c" %(tvm_home_path)):
        f1 = open("/root/.tvm/slimai_workspace/output/build_dir/libxi/cnn/src/datatransform.c", 'a+')
        f2 = open("%s/vendor/sdrv/source/slimai/libxi/cnn/src/datatransform.c" %(tvm_home_path), 'r')
        f1.write(f2.read())
        f1.close()
        f2.close()
    if os.path.exists("%s/vendor/sdrv/source/slimai/libxi/include/xi_cnn_api.h" %(tvm_home_path)):
        f1 = open("/root/.tvm/slimai_workspace/output/build_dir/libxi/include/xi_cnn_api.h", 'a+')
        f2 = open("%s/vendor/sdrv/source/slimai/libxi/include/xi_cnn_api.h" %(tvm_home_path), 'r')
        f1.write(f2.read())
        f1.close()
        f2.close()

    add_include = False
    add_lib = False
    change_compile_target = False
    change_link_libraries = False
    change_install = False
    fo = open("./elf_proj/CMakeLists.tmp", "w")
    with open("./elf_proj/CMakeLists.txt", "r") as fi:
        for line in fi:
            if (not add_include) and "include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libcommon/include)" in line:
                fo.writelines(line)
                fo.writelines("include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libxrp-dsp/include)\n")
                fo.writelines("include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../libuni2d_cv/include)\n")
                add_include = True
            elif (not add_lib) and "find_library(LIB_shared NAMES shared)" in line:
                fo.writelines(line)
                fo.writelines("find_library(LIB_xrp-dsp NAMES xrp-dsp)\n")
                fo.writelines("find_library(LIB_uni2d_cv NAMES uni2d_cv)\n")
                add_lib = True
            elif (not change_compile_target) and "add_executable(test_random test_random.c" in line:
                model_nums = len(line.split(" ")) - 1
                newline  = line.replace("test_random test_random.c", elfname + " xtensa.c")
                fo.writelines(newline)
                change_compile_target = True
            elif (not change_link_libraries) and "target_link_libraries(test_random" in line:
                newline  = line.replace("test_random", elfname + " ${LIB_uni2d_cv} ${LIB_xrp-dsp}")
                fo.writelines(newline)
                change_link_libraries = True
            elif (not change_install) and "install(TARGETS test_random DESTINATION bin)" in line:
                fo.writelines("install(TARGETS " + elfname + " DESTINATION bin)\n")
                change_install = True
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv ./elf_proj/CMakeLists.tmp ./elf_proj/CMakeLists.txt")

    add_op_list = False
    fo = open("./elf_proj/xtensa.tmp", "w")
    with open("./elf_proj/xtensa.c", "r") as fi:
        for line in fi:
            if (not add_op_list) and "#if ENABLE_VERIFY" in line:
                fo.writelines("#include \"%s/target_template_head.h\"\n"%(xrp_code_dir))
                fo.writelines("void XI_TILE4D_DEQUANTIZE(const xi_pTile4D in, xi_pTile4D out, const float ratio)\n")
                fo.writelines("{\n")
                fo.writelines("	xi_tile3D in3d;\n")
                fo.writelines("	xi_tile3D out3d;\n")
                fo.writelines("	in3d.pBuffer = in->pBuffer;\n")
                fo.writelines("	out3d.pBuffer = out->pBuffer;\n")
                fo.writelines("	in3d.bufferSize = in->bufferSize;\n")
                fo.writelines("	out3d.bufferSize = out->bufferSize;\n")
                fo.writelines("	in3d.pData = in->pData;\n")
                fo.writelines("	out3d.pData = out->pData;\n")
                fo.writelines("	in3d.dim1Size = in->dim1Size;\n")
                fo.writelines("	out3d.dim1Size = out->dim1Size;\n")
                fo.writelines("	in3d.dim1Pitch = in->dim1Pitch;\n")
                fo.writelines("	out3d.dim1Pitch = out->dim1Pitch;\n")
                fo.writelines("	in3d.status = in->status;\n")
                fo.writelines("	out3d.status = out->status;\n")
                fo.writelines("	in3d.type = in->type;\n")
                fo.writelines("	out3d.type = out->type;\n")
                fo.writelines("	in3d.dim2Size = in->dim2Size;\n")
                fo.writelines("	out3d.dim2Size = out->dim2Size;\n")
                fo.writelines("	in3d.pFrame = (xi_frame3D *)in->pFrame;\n")
                fo.writelines("	out3d.pFrame = (xi_frame3D *)out->pFrame;\n")
                fo.writelines("	in3d.dim1Loc = in->dim1Loc;\n")
                fo.writelines("	out3d.dim1Loc = out->dim1Loc;\n")
                fo.writelines("	in3d.dim2Loc = in->dim2Loc;\n")
                fo.writelines("	out3d.dim2Loc = out->dim2Loc;\n")
                fo.writelines("	in3d.dim1Edge1 = in->dim1Edge1;\n")
                fo.writelines("	out3d.dim1Edge1 = out->dim1Edge1;\n")
                fo.writelines("	in3d.dim2Edge1 = in->dim2Edge1;\n")
                fo.writelines("	out3d.dim2Edge1 = out->dim2Edge1;\n")
                fo.writelines("	in3d.dim1Edge2 = in->dim1Edge2;\n")
                fo.writelines("	out3d.dim1Edge2 = out->dim1Edge2;\n")
                fo.writelines("	in3d.dim2Edge2 = in->dim2Edge2;\n")
                fo.writelines("	out3d.dim2Edge2 = out->dim2Edge2;\n")
                fo.writelines("	in3d.dim2Pitch = in->dim2Pitch;\n")
                fo.writelines("	out3d.dim2Pitch = out->dim2Pitch;\n")
                fo.writelines("	in3d.dim3Size = in->dim3Size*in->dim4Size;\n")
                fo.writelines("	out3d.dim3Size = out->dim3Size*out->dim4Size;\n")
                fo.writelines("	in3d.dataOrder = in->dataOrder;\n")
                fo.writelines("	out3d.dataOrder = out->dataOrder;\n")
                fo.writelines("	in3d.dim3Loc = in->dim3Loc;\n")
                fo.writelines("	out3d.dim3Loc = out->dim3Loc;\n")
                fo.writelines("	in3d.dim3Edge1 = in->dim3Edge1;\n")
                fo.writelines("	out3d.dim3Edge1 = out->dim3Edge1;\n")
                fo.writelines("	in3d.dim3Edge2 = in->dim3Edge2;\n")
                fo.writelines("	out3d.dim3Edge2 = out->dim3Edge2;\n")
                fo.writelines("	in3d.numPtilesDim1 = in->numPtilesDim1;\n")
                fo.writelines("	out3d.numPtilesDim1 = out->numPtilesDim1;\n")
                fo.writelines("	in3d.numPtilesDim2 = in->numPtilesDim2;\n")
                fo.writelines("	out3d.numPtilesDim2 = out->numPtilesDim2;\n")
                fo.writelines("	in3d.numPtilesDim3 = in->numPtilesDim3;\n")
                fo.writelines("	out3d.numPtilesDim3 = out->numPtilesDim3;\n")
                fo.writelines("   xiDataConversion3D_IXFLOAT(&in3d, &out3d, ratio);\n")
                fo.writelines("}\n")
                for k in range(model_nums):
                    fo.writelines("XI_ERR_TYPE flk_start_inf" + str(k) + \
                      "(const uint8_t *params, struct XtensaOperationArgs *input, struct XtensaOperationArgs *output);\n")
                fo.writelines("static void register_all_ops(){\n")
                for k in range(model_nums):
                    fo.writelines("    XtensaOpExecuteCallBacks[" + str(k) + \
                      "] = flk_start_inf"+ str(k) + ";\n")
                fo.writelines("}\n")
                fo.writelines("#include \"%s/target_template.h\"\n"%(xrp_code_dir))
                add_op_list = True
                fo.writelines(line)
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv ./elf_proj/xtensa.tmp ./elf_proj/xtensa.c")
    os.system("rm -rf /root/.tvm/slimai_workspace/temp/")

    fo = open("Makefile_elf.linux", "w")

    with open("Makefile.linux", "r") as fi:
        for line in fi:
            if "TESTS := $(addprefix do-build/,$(wildcard test_*))" in line:
                fo.writelines("TESTS := $(addprefix do-build/, $(wildcard elf_proj*))\n")
            else:
                fo.writelines(line)
    fo.close()
    os.system("mv Makefile Makefile_bak")
    os.system("mv Makefile_elf.linux Makefile")
    os.system("cp Makefile Makefile.linux")

    os.system("make -f Makefile.linux build-xtensa BUILD_TYPE=Release \
        ENABLE_VERIFY=0 NO_REF_TABLES=1 CNNRT_PERF_CONTROL_ISS=0 CNNRT_PERF_LEVEL=0 \
        LSP=lsp_semidrive -j$(nproc)")

    os.system("mv build/bin/"+ elfname + " /root/.tvm/slimai_workspace/elf/")

    #move the generated files from tmp output dir to user defined output dir
    if not os.path.exists(uout):
        os.system("mkdir -p " + uout)
    slimai_odebug = os.getenv('SLIMAI_OUTPUT_DEBUG')
    # list = os.listdir("/root/.tvm/slimai_workspace/output/")
    # for forp in list:
    #     if slimai_odebug == None:
    #         if name + "_opt" in forp:
    #             if os.path.isfile("/root/.tvm/slimai_workspace/output/" + forp):
    #                 os.system("rm /root/.tvm/slimai_workspace/output/" + forp)
    #             else:
    #                 os.system("rm -rf /root/.tvm/slimai_workspace/output/" + forp)
    #         else:
    #             os.system("mv /root/.tvm/slimai_workspace/output/" + forp + " " + uout + "/")
    #     else:
    #         os.system("mv /root/.tvm/slimai_workspace/output/" + forp + " " + uout + "/")
    os.chdir(retpath)
    f_list = os.listdir("/root/.tvm/slimai_workspace/output/")
    for f in f_list:
        if os.path.splitext(f)[1]  == '.xws':
            os.system("rm /root/.tvm/slimai_workspace/output/*_opt.xws")
            break

# -*- coding: utf-8 -*-
import json
import requests
import re

# import os
# import shutil
from time import time, sleep
import random
import numpy as np

# import traceback
import datetime
from functools import wraps

# from isqmap import transpile
# from qcis_to_qasm.qcis_to_qasm import QcisToQasm
# from qasm_to_qcis.qasm_to_qcis import QasmToQcis
# from sabreMapper.sabre_mapper import SabreMapper
from typing import List, Optional, Dict, Union

# from simplify import QCIS_Simplify, QASM_Simplify


class Account:

    def __init__(
        self, login_key: Optional[str] = None, machine_name: Optional[str] = None
    ):
        """accout initialization

        Args:
            login_key:
                API Token under personal center on the web. Defaults to None. Defaults to None.
            machine_name:
                name of quantum computer. Defaults to None.

        Raises:
            Exception: throw an exception when login fails
        """
        # self.qasmtoqcis = QasmToQcis()
        # self.qcistoqasm = QcisToQasm()
        # self.qcis_simplify = QCIS_Simplify()
        # self.qasm_simplify = QASM_Simplify()
        self.login_key = login_key
        self.token = None
        self.machine_name = machine_name
        cloud_url = "https://quantumcomputer.ac.cn/"
        self.base_url = f"{cloud_url}"
        self.login = self.log_in()
        if self.machine_name:
            self.set_machine(self.machine_name)
        if self.login == 0:
            raise Exception("登录失败")
        self.computer_selection_mark = 1  # 0--原来老的12比特  1--新的66比特

    def reconnect_on_failuer(func, max_retries=2, retry_delay=1):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    print(
                        f"{func.__name__} execution failed, "
                        f"try count:{retries + 1} error info:{e}"
                    )
                    if retries == max_retries:
                        break
                    if hasattr(e, "code") and e.code == 10100101:
                        # 说明是token未设置，需要重新登录
                        print("user token loss or not set, log in again.")
                        self.log_in()
                        sleep(retry_delay)
                    retries = retries + 1
            raise Exception(
                f"function:[{func.__name__}] Max retries exceeded. Attempt {max_retries} times failed. "
            )

        return wrapper

    @reconnect_on_failuer
    def log_in(self):
        """Authenticate username and password and return user credit

        Returns:
            int: log in state, 1 means pass authentication, 0 means failed

        """
        url = f"{self.base_url}/sdk/api/user/login"
        data = {"loginToken": self.login_key}
        res = requests.post(url, json=data)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"登录失败, 请求接口失败, status_code:{status_code}")
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "登录失败")
        if code != 0:
            print(f"登录失败：{msg}")
            raise Exception(f"登录失败：{msg}")
        token = result.get("data").get("token")
        self.token = token
        return 1

    @reconnect_on_failuer
    def create_experiment(self, exp_name: str):
        """create a new experiment, the new one is the experiment set ID.

        Args:
            exp_name: new experiment collection Name

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the experimental set id
        """
        if self.computer_selection_mark:
            url = f"{self.base_url}/sdk/api/multiple/experiment/save"
        else:
            url = f"{self.base_url}/sdk/api/experiment/save"
        print("当前创建实验使用的机器名:", self.machine_name)
        data = {
            "experimentClipId": "",
            "name": exp_name,
            "machineName": self.machine_name,
            "source": "SDK",
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"创建实验失败, 请求接口失败, status_code:{status_code}")
        result = json.loads(res.text)
        code = result.get("code", -1)
        if code == -10:
            raise TokenNotSetException()
        msg = result.get("msg", "创建实验失败")
        if code != 0:
            print(f"创建实验失败：{msg}")
            return 0
        lab_id = result.get("data").get("lab_id")
        return lab_id

    @reconnect_on_failuer
    def save_experiment(
        self, lab_id: str, exp_data: str, version: str, is_verify: Optional[bool] = True
    ):
        """save the experiment and return the experiment ID.

        Args:
            lab_id:
                the result returned by the create_experiment interface, experimental set id
            exp_data:
                experimental content, qics
            version:
                version description
            is_verify:
                Is the circuit verified.True verify, False do not verify. Defaults to True.

        Examples:
            the input parameter can be the following value:

                lab_id: XXX
                exp_data:
                    X Q1
                    Y Q12
                    S Q3
                    SD Q15
                    T Q12
                    TD Q3
                    Z Q12
                    H Q1
                    RX Q3 2.78
                    RY Q9 1.97
                    RXY Q15 1.23 3.04
                    X2P Q1
                    X2M Q1
                    Y2P Q3
                    Y2M Q12
                    X Q19
                    CZ Q1 Q7
                    RZ Q8 2.16
                    I Q1 100
                    B Q1 Q12 Q3
                    M Q15 Q12 Q5 Q6

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the experiment id
        """
        exp_data = exp_data.upper()
        exp_data = self.get_experiment_data(exp_data)
        if self.computer_selection_mark:
            url = f"{self.base_url}/sdk/api/multiple/experiment/detail/save"
        else:
            url = f"{self.base_url}/sdk/api/experiment/detail/save"
        data = {
            "circuit": exp_data,
            "lab_id": lab_id,
            "language": "qcis",
            "version": version,
            "machineName": self.machine_name,
            "is_verify": is_verify,
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"保存实验失败, 请求接口失败, status_code:{status_code}")
        result = json.loads(res.text)
        code = result.get("code", -1)
        if code == -10:
            raise TokenNotSetException()
        msg = result.get("msg", "保存实验失败")
        if code != 0:
            print(f"保存实验失败：{msg}")
            return 0
        save_result = result.get("data").get("exp_id")

        return save_result

    @reconnect_on_failuer
    def run_experiment(self, exp_id: str, num_shots: Optional[int] = 12000):
        """running the experiment returns the query result id.

        Args:
            exp_id:
                the result returned by the save_experiment interface, experimental id
            num_shots:
                number of repetitions per experiment. Defaults to 12000.

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the query id.
        """
        if self.computer_selection_mark:
            url = f"{self.base_url}/sdk/api/multiple/experiment/temporary/save"
        else:
            url = f"{self.base_url}/sdk/api/experiment/temporary/save"
        data = {
            "circuit": [""],
            "exp_id": exp_id,
            "lab_id": "",
            "query_id": [""],
            "shots": num_shots,
            "version": "",
            "machineName": self.machine_name,
            "source": "SDK",
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"运行实验失败, 请求接口失败, status_code:{status_code}")
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "运行实验失败")
        if code == -10:
            raise TokenNotSetException()
        if code != 0:
            print(f"运行实验失败：{msg}, {result}")
            return 0
        run_result = result.get("data").get("query_id")
        return run_result

    @reconnect_on_failuer
    def query_experiment(
        self,
        query_id: Union[str, List[str]],
        max_wait_time: Optional[int] = 60,
        result_type=2,
    ):
        """query experimental results

        Args:
            query_id:
                the result returned by the run_experiment interface, experimental set id
            max_wait_time:
                maximum waiting time for querying experiments. Defaults to 60.
            result_type:
                election of return value type of other quantum computer except oneD12,
                only probability is returned by oneD12,
                result_type value of 0 represents the raw data,
                and a value of 1 represents the probability valueDefaults to 2.

            The maximum number of experimental result queries supported by the server is 50.
            If there are more than 50, an error message will be displayed.

        Raises:
            Exception: query experiment result type error

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the experimental result
        """
        if isinstance(query_id, str):
            query_id = [query_id]
        t0 = time()
        while time() - t0 < max_wait_time:
            try:
                if self.computer_selection_mark:
                    url = f"{self.base_url}/sdk/api/multiple/experiment/find/results"
                    if result_type not in [0, 1, 2]:
                        print("查询实验结果类型错误")
                        return 0
                else:
                    url = f"{self.base_url}/sdk/api/experiment/find/results"
                    result_type = 1
                data = {"query_id": query_id, "type": result_type}
                headers = {"sdk_token": self.token}
                res = requests.post(url, json=data, headers=headers)
                status_code = res.status_code
                if status_code != 200:
                    raise Exception(
                        f"查询实验失败, 请求接口失败, status_code:{status_code}"
                    )
                result = json.loads(res.text)
                code = result.get("code", -1)
                msg = result.get("msg", "查询实验失败")
                if code == -10:
                    raise TokenNotSetException()
                if code != 0:
                    print(f"查询实验失败：{msg}")
                    return 0
                query_exp = result.get("data", None)
                if query_exp:
                    return query_exp
            except:
                import traceback

                print(traceback.format_exc())
                continue
            sleep_time = random.randint(0, 15) * 0.3 + round(random.uniform(0, 1.5), 2)
            print(f"查询实验结果请等待: {{:.2f}}秒".format(sleep_time))
            sleep(sleep_time)
        raise Exception("查询实验结果失败, 实验结果为空")

    @reconnect_on_failuer
    def submit_job(
        self,
        circuit: Optional[Union[List, str]] = None,
        exp_name: Optional[str] = "exp0",
        parameters: Optional[List[List]] = None,
        values: Optional[List[List]] = None,
        num_shots: Optional[int] = 12000,
        lab_id: Optional[str] = None,
        exp_id: Optional[str] = None,
        version: Optional[str] = "version01",
        is_verify: Optional[bool] = True,
    ):
        """submit experimental tasks
            There are some parameter range limitations when using batch submission circiuts.
                1.  circuits length less than 50
                    numshots maximum 100000
                    the number of measurement qubits is less than 15
                2.  circuits length greater than 50 but less than 100
                    numshots maximum 50000
                    the number of measurement qubits is less than 30
                3.  circuits length greater than 100 but less than 600
                    numshots maximum 10000
                    the number of measurement bits is less than the number of all available qubits

        Args:
            circuit:
                experimental content, qics. Defaults to None.
            exp_name:
                new experiment collection Name. Defaults to 'exp0'.
            parameters:
                parameters that need to be assigned in the experimental content. Defaults to None.
            values:
                The values corresponding to the parameters that need to be assigned in the experimental content. Defaults to None.
            num_shots:
                number of repetitions per experiment. Defaults to 12000.
            lab_id:
                the result returned by the create_experiment interface, experimental set id. Defaults to None.
            exp_id:
                the result returned by the save_experiment interface, experimental id. Defaults to None.
            version:
                version description. Defaults to 'version01'.
            is_verify:
                Is the circuit verified.True verify, False do not verify. Defaults to True.

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the query id.
        """
        if isinstance(circuit, str):
            circuit = [circuit]
        if len(circuit) > 1:
            version = None
        if (
            circuit
            and parameters
            and values
            and len(parameters) == len(circuit) == len(values)
        ):
            new_circuit = self.assign_parameters(circuit, parameters, values)
            if not new_circuit:
                print("无法为线路赋值，请检查线路，参数和参数值之后重试")
                return 0
        else:
            new_circuit = circuit
        if self.computer_selection_mark:
            url = f"{self.base_url}/sdk/api/multiple/experiment/temporary/save"
        else:
            url = f"{self.base_url}/sdk/api/experiment/temporary/save"
        data = {
            "circuit": new_circuit,
            "exp_id": exp_id,
            "lab_id": lab_id,
            "name": exp_name,
            "shots": num_shots,
            "version": version,
            "machineName": self.machine_name,
            "source": "SDK",
            "is_verify": is_verify,
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(f"运行实验失败, 请求接口失败, status_code:{status_code}")
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "运行实验失败")
        if code == -10:
            raise TokenNotSetException()
        if code != 0:
            print(f"运行实验失败：{msg}")
            return 0
        run_result = result.get("data").get("query_id")
        return run_result

    def assign_parameters(
        self, circuits: List[str], parameters: List[List], values: List[List]
    ):
        """Check if the number of parameters, values match the circuit definition

        Args:
            circuits:
                string, QCIS circuit definition with or without parameter place holder
            parameters:
                list or ndarray of strings, parameters to be filled
            values:
                list or ndarray of floats, values to be assigned

        Returns:
            circuit: circuit with parameters replaced by values or empty string
            empty string occurs when errors prevents parameters to be assigned
        """
        new_circuit = []
        for circuit, parameter, value in zip(circuits, parameters, values):
            circuit = circuit.upper()
            p = re.compile(r"\{(\w+)\}")
            circuit_parameters = p.findall(circuit)
            if circuit_parameters:
                # # 如果values为整数或浮点数，改为列表格式##########################################################
                # if isinstance(values, (float, int)):
                #     values = [values]
                # # 如果parameters为字符格式，改为列表格式#########################################################
                # if isinstance(parameters, str):
                #     parameters = [parameters]

                # 将所有parameter变为大写， 否则set(parameters) != set(circuit_parameters) 不通过 ###############
                after_parameter = [p.upper() for p in parameter]

                if not value:
                    error_message = (
                        f"线路含有参数{circuit_parameters}, 请提供相应的参数值"
                    )
                    print(error_message)
                    return ""

                else:
                    if len(circuit_parameters) != len(value):
                        error_message = f"线路含有{len(circuit_parameters)}个参数, 您提供了{len(value)}个参数值"
                        print(error_message)
                        return ""

                    elif after_parameter and len(circuit_parameters) != len(
                        after_parameter
                    ):
                        error_message = f"线路含有{len(circuit_parameters)}个参数, 您提供了{len(after_parameter)}个参数"
                        print(error_message)
                        return ""

                    elif set(after_parameter) != set(circuit_parameters):
                        error_message = "线路中的参数与您输入的参数名称不符"
                        print(error_message)
                    else:
                        param_dic = {}
                        ############################# 这个转化可以删了 #########################################
                        # parameters_upper = [p.upper() for p in parameters]
                        for p, v in zip(after_parameter, value):
                            param_dic[p] = v
                        expData = circuit.format(**param_dic)
                        new_circuit.append(expData)
            elif parameter or value:
                error_message = "线路定义中不含有参数，无法接受您输入的参数或参数值"
                print(error_message)
                return ""
            else:
                expData = circuit
                new_circuit.append(expData)
        return new_circuit

    def get_experiment_data(self, circuit: str):
        """Parse circuit description and generate
           experiment script and extract number of measured qubits.

        Args:
            circuit:
                string, QCIS circuit

        Returns:
            expData:
                string, transformed circuit
        """
        # get gates from circuit
        if self.login_key:
            gates_list = circuit.split("\n")
            gates_list_strip = [g.strip() for g in gates_list if g]
            gates_list_strip = [g for g in gates_list_strip if g]

            # transform circuit from QCIS to expData
            expData = "\n".join(gates_list_strip)
            return expData
        else:
            gates_list = circuit.split("\n")
            gates_list_strip = [g.strip() for g in gates_list if g]
            gates_list_strip = [g for g in gates_list_strip if g]

            # transform circuit from QCIS to expData
            expData = ";".join(gates_list_strip)
            return expData

    @reconnect_on_failuer
    def set_machine(self, machine_name: str):
        """set the machine name.

        Args:
            machine_name: name of quantum computer.

        Raises:
            Exception: Failed to set machine name, request interface failed.
            Exception: Failed to set machine name.
        """
        url = f"{self.base_url}/sdk/api/quantum/computer/verify"
        data = {
            "experimentClipId": "",
            "machineName": machine_name,
            "name": "",
            "source": "SDK",
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(
                f"下载实验参数失败, 请求接口失败, status_code:{status_code}"
            )
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "设置机器名失败")
        if code == -10:
            raise TokenNotSetException()
        if code != 0:
            print(f"设置机器名失败：{msg}")
            return 0
        self.machine_name = machine_name
        data = result.get("data")
        if data:
            self.computer_selection_mark = 0
        else:
            self.computer_selection_mark = 1

    @reconnect_on_failuer
    def download_config(self, read_time=None, down_file: Optional[bool] = True):
        """except oneD12 quantum computer, download experimental parameters.

        Args:
            read_time:
                select configuration data according to the reading time, and the parameter format is yyyy-MM-dd HH:mm:ss, Defaults to None.
            down_file:
                the parameter is True to write to the file, and False to directly return the experimental parameters. Defaults to True.

        Returns:
            Union[int, str]: 0 failed, not 0 successful, success returns the experimental parameters.
        """
        if not self.computer_selection_mark:
            raise Exception(
                f"current quantum computer does not support download_config"
            )
        url = f"{self.base_url}/sdk/api/multiple/experiment/config/download"
        data = {"name": self.machine_name, "readTime": read_time}
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(
                f"下载实验参数失败, 请求接口失败, status_code:{status_code}"
            )
        result = json.loads(res.text)
        if "code" in result:
            msg = result.get("msg", "下载实验参数失败")
            print(f"下载实验参数失败:{msg}")
            return 0
        cur_time = self.current_time()
        if down_file:
            with open(f"./{self.machine_name}_config_param_{cur_time}.json", "w") as f:
                f.write(json.dumps(result))
        return result

    # def convert_qasm_to_qcis(
    #         self,
    #         qasm: str,
    #         qubit_map: Optional[Dict]=None
    #     ):
    #     """convert qasm to qcis.

    #     Args:
    #         qasm:
    #             qasm.
    #         qubit_map:
    #             Number mapping in qasm, where the value is None,
    #             directly maps bits based on the format of number plus 1. Defaults to None.
    #     Raises:
    #         Exception: language conversion failed.

    #     Returns:
    #         str: simplified qcis.
    #     """
    #     qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis(
    #         qasm, qubit_map=qubit_map)
    #     simplity_qcis = self.simplify_qcis(qcis_raw)
    #     return simplity_qcis

    # def convert_qasm_to_qcis_from_file(
    #         self,
    #         qasm_file: str,
    #         qubit_map: Optional[Dict]=None):
    #     """Read qasm from file and convert it to qcis

    #     Args:
    #         qasm_file:
    #             qasm file.
    #         qubit_map:
    #             Number mapping in qasm, where the value is None,
    #             directly maps bits based on the format of number plus 1. Defaults to None.

    #     Raises:
    #         Exception: language conversion failed.

    #     Returns:
    #         str: simplified qcis.
    #     """
    #     qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis_from_file(
    #         qasm_file, qubit_map=qubit_map)
    #     simplity_qcis = self.simplify_qcis(qcis_raw)
    #     return simplity_qcis

    # def convert_qcis_to_qasm(
    #         self,
    #         qcis: str
    #     ):
    #     """convert qcis to qasm.

    #     Args:
    #         qcis: qcis

    #     Returns:
    #         str: converted qasm.
    #     """
    #     qasm_circuit = self.qcistoqasm.convert_qcis_to_qasm(qcis)
    #     return qasm_circuit

    def qcis_check_regular(self, qcis_raw: str):
        """qcis regular check,normal returns 1, abnormal returns 0

        Args:
            qcis_raw: qcis

        Returns:
            Union[int, str]: 0 failed, not 0 successful, successfully returned the input qics.
        """
        url = f"{self.base_url}/server/api/multiple/experiment/verify"
        data = {"quantumComputerName": self.machine_name, "qcis": qcis_raw}
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(
                f"下载实验参数失败, 请求接口失败, status_code:{status_code}"
            )
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "qcis检验失败")
        if code == -10:
            raise TokenNotSetException()
        if code != 0:
            print(f"qcis检验失败: {msg}")
            return 0
        return qcis_raw

    # def simplify_qcis(
    #         self,
    #         qcis_raw: str):
    #     """simplification of qcis lines.
    #         If simplification fails, prompt an error message and return the original qcis circuit.

    #     Args:
    #         qcis_raw: qcis

    #     Returns:
    #         str: simplified qcis.
    #     """
    #     simplity_qcis = self.qcis_simplify.simplify(qcis_raw)
    #     return simplity_qcis

    # def simplify_qasm(self, qasm_raw: str):
    #     """simplification of qasm lines.
    #         If simplification fails, prompt an error message and return the original qasm circuit.

    #     Args:
    #         qasm_raw: qasm

    #     Returns:
    #         str: simplified qasm.
    #     """
    #     simplify_qasm = self.qasm_simplify.simplify(qasm_raw)
    #     return simplify_qasm

    def current_time(self):
        """get the current time

        Returns:
            str: time string
        """
        timestamp = datetime.datetime.fromtimestamp(time())
        str_time = timestamp.strftime("%Y%m%d%H%M%S")
        return str_time

    def readout_data_to_state_probabilities(self, result):
        state01 = result.get("results")
        basis_list = []
        basis_content = "".join(
            ["".join([str(s) for s in state]) for state in state01[1:]]
        )
        qubits_num = len(state01[0])  # 测量比特个数
        for idx in range(qubits_num):
            basis_result = basis_content[idx : len(basis_content) : qubits_num]
            basis_list.append([True if res == "1" else False for res in basis_result])
        return basis_list

    # 读取数据转换成量子态概率全部返回
    def readout_data_to_state_probabilities_whole(self, result: Dict):
        """read data and convert it into a quantum state probability, all returns.

        Args:
            result: the results returned after query_experiment.

        Returns:
            Dict: probability
        """
        if not self.computer_selection_mark:
            raise Exception(
                f"{self.machine_name}:current quantum computer does not support computational state probabilities"
            )
        basis_list = self.readout_data_to_state_probabilities(result)
        probabilities = self.original_onversion_whole(basis_list)
        return probabilities

    # 读取数据转换成量子态概率部分，概率为0不返回
    def readout_data_to_state_probabilities_part(self, result: Dict):
        """read data and convert it into a quantum state probability, do not return with a probability of 0.

        Args:
            result: the results returned after query_experiment.

        Returns:
            Dict: probability
        """
        if not self.computer_selection_mark:
            raise Exception(
                f"{self.machine_name}:current quantum computer does not support computational state probabilities"
            )
        basis_list = self.readout_data_to_state_probabilities(result)
        probabilities = self.original_onversion_part(basis_list)
        return probabilities

    def original_onversion_whole(self, state01):
        # 当state01为一维时转换成二维数据
        if isinstance(state01[0], bool):
            state01 = [state01]
        n = len(state01)  # 读取比特数
        # 测量比特概率限制
        # if n > MAX_QUBIT_NUM:
        #     print(f'Number of qubits > {MAX_QUBIT_NUM}, cannot calculate probabilities.')
        counts = [0] * (2**n)
        state01_T = np.transpose(state01)  # 转置
        numShots = len(state01_T)  # 测量重复次数
        # 统计所有numShots 列
        for num in range(numShots):
            k = 0
            for i in range(n):
                k += state01_T[num][i] * (2**i)
            counts[k] += 1
        # 计算概率
        # P=[counts[k]/numShots for k in range(2**n)]
        P = {bin(k)[2:].zfill(n): counts[k] / numShots for k in range(2**n)}
        return P

    def original_onversion_part(self, state01):
        # 当state01为一维时转换成二维数据
        if isinstance(state01[0], bool):
            state01 = [state01]
        n = len(state01)  # 读取比特数
        # 测量比特概率限制
        # if n > MAX_QUBIT_NUM:
        #     raise Exception(f'Number of qubits > {MAX_QUBIT_NUM}, cannot calculate probabilities.')
        counts = {}
        state01_T = np.transpose(state01)  # 转置
        numShots = len(state01_T)  # 测量重复次数
        # 统计所有numShots 列
        for num in range(numShots):
            k = 0
            for i in range(n):
                k += state01_T[num][i] * (2**i)
            prob_state = bin(k)[2:].zfill(n)
            if prob_state not in counts:
                counts[prob_state] = 1
            else:
                counts[prob_state] += 1
        # 计算概率
        # P=[counts[k]/numShots for k in range(2**n)]
        P = {k: v / numShots for k, v in counts.items()}
        return P

    # 量子态概率矫正
    def probability_calibration(self, result: Dict, config_json: Optional[Dict] = None):
        """correction of the measured probability of 01 quantum state.

        Args:
            result:
                the results returned after query_experiment.
            config_json:
                experimental parameters of quantum computer.
                config_json value is None, read the latest experimental parameters for calculation.
                Defaults to None.

        Raises:
            Exception: cannot calibrate probability with fidelity.

        Returns:
            Dict: corrected probability.
        """
        if not self.computer_selection_mark:
            raise Exception(
                f"{self.machine_name}:current quantum computer does not support computational probability correction"
            )
        CM_CACHE = {}
        if config_json is None:
            config_json = self.download_config(down_file=False)
        qubit_num = [f"Q{i}" for i in result.get("results")[0]]
        n = len(qubit_num)  # 测量比特个数
        qubits = config_json["readout"]["readoutArray"]["|0> readout fidelity"][
            "qubit_used"
        ]
        readout_fidelity0 = config_json["readout"]["readoutArray"][
            "|0> readout fidelity"
        ]["param_list"]
        readout_fidelity1 = config_json["readout"]["readoutArray"][
            "|1> readout fidelity"
        ]["param_list"]
        iq2probFidelity = [
            [readout_fidelity0[qubits.index(q)], readout_fidelity1[qubits.index(q)]]
            for q in qubit_num
        ]
        P = self.readout_data_to_state_probabilities_whole(result)
        Pm = list(P.values())
        if not isinstance(iq2probFidelity[0], list):
            iq2probFidelity = [iq2probFidelity]
        f = tuple([float(fi) for fi in sum(iq2probFidelity, [])])
        if f not in CM_CACHE:
            inv_CM = 1
            for k in iq2probFidelity[::-1]:
                F00 = k[0]
                F11 = k[1]
                if F00 + F11 == 1:
                    raise Exception(
                        f"Cannot calibrate probability with fidelity: [{F00}, {F11}]"
                    )
                inv_cm = np.array([[F11, F11 - 1], [F00 - 1, F00]]) / (F00 + F11 - 1)
                inv_CM = np.kron(inv_CM, inv_cm)
            CM_CACHE[f] = inv_CM
        else:
            inv_CM = CM_CACHE[f]
        Pi = np.dot(inv_CM, (np.array(Pm, ndmin=2).T))
        Pi = {bin(idx)[2:].zfill(n): k[0] for idx, k in enumerate(Pi)}
        return Pi

    # 对矫正后的概率进行修正
    def probability_correction(self, probabilities):
        """correction of the measured probability of 01 quantum state.
           If there is a probability greater than 1, change this item to 1;
           If there is anything less than 0, change the item to 0.

        Args:
            probabilities:
                corrected probability.

        Returns:
            Dict: corrected probability.
        """
        abnormal_fidelity_list = list(
            filter(lambda x: x < 0 or x > 1, probabilities.values())
        )
        if not abnormal_fidelity_list:
            return probabilities
        for k, v in probabilities.items():
            if v > 1:
                probabilities[k] = 1
            elif v < 0:
                probabilities[k] = 0
        fidelity_sum = sum(probabilities.values())
        for k, v in probabilities.items():
            probabilities[k] = v / fidelity_sum
        return probabilities

    def get_coupling_map(self, config_json):
        qubits = config_json["overview"]["qubits"]
        qubits_used = config_json["qubit"]["singleQubit"]["gate error"]["qubit_used"]
        disable_qubits = [q for q in qubits if q not in qubits_used]
        coupler_map = config_json["overview"]["coupler_map"]
        adjacency_list = []
        for Q1, Q2 in coupler_map.values():
            q1 = int(Q1[1:])
            q2 = int(Q2[1:])
            if Q1 in disable_qubits or Q2 in disable_qubits:
                continue
            adjacency_list.append([q1, q2])
        return adjacency_list

    # def qcis_mapping_isq(
    #         self,
    #         qcis_circuit: str,
    #         initial_layout: Optional[Dict]=None,
    #         objective: Optional[str]='size',
    #         seed: Optional[int]=None,
    #         use_post_opt: Optional[bool]=False):
    #     """The script transpiles qcis string by searching for a mapping from virtual to physical qubit
    #        and a swap strategy such that the circuit described by qcis can be fitted into a hardware
    #        described by the coupling_map, in the meanwhile reduces circuit depth.

    #     Args:
    #         qcis_circuit: qcis circuit
    #         initial_layout:
    #             Initial position of virtual qubits on physical qubits.
    #             If given, this is the initial state in search of virtual to physical qubit mapping
    #             e.g.:
    #                 {0:4, 1:1, 2:5, 3:2, 4:0, 5:3}. Defaults to None.
    #         objective:
    #             size: min. # of added swaps
    #             depth: min. depth
    #             no_swap: try best to find an initial mapping requiring no swaps; raise
    #             an error if fail. Defaults to 'size'.
    #         seed:
    #             Set random seed for the stochastic part of the tranpiler. Defaults to None.
    #         use_post_opt:
    #             we provide a genetic alg. which utilizes exchange rules for
    #             swaps to futher min. depth. Defaults to False.

    #     Raises:
    #         TranspileError: if graph specified by coupling map is disconnected.

    #     Returns:
    #         str: qcis string after transpilation
    #     """
    #     if not self.computer_selection_mark:
    #         raise Exception(f'current quantum computer does not support qcis_mapping_isq')
    #     config_json = self.download_config(down_file=False)
    #     coupling_map = self.get_coupling_map(config_json)
    #     try:
    #         qasm_circuit = self.convert_qcis_to_qasm(qcis_circuit)
    #         cur_time = self.current_time()
    #         qpu_file = f'./{self.machine_name}_config_param_{cur_time}.json'
    #         with open(qpu_file, 'w') as f:
    #             f.write(json.dumps(config_json))
    #         qasm_transpiled, _, _, _ = transpile(qasm_circuit,
    #                                              coupling_map,
    #                                              initial_layout=initial_layout,
    #                                              objective=objective,
    #                                              seed=seed,
    #                                              use_post_opt=use_post_opt)
    #         simplity_qcis = self.convert_qasm_to_qcis(qasm_transpiled)
    #         os.remove(qpu_file)
    #         return simplity_qcis
    #     except Exception as e:
    #         print(e)
    #         print(traceback.format_exc())
    #         print('circuit mapping error, will submit using the original route')
    #         os.remove(qpu_file)
    #         return qcis_circuit

    # def qcis_mapping_sabre(
    #         self,
    #         qcis_circuit: str):
    #     """The script transpiles qcis string by searching for a mapping from virtual to physical qubit
    #        and a swap strategy such that the circuit described by qcis can be fitted into a hardware
    #        described by the coupling_map, in the meanwhile reduces circuit depth.

    #     Args:
    #         qcis_circuit: qcis circuit

    #     Returns:
    #         str : qcis after mapping
    #     """
    #     if not self.computer_selection_mark:
    #         raise Exception(f'current quantum computer does not support qcis_mapping_quingo')
    #     config_json = self.download_config(down_file=False)
    #     try:
    #         # qcis转换成qasm并写入qasm_file中
    #         qasm_circuit = self.qcistoqasm.convert_qcis_to_qasm(qcis_circuit)
    #         folder_path = 'temp'
    #         if not os.path.exists(folder_path):
    #             os.makedirs(folder_path)
    #         qasm_file = f'{folder_path}/qasm.qasm'
    #         with open(qasm_file, 'w') as f:
    #             f.write(qasm_circuit)
    #         sabre = SabreMapper()
    #         # 组装chip_info_fn映射信息
    #         chip_info_fn = {}
    #         couplings = []
    #         coupler_maps = config_json.get('overview').get('coupler_map')
    #         coupler_used = config_json.get('twoQubitGate').get(
    #             'czGate').get('gate error').get('qubit_used')
    #         cz_gate_error = config_json.get('twoQubitGate').get(
    #             'czGate').get('gate error').get('param_list')
    #         for coupler, error in zip(coupler_used, cz_gate_error):
    #             fidelity = 1 - error
    #             coupler_qubit_map = coupler_maps.get(coupler)
    #             couplings.append(
    #                 {"fidelity": fidelity, "qubit pair": coupler_qubit_map})
    #         chip_info_fn['couplings'] = couplings
    #         qubit_used = config_json.get('qubit').get(
    #             'singleQubit').get('gate error').get('qubit_used')
    #         qubit_gate_error = config_json.get('qubit').get(
    #             'singleQubit').get('gate error').get('param_list')
    #         qubit_fidelity = {}
    #         for qubit, error in zip(qubit_used, qubit_gate_error):
    #             qubit_fidelity[qubit] = 1 - error
    #         chip_info_fn['fidelity'] = qubit_fidelity
    #         chip_info_fn['has multiple chips'] = False
    #         chip_info_fn['qubits'] = qubit_used

    #         chip_info_fn_file = f'{folder_path}/chip_info_fn.json'
    #         mapped_qasm_fn_file = f'{folder_path}/mapped_qasm_fn.qasm'
    #         qubit_mapping_fn_file = f'{folder_path}/qubit_mapping_fn.json'
    #         with open(chip_info_fn_file, 'w') as f:
    #             json.dump(chip_info_fn, f)
    #         # 调用quMapper做mapping操作
    #         success = sabre.map_schedule(
    #             qasm_file, chip_info_fn_file, mapped_qasm_fn_file, qubit_mapping_fn_file)
    #         if success:
    #             with open(qubit_mapping_fn_file, 'r') as f:
    #                 qubit_mapping_fn = json.load(f)
    #             qubit_map = qubit_mapping_fn.get('physical qubits idx')
    #             # mapping成功，将转换后的qasm转为qcis，其中编号根据physical qubits idx做映射
    #             simplity_qcis = self.convert_qasm_to_qcis_from_file(
    #                 mapped_qasm_fn_file, qubit_map)
    #             shutil.rmtree(folder_path)
    #             return simplity_qcis
    #     except Exception as e:
    #         print(e)
    #         print(traceback.format_exc())
    #         print('circuit mapping error, will submit using the original route')
    #         shutil.rmtree(folder_path)
    #         return qcis_circuit

    @reconnect_on_failuer
    def get_experiment_circuit(self, query_id: Union[str, List[str]]):
        """according to the exp_id obtained experimental circuit

        Args:
            query_id: the result returned by the run_experiment interface, experimental set id.

        The maximum number of experimental line queries supported by the server is 50.
        If it exceeds 50, an error message will be displayed.

        Returns:
            Union[int, List[Dict]]: 0 failed, not 0 successful, success returns the experimental circuit,
            The parameters of the returned experimental circuit include qcis、mapQcis and computerQcis,
            qcis is the line submitted by the user, mapQcis is the compiled circuit,
            computerQcis is a circuit submitted to a quantum computer.
        """
        if isinstance(query_id, str):
            query_id = [query_id]
        if self.computer_selection_mark:
            url = f"{self.base_url}/sdk/api/multiple/experiment/detail"
        else:
            url = f"{self.base_url}/sdk/api/experiment/detail/find"
        data = {"query_id": query_id}
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception(
                f"查询实验线路失败, 请求接口失败, status_code:{status_code}"
            )
        result = json.loads(res.text)
        code = result.get("code", -1)
        msg = result.get("msg", "查询实验线路失败")
        if code != 0:
            print(f"查询实验线路: {msg}")
            return 0
        circuit = result.get("data")
        return circuit


class StandradError(Exception):
    def __init__(self, msg="", code=0):
        self.msg = msg
        self.code = code

    def __str__(self):
        return f"[{self.code}] [{self.msg}]"


class TokenNotSetException(StandradError):
    code = 10100101

    def __init__(self):
        self.msg = f"user token has expired or not set."

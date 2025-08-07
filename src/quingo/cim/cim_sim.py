import numpy as np
from typing import Callable, Optional
import pycim as cim

def cim_envolve(
    couple_matrix: np.ndarray,
    round_number: int = 300,
    pump_coeff: float = 5e-3,
    intensity_value: float = 0.1,
    custom_pump_schedule: Optional[Callable] = None,
    custom_intensity: Optional[Callable] = None,
) -> np.ndarray:
    """
    执行CIM动力学模拟并返回演化结果

    参数:
        couple_matrix (np.ndarray): 耦合矩阵,描述系统相互作用
        round_number (int): 模拟轮数,默认300
        pump_coeff (float): 泵浦系数,默认0.005
        intensity_value (float): 耦合强度值,默认0.1
        custom_pump_schedule (Callable): 自定义泵浦函数,需接受时间参数t
        custom_intensity (Callable): 自定义耦合强度函数,需接受时间参数t

    返回:
        np.ndarray: 模拟结果数组,形状为(round_number, n_nodes)

    异常:
        ValueError: 耦合矩阵非方阵或泵浦系数为负
        RuntimeError: 未知错误
    """
    # 输入校验
    if couple_matrix.ndim != 2 or couple_matrix.shape[0] != couple_matrix.shape[1]:
        raise ValueError("耦合矩阵必须是方阵")
    if pump_coeff < 0:
        raise ValueError("泵浦系数不能为负")


    try:
        # 初始化设备与配置
        device = cim.simulation.device()
        setup = cim.simulation.setup()
        setup.round_number = round_number
        # times -1 according to match the simulator behavior
        setup.couple_matrix = -1 * couple_matrix

        # 使用自定义函数或默认实现
        setup.p = custom_pump_schedule or (lambda t: np.sqrt(pump_coeff * t))
        setup.intensity = custom_intensity or (lambda t: intensity_value)

        # 执行模拟
        sol_info = cim.simulation.singleSimulation(
            device, setup, model="meanField", solver="RK45"
        )
        return np.sign(sol_info.y[:, -1])

    except Exception as e:
        raise RuntimeError(f"未知错误: {str(e)}") from e
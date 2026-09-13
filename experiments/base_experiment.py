# ============================================================
# BASE EXPERIMENT
# experiments/base_experiment.py
# ============================================================

from abc import ABC, abstractmethod


class BaseExperiment(ABC):
    """
    Lớp cơ sở cho tất cả các thí nghiệm trong
    Virtual Chemistry Lab.

    BaseExperiment không phụ thuộc vào Kivy.

    Nhiệm vụ:
        - cung cấp metadata thống nhất cho Experiment
        - kiểm tra input cơ bản
        - định nghĩa interface calculate()
        - cung cấp get_info() cho tầng Application/UI
    """

    # ========================================================
    # EXPERIMENT METADATA
    # ========================================================

    id = ""
    name = ""
    category = ""
    description = ""
    equation = ""
    available = False

    # ========================================================
    # CALCULATION
    # ========================================================

    @abstractmethod
    def calculate(self, inputs):
        """
        Thực hiện tính toán thí nghiệm.

        Parameters
        ----------
        inputs : dict
            Dữ liệu đầu vào của thí nghiệm.

        Returns
        -------
        ReactionResult
            Kết quả tính toán.

        Raises
        ------
        NotImplementedError
            Nếu Experiment chưa triển khai calculate().
        """
        raise NotImplementedError

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_inputs(self, inputs):
        """
        Kiểm tra kiểu dữ liệu input ở mức cơ bản.

        Experiment cụ thể có thể override phương thức này
        để kiểm tra các tham số riêng.
        """
        if not isinstance(inputs, dict):
            raise TypeError("inputs phải là dictionary.")

    # ========================================================
    # METADATA
    # ========================================================

    def get_info(self):
        """
        Trả về metadata chuẩn hóa của Experiment.

        Các tầng phía trên có thể sử dụng get_info()
        thay vì phụ thuộc trực tiếp vào implementation
        của từng Experiment.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "equation": self.equation,
            "available": self.available,
        }
# ============================================================
# EXPERIMENT REGISTRY
# experiments/registry.py
# ============================================================

from models.experiment_definition import (
    ExperimentDefinition,
)

from experiments.implementation_registry import (
    ImplementationRegistry,
)

from experiments.experiment_resolver import (
    ExperimentResolver,
)

from experiments.experiment_bundle import (
    ExperimentBundle,
)


class ExperimentRegistry:
    """
    Central Registry của Virtual Chemistry Lab.

    Registry quản lý 3 lớp dữ liệu:

        1. Legacy implementation
           experiment_id -> implementation instance

        2. ExperimentDefinition
           experiment_id -> metadata

        3. Implementation mapping
           experiment_id -> factory

    Registry đồng thời cung cấp API tương thích
    với kiến trúc cũ và kiến trúc Resolution mới.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        experiments=None,
        definitions=None,
        data_loader=None,
        load_defaults=False,
    ):
        """
        Khởi tạo ExperimentRegistry.

        Parameters
        ----------
        experiments : iterable | None
            Danh sách Experiment implementation.

        definitions : iterable | None
            Danh sách ExperimentDefinition.

        data_loader : ExperimentDataLoader | None
            DataLoader dùng để load Definition.

        load_defaults : bool
            Nếu True, tự động đăng ký các experiment mặc định.

            Mặc định False để Registry sạch.
            Điều này rất quan trọng cho testing
            và dependency injection.
        """

        self._data_loader = data_loader

        # ========================================================
        # LEGACY IMPLEMENTATION STORAGE
        # ========================================================

        self._experiments = []
        self._experiment_map = {}

        # ========================================================
        # DEFINITION STORAGE
        # ========================================================

        self._definitions = []
        self._definition_map = {}

        # ========================================================
        # IMPLEMENTATION RESOLUTION
        # ========================================================

        self._implementation_registry = (
            ImplementationRegistry()
        )

        self._resolver = ExperimentResolver(
            self._implementation_registry
        )

        # ========================================================
        # EXPLICIT IMPLEMENTATIONS
        # ========================================================

        if experiments is not None:
            for experiment in experiments:
                self.register(experiment)

        # ========================================================
        # DEFAULT IMPLEMENTATIONS
        # ========================================================

        if load_defaults:
            for experiment in self._get_default_experiments():
                self.register(experiment)

        # ========================================================
        # DEFINITIONS
        # ========================================================

        if definitions is not None:
            for definition in definitions:
                self.register_definition(definition)

    # ========================================================
    # DEFAULT EXPERIMENTS
    # ========================================================

    def _get_default_experiments(self):
        """
        Trả về các implementation mặc định của hệ thống.

        Hiện tại VCL có Zn + HCl.
        """

        try:
            from experiments.zn_hcl import (
                ZnHClExperiment,
            )

            return [
                ZnHClExperiment()
            ]

        except ImportError:
            return []

    # ========================================================
    # LEGACY IMPLEMENTATION API
    # ========================================================

    def register(self, experiment):
        """
        Đăng ký một Experiment implementation.

        Experiment phải có thuộc tính id.

        Đồng thời implementation được đưa vào
        ImplementationRegistry dưới dạng factory.
        """

        if experiment is None:
            raise TypeError(
                "Experiment cannot be None."
            )

        experiment_id = getattr(
            experiment,
            "id",
            None,
        )

        if not isinstance(experiment_id, str):
            raise TypeError(
                "Experiment must have a string id."
            )

        experiment_id = experiment_id.strip()

        if not experiment_id:
            raise ValueError(
                "Experiment id cannot be empty."
            )

        if experiment_id in self._experiment_map:
            raise ValueError(
                f"Experiment already registered: "
                f"{experiment_id}"
            )

        # Legacy storage
        self._experiments.append(experiment)
        self._experiment_map[experiment_id] = experiment

        # New resolution storage
        #
        # Chúng ta dùng class của instance làm factory.
        if not self._implementation_registry.has(
            experiment_id
        ):
            self._implementation_registry.register(
                experiment_id,
                experiment.__class__,
            )

    # --------------------------------------------------------

    def get(self, experiment_id):
        """
        Lấy implementation theo id.

        Không tồn tại -> None.
        """

        return self._experiment_map.get(
            experiment_id
        )

    # --------------------------------------------------------

    def get_all(self):
        """
        Trả về danh sách implementation.

        Trả về list mới để caller không thể
        sửa trực tiếp storage nội bộ.
        """

        return list(self._experiments)

    # --------------------------------------------------------

    def exists(self, experiment_id):
        """
        Kiểm tra implementation tồn tại.
        """

        return experiment_id in self._experiment_map

    # ========================================================
    # DEFINITION API
    # ========================================================

    def register_definition(
        self,
        definition,
    ):
        """
        Đăng ký ExperimentDefinition.

        Raises
        ------
        TypeError
            Nếu object không phải ExperimentDefinition.

        ValueError
            Nếu id đã tồn tại.
        """

        if not isinstance(
            definition,
            ExperimentDefinition,
        ):
            raise TypeError(
                "definition must be an "
                "ExperimentDefinition."
            )

        definition_id = definition.id

        if definition_id in self._definition_map:
            raise ValueError(
                f"Definition {definition_id} đã được đăng ký."
            )

        self._definitions.append(
            definition
        )

        self._definition_map[
            definition_id
        ] = definition

        return definition

    # --------------------------------------------------------

    def get_definition(
        self,
        experiment_id,
    ):
        """
        Lấy Definition theo id.

        Không tồn tại -> None.
        """

        return self._definition_map.get(
            experiment_id
        )

    # --------------------------------------------------------

    def get_all_definitions(self):
        """
        Trả về toàn bộ Definition.

        Trả về list copy.
        """

        return list(
            self._definitions
        )

    # ========================================================
    # DATA LOADER
    # ========================================================

    def load_definition(
        self,
        experiment_id,
    ):
        """
        Load ExperimentDefinition thông qua DataLoader.

        Nếu không có DataLoader -> RuntimeError.

        Lỗi từ DataLoader được giữ nguyên,
        không nuốt exception.
        """

        if self._data_loader is None:
            raise RuntimeError(
                "ExperimentDataLoader is required "
                "to load a definition."
            )

        definition = (
            self._data_loader.load(
                experiment_id
            )
        )

        self.register_definition(
            definition
        )

        return definition

    # ========================================================
    # IMPLEMENTATION RESOLUTION API
    # ========================================================

    def register_implementation(
        self,
        experiment_id,
        factory,
    ):
        """
        Đăng ký factory cho experiment_id.

        Registry sẽ từ chối đăng ký trùng.
        """

        self._implementation_registry.register(
            experiment_id,
            factory,
        )

    # --------------------------------------------------------

    def has_implementation(
        self,
        experiment_id,
    ):
        """
        Kiểm tra implementation đã được đăng ký hay chưa.
        """

        return self._implementation_registry.has(
            experiment_id
        )

    # --------------------------------------------------------

    def get_implementation_factory(
        self,
        experiment_id,
    ):
        """
        Lấy factory của implementation.

        Nếu implementation không tồn tại,
        ImplementationRegistry sẽ raise KeyError.
        """

        return self._implementation_registry.get_factory(
            experiment_id
        )

    # --------------------------------------------------------

    def create_implementation(
        self,
        experiment_id,
    ):
        """
        Tạo implementation instance mới.

        Delegates cho ExperimentResolver.
        """

        return self._resolver.create(
            experiment_id
        )

    # ========================================================
    # RESOLVE
    # ========================================================

    def resolve(
        self,
        experiment_id,
    ):
        """
        Resolve experiment thành ExperimentBundle.

        Bundle gồm:

            - ExperimentDefinition
            - implementation instance

        Definition bắt buộc phải tồn tại.

        Implementation cũng bắt buộc phải tồn tại.
        """

        definition = self.get_definition(
            experiment_id
        )

        if definition is None:
            raise KeyError(
                f"Unknown experiment definition: "
                f"{experiment_id}"
            )

        implementation = (
            self.create_implementation(
                experiment_id
            )
        )

        return ExperimentBundle(
            definition=definition,
            experiment=implementation,
        )

    def definition_count(self):
        """
        Trả về số lượng ExperimentDefinition
        đang được đăng ký.
        """
        return len(self._definition_map)
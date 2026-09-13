class ImplementationRegistry:
    """
    Registry lưu mapping:

        experiment_id -> factory

    Registry này chỉ quản lý implementation.
    Không quản lý Definition.
    Không chạy simulation.
    """

    def __init__(self):
        self._factories = {}

    def register(self, experiment_id, factory):
        """
        Đăng ký factory cho một experiment.

        Raises:
            TypeError:
                Nếu factory không callable.

            ValueError:
                Nếu experiment_id đã tồn tại.
        """

        if not callable(factory):
            raise TypeError(
                "Experiment factory must be callable."
            )

        if experiment_id in self._factories:
            raise ValueError(
                f"Implementation already registered: "
                f"{experiment_id}"
            )

        self._factories[experiment_id] = factory

    def has(self, experiment_id):
        """
        Kiểm tra implementation đã được đăng ký hay chưa.
        """

        return experiment_id in self._factories

    def get_factory(self, experiment_id):
        """
        Trả về factory tương ứng.

        Raises:
            KeyError:
                Nếu experiment_id chưa được đăng ký.
        """

        if experiment_id not in self._factories:
            raise KeyError(
                f"Unknown experiment implementation: "
                f"{experiment_id}"
            )

        return self._factories[experiment_id]
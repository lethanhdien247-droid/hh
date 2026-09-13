from experiments.implementation_registry import (
    ImplementationRegistry,
)


class ExperimentResolver:
    """
    Resolve experiment_id thành một
    Experiment implementation instance.

    Resolver không quản lý Definition.
    Resolver không quản lý Bundle.
    """

    def __init__(
        self,
        implementation_registry: ImplementationRegistry,
    ):
        self._implementation_registry = (
            implementation_registry
        )

    def create(self, experiment_id):
        """
        Tạo một implementation instance mới.

        Mỗi lần gọi create() phải tạo instance mới.
        """

        factory = (
            self._implementation_registry
            .get_factory(experiment_id)
        )

        return factory()
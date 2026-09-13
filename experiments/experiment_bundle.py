class ExperimentBundle:
    """
    Bundle chứa Definition và implementation
    của cùng một experiment.

    Bundle không chạy simulation.
    """

    def __init__(
        self,
        definition,
        experiment,
    ):
        if definition is None:
            raise ValueError(
                "Experiment definition cannot be None."
            )

        if experiment is None:
            raise ValueError(
                "Experiment implementation cannot be None."
            )

        definition_id = getattr(
            definition,
            "id",
            None,
        )

        implementation_id = getattr(
            experiment,
            "id",
            None,
        )

        if definition_id is None:
            raise ValueError(
                "Experiment definition must have an id."
            )

        if implementation_id is None:
            raise ValueError(
                "Experiment implementation must have an id."
            )

        if definition_id != implementation_id:
            raise ValueError(
                "Experiment definition and implementation "
                "must have the same id."
            )

        self.definition = definition
        self.experiment = experiment

    @property
    def id(self):
        """
        ID của experiment.
        """

        return self.definition.id
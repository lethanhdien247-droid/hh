# ============================================================
# EXPERIMENT SERVICE
# services/experiment_service.py
# ============================================================

from experiments.registry import ExperimentRegistry


class ExperimentService:
    """
    Application service cho việc truy cập và tìm kiếm Experiment.

    Service nằm giữa UI/Application và ExperimentRegistry.

    Kiến trúc:
        UI
         ↓
        ExperimentService
         ↓
        ExperimentRegistry
         ↓
        Experiment
    """

    def __init__(self, registry=None):
        """
        Parameters
        ----------
        registry : ExperimentRegistry, optional
            Registry được inject từ bên ngoài.

            Nếu không truyền, Service tự tạo Registry mặc định
            với các Experiment có sẵn của hệ thống
            (load_defaults=True).
            Dependency injection giúp test Service dễ dàng hơn.
        """
        self._registry = registry or ExperimentRegistry(
            load_defaults=True
        )

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_experiments(self):
        """
        Lấy toàn bộ Experiment.

        Returns
        -------
        list
            Danh sách Experiment.
        """
        return self._registry.get_all()

    # ========================================================
    # GET ONE
    # ========================================================

    def get_experiment(self, experiment_id):
        """
        Lấy Experiment theo id.

        Returns
        -------
        BaseExperiment | None
            Experiment nếu tồn tại, ngược lại None.
        """
        return self._registry.get(experiment_id)

    # ========================================================
    # EXISTS
    # ========================================================

    def experiment_exists(self, experiment_id):
        """Kiểm tra Experiment có tồn tại hay không."""
        return self._registry.exists(experiment_id)

    # ========================================================
    # SEARCH
    # ========================================================

    def search_experiments(self, query):
        """
        Tìm Experiment theo tên, id, category hoặc description.

        Tìm kiếm không phân biệt hoa thường.

        query rỗng:
            trả về toàn bộ Experiment.

        Returns
        -------
        list
            Danh sách Experiment phù hợp.
        """
        if query is None:
            query = ""

        query = str(query).strip().lower()

        experiments = self._registry.get_all()

        if not query:
            return experiments

        results = []

        for experiment in experiments:
            info = experiment.get_info()

            searchable_text = " ".join(
                str(info.get(field, ""))
                for field in (
                    "id",
                    "name",
                    "category",
                    "description",
                    "equation",
                )
            ).lower()

            if query in searchable_text:
                results.append(experiment)

        return results

    # ========================================================
    # CATEGORIES
    # ========================================================

    def get_categories(self):
        """
        Lấy danh sách category duy nhất.

        Category rỗng sẽ không được đưa vào kết quả.

        Returns
        -------
        list[str]
            Danh sách category, giữ thứ tự xuất hiện.
        """
        categories = []

        for experiment in self._registry.get_all():
            category = getattr(experiment, "category", "")

            if category and category not in categories:
                categories.append(category)

        return categories

    # ========================================================
    # FILTER BY CATEGORY
    # ========================================================

    def filter_by_category(self, category):
        """
        Lọc Experiment theo category.

        category rỗng hoặc None:
            trả về toàn bộ Experiment.

        So sánh category không phân biệt hoa thường.
        """
        if category is None:
            return self._registry.get_all()

        category = str(category).strip()

        if not category:
            return self._registry.get_all()

        category_lower = category.lower()

        return [
            experiment
            for experiment in self._registry.get_all()
            if str(getattr(experiment, "category", "")).lower()
            == category_lower
        ]
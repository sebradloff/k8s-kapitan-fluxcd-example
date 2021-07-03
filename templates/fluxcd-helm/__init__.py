from kapitan.inputs.kadet import BaseObj, inventory

inv = inventory()

class HelmRelease(BaseObj):
    def new(self):
        self.need("name", "name string needed")
        self.need("namespace", "namespace string needed")
        self.need("chart_name", "chart_name string needed")
        self.need("chart_version", "chart_version string needed")
        self.need("repository_name", "repository_name string needed")
        self.need("helm_values_files", "helm_values_files list needed")
        self.update_root("templates/fluxcd-helm/HelmRelease.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name
        self.root.metadata.namespace = self.kwargs.namespace
        self.root.spec.chart.spec.chart = self.kwargs.chart_name
        self.root.spec.chart.spec.version = self.kwargs.chart_version
        self.root.spec.chart.spec.sourceRef.name = self.kwargs.repository_name
        self.root.spec.chart.spec.sourceRef.namespace = self.kwargs.namespace

        root_values_dict = {}
        for file in self.kwargs.helm_values_files:
            values_obj = BaseObj()
            values_obj.update_root(file)
            root_values_dict.update(values_obj.to_dict())

        self.root.spec["values"] = root_values_dict

class HelmRepository(BaseObj):
    def new(self):
        self.need("repository_name", "repository_name string needed")
        self.need("namespace", "namespace string needed")
        self.need("repository_url", "repository_url string needed")
        self.update_root("templates/fluxcd-helm/HelmRepository.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.repository_name
        self.root.metadata.namespace = self.kwargs.namespace
        self.root.spec.url = self.kwargs.repository_url

def main(input_params):
    name = input_params.get("name")
    namespace = input_params.get("namespace")
    chart_name = input_params.get("chart_name")
    chart_version = input_params.get("chart_version")
    repository_name = input_params.get("repository_name")
    repository_url = input_params.get("repository_url")
    helm_values_files = input_params.get("helm_values_files")

    obj = BaseObj()
    obj.root.HelmRelease = HelmRelease(name=name, namespace=namespace, chart_name=chart_name, chart_version=chart_version, repository_name=repository_name, helm_values_files=helm_values_files)
    obj.root.HelmRepository = HelmRepository(namespace=namespace, repository_name=repository_name, repository_url=repository_url)

    return obj

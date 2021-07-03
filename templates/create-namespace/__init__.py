from kapitan.inputs.kadet import BaseObj, inventory

inv = inventory()

class Namespace(BaseObj):
    def new(self):
        self.need("name", "name string needed")
        self.update_root("templates/create-namespace/namespace.yml")

    def body(self):
        self.root.metadata.name = self.kwargs.name

def main(input_params):
    name = input_params.get("name")

    obj = BaseObj()
    obj.root.namespace = Namespace(name=name)
    return obj

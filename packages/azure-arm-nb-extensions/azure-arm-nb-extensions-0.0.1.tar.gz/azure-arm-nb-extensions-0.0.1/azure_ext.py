# import json
from collections import OrderedDict
from copy import deepcopy
import hashlib
from time import sleep
import json5 as json
import sys
from abc import ABC, abstractmethod
import os
import ipywidgets as widgets
from IPython.core.magic import Magics, line_magic, magics_class
from IPython.display import display, HTML, display_html
from ipywidgets.embed import embed_minimal_html
PARAMETER_FILE_TEMPLATE = {
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": None
}


from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter, FileHandler
APP_BASE_DIR=os.path.join(os.environ["HOME"], ".azure-arm-extensions")
LOG_BASE_DIR=os.path.join(APP_BASE_DIR, "log")
HTML_BASE_DIR=os.path.join(APP_BASE_DIR, "html")
os.makedirs(LOG_BASE_DIR, exist_ok=True)
os.makedirs(HTML_BASE_DIR, exist_ok=True)

verbose = True
logger = getLogger(__file__)
handler = FileHandler(os.path.join(LOG_BASE_DIR, "azure-arm-extensions.log"))
if verbose:
    handler.setLevel(DEBUG)
else:
    handler.setLevel(INFO)
handler.setFormatter(Formatter("%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s"))
logger.addHandler(handler)
logger.setLevel(DEBUG)
logger.propagate = False


class BaseArmParameter(ABC):

    def __init__(self, param_name:str, param_def:dict) -> None:
        self.name = param_name
        self.param_def = param_def

        self.description = param_def.get("metadata", {}).get("description", None)
        self.default_value = param_def.get("defaultValue", None)
        self.allowed_values = param_def.get("allowedValues", [])
        self.max_value = int(param_def.get("maxLength", sys.maxsize))
        self.min_value = int(param_def.get("minLength", 0))
        self.max_length = int(param_def.get("maxLength", sys.maxsize))
        self.min_length = int(param_def.get("minLength", 0))

        self.common_style = {'description_width': '400px'}
        self.common_layout = {"width": "auto"}

        self.description_fmt = "{name} ({description})"
        self.disabled = False

        self.widget = None


        self._create_widget()

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def _create_widget(self):
        pass

    @abstractmethod
    def get_value(self):
        pass


    def update_state(self, state:bool):
        self.widget.disabled = state


class StringParameter(BaseArmParameter):
    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=self.default_value,
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )
        if len(self.allowed_values) > 0:
            kwargs["options"] = self.allowed_values
            w = widgets.Dropdown
        else:
            w = widgets.Text

        self.widget = w(**kwargs)

    def validate(self):
        val = self.widget.value
        name = self.name

        assert bool(val), f"{name} is empty"
        assert len(val) <= self.max_length, f"{name}'s length must be smaller equal than {self.max_length}"
        assert len(val) >= self.min_length, f"{name}'s length must be greater equal than {self.min_length}"

    def get_value(self):
        return self.widget.value

class IntParameter(BaseArmParameter):
    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)


    def _create_widget(self):
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=self.default_value,
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )
        if len(self.allowed_values) > 0:
            kwargs["options"] = self.allowed_values
            w = widgets.Dropdown
        else:
            w = widgets.BoundedIntText

        self.widget = w(**kwargs)

    def validate(self):
        val = self.widget.value
        name = self.name

        assert val is not None, f"{name} is empty"
        assert val <= self.max_value, f"{name}'s value must be smaller equal than {self.max_value}"
        assert val >= self.min_value, f"{name}'s value must be greater equal than {self.min_value}"

    def get_value(self):
        return self.widget.value

class BoolParameter(BaseArmParameter):

    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        kwargs = dict(
            value=self.default_value,
            options=[True, False],
            description=self.description_fmt.format(
                name=self.name, description=self.description
            ),
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )

        self.widget = widgets.Dropdown(**kwargs)

    def validate(self):
        val = self.widget.value
        name = self.name

        assert val == True or val == False, f"{name} must be either True of False"

    def get_value(self):
        return self.widget.value


class ArrayParameter(BaseArmParameter):
    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        if self.default_value is not None:
            self.default_value = ",".join(self.default_value)
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=self.default_value,
            placeholder="seperate values with ','",
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )
        self.widget = widgets.Text(**kwargs)

    def validate(self):
        val = self.widget.value
        name = self.name

        assert val is not None, f"{val} is empty"

    def get_value(self):
        return self.widget.value.split(",")

class SecureStringParameter(BaseArmParameter):
    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=self.default_value,
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )

        self.widget = widgets.Password(**kwargs)

    def validate(self):
        val = self.widget.value
        name = self.name

        assert val is not None, f"{name} is empty"
        assert len(val) <= self.max_length, f"{name}'s length must be smaller equal than {self.max_length}"
        assert len(val) >= self.min_length, f"{name}'s length must be greater equal than {self.min_length}"

    def get_value(self):
        return self.widget.value

class ObjectParameter(BaseArmParameter):

    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        if self.default_value is not None:
            self.default_value = json.dumps(self.default_value)
        else:
            self.default_value = json.dumps({})
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=self.default_value,
            placeholder="set json like string e.g. {'k1': 'v1'}",
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )

        self.widget = widgets.Text(**kwargs)

    def validate(self):

        val = self.widget.value
        name = self.name

        assert val is not None, f"{name} is empty"
        try:
            _ = json.loads(val)
        except Exception as ex:
            raise AssertionError(f"{name} is invalid format for json")

    def get_value(self):
        return json.loads(self.widget.value)

class SecureObjectParameter(BaseArmParameter):

    def __init__(self, param_name: str, param_def: dict) -> None:
        super().__init__(param_name, param_def)

    def _create_widget(self):
        kwargs = dict(
            description=self.description_fmt.format(
                name=self.name, description=self.description,
            ),
            value=json.dumps(self.default_value),
            placeholder="set json like string e.g. {'k1': 'v1'}",
            style=self.common_style,
            layout=self.common_layout,
            disabled=self.disabled,
        )

        self.widget = widgets.Password(**kwargs)

    def validate(self):

        val = self.widget.value
        name = self.name

        assert val is not None, f"{name} is empty"
        try:
            _ = json.loads(val)
        except Exception as ex:
            raise AssertionError(f"{name} is invalid format for json")
    
    def get_value(self):
        return json.loads(self.widget.value)


@magics_class
class AzureExtension(Magics):
    def __init__(self, shell=None, **kwargs):
        self.template_path = None
        self.parameter_path = None

        self.parameter_vals = OrderedDict()
        self.parameter_widgets = {
            "string": StringParameter,
            "int": IntParameter,
            "bool": BoolParameter,
            "array": ArrayParameter,
            "securestring": SecureStringParameter,
            "object": ObjectParameter,
            "secureobject": SecureObjectParameter,
        }

        self.common_style = {'description_width': '250px'}
        self.common_layout = {"width": "auto"}

        self.description_fmt = "{name} ({description})"
        self.disabled = False

        self.output = None
        self.global_output = None

        super().__init__(shell, **kwargs)


    @line_magic
    def set_arm_parameters(self, line):
        """
        args:
            - template_path: path to ARM template json file in which parameter definitions written
            - parameter_path: path to parameter json file for saving actual parameter values for ARM template
                - if not specified, the default path is `{template_path's dir}/{template_path's basename}.parameters.json`
        - load parameters definitions from ARM template file
        - display widgets for setting each parameter values and save button
        - when save button pushed, validate parameter values and save them as parameter file
        """
        if self.global_output is None:
            self.global_output = widgets.Output()
            display(self.global_output)
        
        line = line.split()
        template_path = line[0]
        try:
            parameter_path = line[1]
        except IndexError:
            parameter_path = None

        logger.debug(f"template_path: {template_path}")
        logger.debug(f"parameter_path: {parameter_path}")
        self.template_path = template_path
        self.parameter_path = parameter_path
        if self.parameter_path is None:
            self.parameter_path = self.template_path.rsplit(
                ".", maxsplit=1
            )[0] + ".parameters.json"

        # load ARM template and parameters section in it
        with open(template_path, "r", encoding="utf-8") as fp:
            template = json.load(fp)
        parameter_defs = template["parameters"]
        logger.debug(f"loaded parameter definitions : {parameter_defs}")

        # if parameter file specified and already exists with default values load its values
        parameters = None
        if parameter_path:
            try:
                with open(self.parameter_path, "r", encoding="utf-8") as fp:
                    parameters = json.load(fp)
            except FileNotFoundError as ex:
                pass


        # initialize widgets for each parameters
        for param_name, param_def in parameter_defs.items():
            if parameters is not None:
                try:
                    param_def["defaultValue"] = parameters["parameters"][param_name]["value"]
                except KeyError as ex:
                    pass
            p = self.parameter_widgets[param_def["type"].lower()](param_name, param_def)
            self.parameter_vals[param_name] = p
            # display(p.widget)
        self.display_widgets(self._save_widget())


    def display_widgets(self, button):
        with self.global_output:
            for p in self.parameter_vals.values():
                display(p.widget)
        display(button)

    def create_freeze_views(self, message_widget):
        views = []
        for p in self.parameter_vals.values():
            if isinstance(p.widget, widgets.Password):
                p.widget.value = "*****"
            views.append(p.widget)

        views.append(message_widget)
        views.append(widgets.Button(
            value=self.disabled,
            description='freezed',
            disabled=False,
            style=self.common_style,
            layout=self.common_layout,
            button_style='success',
            icon='check',
        ))

        for v in views:
            v.add_class("EmbedWidgets")
        return views

    def create_freezed_html_path(self) -> str:
        filepath = os.path.join(
            HTML_BASE_DIR, hashlib.sha256(self.parameter_path.encode()).hexdigest() + ".html",
        )
        return filepath


    def _save_widget(self) -> widgets.Widget:
        w = widgets.Button(
            value=self.disabled,
            description='save',
            disabled=False,
            style=self.common_style,
            layout=self.common_layout,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click here if you want to save parameter values',
            icon='check' # (FontAwesome names without the `fa-` prefix),
        )

        def on_button_click(b):
            if self.output is None:
                self.output = widgets.Output()
                with self.global_output:
                    display(self.output)
            try:
                for v in self.parameter_vals.values():
                    v.validate()
            except AssertionError as ex:
                with self.global_output:
                    with self.output:
                        self.output.clear_output()
                        display(widgets.HTML(f"<b style='color:red'>parameter validation error! : {ex}</b>"))
                return

            # if all validation passes, freeze parameter values and save in them in files
            for v in self.parameter_vals.values():
                v.update_state(True)
            self._save_parameters_as_file()

            success_widget = widgets.HTML(value=f"<b style='color:green'>successfully save parameters in {self.parameter_path}!</b>")
            with self.global_output:
                with self.output:
                    self.output.clear_output()
                    display(success_widget)
                    sleep(1)
                    # with self.global_output:

            self.global_output.clear_output()
            w.close()
            html_path = self.create_freezed_html_path()
            embed_minimal_html(html_path, views=self.create_freeze_views(success_widget), title='freezed parameters')
            display_html(HTML("<style>.EmbedWidgets {background-color:white}</style>"))
            display_html(HTML(filename=html_path))

        w.on_click(on_button_click)
        return w

    def _save_parameters_as_file(self):


        parameters_file_body = PARAMETER_FILE_TEMPLATE
        parameters_file_body["parameters"] = dict()
        for k, v in self.parameter_vals.items():
            parameters_file_body["parameters"][k] = {"value" : v.get_value()}
        
        with open(self.parameter_path, "w", encoding="utf-8") as fp:
            json.dump(parameters_file_body, fp, indent=4, quote_keys=True, trailing_commas=False)




def load_ipython_extension(ipython):
    ipython.register_magics(AzureExtension)


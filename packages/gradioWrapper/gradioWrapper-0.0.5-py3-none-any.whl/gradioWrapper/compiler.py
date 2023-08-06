import gradio as gr
import socket
import random

class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


    
def register(inputs, outputs):
    def register_gradio(func):
        def wrap(self, *args, **kwargs):            
            try:
                self.registered_gradio_functons
            except AttributeError:
                print("✨Initializing Class Functions...✨\n")
                self.registered_gradio_functons = dict()

            fn_name = func.__name__ 
            if fn_name in self.registered_gradio_functons: 
                result = func(self, *args, **kwargs)
                return result
            else:
                self.registered_gradio_functons[fn_name] = dict(inputs=inputs, outputs=outputs)
                return None
        return wrap
    return register_gradio
    
 
      

def gradio_compile(cls):
    class GradioWrapper:
        port_range = (7860, 7880)
        active_port_map = {}

        def __init__(self) -> None:
            self.cls = cls()

        def get_funcs(self):
            return [func for func in dir(self.cls) if not func.startswith("__") and type(getattr(self.cls, func, None)) == type(self.get_funcs) ]

        def compile(self, **kwargs):
            print("Just putting on the finishing touches... 🔧🧰")
            for func in self.get_funcs():
                this = getattr(self.cls, func, None)
                if this.__name__ == "wrap":
                    this()

            demos = []
            names = []
            for func, param in self.get_registered_gradio_functons().items():                
                names.append(func)
                demos.append(gr.Interface(fn=getattr(self.cls, func, None),
                                            inputs=param['inputs'],
                                            outputs=param['outputs'],
                                            live=kwargs['live'] if "live" in kwargs else False,
                                            allow_flagging=kwargs['flagging'] if "flagging" in kwargs else 'never',
                                            theme='default'))
                print(f"{func}....{bcolor.BOLD}{bcolor.OKGREEN} done {bcolor.ENDC}")

            print("\nHappy Visualizing... 🚀")
            return gr.TabbedInterface(demos, names)
            
        def get_registered_gradio_functons(self):
            try:
                self.cls.registered_gradio_functons
            except AttributeError:
                return None
            return self.cls.registered_gradio_functons
        

        def run(self, **kwargs):
            port= kwargs["port"] if "port" in kwargs else self.determinePort() 

            self.compile(live=kwargs[ 'live' ] if "live" in kwargs else False,
                                    allow_flagging=kwargs[ 'flagging' ] if "flagging" in kwargs else 'never',).launch(server_port=port) 

        def portConnection(self ,port : int):
            s = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
                    
            result = s.connect_ex(("localhost", port))
            if result == 0: return True
            return False

        def active_port(self, port:int):
            return self.active_port_map.get(port, False)
        
        def determinePort(self, max_trial_count=10):
            trial_count = 0 
            while trial_count <= max_trial_count:
                port=random.randint(*self.port_range)
                if not self.portConnection(port):
                    return port
                trial_count += 1
            raise Exception('Exceeded Max Trial count without finding port')
        
    return GradioWrapper
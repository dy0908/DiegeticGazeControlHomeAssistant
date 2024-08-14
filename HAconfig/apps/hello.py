import hassapi as hass
import datetime
#
# Hello World App
#
# Args:
#

"""
class HelloWorld(hass.Hass):
        
    def initialize(self):
        
        host='127.0.0.1'
        port=65111
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.clients = []

        self.log(f"Server listening")
        #self.run_script("script.switch1")
        while True:
            client_socket, address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_handler.start()
        # Clean up the connection
        client_socket.close()

        self.listen_state(self.callback, "sensor.file", constrain_state=lambda  x: x>0)
        self.log(f"Server listening")
        self.log(self.sensor.file.attribute)
        # self.turn_on("script.test2")
                
    
"""
import adbase as ad

class HelloWorld(ad.ADBase):

    def initialize(self):

        # Grab an object for the HASS API
        self.hass = self.get_plugin_api("HASS")
        # Hass API Call
        """
        hass.turn_on("light.office")
        # Listen for state changes for this plugin only
        hass.listen_state(my_callback, "light.kitchen")
    """
    # Make a scheduler call using the ADBase class
        self.adapi = self.get_ad_api()
        self.file = self.adapi.get_entity("switch.wemo_switch_1")
        state = self.adapi.get_state("sensor.file")
        self.hass.log(state)
        self.adapi.handle=self.adapi.listen_state(self.callback_on, "sensor.file",new = "1", old="0")
        self.adapi.handle=self.adapi.listen_state(self.callback_off, "sensor.file",new = "0", old="1")
        self.adapi.handle=self.adapi.listen_state(self.switch_on, "switch.wemo_switch_1",new = "on", old="off")
        self.adapi.handle=self.adapi.listen_state(self.switch_off, "switch.wemo_switch_1",new = "off", old="on")
    def callback_on(self, entity, attribute, old, new, cb_args):
        self.hass.log(f"Run Callback on")
        self.hass.turn_on("switch.wemo_switch_1")
    
    def callback_off(self, entity, attribute, old, new, cb_args):
        self.hass.log(f"Run Callback off")
        self.hass.turn_off("switch.wemo_switch_1")

    def switch_on(self, entity, attribute, old, new, cb_args):
        self.hass.log(f"Switch on")
    
    def switch_off(self, entity, attribute, old, new, cb_args):
        self.hass.log(f"Switch off")
        """
        def handle_client(self, client_socket, address):
        print(f"Connection from {address} has been established.")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received from {address}: {message}")
                    self.broadcast(message, client_socket)
                else:
                    break
            except:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        print(f"Connection from {address} has been closed.")
    """
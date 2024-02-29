"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .. import ivi
from .. import dcpwr
from .. import scpi
import time

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

class hmp2020 (scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger,
                scpi.dcpwr.Measurement,
                scpi.common.Memory):
    "R&S HMP2020 IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'HMP2020')
        
        # don't do standard SCPI init routine
        self._do_scpi_init = False
        
        super(hmp2020, self).__init__(*args, **kwargs)
        
        self._output_count = 2
        
        self._output_spec = [
            {
                'range': {
                    'P30V': (30.0, 5.0)
                },
                'ovp_max': 30.0,
                'voltage_max': 30.0,
                'current_max': 5.0
            },
          
        ]
        
        self._memory_size = 3
        self._memory_offset = 1
        
        self._output_trigger_delay = list()
        
        self._couple_tracking_enabled = False
        self._couple_tracking_type = 'floating'
        self._couple_trigger = False
        
        self._identity_description = "R&S HMP2020 series DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Rohde & Schwarz"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['hmp2020']
        

        
        self._init_outputs()
    
    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(hmp2020, self)._initialize(resource, id_query, reset, **keywargs)
        
        # configure interface
        if self._interface is not None:
            if 'dsrdtr' in self._interface.__dict__:
                self._interface.dsrdtr = True
                self._interface.update_settings()
        
        # interface clear
        #if not self._driver_operation_simulate:
            #self._clear()
        
        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)
        
        # reset
        if reset:
            self.utility_reset()
        
    def _get_output_current_limit(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_current_limit[index] = float(self._ask("CURR?"))
            self._set_cache_valid(index=index)
        return self._output_current_limit[index]
        
        
    def _set_output_current_limit(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0 or value > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("CURR %.2f" % value)
        self._output_current_limit[index] = value
        self._set_cache_valid(index=index)
    

    def _get_output_voltage_level(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_voltage_level[index] = float(self._ask("VOLT?"))
            self._set_cache_valid(index=index)
        return self._output_voltage_level[index]
    
    
    
    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            time.sleep(0.1)
            if self._get_bool_str(value) == "1" :
                self._write("OUTP:SEL %d", index+1)
                self._write("OUTP 1")
            else:
                self._write("OUTP:SEL %d", index+1)
                self._write("OUTP 0")
                
        self._output_enabled[index] = value
        for k in range(self._output_count):
            self._set_cache_valid(valid=False,index=k)
        self._set_cache_valid(index=index)
        
        
    def _set_output_voltage_level(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if self._output_spec[index]['voltage_max'] >= 0:
            if value < 0 or value > self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        else:
            if value > 0 or value < self._output_spec[index]['voltage_max']:
                raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._write("VOLT %.2f" % value)
        self._output_voltage_level[index] = value
        self._set_cache_valid(index=index)


    def _get_output_ovp_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            self._output_ovp_enabled[index] = self._ask("VOLTage:PROTection:TRIPped?") == self._get_bool_str(True)
            self._set_cache_valid(index=index)
        return self._output_ovp_enabled[index]
    
    def _set_output_ovp_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            if self._output_count > 1:
                self._write("instrument:nselect %d" % (index+1))
            if self._get_bool_str(value) == "1":
                self._write("VOLTage:PROTection:MODE PROT")
            else:
                self._write("VOLTage:PROTection:MODE MEAS")
                 
        self._output_ovp_enabled[index] = value
        self._set_cache_valid(index=index)
    
 
    
    def _set_output_ovp_limit(self, index, value):
        pass
    
    

    
    


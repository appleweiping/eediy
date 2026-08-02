# Generic interface timing budget, not a board pinout or implementation result.
create_clock -name clk -period 10.000 [get_ports clk]
set_clock_uncertainty 0.200 [get_clocks clk]

set_input_delay -clock clk -max 1.500 \
    [get_ports {rst_n in_valid in_data[*] out_ready}]
set_input_delay -clock clk -min 0.200 \
    [get_ports {rst_n in_valid in_data[*] out_ready}]

set_output_delay -clock clk -max 1.500 \
    [get_ports {in_ready out_valid out_data[*] occupancy[*]}]
set_output_delay -clock clk -min 0.200 \
    [get_ports {in_ready out_valid out_data[*] occupancy[*]}]

`timescale 1ns/1ps
`default_nettype none

module sync_fifo #(
    parameter int unsigned DATA_WIDTH = 8,
    parameter int unsigned DEPTH = 4,
    parameter bit FAULT_READ_POINTER = 1'b0,
    localparam int unsigned COUNT_WIDTH = $clog2(DEPTH + 1)
) (
    input  logic                   clk,
    input  logic                   rst_n,

    input  logic                   in_valid,
    output logic                   in_ready,
    input  logic [DATA_WIDTH-1:0]  in_data,

    output logic                   out_valid,
    input  logic                   out_ready,
    output logic [DATA_WIDTH-1:0]  out_data,

    output logic [COUNT_WIDTH-1:0] occupancy
);
    localparam int unsigned PTR_WIDTH = $clog2(DEPTH);

    logic [DATA_WIDTH-1:0] memory [0:DEPTH-1];
    logic [PTR_WIDTH-1:0] write_pointer;
    logic [PTR_WIDTH-1:0] read_pointer;
    logic [COUNT_WIDTH-1:0] count;
    logic push;
    logic pop;

`ifndef SYNTHESIS
    initial begin : validate_parameters
        if (DATA_WIDTH < 1) begin
            $fatal(1, "DATA_WIDTH must be at least one");
        end
        if ((DEPTH < 2) || ((DEPTH & (DEPTH - 1)) != 0)) begin
            $fatal(1, "DEPTH must be a power of two and at least two");
        end
    end
`endif

    assign out_valid = (count != 0);
    assign out_data = memory[read_pointer];
    assign occupancy = count;

    // A full FIFO may accept a write when the same edge also accepts a read.
    // There is no fall-through path: an empty FIFO exposes new data one cycle
    // after the write is accepted.
    assign in_ready =
        (count < COUNT_WIDTH'(DEPTH)) || (out_valid && out_ready);
    assign push = in_valid && in_ready;
    assign pop = out_valid && out_ready;

    always_ff @(posedge clk) begin
        if (!rst_n) begin
            write_pointer <= '0;
            read_pointer <= '0;
            count <= '0;
        end else begin
            case ({push, pop})
                2'b10: count <= count + 1'b1;
                2'b01: count <= count - 1'b1;
                default: count <= count;
            endcase

            if (push) begin
                memory[write_pointer] <= in_data;
                write_pointer <= write_pointer + 1'b1;
            end

            if (pop) begin
                if (FAULT_READ_POINTER) begin
                    // Deliberate negative control. The shared testbench and
                    // formal reference model must both reject this revision.
                    read_pointer <= read_pointer;
                end else begin
                    read_pointer <= read_pointer + 1'b1;
                end
            end
        end
    end
endmodule

`default_nettype wire

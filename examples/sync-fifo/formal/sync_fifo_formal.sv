`default_nettype none

module sync_fifo_formal (
    input logic clk
);
    // Formal checks one small parameter instance exhaustively through the
    // declared bound. Simulation separately exercises DATA_WIDTH=8, DEPTH=4,
    // and synthesis elaborates DATA_WIDTH=8, DEPTH=16.
    localparam int unsigned DATA_WIDTH = 2;
    localparam int unsigned DEPTH = 2;
    localparam int unsigned COUNT_WIDTH = $clog2(DEPTH + 1);

`ifdef FAULT_READ_POINTER
    localparam bit INJECT_READ_POINTER_FAULT = 1'b1;
`else
    localparam bit INJECT_READ_POINTER_FAULT = 1'b0;
`endif

    logic rst_n;
    (* anyseq *) logic in_valid;
    logic in_ready;
    (* anyseq *) logic [DATA_WIDTH-1:0] in_data;
    logic out_valid;
    (* anyseq *) logic out_ready;
    logic [DATA_WIDTH-1:0] out_data;
    logic [COUNT_WIDTH-1:0] occupancy;

    logic [DATA_WIDTH-1:0] reference_head_data;
    logic [DATA_WIDTH-1:0] reference_tail_data;
    logic [COUNT_WIDTH-1:0] reference_count;
    logic past_valid;
    logic reference_push;
    logic reference_pop;

    sync_fifo #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .FAULT_READ_POINTER(INJECT_READ_POINTER_FAULT)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .in_valid(in_valid),
        .in_ready(in_ready),
        .in_data(in_data),
        .out_valid(out_valid),
        .out_ready(out_ready),
        .out_data(out_data),
        .occupancy(occupancy)
    );

    assign reference_push = in_valid && in_ready;
    assign reference_pop = out_valid && out_ready;

    initial begin
        rst_n = 1'b0;
        past_valid = 1'b0;
        reference_count = '0;
    end

    // The only environment restriction is a two-edge synchronous reset.
    // After that, valid, ready, and data remain completely unconstrained.
    always_ff @(posedge clk) begin
        // Keep reset asserted through two sampled edges. This prevents the
        // unconstrained power-up state used by formal engines from being
        // mistaken for a post-reset DUT state.
        rst_n <= past_valid;
        past_valid <= 1'b1;

        if (!rst_n) begin
            reference_count <= '0;
        end else begin
            case ({reference_push, reference_pop})
                2'b10: begin
                    reference_count <= reference_count + 1'b1;
                    if (reference_count == 0) begin
                        reference_head_data <= in_data;
                    end else begin
                        reference_tail_data <= in_data;
                    end
                end
                2'b01: begin
                    reference_count <= reference_count - 1'b1;
                    reference_head_data <= reference_tail_data;
                end
                2'b11: begin
                    reference_count <= reference_count;
                    if (reference_count == 1) begin
                        reference_head_data <= in_data;
                    end else begin
                        reference_head_data <= reference_tail_data;
                        reference_tail_data <= in_data;
                    end
                end
                default: reference_count <= reference_count;
            endcase
        end
    end

    always_ff @(posedge clk) begin
        if (past_valid && !rst_n) begin
            assert (occupancy == 0);
            assert (!out_valid);
        end

        if (past_valid && rst_n) begin
            assert (occupancy == reference_count);
            assert (out_valid == (reference_count != 0));
            assert (
                in_ready
                == (
                    (reference_count < COUNT_WIDTH'(DEPTH))
                    || ((reference_count != 0) && out_ready)
                )
            );
            assert (occupancy <= COUNT_WIDTH'(DEPTH));

            if (reference_count != 0) begin
                assert (out_data == reference_head_data);
            end

            if (!$past(rst_n)) begin
                assert (occupancy == 0);
                assert (!out_valid);
            end else begin
                case ({$past(reference_push), $past(reference_pop)})
                    2'b10: assert (
                        occupancy == ($past(occupancy) + 1'b1)
                    );
                    2'b01: assert (
                        occupancy == ($past(occupancy) - 1'b1)
                    );
                    default: assert (occupancy == $past(occupancy));
                endcase
            end
        end

        if (rst_n) begin
            cover (occupancy == COUNT_WIDTH'(DEPTH));
            cover (out_valid && out_ready && in_valid && in_ready);
            cover (!out_valid && out_ready);
        end
    end
endmodule

`default_nettype wire

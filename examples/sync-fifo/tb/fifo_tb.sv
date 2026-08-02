`timescale 1ns/1ps
`default_nettype none

module fifo_tb;
    localparam int unsigned DATA_WIDTH = 8;
    localparam int unsigned DEPTH = 4;
    localparam int unsigned COUNT_WIDTH = $clog2(DEPTH + 1);

`ifdef FAULT_READ_POINTER
    localparam bit INJECT_READ_POINTER_FAULT = 1'b1;
`else
    localparam bit INJECT_READ_POINTER_FAULT = 1'b0;
`endif

    logic clk;
    logic rst_n;
    logic in_valid;
    logic in_ready;
    logic [DATA_WIDTH-1:0] in_data;
    logic out_valid;
    logic out_ready;
    logic [DATA_WIDTH-1:0] out_data;
    logic [COUNT_WIDTH-1:0] occupancy;

    logic [DATA_WIDTH-1:0] reference_queue [0:DEPTH-1];
    integer reference_head;
    integer reference_tail;
    integer reference_count;
    integer cycle;

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

    always #5 clk <= ~clk;

    task automatic fail_check(input string check_name);
        begin
            $display(
                "SYNC_FIFO_MISMATCH check=%s cycle=%0d count=%0d in_valid=%0b in_ready=%0b out_valid=%0b out_ready=%0b out_data=0x%0h",
                check_name,
                cycle,
                reference_count,
                in_valid,
                in_ready,
                out_valid,
                out_ready,
                out_data
            );
            $fatal(1, "self-checking FIFO regression failed");
        end
    endtask

    task automatic check_visible_state(input string checkpoint);
        logic expected_out_valid;
        logic expected_in_ready;
        begin
            expected_out_valid = (reference_count != 0);
            expected_in_ready =
                (reference_count < DEPTH)
                || (expected_out_valid && out_ready);

            if (out_valid !== expected_out_valid) begin
                $display(
                    "expected out_valid=%0b actual=%0b at %s",
                    expected_out_valid,
                    out_valid,
                    checkpoint
                );
                fail_check("out_valid");
            end
            if (in_ready !== expected_in_ready) begin
                $display(
                    "expected in_ready=%0b actual=%0b at %s",
                    expected_in_ready,
                    in_ready,
                    checkpoint
                );
                fail_check("in_ready");
            end
            if (occupancy !== COUNT_WIDTH'(reference_count)) begin
                $display(
                    "expected occupancy=%0d actual=%0d at %s",
                    reference_count,
                    occupancy,
                    checkpoint
                );
                fail_check("occupancy");
            end
            if (
                expected_out_valid
                && (out_data !== reference_queue[reference_head])
            ) begin
                $display(
                    "expected out_data=0x%0h actual=0x%0h at %s",
                    reference_queue[reference_head],
                    out_data,
                    checkpoint
                );
                fail_check("read_order");
            end
        end
    endtask

    task automatic reset_model;
        begin
            reference_head = 0;
            reference_tail = 0;
            reference_count = 0;
        end
    endtask

    task automatic apply_reset;
        integer reset_edge;
        begin
            @(negedge clk);
            rst_n = 1'b0;
            in_valid = 1'b0;
            in_data = '0;
            out_ready = 1'b0;
            for (reset_edge = 0; reset_edge < 2; reset_edge = reset_edge + 1) begin
                @(posedge clk);
                cycle = cycle + 1;
                reset_model();
                #1;
                check_visible_state("reset");
            end
            @(negedge clk);
            rst_n = 1'b1;
            #1;
            check_visible_state("reset_release");
        end
    endtask

    task automatic step(
        input logic request_write,
        input logic [DATA_WIDTH-1:0] write_data,
        input logic request_read
    );
        logic accepted_write;
        logic accepted_read;
        begin
            @(negedge clk);
            in_valid = request_write;
            in_data = write_data;
            out_ready = request_read;
            #1;
            check_visible_state("before_edge");
            accepted_write = in_valid && in_ready;
            accepted_read = out_valid && out_ready;

            @(posedge clk);
            cycle = cycle + 1;
            if (accepted_read) begin
                reference_head = (reference_head + 1) % DEPTH;
                reference_count = reference_count - 1;
            end
            if (accepted_write) begin
                reference_queue[reference_tail] = write_data;
                reference_tail = (reference_tail + 1) % DEPTH;
                reference_count = reference_count + 1;
            end
            #1;
            check_visible_state("after_edge");
        end
    endtask

    initial begin
        clk = 1'b0;
        rst_n = 1'b0;
        in_valid = 1'b0;
        in_data = '0;
        out_ready = 1'b0;
        cycle = 0;
        reset_model();

        // Reset and empty behavior, including a read request while empty.
        apply_reset();
        step(1'b0, 8'h00, 1'b1);

        // One item remains stable under backpressure, then drains.
        step(1'b1, 8'h11, 1'b0);
        step(1'b0, 8'h00, 1'b0);
        step(1'b0, 8'h00, 1'b1);

        // Fill to the boundary. A blocked write must not overwrite data.
        step(1'b1, 8'h21, 1'b0);
        step(1'b1, 8'h22, 1'b0);
        step(1'b1, 8'h23, 1'b0);
        step(1'b1, 8'h24, 1'b0);
        step(1'b1, 8'hee, 1'b0);

        // Read and write together while full and on the following cycle.
        // These transfers also force both pointers to wrap.
        step(1'b1, 8'h31, 1'b1);
        step(1'b1, 8'h32, 1'b1);

        // Drain in order through empty.
        step(1'b0, 8'h00, 1'b1);
        step(1'b0, 8'h00, 1'b1);
        step(1'b0, 8'h00, 1'b1);
        step(1'b0, 8'h00, 1'b1);

        // Insert reset with queued data and prove old data is no longer valid.
        step(1'b1, 8'ha1, 1'b0);
        step(1'b1, 8'ha2, 1'b0);
        apply_reset();

        // A final non-full simultaneous transfer checks the steady-state path.
        step(1'b1, 8'hb1, 1'b0);
        step(1'b1, 8'hb2, 1'b1);
        step(1'b0, 8'h00, 1'b1);

`ifdef FAULT_READ_POINTER
        $display(
            "SYNC_FIFO_NEGATIVE_CONTROL_UNEXPECTED_PASS cycles=%0d",
            cycle
        );
        $fatal(1, "read-pointer fault escaped the regression");
`else
        $display("SYNC_FIFO_SIM_PASS revision=baseline cycles=%0d", cycle);
        $finish;
`endif
    end

    initial begin : timeout_guard
        #5000;
        $display("SYNC_FIFO_MISMATCH check=timeout cycle=%0d", cycle);
        $fatal(1, "simulation timeout");
    end
endmodule

`default_nettype wire

if(NOT DEFINED PROBE)
  message(FATAL_ERROR "PROBE executable was not provided")
endif()

execute_process(
  COMMAND "${PROBE}"
  RESULT_VARIABLE probe_result
  OUTPUT_VARIABLE probe_stdout
  ERROR_VARIABLE probe_stderr
)

if(NOT probe_result EQUAL 7)
  message(FATAL_ERROR
    "fault probe must exit 7, got ${probe_result}\n"
    "stdout:\n${probe_stdout}\n"
    "stderr:\n${probe_stderr}"
  )
endif()

string(FIND
  "${probe_stdout}"
  "deliberate-fault: accepted sample 999 while full"
  expected_message_at
)
if(expected_message_at EQUAL -1)
  message(FATAL_ERROR "fault probe did not report the observed contract breach")
endif()

message(STATUS "deliberate fault was detected and rejected as expected")

cmake_minimum_required(VERSION 3.25)

project(eediy_ring_buffer LANGUAGES C)

include(CTest)

option(ENABLE_SANITIZERS "Enable AddressSanitizer and UndefinedBehaviorSanitizer" OFF)

function(enable_strict_warnings target_name)
  if(MSVC)
    target_compile_options(${target_name} PRIVATE /W4 /WX)
  else()
    target_compile_options(
      ${target_name}
      PRIVATE
        -Wall
        -Wextra
        -Wpedantic
        -Wconversion
        -Wshadow
        -Werror
    )
  endif()
endfunction()

function(enable_sanitizer_compile target_name)
  if(ENABLE_SANITIZERS)
    if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
      target_compile_options(
        ${target_name}
        PRIVATE
          -fsanitize=address,undefined
          -fno-omit-frame-pointer
      )
    else()
      message(FATAL_ERROR
        "ENABLE_SANITIZERS requires a GCC- or Clang-compatible C compiler"
      )
    endif()
  endif()
endfunction()

function(enable_sanitizer_link target_name)
  if(ENABLE_SANITIZERS)
    target_link_options(
      ${target_name}
      PRIVATE
        -fsanitize=address,undefined
        -fno-omit-frame-pointer
    )
  endif()
endfunction()

add_library(
  ring_buffer
  src/ring_buffer.c
  src/adc_dma_adapter.c
)
target_include_directories(ring_buffer PUBLIC include)
target_compile_features(ring_buffer PUBLIC c_std_11)
set_target_properties(ring_buffer PROPERTIES C_EXTENSIONS OFF)
enable_strict_warnings(ring_buffer)
enable_sanitizer_compile(ring_buffer)

add_executable(ring_buffer_tests tests/test_ring_buffer.c)
target_link_libraries(ring_buffer_tests PRIVATE ring_buffer)
enable_strict_warnings(ring_buffer_tests)
enable_sanitizer_compile(ring_buffer_tests)
enable_sanitizer_link(ring_buffer_tests)

add_library(ring_buffer_faulty STATIC src/ring_buffer.c)
target_include_directories(ring_buffer_faulty PUBLIC include)
target_compile_features(ring_buffer_faulty PUBLIC c_std_11)
target_compile_definitions(
  ring_buffer_faulty
  PRIVATE RING_BUFFER_DELIBERATE_FULL_FAULT=1
)
set_target_properties(ring_buffer_faulty PROPERTIES C_EXTENSIONS OFF)
enable_strict_warnings(ring_buffer_faulty)
enable_sanitizer_compile(ring_buffer_faulty)

add_executable(ring_buffer_fault_probe tests/fault_probe.c)
target_link_libraries(ring_buffer_fault_probe PRIVATE ring_buffer_faulty)
enable_strict_warnings(ring_buffer_fault_probe)
enable_sanitizer_compile(ring_buffer_fault_probe)
enable_sanitizer_link(ring_buffer_fault_probe)

if(BUILD_TESTING)
  add_test(NAME ring_buffer_contract COMMAND ring_buffer_tests)
  add_test(
    NAME ring_buffer_deliberate_fault
    COMMAND
      "${CMAKE_COMMAND}"
      "-DPROBE=$<TARGET_FILE:ring_buffer_fault_probe>"
      -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/ExpectFailure.cmake"
  )
endif()

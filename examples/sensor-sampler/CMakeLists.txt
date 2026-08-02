cmake_minimum_required(VERSION 3.25)

project(eediy_sensor_sampler LANGUAGES C)

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

add_library(sensor_sampler src/sampler.c)
target_include_directories(sensor_sampler PUBLIC include)
target_compile_features(sensor_sampler PUBLIC c_std_11)
set_target_properties(sensor_sampler PROPERTIES C_EXTENSIONS OFF)
enable_strict_warnings(sensor_sampler)
enable_sanitizer_compile(sensor_sampler)

add_executable(sensor_sampler_tests tests/test_sensor_sampler.c)
target_link_libraries(sensor_sampler_tests PRIVATE sensor_sampler)
enable_strict_warnings(sensor_sampler_tests)
enable_sanitizer_compile(sensor_sampler_tests)
enable_sanitizer_link(sensor_sampler_tests)

if(BUILD_TESTING)
  add_test(NAME sensor_sampler_fault_matrix COMMAND sensor_sampler_tests)
endif()

project(EXO)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_C_FLAGS "-mthumb -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16")

include_directories(
FreeRTOSv9.0.0/FreeRTOS/Source/include
FreeRTOSv9.0.0/FreeRTOS/Source/portable/GCC/ARM_CM4_MPU
)


add_library(freertos STATIC
FreeRTOSv9.0.0/FreeRTOS/Source/portable/GCC/ARM_CM4_MPU/port.c
FreeRTOSv9.0.0/FreeRTOS/Source/portable/MemMang/heap_3.c
FreeRTOSv9.0.0/FreeRTOS/Source/list.c
FreeRTOSv9.0.0/FreeRTOS/Source/queue.c
FreeRTOSv9.0.0/FreeRTOS/Source/tasks.c
)

add_executable(tests
main.c
)

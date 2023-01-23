cmake_minimum_required(VERSION 3.2 FATAL_ERROR)
project(omega_cpp VERSION 1.0 LANGUAGES C CXX)

# Must use GNUInstallDirs to install libraries into correct
# locations on all platforms.
include(GNUInstallDirs)

# Define C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Targets that we develop here
find_package(h5cpp REQUIRED)
message(STATUS "h5cpp found: ${h5cpp_FOUND}")

# Targets that we develop here
add_library(omega_cpp_lib
        src/ReferenceRecording.cpp
        src/MetaData.cpp
        src/road/Boundary.cpp
        src/road/Border.cpp
        src/road/RoadObject.cpp
        src/road/StructuralObject.cpp
        src/road/FlatMarking.cpp
        src/road/Lane.cpp
        src/road/Surface.cpp
        src/road/Sign.cpp
        src/road/LateralMarking.cpp
        src/road/Road.cpp
        src/dynamics/BoundingBox.cpp
        src/dynamics/MiscObject.cpp
        src/dynamics/Trajectory.cpp
        src/dynamics/RoadUser.cpp
        src/dynamics/VehicleLights.cpp
        src/weather/AirPressure.cpp
        src/weather/Cloudiness.cpp
        src/weather/GustOfWind.cpp
        src/weather/Humidity.cpp
        src/weather/Precipitation.cpp
        src/weather/RoadCondition.cpp
        src/weather/Solar.cpp
        src/weather/Temperature.cpp
        src/weather/Visibility.cpp
        src/weather/Weather.cpp
        src/weather/Wind.cpp)


# Define headers for this library. PUBLIC headers are used for
# compiling the library, and will be added to consumers' build
# paths.
target_include_directories(omega_cpp_lib PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
        PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../omega_format/enums>)

# If we have compiler requirements for this library, list them
# here
target_compile_features(omega_cpp_lib
        PUBLIC cxx_auto_type
        PRIVATE cxx_variadic_templates)

# Depend on a library that we defined in the top-level file
target_link_libraries(omega_cpp_lib
        h5cpp)

# 'make install' to the correct locations (provided by GNUInstallDirs).
install(TARGETS omega_cpp_lib EXPORT omega_cpp_lib-config
        ARCHIVE  DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY  DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME  DESTINATION ${CMAKE_INSTALL_BINDIR})  # This is for Windows
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# This makes the project importable from the install directory
# Put config file in per-project dir (name MUST match), can also
# just go into 'cmake'.
install(EXPORT omega_cpp_lib-config DESTINATION share/OmegaCppLib/cmake)

# This makes the project importable from the build directory
export(TARGETS omega_cpp_lib FILE omega_cpp_lib-config.cmake)

# example usage
# add_executable(omega_cpp_example example.cpp)
# target_link_libraries(omega_cpp_example
#        omega_cpp_lib
#        h5cpp)

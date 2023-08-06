#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "MODENA::twoTanksFullProblem" for configuration "Debug"
set_property(TARGET MODENA::twoTanksFullProblem APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(MODENA::twoTanksFullProblem PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/twoTanksFullProblem"
  )

list(APPEND _IMPORT_CHECK_TARGETS MODENA::twoTanksFullProblem )
list(APPEND _IMPORT_CHECK_FILES_FOR_MODENA::twoTanksFullProblem "${_IMPORT_PREFIX}/bin/twoTanksFullProblem" )

# Import target "MODENA::modena" for configuration "Debug"
set_property(TARGET MODENA::modena APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(MODENA::modena PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/modena/libmodena.so.1.0"
  IMPORTED_SONAME_DEBUG "libmodena.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS MODENA::modena )
list(APPEND _IMPORT_CHECK_FILES_FOR_MODENA::modena "${_IMPORT_PREFIX}/lib/modena/libmodena.so.1.0" )

# Import target "MODENA::fmodena" for configuration "Debug"
set_property(TARGET MODENA::fmodena APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(MODENA::fmodena PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/modena/libfmodena.so"
  IMPORTED_SONAME_DEBUG "libfmodena.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS MODENA::fmodena )
list(APPEND _IMPORT_CHECK_FILES_FOR_MODENA::fmodena "${_IMPORT_PREFIX}/lib/modena/libfmodena.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "mindquantum::mq_base" for configuration "Release"
set_property(TARGET mindquantum::mq_base APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mindquantum::mq_base PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/mindquantum/libmq_base.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS mindquantum::mq_base )
list(APPEND _IMPORT_CHECK_FILES_FOR_mindquantum::mq_base "${_IMPORT_PREFIX}/lib64/mindquantum/libmq_base.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

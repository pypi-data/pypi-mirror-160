#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "OpenEXR::IlmImf" for configuration "Release"
set_property(TARGET OpenEXR::IlmImf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenEXR::IlmImf PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/libIlmImf.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libIlmImf.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenEXR::IlmImf )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenEXR::IlmImf "${_IMPORT_PREFIX}/mitsuba/libIlmImf.dylib" )

# Import target "OpenEXR::IlmImfUtil" for configuration "Release"
set_property(TARGET OpenEXR::IlmImfUtil APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenEXR::IlmImfUtil PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/libIlmImfUtil.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libIlmImfUtil.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenEXR::IlmImfUtil )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenEXR::IlmImfUtil "${_IMPORT_PREFIX}/mitsuba/libIlmImfUtil.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

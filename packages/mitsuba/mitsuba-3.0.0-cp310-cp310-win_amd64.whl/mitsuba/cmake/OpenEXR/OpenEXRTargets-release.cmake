#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "OpenEXR::IlmImf" for configuration "Release"
set_property(TARGET OpenEXR::IlmImf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenEXR::IlmImf PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmImf.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "OpenEXR::zlib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmImf.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenEXR::IlmImf )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenEXR::IlmImf "${_IMPORT_PREFIX}/mitsuba/IlmImf.lib" "${_IMPORT_PREFIX}/mitsuba/IlmImf.dll" )

# Import target "OpenEXR::zlib" for configuration "Release"
set_property(TARGET OpenEXR::zlib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenEXR::zlib PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/zlib.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/zlib1.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenEXR::zlib )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenEXR::zlib "${_IMPORT_PREFIX}/mitsuba/zlib.lib" "${_IMPORT_PREFIX}/mitsuba/zlib1.dll" )

# Import target "OpenEXR::IlmImfUtil" for configuration "Release"
set_property(TARGET OpenEXR::IlmImfUtil APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(OpenEXR::IlmImfUtil PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmImfUtil.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmImfUtil.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS OpenEXR::IlmImfUtil )
list(APPEND _IMPORT_CHECK_FILES_FOR_OpenEXR::IlmImfUtil "${_IMPORT_PREFIX}/mitsuba/IlmImfUtil.lib" "${_IMPORT_PREFIX}/mitsuba/IlmImfUtil.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

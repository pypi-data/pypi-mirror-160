#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "IlmBase::Half" for configuration "Release"
set_property(TARGET IlmBase::Half APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IlmBase::Half PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/Half.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/Half.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS IlmBase::Half )
list(APPEND _IMPORT_CHECK_FILES_FOR_IlmBase::Half "${_IMPORT_PREFIX}/mitsuba/Half.lib" "${_IMPORT_PREFIX}/mitsuba/Half.dll" )

# Import target "IlmBase::Iex" for configuration "Release"
set_property(TARGET IlmBase::Iex APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IlmBase::Iex PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/Iex.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/Iex.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS IlmBase::Iex )
list(APPEND _IMPORT_CHECK_FILES_FOR_IlmBase::Iex "${_IMPORT_PREFIX}/mitsuba/Iex.lib" "${_IMPORT_PREFIX}/mitsuba/Iex.dll" )

# Import target "IlmBase::IexMath" for configuration "Release"
set_property(TARGET IlmBase::IexMath APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IlmBase::IexMath PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/IexMath.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/IexMath.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS IlmBase::IexMath )
list(APPEND _IMPORT_CHECK_FILES_FOR_IlmBase::IexMath "${_IMPORT_PREFIX}/mitsuba/IexMath.lib" "${_IMPORT_PREFIX}/mitsuba/IexMath.dll" )

# Import target "IlmBase::Imath" for configuration "Release"
set_property(TARGET IlmBase::Imath APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IlmBase::Imath PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/Imath.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/Imath.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS IlmBase::Imath )
list(APPEND _IMPORT_CHECK_FILES_FOR_IlmBase::Imath "${_IMPORT_PREFIX}/mitsuba/Imath.lib" "${_IMPORT_PREFIX}/mitsuba/Imath.dll" )

# Import target "IlmBase::IlmThread" for configuration "Release"
set_property(TARGET IlmBase::IlmThread APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(IlmBase::IlmThread PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmThread.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/mitsuba/IlmThread.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS IlmBase::IlmThread )
list(APPEND _IMPORT_CHECK_FILES_FOR_IlmBase::IlmThread "${_IMPORT_PREFIX}/mitsuba/IlmThread.lib" "${_IMPORT_PREFIX}/mitsuba/IlmThread.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

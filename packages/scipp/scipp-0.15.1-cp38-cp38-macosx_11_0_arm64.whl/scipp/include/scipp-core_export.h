
#ifndef SCIPP_CORE_EXPORT_H
#define SCIPP_CORE_EXPORT_H

#ifdef SCIPP_CORE_STATIC_DEFINE
#  define SCIPP_CORE_EXPORT
#  define SCIPP_CORE_NO_EXPORT
#else
#  ifndef SCIPP_CORE_EXPORT
#    ifdef scipp_core_EXPORTS
        /* We are building this library */
#      define SCIPP_CORE_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define SCIPP_CORE_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef SCIPP_CORE_NO_EXPORT
#    define SCIPP_CORE_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef SCIPP_CORE_DEPRECATED
#  define SCIPP_CORE_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef SCIPP_CORE_DEPRECATED_EXPORT
#  define SCIPP_CORE_DEPRECATED_EXPORT SCIPP_CORE_EXPORT SCIPP_CORE_DEPRECATED
#endif

#ifndef SCIPP_CORE_DEPRECATED_NO_EXPORT
#  define SCIPP_CORE_DEPRECATED_NO_EXPORT SCIPP_CORE_NO_EXPORT SCIPP_CORE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef SCIPP_CORE_NO_DEPRECATED
#    define SCIPP_CORE_NO_DEPRECATED
#  endif
#endif

#endif /* SCIPP_CORE_EXPORT_H */

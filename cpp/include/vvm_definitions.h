/**
 * @file vvm_definitions.h
 * @authors Simon Schaefer
 * @date 16.09.2020
 *
 * This file contains all general definitions, types, enums etc. used by the VVM project.
 *
 * Styleguide:
 *  - Do not use enums as there are imported in the global namespace without requiring the prefix. This may lead to
 *    unintuitive naming. Use enum class instead as this always require the prefix to be used.
 */

#ifndef VVM_DEFINITIONS_H
#define VVM_DEFINITIONS_H

// Check if the generated files where created and at the proper location
#if __has_include("reference_types.h") && __has_include("perception_types.h")

#include "reference_types.h"
#include "perception_types.h"

#else
#error Generated headers are missing. Generate them be executing the generate_enums.py in the omega_format/enums directory.
#endif

#endif //VVM_DEFINITIONS_H

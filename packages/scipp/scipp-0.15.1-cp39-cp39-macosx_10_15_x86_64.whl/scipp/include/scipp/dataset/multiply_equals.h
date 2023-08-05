// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Simon Heybrock
#pragma once

#include "scipp-variable_export.h"
#include "scipp/dataset/dataset.h"

namespace scipp::dataset {

SCIPP_DATASET_EXPORT DataArray &operator*=(DataArray &lhs, const Variable &rhs);
SCIPP_DATASET_EXPORT DataArray &operator*=(DataArray &lhs, const DataArray &rhs);
SCIPP_DATASET_EXPORT DataArray operator*=(DataArray &&lhs, const Variable &rhs);
SCIPP_DATASET_EXPORT DataArray operator*=(DataArray &&lhs, const DataArray &rhs);

} // namespace scipp::dataset

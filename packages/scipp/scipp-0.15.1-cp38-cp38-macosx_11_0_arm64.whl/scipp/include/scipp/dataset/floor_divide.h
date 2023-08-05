// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Simon Heybrock
#pragma once

#include "scipp/dataset/dataset.h"

namespace scipp::dataset {

[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
floor_divide(const DataArray &a, const DataArray &b);
[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
floor_divide(const DataArray &a, const Variable &b);
[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
floor_divide(const Variable &a, const DataArray &b);

} // namespace scipp::dataset

# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from spaceflights.pipelines import data_processing as dp
from spaceflights.pipelines import data_filtering as df
from spaceflights.pipelines import data_science as ds


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    data_processing_pipeline = dp.create_pipeline()
    # TODO: define data_filtering_pipeline.
    # TODO: alter the appropriate parameters file to filter by engine_type == "Quantum".
    data_filtering_pipeline = df.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    unfiltered_pipeline = data_processing_pipeline + data_science_pipeline

    # TODO: use the `inputs` and `outputs` arguments of `pipeline` to connect
    #  data_filtering_pipeline onto data_processing_pipeline and data_science_pipeline.
    #  If you have node name clashes, use the `namespace` argument.
    filtered_pipeline = (
        pipeline(data_processing_pipeline)
        + pipeline(data_filtering_pipeline,
                   inputs={"input_table": "model_input_table"},
                   outputs={"output_table": "filtered_model_input_table"})
        + pipeline(data_science_pipeline,
                   inputs={"model_input_table": "filtered_model_input_table"},
                   namespace="filtered")
    )

    return {
        # TODO: update the pipeline registry to include filtered_pipeline in __default__
        #  and to register new pipelines "unfiltered_pipeline" and "filtered_pipeline".
        "__default__": (unfiltered_pipeline + filtered_pipeline),
        "dp": data_processing_pipeline,
        "df": data_filtering_pipeline,
        "ds": data_science_pipeline,
    }

# CHALLENGE TODO 1: run the data_filtering_pipeline twice in series to get model
#  performance after filtering by engine_type == "Quantum" AND then by
#  shuttle_type == "Type F5". You should do this just by altering this file and
#  parameters file without touching anything in pipelines/data_filtering.

# CHALLENGE TODO 2: run the data_filtering_pipeline onwards twice in parallel to get
#  model  performance after filtering by engine_type == "Quantum" OR by
#  shuttle_type == "Type F5". You should do this just by altering this file and
#  parameters file without touching anything in pipelines/data_filtering.

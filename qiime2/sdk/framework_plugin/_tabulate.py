# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import re
import shutil

import qiime2
import q2templates


TEMPLATES = pkg_resources.resource_filename('qiime2.sdk.framework_plugin',
                                            'templates')


def tabulate(output_dir: str, metadata: qiime2.Metadata) -> None:
    df = metadata.to_dataframe()
    df.reset_index(inplace=True)

    table = df.to_html(index=False, classes="table table-striped table-hover")
    table = table.replace('border="1"', 'border="0"')
    # Gross hack, but `to_html` doesn't support specifying the id
    table = re.sub(' table-hover', '" id="table', table)

    index = os.path.join(TEMPLATES, 'tabulate', 'index.html')
    q2templates.render(index, output_dir, context={'table': table})

    df.to_csv(os.path.join(output_dir, 'metadata.tsv'), sep='\t')

    js = os.path.join(TEMPLATES, 'tabulate', 'tsorter.min.js')
    os.mkdir(os.path.join(output_dir, 'js'))
    shutil.copy(js, os.path.join(output_dir, 'js', 'tsorter.min.js'))

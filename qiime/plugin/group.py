# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
import qiime.core.mypy.interpreter as interpreter


class Group:
    def __init__(self, name, pathspec, format=None, iterable=None,
                 path_handler=None, _mode=None):
        if _mode not in ('r', 'w', None):
            raise Exception()
        if format is None and iterable is None:
            raise Exception()
        if format is not None and iterable is not None:
            raise Exception()

        self.name = name
        self.pathspec = pathspec
        self.is_iterable = iterable is not None
        self.format = format if format is not None else iterable
        self._mode = _mode

    def view(self, type):
        resource_pattern = interpreter.view_interpreter(type)
        pattern = resource_pattern.pattern
        # Find a mapping from self.format -> pattern
        # if iterable, produce an iterator of that mapping
        if resource_pattern.resource_type == 'Object':
            pass
        elif resource_pattern.resource_type == 'FilePath':
            pass
        elif resource_pattern.resource_type == 'DirectoryPath':
            pass
        else:
            raise Exception()

    def inject(self, source, type, **kwargs):
        if self._mode != 'w':
            raise Exception()



dl.group['reverse_reads'].view(Iterable[skbio.DNA]) -> iterable[iterable[skbio.DNA]]

dl.group['reverse_reads'].inject(seqs, Iterable[skbio.DNA], sample_id="foo")

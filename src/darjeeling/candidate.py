from typing import List, Iterator
from darjeeling.transformation import Transformation, \
                                      DeleteTransformation, \
                                      ReplaceTransformation, \
                                      AppendTransformation
from darjeeling.problem import Problem


class Candidate(object):
    """
    Represents a candidate repair as a set of atomic program transformations.
    """
    def __init__(self,
                 transformations: List[Transformation]
                 ) -> None:
        self.__transformations = frozenset(transformations)


    @property
    def transformations(self) -> Iterator[Transformation]:
        """
        The transformations that comprise this repair.
        """
        for t in self.__transformations:
            yield t

    def diff(self, problem: Problem) -> str:
        """
        Computes a plaintext diff for this repair.
        """
        # group transformations by file
        tf = {}
        for t in self.transformations:
            fn = t.line.filename
            if fn not in tf:
                tf[fn] = []
            tf[fn].append(t)

        # order each group of transformations in descending order of
        # line number
        for group in tf.values():
            group.sort(key=lambda t: t.line.num, reverse=True)

        # transform each group into a modified source code file
        transformed = {}
        for (fn, transformations) in tf.items():
            src = problem.source(fn)
            for t in transformations:
                if isinstance(t, DeleteTransformation):
                    src = src.with_line_removed(t.line.num)
                elif isinstance(t, AppendTransformation):
                    src = src.with_line_inserted(t.line.num + 1, t.snippet.content)
                elif isinstance(t, ReplaceTransformation):
                    src = src.with_line_replaced(t.line.num, t.snippet.content)
                else:
                    raise Exception("unsupported transformation")
            transformed[fn] = src

        # compute a diff for each modified source code file

        # combine the diffs for each file into a single diff

        raise NotImplementedError
        return diff

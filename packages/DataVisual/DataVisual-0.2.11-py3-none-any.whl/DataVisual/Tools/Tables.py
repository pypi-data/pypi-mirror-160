from itertools import product
import numpy as np
from dataclasses import dataclass
from copy import deepcopy

from DataVisual.Tools.utils import ToList


@dataclass
class XParameter(object):
    Name: str  = None
    Values: str  = None
    Format: str  = ""
    LongLabel: str  = ""
    Unit: str  = ""
    Legend: str  = ""
    Type: type = float
    Position: int = None

    def __post_init__(self):
        self.Values  = ToList(self.Values).astype(self.Type) if self.Type is not None else ToList(self.Values)
        self.Init()

    def Init(self):
        self.Label  = self.LongLabel + f" {self.Unit}" if self.LongLabel != "" else self.Name
        self.Legend = self.Legend if self.Legend != "" else self.Name

    @property
    def Unique(self):
        if self.Values.shape[0] == 1:
            return True
        else:
            return False

    def Normalize(self):
        self.Unit = "[U.A.]"
        self.Init()


    def GetValues(self, idx: int=None):
        if self.Format is None:
            return f" | {self.Legend} : {self.Values[idx]}"

        if self.Values[idx] is None:
            return f" | {self.Legend} : None"

        else:
            return f" | {self.Legend} : {self.Values[idx]:{self.Format}}"


    def GetLabels(self):
        return [self.GetValues(idx) for idx in range(self.Values.shape[0])]


    def flatten(self):
        return np.array( [x for x in self.Values] ).flatten()

    def __getitem__(self, item):
        return self.Values[item]

    def __repr__(self):
        return self.Name

    def GetSize(self):
        return self.Values.shape[0]

    def __eq__(self, other):
        return True if self.Name == other.Name else False

    def str(self, item):
        return f" | {self.LongLabel} : {self.Values[item]:{self.Format}}"

    def __str__(self):
        if self.Values.size == 1:
            return f" | {self.LongLabel} : {self.Values[0]:{self.Format}} {self.Unit}"
        else:
            return self.Values.__str__()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class XTable(object):
    def __init__(self, X, Settings):
        self.X         = X
        self.Shape     = [x.GetSize() for x in self.X]
        self.NameTable = { x.Name: order for order, x in enumerate(self.X) }
        self.Settings  = Settings

    def GetValues(self, Axis):
        return self[Axis].Value


    def GetPosition(self, Value):
        for order, x in enumerate(self.X):
            if x == Value:
                return order


    def __getitem__(self, Val):
        if Val is None: return None

        Val = self.NameTable[Val] if isinstance(Val, str) else Val

        return self.X[Val]

    def ExcludeTable(self, Axis, Exclude):
        Shape = self.Shape

        Shape[self.GetPosition(Axis)] = None
        ExcludedTable = self.X

        if Exclude is not None:
            ExcludeIDX = self.GetPosition(Exclude)
            Shape = np.delete(Shape, ExcludeIDX)
            ExcludedTable.pop(ExcludeIDX)

        return Shape, ExcludedTable


    def GetSlicer(self, Axis, Exclude=None):
        Shape, ExcludedTable = self.ExcludeTable(Axis, Exclude)

        DimSlicer = [range(s) if s is not None else [slice(None)] for s in Shape]
        Fixed = [x for x in ExcludedTable if x.Unique]
        Variable = [x for x in ExcludedTable if not x.Unique and x != Axis]

        self.Settings.CommonLabel = "".join( [ x.GetValues(0) for x in Fixed ] )

        Slicer = product(*DimSlicer)

        P = [x.GetLabels() for x in Variable]

        DiffLabel = [ ''.join(p) for p in product(*P) ]

        return zip(Slicer, DiffLabel)


    def Remove(self, Axis):
        return XTable( X = [x for x in self if x != Axis], Settings=self.Settings )



class YTable(object):
    def __init__(self, Y, Settings):
        self.Y = Y
        self.NameTable = self.GetNameTable()
        self.Settings = Settings


    def GetShape(self):
        return [x.Size for x in self.Y] + [1]

    def GetNameTable(self):
        return { x.Name: order for order, x in enumerate(self.Y) }


    def __getitem__(self, Val):
        if isinstance(Val, str):
            Val = Val
            idx = self.NameTable[Val]
            return self.Y[idx]
        else:
            return self.Y[Val]

    def GetSlicer(self, x):
        Xidx        = self.NameTable[x]

        self.Shape[Xidx] = None

        xval        = self.Y[Xidx].Array

        DimSlicer   = [range(s) if s is not None else [slice(None)] for s in self.Shape[:-1]]

        return product(*DimSlicer), xval

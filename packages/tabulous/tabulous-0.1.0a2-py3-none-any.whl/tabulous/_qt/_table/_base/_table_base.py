from __future__ import annotations
from typing import Any, Callable, TYPE_CHECKING
import warnings
from qtpy import QtWidgets as QtW, QtGui, QtCore
from qtpy.QtCore import Signal, Qt

import numpy as np
import pandas as pd

from collections_undo import UndoManager
from ._model_base import AbstractDataFrameModel
from ..._utils import show_messagebox, QtKeys
from ....types import FilterType, ItemInfo, HeaderInfo, SelectionType, _Sliceable

if TYPE_CHECKING:
    from ._delegate import TableItemDelegate

# Flags
_EDITABLE = (
    QtW.QAbstractItemView.EditTrigger.EditKeyPressed
    | QtW.QAbstractItemView.EditTrigger.DoubleClicked
)
_READ_ONLY = QtW.QAbstractItemView.EditTrigger.NoEditTriggers
_SCROLL_PER_PIXEL = QtW.QAbstractItemView.ScrollMode.ScrollPerPixel


def _count_data_size(*args, **kwargs) -> float:
    total_nbytes = 0
    for arg in args:
        total_nbytes += _getsizeof(arg)
    for v in kwargs.values():
        total_nbytes += _getsizeof(v)
    return total_nbytes


def _getsizeof(obj) -> float:
    if isinstance(obj, pd.DataFrame):
        nbytes = obj.memory_usage(deep=True).sum()
    elif isinstance(obj, pd.Series):
        nbytes = obj.memory_usage(deep=True)
    elif isinstance(obj, np.ndarray):
        nbytes = obj.nbytes
    elif isinstance(obj, (list, tuple, set)):
        nbytes = sum(_getsizeof(x) for x in obj)
    elif isinstance(obj, dict):
        nbytes = sum(_getsizeof(x) for x in obj.values())
    else:
        nbytes = 1  # approximate
    return nbytes


class _QTableViewEnhanced(QtW.QTableView):
    selectionChangedSignal = Signal()
    rightClickedSignal = Signal(QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_pos: QtCore.QPoint | None = None
        self._was_right_dragging: bool = False
        self._zoom = 1.0
        self._initial_font_size = self.font().pointSize()
        vheader, hheader = self.verticalHeader(), self.horizontalHeader()
        self.setFrameStyle(QtW.QFrame.Shape.Box)
        vheader.setFrameStyle(QtW.QFrame.Shape.Box)
        hheader.setFrameStyle(QtW.QFrame.Shape.Box)
        vheader.resize(16, vheader.height())
        self.setStyleSheet("QHeaderView::section { border: 1px solid black}")
        vheader.setMinimumSectionSize(0)
        hheader.setMinimumSectionSize(0)
        vheader.font().setPointSize(self._initial_font_size)
        hheader.font().setPointSize(self._initial_font_size)

        vheader.setDefaultSectionSize(28)
        hheader.setDefaultSectionSize(100)

        hheader.setSectionResizeMode(QtW.QHeaderView.ResizeMode.Fixed)
        vheader.setSectionResizeMode(QtW.QHeaderView.ResizeMode.Fixed)

        self._initial_section_size = (
            hheader.defaultSectionSize(),
            vheader.defaultSectionSize(),
        )
        self.setZoom(1.0)  # initialize

    def selectionChanged(
        self,
        selected: QtCore.QItemSelection,
        deselected: QtCore.QItemSelection,
    ) -> None:
        """Evoked when table selection range is changed."""
        self.selectionChangedSignal.emit()
        return super().selectionChanged(selected, deselected)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        """Register clicked position"""
        if e.button() == Qt.MouseButton.RightButton:
            self._last_pos = e.pos()
            self._was_right_dragging = False
        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        """Scroll table plane when mouse is moved with right click."""
        if self._last_pos is not None:
            pos = e.pos()
            dy = pos.y() - self._last_pos.y()
            dx = pos.x() - self._last_pos.x()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - dy)
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dx)
            self._last_pos = pos
            self._was_right_dragging = True
        return super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        """Delete last position."""
        if e.button() == Qt.MouseButton.RightButton and not self._was_right_dragging:
            self.rightClickedSignal.emit(e.pos())
        self._last_pos = None
        self._was_right_dragging = False
        return super().mouseReleaseEvent(e)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        """Evoke parent keyPressEvent."""
        keys = QtKeys(e)
        if keys.is_typing():
            parent = self.parent()
            if isinstance(parent, QBaseTable):
                parent.keyPressEvent(e)
        else:
            return super().keyPressEvent(e)

    def zoom(self) -> float:
        """Get current zoom factor."""
        return self._zoom

    def setZoom(self, value: float) -> None:
        """Set zoom factor."""
        if not 0.25 <= value <= 2.0:
            raise ValueError("Zoom factor must between 0.25 and 2.0.")
        # To keep table at the same position.
        zoom_ratio = 1 / self._zoom * value
        pos = self.verticalScrollBar().sliderPosition()
        self.verticalScrollBar().setSliderPosition(int(pos * zoom_ratio))
        pos = self.horizontalScrollBar().sliderPosition()
        self.horizontalScrollBar().setSliderPosition(int(pos * zoom_ratio))

        # Zoom font size
        font = self.font()
        font.setPointSize(int(self._initial_font_size * value))
        self.setFont(font)
        self.verticalHeader().setFont(font)
        self.horizontalHeader().setFont(font)

        # Zoom section size of headers
        h, v = self._initial_section_size
        self.setSectionSize(int(h * value), int(v * value))

        # Update stuff
        self._zoom = value
        return

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        """Zoom in/out table."""
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier:
            dt = e.angleDelta().y() / 120
            zoom = self.zoom() + 0.15 * dt
            self.setZoom(min(max(zoom, 0.25), 2.0))
            return None

        return super().wheelEvent(e)

    def sectionSize(self) -> tuple[int, int]:
        return (
            self.horizontalHeader().defaultSectionSize(),
            self.verticalHeader().defaultSectionSize(),
        )

    def setSectionSize(self, horizontal: int, vertical: int) -> None:
        """Update section size of headers."""
        self.verticalHeader().setDefaultSectionSize(vertical)
        self.horizontalHeader().setDefaultSectionSize(horizontal)
        return


class QBaseTable(QtW.QWidget):
    """
    The base widget for a table.

    Abstract Methods
    ----------------
    def createQTableView(self) -> None: ...
    def getDataFrame(self) -> pd.DataFrame: ...
    def setDataFrame(self) -> None: ...
    def createModel(self) -> AbstractDataFrameModel: ...
    def tableSlice(self) -> pd.DataFrame: ...
    """

    selectionChangedSignal = Signal(list)
    _DEFAULT_EDITABLE = False
    _mgr = UndoManager(measure=_count_data_size, maxsize=1e7)

    def __init__(
        self, parent: QtW.QWidget | None = None, data: pd.DataFrame | None = None
    ):
        super().__init__(parent)
        self._filter_slice: FilterType | None = None
        self.createQTableView()
        self.createModel()
        self.setDataFrame(data)
        self._qtable_view.setVerticalScrollMode(_SCROLL_PER_PIXEL)
        self._qtable_view.setHorizontalScrollMode(_SCROLL_PER_PIXEL)
        self._qtable_view.setFrameStyle(QtW.QFrame.Shape.NoFrame)

        from ._delegate import TableItemDelegate

        delegate = TableItemDelegate(parent=self)
        self._qtable_view.setItemDelegate(delegate)
        self._qtable_view.selectionChangedSignal.connect(
            lambda: self.selectionChangedSignal.emit(self.selections())
        )
        if not self._DEFAULT_EDITABLE:
            self._qtable_view.setEditTriggers(_READ_ONLY)

    @property
    def _qtable_view(self) -> _QTableViewEnhanced:
        raise NotImplementedError()

    def createQTableView(self) -> None:
        """Create QTableView."""
        raise NotImplementedError()

    def getDataFrame(self) -> pd.DataFrame:
        raise NotImplementedError()

    def setDataFrame(self) -> None:
        raise NotImplementedError()

    def createModel(self) -> AbstractDataFrameModel:
        raise NotImplementedError()

    def tableSlice(self) -> pd.DataFrame:
        raise NotImplementedError()

    def tableShape(self) -> tuple[int, int]:
        model = self._qtable_view.model()
        nr = model.rowCount()
        nc = model.columnCount()
        return (nr, nc)

    def zoom(self) -> float:
        """Get current zoom factor."""
        return self._qtable_view.zoom()

    def setZoom(self, value: float) -> None:
        """Set zoom factor."""
        return self._qtable_view.setZoom(value)

    def itemDelegate(self) -> TableItemDelegate:
        return QtW.QTableView.itemDelegate(self._qtable_view)

    def model(self) -> AbstractDataFrameModel:
        return QtW.QTableView.model(self._qtable_view)

    def precision(self) -> int:
        """Return table value precision."""
        return self.itemDelegate().ndigits

    def setPrecision(self, ndigits: int) -> None:
        """Set table value precision."""
        ndigits = int(ndigits)
        if ndigits <= 0:
            raise ValueError("Cannot set negative precision.")
        self.itemDelegate().ndigits = ndigits

    def connectSelectionChangedSignal(self, slot):
        self.selectionChangedSignal.connect(slot)
        return slot

    def selections(self) -> SelectionType:
        """Get list of selections as slicable tuples"""
        qtable = self._qtable_view
        selections = qtable.selectionModel().selection()

        # selections = self.selectedRanges()
        out: SelectionType = []
        for i in range(len(selections)):
            sel = selections[i]
            r0 = sel.top()
            r1 = sel.bottom() + 1
            c0 = sel.left()
            c1 = sel.right() + 1
            out.append((slice(r0, r1), slice(c0, c1)))

        return out

    def setSelections(self, selections: SelectionType):
        """Set list of selections."""
        qtable = self._qtable_view
        qtable.clearSelection()

        model = self.model()
        nr, nc = model.df.shape
        try:
            for sel in selections:
                r, c = sel
                # if int is used instead of slice
                if not isinstance(r, slice):
                    _r = r.__index__()
                    r = slice(_r, _r + 1)
                if not isinstance(c, slice):
                    _c = c.__index__()
                    c = slice(_c, _c + 1)
                r0, r1, _ = r.indices(nr)
                c0, c1, _ = c.indices(nc)
                selection = QtCore.QItemSelection(
                    model.index(r0, c0), model.index(r1 - 1, c1 - 1)
                )
                qtable.selectionModel().select(
                    selection, QtCore.QItemSelectionModel.SelectionFlag.Select
                )

        except Exception as e:
            qtable.clearSelection()
            raise e

    def copyToClipboard(self, headers: bool = True):
        """Copy currently selected cells to clipboard."""
        selections = self.selections()
        if len(selections) == 0:
            return
        r_ranges = set()
        c_ranges = set()
        for rsel, csel in selections:
            r_ranges.add((rsel.start, rsel.stop))
            c_ranges.add((csel.start, csel.stop))

        nr = len(r_ranges)
        nc = len(c_ranges)
        if nr > 1 and nc > 1:
            show_messagebox(
                mode="error", title="Error", text="Wrong selection range.", parent=self
            )
            return
        else:
            data = self.model().df
            if nr == 1:
                axis = 1
            else:
                axis = 0
            ref = pd.concat([data.iloc[sel] for sel in selections], axis=axis)
            ref.to_clipboard(index=headers, header=headers)

    def pasteFromClipBoard(self):
        raise TypeError("Table is immutable.")

    def readClipBoard(self) -> pd.DataFrame:
        """Read clipboard data and return as pandas DataFrame."""
        return pd.read_clipboard(header=None)

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        keys = QtKeys(e)
        if keys == "Ctrl+C":
            return self.copyToClipboard(False)
        elif keys == "Ctrl+Shift+C":
            return self.copyToClipboard(True)

        return super().keyPressEvent(e)

    def filter(self) -> FilterType | None:
        """Return the current filter."""
        return self._filter_slice

    def setFilter(self, sl: FilterType):
        """Set filter to the table view."""
        # NOTE: This method is also called when table needs initialization.

        self._filter_slice = sl
        data_sliced = self.tableSlice()

        if sl is None:
            self.model().df = data_sliced
        else:
            try:
                if callable(sl):
                    sl_filt = sl(data_sliced)
                else:
                    sl_filt = sl
                self.model().df = data_sliced[sl_filt]
            except Exception as e:
                self._filter_slice = None
                msg = f"Error in filter.\n\n{type(e).__name__} {e}\n\n Filter is reset."
                show_messagebox("error", "Error", msg, self)
        self.refresh()

    def refresh(self) -> None:
        qtable = self._qtable_view
        qtable.viewport().update()
        # headers have also to be updated.
        qtable.horizontalHeader().viewport().update()
        qtable.verticalHeader().viewport().update()
        return None


class QMutableTable(QBaseTable):
    """A mutable table widget."""

    itemChangedSignal = Signal(ItemInfo)
    rowChangedSignal = Signal(HeaderInfo)
    columnChangedSignal = Signal(HeaderInfo)
    selectionChangedSignal = Signal(list)
    _data_raw: pd.DataFrame

    def __init__(
        self, parent: QtW.QWidget | None = None, data: pd.DataFrame | None = None
    ):
        super().__init__(parent, data)
        self._editable = False
        self.model().dataEdited.connect(self.setDataFrameValue)

        # header editing signals
        self._qtable_view.horizontalHeader().sectionDoubleClicked.connect(
            self.editHorizontalHeader
        )
        self._qtable_view.verticalHeader().sectionDoubleClicked.connect(
            self.editVerticalHeader
        )
        self._mgr.clear()

    def tableShape(self) -> tuple[int, int]:
        """Return the available shape of the table."""
        model = self.model()
        nr = model.rowCount()
        nc = model.columnCount()
        return (nr, nc)

    def tableSlice(self) -> pd.DataFrame:
        """Return 2D table for display."""
        return self._data_raw

    def convertValue(self, r: int, c: int, value: Any) -> Any:
        """Convert value before updating DataFrame."""
        return value

    def setDataFrameValue(self, r: _Sliceable, c: _Sliceable, value: Any) -> None:
        data = self._data_raw

        # convert values
        if isinstance(r, slice) and isinstance(c, slice):
            _value: pd.DataFrame = value
            if _value.size == 1:
                v = _value.values[0, 0]
                _value = data.iloc[r, c].copy()
                for _ir, _r in enumerate(range(r.start, r.stop)):
                    for _ic, _c in enumerate(range(c.start, c.stop)):
                        _value.iloc[_ir, _ic] = self.convertValue(_r, _c, v)
            else:
                for _ir, _r in enumerate(range(r.start, r.stop)):
                    for _ic, _c in enumerate(range(c.start, c.stop)):
                        _value.iloc[_ir, _ic] = self.convertValue(
                            _r, _c, _value.iloc[_ir, _ic]
                        )
            _is_scalar = False
        else:
            _value = self.convertValue(r, c, value)
            _is_scalar = True

        # if table has filter, indices must be adjusted
        if self._filter_slice is None:
            r0 = r
        else:
            if callable(self._filter_slice):
                sl = self._filter_slice(data)
            else:
                sl = self._filter_slice

            spec = np.where(sl)[0].tolist()
            r0 = spec[r]
            self.model().updateValue(r, c, _value)

        _old_value = data.iloc[r0, c]
        if not _is_scalar:
            _old_value: pd.DataFrame
            _old_value = _old_value.copy()  # this is needed for undo

        # emit item changed signal if value changed
        if _equal(_value, _old_value) and self._editable:
            self._set_value(r0, c, r, c, _value, _old_value)
        return None

    @QBaseTable._mgr.undoable(name="setDataFrameValue")
    def _set_value(self, r, c, r_ori, c_ori, value, old_value):
        self.updateValue(r, c, value)
        self.setSelections([(r_ori, c_ori)])
        self.itemChangedSignal.emit(ItemInfo(r, c, value, old_value))
        return None

    @_set_value.undo_def
    def _set_value(self, r, c, r_ori, c_ori, value, old_value):
        self.updateValue(r, c, old_value)
        self.setSelections([(r_ori, c_ori)])
        self.itemChangedSignal.emit(ItemInfo(r, c, old_value, value))
        return None

    def updateValue(self, r, c, value):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._data_raw.iloc[r, c] = value

        if self._filter_slice is not None:
            self.setFilter(self._filter_slice)
        self.refresh()

    def isEditable(self) -> bool:
        """Return the editability of the table."""
        return self._editable

    def setEditable(self, editable: bool):
        """Set the editability of the table."""
        if editable:
            self._qtable_view.setEditTriggers(_EDITABLE)
        else:
            self._qtable_view.setEditTriggers(_READ_ONLY)
        self._editable = editable

    def connectItemChangedSignal(
        self,
        slot_val: Callable[[ItemInfo], None],
        slot_row: Callable[[HeaderInfo], None],
        slot_col: Callable[[HeaderInfo], None],
    ) -> None:
        self.itemChangedSignal.connect(slot_val)
        self.rowChangedSignal.connect(slot_row)
        self.columnChangedSignal.connect(slot_col)
        return None

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        keys = QtKeys(e)
        if keys == "Ctrl+C":
            return self.copyToClipboard(headers=False)
        elif keys == "Ctrl+Shift+C":
            return self.copyToClipboard(headers=True)
        elif keys == "Ctrl+V":
            return self.pasteFromClipBoard()
        elif keys in ("Delete", "Backspace"):
            return self.deleteValues()
        elif keys == "Ctrl+Z":
            self.undo()
        elif keys == "Ctrl+Y":
            self.redo()
        elif keys.is_typing() and self.isEditable():
            # Enter editing mode
            qtable = self._qtable_view
            text = keys.key_string()
            if not keys.has_shift():
                text = text.lower()
            qtable.edit(qtable.currentIndex())
            focused_widget = QtW.QApplication.focusWidget()
            if isinstance(focused_widget, QtW.QLineEdit):
                focused_widget.setText(text)
                focused_widget.deselect()
            return
        else:
            return super().keyPressEvent(e)

    def pasteFromClipBoard(self):
        """
        Paste data to table.

        This function supports many types of pasting.
        1. Single selection, single data in clipboard -> just paste
        2. Single selection, multiple data in clipboard -> paste starts from the selection position.
        3. Multiple selection, single data in clipboard -> paste the same value for all the selection.
        4. Multiple selection, multiple data in clipboard -> paste only if their shape is identical.

        Also, if data is filtrated, pasted data also follows the filtration.
        """
        selections = self.selections()
        n_selections = len(selections)
        if n_selections == 0 or not self.isEditable():
            return
        elif n_selections > 1:
            return show_messagebox(
                mode="error",
                title="Error",
                text="Cannot paste with multiple selections.",
                parent=self,
            )

        df = self.readClipBoard()

        # check size and normalize selection slices
        sel = selections[0]
        rrange, crange = sel
        rlen = rrange.stop - rrange.start
        clen = crange.stop - crange.start
        dr, dc = df.shape
        size = dr * dc

        if rlen * clen == 1 and size > 1:
            sel = (
                slice(rrange.start, rrange.start + dr),
                slice(crange.start, crange.start + dc),
            )

        elif size > 1 and (rlen, clen) != (dr, dc):
            # If selection is column-wide or row-wide, resize them
            model = self.model()
            if rlen == model.df.shape[0]:
                rrange = slice(0, dr)
                rlen = dr
            if clen == model.df.shape[1]:
                crange = slice(0, dc)
                clen = dc

            if (rlen, clen) != (dr, dc):
                return show_messagebox(
                    mode="error",
                    title="Error",
                    text=f"Shape mismatch between data in clipboard {(rlen, clen)} and "
                    f"destination {(dr, dc)}.",
                    parent=self,
                )
            else:
                sel = (rrange, crange)

        rsel, csel = sel

        # check dtype
        dtype_src = df.dtypes.values
        dtype_dst = self._data_raw.dtypes.values[csel]
        if any(a.kind != b.kind for a, b in zip(dtype_src, dtype_dst)):
            return show_messagebox(
                mode="error",
                title="Error",
                text=f"Data type mismatch between data in clipboard {list(dtype_src)} and "
                f"destination {list(dtype_dst)}.",
                parent=self,
            )
        # update table
        try:
            self.setDataFrameValue(rsel, csel, df)

        except Exception as e:
            show_messagebox(
                mode="error",
                title=e.__class__.__name__,
                text=str(e),
                parent=self,
            )
            raise e from None

        else:
            self.setSelections([sel])

        return None

    def deleteValues(self):
        """Replace selected cells with NaN."""
        if not self.isEditable():
            return None
        selections = self.selections()
        for sel in selections:
            rsel, csel = sel
            nr = rsel.stop - rsel.start
            nc = csel.stop - csel.start
            dtypes = list(self._data_raw.dtypes.values[csel])
            df = pd.DataFrame(
                {c: pd.Series(np.full(nr, np.nan), dtype=dtypes[c]) for c in range(nc)},
            )
            self.setDataFrameValue(rsel, csel, df)
        return None

    def editHorizontalHeader(self, index: int):
        """Edit the horizontal header."""
        if not self.isEditable():
            return

        qtable = self._qtable_view
        _header = qtable.horizontalHeader()
        _line = QtW.QLineEdit(_header)
        edit_geometry = _line.geometry()
        edit_geometry.setHeight(_header.height())
        edit_geometry.setWidth(_header.sectionSize(index))
        edit_geometry.moveLeft(_header.sectionViewportPosition(index))
        _line.setGeometry(edit_geometry)
        _line.setHidden(False)
        _line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        column_axis = self.model().df.columns
        if index < column_axis.size:
            old_value = column_axis[index]
            text = str(old_value)
        else:
            old_value = None
            text = ""

        _line.setText(text)
        _line.selectAll()
        _line.setFocus()

        self._line = _line

        @_line.editingFinished.connect
        def _set_header_data():
            if self._line is None:
                return None
            self._line.setHidden(True)
            value = self._line.text()
            if not value == old_value:
                self.setHorizontalHeaderValue(index, value)
                self.columnChangedSignal.emit(HeaderInfo(index, value, old_value))
            self._line = None
            qtable.setFocus()
            qtable.clearSelection()
            return None

        return None

    def editVerticalHeader(self, index: int):
        if not self.isEditable():
            return

        qtable = self._qtable_view
        _header = qtable.verticalHeader()
        _line = QtW.QLineEdit(_header)
        edit_geometry = _line.geometry()
        edit_geometry.setHeight(_header.sectionSize(index))
        edit_geometry.setWidth(_header.width())
        edit_geometry.moveTop(_header.sectionViewportPosition(index))
        _line.setGeometry(edit_geometry)
        _line.setHidden(False)

        index_axis = self.model().df.index

        if index < index_axis.size:
            old_value = index_axis[index]
            text = str(old_value)
        else:
            old_value = None
            text = ""

        _line.setText(str(text))
        _line.setFocus()
        _line.selectAll()
        _line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._line = _line

        @_line.editingFinished.connect
        def _set_header_data():
            if self._line is None:
                return None
            self._line.setHidden(True)
            value = self._line.text()
            if not value == old_value:
                self.setVerticalHeaderValue(index, value)
                self.rowChangedSignal.emit(HeaderInfo(index, value, old_value))
            self._line = None
            qtable.setFocus()
            qtable.clearSelection()
            return None

        return None

    @QBaseTable._mgr.interface
    def setHorizontalHeaderValue(self, index: int, value: Any) -> None:
        qtable = self._qtable_view
        column_axis = self.model().df.columns
        _header = qtable.horizontalHeader()

        mapping = {column_axis[index]: value}

        self._data_raw.rename(columns=mapping, inplace=True)
        self.model().df.rename(columns=mapping, inplace=True)

        size_hint = _header.sectionSizeHint(index)
        if _header.sectionSize(index) < size_hint:
            _header.resizeSection(index, size_hint)
        self.refresh()
        return None

    @setHorizontalHeaderValue.server
    def setHorizontalHeaderValue(self, index: int, value: Any) -> Any:
        return (index, self.model().df.columns[index]), {}

    @QBaseTable._mgr.interface
    def setVerticalHeaderValue(self, index: int, value: Any) -> None:
        qtable = self._qtable_view
        index_axis = self.model().df.index
        _header = qtable.verticalHeader()

        mapping = {index_axis[index]: value}

        self._data_raw.rename(index=mapping, inplace=True)
        self.model().df.rename(index=mapping, inplace=True)
        _width_hint = _header.sizeHint().width()
        _header.resize(QtCore.QSize(_width_hint, _header.height()))
        self.refresh()
        return None

    @setVerticalHeaderValue.server
    def setVerticalHeaderValue(self, index: int, value: Any) -> Any:
        return (index, self.model().df.index[index]), {}

    @QBaseTable._mgr.interface
    def setFilter(self, sl: FilterType):
        """Set filter to the table view. This operation is undoable."""
        return super().setFilter(sl)

    @setFilter.server
    def setFilter(self, sl: FilterType):
        return (self.filter(),), {}

    def undo(self) -> None:
        """Undo last operation."""
        self._mgr.undo()
        return None

    def redo(self) -> None:
        """Redo last undo operation."""
        self._mgr.redo()
        return None


class QMutableSimpleTable(QMutableTable):
    """A mutable table with a single QTableView."""

    @property
    def _qtable_view(self) -> _QTableViewEnhanced:
        return self._qtable_view_

    def createQTableView(self):
        self._qtable_view_ = _QTableViewEnhanced()
        _layout = QtW.QVBoxLayout()
        _layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_layout)
        self.layout().addWidget(self._qtable_view_)


def _equal(val: Any, old_val: Any) -> bool:
    # NOTE pd.NA == x returns pd.NA, not False
    eq = False
    if isinstance(val, pd.DataFrame):
        eq = True

    elif pd.isna(val):
        if not pd.isna(old_val):
            eq = True
    else:
        if pd.isna(old_val) or val != old_val:
            eq = True
    return eq

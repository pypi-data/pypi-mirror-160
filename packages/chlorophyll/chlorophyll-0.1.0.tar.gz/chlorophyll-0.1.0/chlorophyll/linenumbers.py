from __future__ import annotations

import tkinter


def line_is_elided(textwidget: tkinter.Text, lineno: int) -> bool:
    tags = textwidget.tag_names(f"{lineno}.0")
    elide_values = (textwidget.tag_cget(tag, "elide") for tag in tags)
    # elide values can be empty
    return any(tkinter.getboolean(v or "false") for v in elide_values)


class LineNumberBar(tkinter.Canvas):
    def __init__(self, parent: tkinter.Misc, widget: tkinter.Text) -> None:
        super().__init__(parent, highlightthickness=0)

        self._widget = widget
        self._update()
        self._update_width()

        self._widget.bind("<<Scroll>>", self._update)
        self._widget.bind("<<ColorSchemeChanged>>", self._update_colors)
        self._update_colors()

    def _update(self, junk: object = None) -> None:
        self.delete("all")

        first = int(self._widget.index("@0,0").split(".")[0])
        last = int(self._widget.index(f"@0,10000").split(".")[0])
        for lineno in range(first, last + 1):
            dlineinfo = self._widget.dlineinfo(f"{lineno}.0")
            if dlineinfo is None:
                break

            self.create_text(
                10, dlineinfo[1], text=lineno, anchor="nw", font="TkFixedFont"
            )

    def _update_width(self, *_) -> None:
        self.config(
            width=tkinter.font.Font(name="TkFixedFont", exists=True).measure(" 1234 ")
        )

    def _update_colors(self, *_) -> None:
        print("run")
        self.config(background=self._widget.cget("background"))
        self.itemconfig("all", fill=self._widget.cget("fg"))

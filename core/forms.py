from django import forms


class TailwindFormMixin:
    base_input_class = (
        "mt-1 block w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-slate-900 "
        "shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
    )
    file_input_class = "mt-1 block w-full text-slate-700"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            current = widget.attrs.get("class", "")
            classes = self.base_input_class

            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                classes = "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                classes = self.base_input_class
            elif isinstance(widget, forms.FileInput):
                classes = self.file_input_class
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("rows", 4)

            widget.attrs["class"] = f"{current} {classes}".strip()

from django import forms

from .models import Brief


class BriefForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = [
            "cliente", "nombre_marca", "rubro", "estado",
            "historia", "objetivos", "publico_objetivo", "competencia",
            "personalidad", "referencias", "colores_deseados",
            "colores_prohibidos", "tipografias", "adjunto",
        ]
        widgets = {
            "historia": forms.Textarea(attrs={"rows": 3}),
            "objetivos": forms.Textarea(attrs={"rows": 3}),
            "publico_objetivo": forms.Textarea(attrs={"rows": 2}),
            "competencia": forms.Textarea(attrs={"rows": 2}),
            "referencias": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.setdefault("class", "form-control")
            else:
                field.widget.attrs.setdefault("class", "form-control")

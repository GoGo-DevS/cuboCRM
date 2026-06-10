from django import forms

from .models import Deliverable, Project, Revision


class _Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            elif isinstance(field.widget, (forms.DateInput,)):
                field.widget.attrs.setdefault("class", "form-control")
            else:
                field.widget.attrs.setdefault("class", "form-control")


class ProjectForm(_Bootstrap, forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "nombre", "cliente", "brief", "tipo", "estado",
            "descripcion", "fecha_inicio", "fecha_entrega", "monto", "responsable",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_entrega": forms.DateInput(attrs={"type": "date"}),
        }


class DeliverableForm(_Bootstrap, forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ["nombre", "tipo", "estado", "archivo", "responsable", "fecha"]
        widgets = {"fecha": forms.DateInput(attrs={"type": "date"})}


class RevisionForm(_Bootstrap, forms.ModelForm):
    class Meta:
        model = Revision
        fields = ["entregable", "version", "estado", "comentarios"]
        widgets = {"comentarios": forms.Textarea(attrs={"rows": 2})}

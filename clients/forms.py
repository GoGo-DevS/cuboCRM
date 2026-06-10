from django import forms

from .models import Client, Company


class _Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")


class ClientForm(_Bootstrap, forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "nombre", "empresa", "cargo", "email", "whatsapp",
            "instagram", "linkedin", "notas", "activo",
        ]
        widgets = {"notas": forms.Textarea(attrs={"rows": 3})}


class CompanyForm(_Bootstrap, forms.ModelForm):
    class Meta:
        model = Company
        fields = ["nombre", "rubro", "sitio_web", "instagram", "ciudad", "pais", "logo"]

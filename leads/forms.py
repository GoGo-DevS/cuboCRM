from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "nombre", "empresa", "cargo", "email", "whatsapp",
            "instagram", "linkedin", "behance", "sitio_web",
            "fuente", "estado", "valor_estimado", "notas",
        ]
        widgets = {
            "notas": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)

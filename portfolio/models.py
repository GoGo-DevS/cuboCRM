from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.models import TimeStampedModel


class Testimonial(TimeStampedModel):
    cliente = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="testimonios"
    )
    proyecto = models.ForeignKey(
        "projects.Project", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="testimonios",
    )
    texto = models.TextField()
    autor_nombre = models.CharField(max_length=160, blank=True)
    autor_cargo = models.CharField(max_length=160, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "testimonio"
        verbose_name_plural = "testimonios"

    def __str__(self):
        return f"Testimonio de {self.autor_nombre or self.cliente}"

    @property
    def estrellas(self):
        return range(self.rating)


class CaseStudy(TimeStampedModel):
    proyecto = models.OneToOneField(
        "projects.Project", on_delete=models.CASCADE, related_name="caso_estudio"
    )
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    resultados = models.TextField(blank=True)
    imagen_portada = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    testimonio = models.ForeignKey(
        Testimonial, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="casos",
    )
    publicado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "caso de estudio"
        verbose_name_plural = "casos de estudio"

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo) or f"caso-{self.proyecto_id}"
            slug = base
            i = 2
            while CaseStudy.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:detail", args=[self.slug])

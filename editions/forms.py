from django import forms
from .widgets import CustomClearableFileInput
from .models import Edition, Year


class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = "__all__"

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = Year.objects.all()
        short_years = [(y.id, y.get_short_year()) for y in years]
        self.fields["year"].choices = short_years
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-black rounded-0"


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

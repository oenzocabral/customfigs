from django import forms
from .models import Figure, Album, UserFigure, FigurePackage

class FigureForm(forms.ModelForm):
    class Meta:
        model = Figure
        fields = ['name', 'description', 'image', 'rarity', 'event']

class AlbumVisibilityForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['is_public']

class FigureSaleForm(forms.ModelForm):
    class Meta:
        model = UserFigure
        fields = ['is_for_sale', 'price']
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class FigureTransferForm(forms.Form):
    username = forms.CharField(max_length=150)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        from users.models import CustomUser
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        return user

class FigurePackageForm(forms.ModelForm):
    class Meta:
        model = FigurePackage
        fields = ['event', 'price']

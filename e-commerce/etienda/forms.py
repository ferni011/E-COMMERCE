from django import forms

class ProductoForm(forms.Form):
	title = forms.CharField(label='Nombre', max_length=100)
	price = forms.DecimalField(label='Precio')
	category_choices = [
        ('men\'s clothing', "Men's Clothing"),
        ('women\'s clothing', "Women's Clothing"),
        ('jewelery', 'Jewelery'),
        ('electronics', 'Electronics'),
    ]
	category = forms.ChoiceField(choices=category_choices, label='Categoría')
	description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}), label='Descripción')
	image = forms.FileField(label='Imagen')



from django import forms

class PlayerForm(forms.Form):
    player_name = forms.CharField(max_length=100, label='Player Name')
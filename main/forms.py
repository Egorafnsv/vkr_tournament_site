
from django import forms


class CreateNewPlayer(forms.Form):
    number = forms.CharField()
    name = forms.CharField(label="Фамилия", max_length=50)

    field_order = ["number", "name"]

    def __init__(self, numbers, *args, **kwargs):
        super(CreateNewPlayer, self).__init__(*args, **kwargs)
        self.fields["number"] = forms.ChoiceField(choices=numbers)


class CreateNewTournament(forms.Form):
    name = forms.CharField(label="Название", max_length=100, initial="my championship")
    rounds = forms.IntegerField(label="Количество кругов", min_value=1, max_value=4, initial=1)
    cards = forms.IntegerField(label="Лимит желтых карточек", min_value=2, initial=4)
    clubs = forms.ChoiceField(label="Выберите количество команд из списка", choices=[(str(i), i) for i in range(3, 33)], initial='2',
                              widget=forms.Select(attrs={'onchange': "add_clubs();"}))

class AddDateTimeMatch(forms.Form):
    match_day = forms.DateTimeField()

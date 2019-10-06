from django import forms

class Register(forms.Form):
    name = forms.CharField(required=True,label="姓名")
    password = forms.CharField(required=True,label="密码")

    def clean_name(self):
        """ 自定义校验 用户名不允许是admin """

        name = self.cleaned_data.get("name")
        if name == "admin":
            self.add_error("name", "不可以是admin")
        else:
            return name
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if str(name) == 'admin':
    #         self.add_error("name","不可以是admin")
    #     else:
    #         return name
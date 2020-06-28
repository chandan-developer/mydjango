from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, FrequencyForm
from django.contrib.auth.decorators import login_required
from blog.models import Scraping
from  django.core.exceptions import ValidationError
from bs4 import BeautifulSoup
from django.core.files import File
import requests
import os
from mydjango.settings import BASE_DIR
from urllib.request import urlopen
from collections import Counter
import re

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if request.POST.get('captcha_value') != request.POST.get('captcha'):
                # raise ValidationError(
                #     "Did not send for 'help' in the subject despite "
                #     "CC'ing yourself."
                # )
                print("#########")
                print(request.POST.get('captcha_value'))
                print(request.POST.get('captcha'))
                messages.error(request, 'Incorrect captcha value')
                return redirect('register')
            else:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created with username: {username.upper()}')
                return redirect('blog-home')
    else:
        
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'users/profile.html', context)


def frequency(request):

    if request.method == 'POST':
        # f_form = FrequencyForm(request.POST)
        # if f_form.is_valid():

        url = request.POST.get('url')
        #extractData(url)
        data = Scraping.objects.filter(url=url).first()
        #data = get_object_or_404(Scraping, url=)
        if data:
            data.status = 1
            data.save()
            request.session['url_pk_id'] = data.id
            data = list(data.extracted_data)
            status = 1
            
        else:
            data = get_text(url)
            if data is False:
                request.session['url_pk_id'] = 0
                messages.error(request, f'No Data extracted from this url: {url} Try with some other url.')
            else:
                scrapping = Scraping(url=url, extracted_data=data, status=0)            
                scrapping.save()
                status = 0
                request.session['url_pk_id'] = scrapping.id
                messages.success(request, f'Data extracted from this url: {url}')
        #f_form.save()        
        #return render(request, 'users/result.html',{'data':data,'status':status})
        return redirect('result')
    else:
        f_form = FrequencyForm()

    return render(request, 'users/frequency.html', {'f_form':f_form})

def result(request):
    url_pk_id = request.session.get('url_pk_id',0)
    if url_pk_id != 0:
        result = get_object_or_404(Scraping, pk=url_pk_id)
        data = result.extracted_data
        print('######')
        data = eval(data)
        print(data)
        status = result.status
    else:
        status = 0
        result = False
        data = False

    return render(request, 'users/result.html',{'data':data,'status':status})

def extractData(url):  
    url = requests.get(url)  
    html_page = url.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    print(text)
    output = ''
    blacklist = []

    f = open(os.path.join(BASE_DIR, 'mydjango/common-words.txt'),'r')
    blacklist = File(f)
    print('###################')
    #print(blacklist.readlines())
    

    for t in text:
	    if t.parent.name not in blacklist:
		    output += '{} '.format(t)

def get_text(url):
    
    try:
        html = urlopen(url).read()

        soup = BeautifulSoup(html,"html.parser")

        for script in soup(["script", "style"]):

            script.decompose()

        #print(soup.stripped_strings)
        strips = list(soup.stripped_strings)
        
        #print(strips)
        strips = [re.sub('[^a-zA-Z]+', ' ', _) for _ in strips]
        print('before split space')
        print(strips)
        strips = ' '.join(strips).split()
        print('after')
        print(strips)
        # strips = list(map(str.strip, strips))

        new_strips = []
        # for w in strips:
        #     w.split()
        #     new_strips.append()


        f = open(os.path.join(BASE_DIR, 'mydjango/common-words.txt'),'r')
        blacklist = '\n'.join(f.readlines()).split()
        text_after_remove_common_words = []
        for text in strips:
            if text.lower() not in blacklist:
                text_after_remove_common_words.append(text)


        a = dict(Counter(text_after_remove_common_words))
        sorted_words = sorted(a.items(), key=lambda x: x[1], reverse=True)
        
        for sorted_word in sorted_words:
            if len(sorted_word[0]) < 4:
                #print(sorted_word)
                #sorted_words.pop(sorted_word) 
                pass
    
        return sorted_words[:10]
    except Exception as e:
        print('$$$$$$$$$$$')
        print(e)
        return False